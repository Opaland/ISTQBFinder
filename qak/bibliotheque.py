"""Bibliothèque documentaire : import, métadonnées, doublons, versions et index plein texte.

Deux fichiers :
- `bibliotheque/manifeste.json` (versionné) : une entrée par fichier source, indexée par
  empreinte SHA-256, avec les métadonnées détectées ou saisies. C'est la mémoire durable
  de la bibliothèque : il permet de reconstruire l'index à l'identique.
- `bibliotheque/index.db` (non versionné, reconstructible) : documents, sections et
  passages + table FTS5. `actualiser()` le remet à jour de façon incrémentale.
"""
import hashlib
from contextlib import contextmanager
from functools import cmp_to_key
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from . import chemins, extraction, journal
from .textes import normaliser, sans_accents

EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}
IGNORES = {"lisezmoi.md", "readme.md"}  # notes du dossier sources, pas des documents

# Tokeniseur de l'index plein texte, partagé avec le reclassement de recherche.py.
TOKENISEUR = "porter unicode61 remove_diacritics 2"
SCHEMA = f"""
CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY, sha256 TEXT UNIQUE NOT NULL, fichier TEXT NOT NULL,
    titre TEXT, code TEXT, type TEXT, niveau TEXT, domaine TEXT, version TEXT, langue TEXT,
    date_publication TEXT, source_officielle TEXT, page_officielle TEXT,
    statut_version TEXT DEFAULT 'courant', remplace_par TEXT,
    nb_pages INTEGER, pages_vides TEXT, nb_pages_sommaire INTEGER,
    statut_extraction TEXT, message_extraction TEXT, plan_source TEXT, nb_titres INTEGER,
    version_extracteur INTEGER, indexe_le TEXT, controle_le TEXT
);
CREATE TABLE IF NOT EXISTS sections (
    doc_id TEXT NOT NULL, ordre INTEGER NOT NULL, numero TEXT, titre TEXT, page INTEGER,
    PRIMARY KEY (doc_id, ordre)
);
CREATE TABLE IF NOT EXISTS passages (
    id INTEGER PRIMARY KEY, doc_id TEXT NOT NULL, ordre INTEGER NOT NULL,
    page INTEGER NOT NULL, page_imprimee TEXT, section_num TEXT, section_titre TEXT,
    texte TEXT NOT NULL, sommaire INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS passages_doc ON passages(doc_id, page);
CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts USING fts5(
    texte, section_titre, content='passages', content_rowid='id',
    tokenize='{TOKENISEUR}'
);
"""


ATTENTE_VERROU = 30  # secondes d'attente d'un verrou SQLite avant d'abandonner


def ouvrir_sqlite(chemin: Path) -> sqlite3.Connection:
    """Connexion partagée par les deux bases (index, idées). Le journal WAL laisse lire
    pendant qu'un autre processus écrit (`chercher` pendant `actualiser`) ; deux écritures
    simultanées s'attendent jusqu'à ATTENTE_VERROU secondes au lieu d'échouer aussitôt."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(chemin, timeout=ATTENTE_VERROU)
    cx.row_factory = sqlite3.Row
    _passer_en_wal(cx)
    return cx


def _passer_en_wal(cx: sqlite3.Connection) -> None:
    """Le changement de mode de journal n'attend pas le verrou (SQLite n'appelle pas le
    gestionnaire d'attente pour ce PRAGMA) : on réessaie jusqu'à ATTENTE_VERROU secondes."""
    limite = time.monotonic() + ATTENTE_VERROU
    while True:
        try:
            if cx.execute("PRAGMA journal_mode").fetchone()[0].lower() != "wal":
                cx.execute("PRAGMA journal_mode=WAL")
            return
        except sqlite3.OperationalError as exc:
            if "locked" not in str(exc) or time.monotonic() >= limite:
                raise
            time.sleep(0.05)


def connecter(chemin: Path | None = None) -> sqlite3.Connection:
    cx = ouvrir_sqlite(chemin or chemins.index_db())
    cx.executescript(SCHEMA)
    if "controle_le" not in {r[1] for r in cx.execute("PRAGMA table_info(documents)")}:
        cx.execute("ALTER TABLE documents ADD COLUMN controle_le TEXT")  # index d'avant #36
        cx.commit()
    return cx


def empreinte(chemin: Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# ---------------------------------------------------------------- manifeste

def lire_manifeste(prive: bool = False) -> dict:
    """Manifeste versionné, ou (`prive`) celui des documents internes, rangé dans
    bibliotheque/prive/ et donc jamais versionné : ni chemin ni titre interne dans Git."""
    p = chemins.manifeste_prive() if prive else chemins.manifeste()
    if not p.exists():
        return {"documents": {}}
    return json.loads(p.read_text(encoding="utf-8-sig"))


def ecrire_manifeste(m: dict, prive: bool = False) -> None:
    """Écriture atomique (fichier temporaire puis `os.replace`) : un lecteur voit l'ancien
    ou le nouveau manifeste, jamais un fichier à moitié écrit. Appeler sous `verrou_manifeste()`."""
    p = chemins.manifeste_prive() if prive else chemins.manifeste()
    p.parent.mkdir(parents=True, exist_ok=True)
    m["documents"] = dict(sorted(m["documents"].items(), key=lambda kv: kv[1].get("doc_id", "")))
    contenu = json.dumps(m, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=".manifeste-", suffix=".tmp", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(contenu)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


_verrous_tenus = 0  # profondeur : actualiser() appelle importer(), qui reprend le verrou


def _verrouiller(f, bloquant: bool) -> bool:
    try:
        if sys.platform == "win32":
            import msvcrt
            f.seek(0)
            while True:
                try:
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                    return True
                except OSError:
                    if not bloquant:
                        return False
                    import time
                    time.sleep(0.2)
        import fcntl
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | (0 if bloquant else fcntl.LOCK_NB))
        return True
    except BlockingIOError:
        return False


def _deverrouiller(f) -> None:
    if sys.platform == "win32":
        import msvcrt
        f.seek(0)
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


@contextmanager
def verrou_manifeste():
    """Verrou de fichier (`manifeste.json.verrou`) autour de lecture + modification +
    écriture du manifeste : deux imports simultanés ne s'écrasent plus. Réentrant dans
    un même processus ; un autre processus attend son tour."""
    global _verrous_tenus
    if _verrous_tenus:
        _verrous_tenus += 1
        try:
            yield
        finally:
            _verrous_tenus -= 1
        return
    p = chemins.manifeste()
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p.with_name(p.name + ".verrou"), "a+b") as f:
        if not _verrouiller(f, bloquant=False):
            sys.stderr.write("Manifeste utilisé par une autre commande (import, actualiser…) : attente…\n")
            _verrouiller(f, bloquant=True)
        _verrous_tenus = 1
        try:
            yield
        finally:
            _verrous_tenus = 0
            _deverrouiller(f)


def catalogue() -> dict:
    return json.loads(chemins.catalogue().read_text(encoding="utf-8-sig"))


# ---------------------------------------------------------------- détection des métadonnées

MOIS = {"janvier": 1, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "aout": 8,
        "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12, "january": 1, "february": 2,
        "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9,
        "october": 10, "november": 11, "december": 12}
_NOMS_MOIS = "|".join(MOIS)
RE_DATES = [
    (re.compile(r"\b(\d{1,2})[/.](\d{1,2})[/.](20\d{2})\b"), lambda m: (m[3], m[2], m[1])),
    (re.compile(r"\b(20\d{2})\s?[-/ ]\s?(\d{2})\s?[-/ ]\s?(\d{2})\b"), lambda m: (m[1], m[2], m[3])),
    (re.compile(rf"\b(\d{{1,2}})(?:er|st|nd|rd|th)?\s+({_NOMS_MOIS})\s+(20\d{{2}})\b"), lambda m: (m[3], MOIS[m[2]], m[1])),
    (re.compile(rf"\b({_NOMS_MOIS})\s+(\d{{1,2}}),?\s+(20\d{{2}})\b"), lambda m: (m[3], MOIS[m[1]], m[2])),
]
RE_VERSION = re.compile(r"\bv(?:ersion)?\s?\.?\s?(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?[a-z]?)\b", re.I)
RE_VERSION_ENTETE = re.compile(r"(?:\bversion\s+v?|\bv)(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?[a-z]?|20\d{2})\b", re.I)


def _date(textes: list[str]) -> str | None:
    """Date de publication : la plus fréquente des premières pages (elle figure dans
    l'en-tête ou le pied de chaque page)."""
    vues = Counter()
    for t in textes:
        tn = sans_accents(re.sub(r"\s+", " ", t.lower()))
        for rx, conv in RE_DATES:
            for m in rx.finditer(tn):
                try:
                    a, mo, j = (int(x) for x in conv(m))
                except (ValueError, KeyError):
                    continue
                if 1 <= mo <= 12 and 1 <= j <= 31 and 2000 <= a <= 2100:
                    vues[f"{a:04d}-{mo:02d}-{j:02d}"] += 1
    return vues.most_common(1)[0][0] if vues else None


def _version(nom: str, titre: str, textes: list[str]) -> str | None:
    """Version déclarée : celle de l'en-tête répété (« Version 2014 », « v4.0 GA »), sinon
    celle du nom de fichier ou du titre PDF. L'historique des révisions, qui cite toutes
    les versions antérieures une seule fois, ne l'emporte donc pas."""
    pages = Counter()
    for t in textes:
        pages.update({m.group(1).lower() for m in RE_VERSION_ENTETE.finditer(t)})
    if pages and pages.most_common(1)[0][1] >= 2:
        return pages.most_common(1)[0][0]
    for source in (nom.replace("_", " "), titre):
        m = RE_VERSION.search(source)
        if m:
            return m.group(1)
    if pages:
        return pages.most_common(1)[0][0]
    m = re.search(r"\b(20\d{2})\b", nom)
    return m.group(1) if m else None


def _langue(texte: str) -> str:
    mots = normaliser(texte).split()
    fr = sum(m in {"le", "la", "les", "des", "est", "et", "pour", "une", "dans", "du"} for m in mots)
    en = sum(m in {"the", "and", "of", "is", "to", "for", "in", "with", "are", "be"} for m in mots)
    return "fr" if fr > en else "en"


def _type(texte: str) -> str:
    t = normaliser(texte)
    if "body of knowledge" in t or "ensemble des connaissances" in t:
        return "bok"
    if "glossa" in t:
        return "glossaire"
    if "release notes" in t or "notes de version" in t:
        return "notes"
    if "sample exam" in t or "examen blanc" in t or "exam questions" in t:
        return "examen"
    return "syllabus" if "syllabus" in t else "document"


def entree_catalogue(zones: list[str]) -> dict | None:
    """Entrée du catalogue reconnue dans la première zone qui en mentionne une
    (zones de la plus fiable à la moins fiable ; motifs du plus spécifique au plus général)."""
    for zone in zones:
        zn = normaliser(zone)
        for e in catalogue()["documents"]:
            if any(re.search(rx, zn) for rx in e["motifs"]):
                return e
    return None


def detecter(chemin: Path, ext: extraction.Extraction) -> dict:
    """Métadonnées déduites du nom de fichier, des métadonnées PDF et de la couverture.
    Seule la couverture compte pour le code : les pages suivantes citent d'autres syllabus."""
    nom = chemin.stem.replace("_", " ").replace("-", " ")
    titre_pdf = ext.meta_pdf.get("Title", "")
    if titre_pdf.lower().startswith("microsoft word") or len(titre_pdf) < 6:
        titre_pdf = ""
    couverture = ext.brut_debut[0] if ext.brut_debut else ""
    entete = "\n".join(ext.brut_debut[:3])
    entree = entree_catalogue([nom, titre_pdf, couverture, entete])
    code = entree["code"] if entree else None
    corps = " ".join(p.texte for p in ext.pages[:12])
    meta = {
        "code": code,
        "type": _type(f"{nom} {titre_pdf} {couverture}"),
        "langue": _langue(corps),
        "version": _version(chemin.name, titre_pdf, ext.brut_debut),
        "date_publication": _date(ext.brut_debut),
        "niveau": entree["niveau"] if entree else None,
        "domaine": entree["domaine"] if entree else None,
        "page_officielle": entree["page_officielle"] if entree else None,
    }
    lib = (entree["titre"] if entree else (titre_pdf or chemin.stem))
    suffixe = {"bok": " — Body of Knowledge", "glossaire": " — Glossaire", "notes": " — Notes de version",
               "examen": " — Examen blanc"}.get(meta["type"], "")
    meta["titre"] = f"ISTQB {lib}{suffixe}" if entree else lib
    return meta


def _doc_id(meta: dict, sha: str, pris: set[str]) -> str:
    if meta.get("code"):
        base = meta["code"] + ("-BoK" if meta.get("type") == "bok" else "") + \
            (f"-{meta['type']}" if meta.get("type") in ("glossaire", "notes", "examen") else "") + \
            f"-{meta.get('version') or 'v?'}-{meta.get('langue') or 'xx'}"
    else:
        base = re.sub(r"[^A-Za-z0-9.]+", "-", meta.get("titre") or sha[:8]).strip("-")[:50]
    return base if base not in pris else f"{base}-{sha[:6]}"


# ---------------------------------------------------------------- versions

def _cle_version(v: str | None) -> tuple:
    if not v:
        return ()
    parts = re.findall(r"\d+|[a-z]", v.lower())
    return tuple(int(p) if p.isdigit() else ord(p) - 96 for p in parts)


def _numero_version(v: str | None) -> tuple:
    """Numéro comparable, ou () pour une « version » qui est une année (2019) ou absente."""
    cle = _cle_version(v)
    return () if not cle or cle[0] >= 1900 else cle


def _comparer_versions(a, b) -> int:
    va, vb = _numero_version(a["version"]), _numero_version(b["version"])
    if va and vb and va != vb:
        return 1 if va > vb else -1
    da, db = a["date_publication"], b["date_publication"]
    if da and db and da != db:
        return 1 if da > db else -1
    return 0


def calculer_versions(cx: sqlite3.Connection) -> list[str]:
    """Pour chaque (code, type, langue), la version la plus récente est « courant »,
    les autres « remplace ». Deux numéros de version comparables (« 3.0 », « 4.0 ») font
    foi ; sinon (version « 2019 », numéro absent) on compare les dates. Faute de critère
    commun, l'ordre est signalé comme incertain (corriger la date ou la version)."""
    notes = []
    groupes: dict[tuple, list] = {}
    for r in cx.execute("SELECT doc_id, code, type, langue, version, date_publication, statut_version "
                        "FROM documents WHERE code IS NOT NULL AND statut_extraction NOT IN ('absent', 'a_confirmer')"):
        groupes.setdefault((r["code"], r["type"], r["langue"]), []).append(r)
    cx.execute("UPDATE documents SET statut_version='courant', remplace_par=NULL")
    for (code, typ, langue), docs in groupes.items():
        if len(docs) < 2:
            continue
        docs.sort(key=cmp_to_key(_comparer_versions), reverse=True)
        tete = docs[0]
        for r in docs[1:]:
            if _comparer_versions(tete, r) == 0 and r["version"] != tete["version"]:
                notes.append(f"ordre incertain entre {tete['doc_id']} et {r['doc_id']} (date ou numéro de "
                             "version manquant) : `corriger <doc_id> --date AAAA-MM-JJ`")
            cx.execute("UPDATE documents SET statut_version='remplace', remplace_par=? WHERE doc_id=?",
                       (tete["doc_id"], r["doc_id"]))
            meme = (r["version"] == tete["version"])
            notes.append(f"{r['doc_id']} {'(même version déclarée, fichier différent) ' if meme else ''}"
                         f"remplacé par {tete['doc_id']} pour {code} {typ} [{langue}]")
    cx.execute("UPDATE documents SET statut_version='absent' WHERE statut_extraction='absent'")
    cx.execute("UPDATE documents SET statut_version='a_confirmer' WHERE statut_extraction='a_confirmer'")
    return notes


# ---------------------------------------------------------------- indexation

def _indexer(cx: sqlite3.Connection, doc_id: str, ext: extraction.Extraction) -> int:
    cx.execute("DELETE FROM passages_fts WHERE rowid IN (SELECT id FROM passages WHERE doc_id=?)", (doc_id,))
    cx.execute("DELETE FROM passages WHERE doc_id=?", (doc_id,))
    cx.execute("DELETE FROM sections WHERE doc_id=?", (doc_id,))
    cx.executemany("INSERT INTO sections(doc_id, ordre, numero, titre, page) VALUES (?,?,?,?,?)",
                   [(doc_id, i, t.numero, t.titre, t.page) for i, t in enumerate(ext.plan)])
    n = 0
    for i, p in enumerate(extraction.passages(ext)):
        cur = cx.execute("INSERT INTO passages(doc_id, ordre, page, page_imprimee, section_num, section_titre, "
                         "texte, sommaire) VALUES (?,?,?,?,?,?,?,?)",
                         (doc_id, i, p.page, p.imprimee, p.section_num, p.section_titre, p.texte, int(p.sommaire)))
        cx.execute("INSERT INTO passages_fts(rowid, texte, section_titre) VALUES (?,?,?)",
                   (cur.lastrowid, p.texte, p.section_titre))
        n += 1
    return n


def _enregistrer(cx, entree: dict, ext: extraction.Extraction) -> int:
    statut, message = ext.statut()
    cx.execute("DELETE FROM documents WHERE sha256=? OR doc_id=?", (entree["sha256"], entree["doc_id"]))
    champs = ("titre", "code", "type", "niveau", "domaine", "version", "langue", "date_publication",
              "source_officielle", "page_officielle")
    cx.execute(
        f"INSERT INTO documents(doc_id, sha256, fichier, {', '.join(champs)}, nb_pages, pages_vides, "
        "nb_pages_sommaire, statut_extraction, message_extraction, plan_source, nb_titres, version_extracteur, "
        f"indexe_le) VALUES ({', '.join('?' * (len(champs) + 12))})",
        (entree["doc_id"], entree["sha256"], entree["fichier"], *[entree.get(c) for c in champs],
         ext.nb_pages, ",".join(map(str, ext.pages_vides())), sum(p.sommaire for p in ext.pages),
         statut, message, ext.plan_source, len(ext.plan), extraction.VERSION_EXTRACTEUR,
         datetime.now().isoformat(timespec="seconds")))
    return _indexer(cx, entree["doc_id"], ext) if statut in ("ok", "partiel") else 0


def _confirmer_remplacement(cx, manif: dict, fichier: Path, sha: str, motif: str | None, copier: bool) -> str:
    """`importer <fichier> --remplacer --motif` : le nouveau contenu prend la place du
    document de même nom de fichier (doc_id et corrections conservés). L'ancienne empreinte
    rejoint l'historique du manifeste et le remplacement est journalisé. Renvoie l'ancienne."""
    if not (motif or "").strip():
        raise ValueError("--remplacer exige --motif \"…\" (ex. « PDF ré-exporté par le CFTL, contenu vérifié ») : "
                         "le remplacement est journalisé.")
    ancien = next((k for k, e in manif["documents"].items() if e["fichier"] == fichier.name and k != sha), None)
    if not ancien:
        raise KeyError(f"Aucun document de la bibliothèque n'a pour fichier {fichier.name} : --remplacer est "
                       "inutile (import normal).")
    entree = manif["documents"].pop(ancien)
    entree.setdefault("historique_empreintes", []).append(
        {"sha256": ancien, "remplace_le": datetime.now().date().isoformat(), "motif": motif.strip()})
    entree.pop("a_confirmer", None)
    entree["sha256"] = sha
    manif["documents"][sha] = entree
    cx.execute("DELETE FROM documents WHERE sha256=?", (ancien,))
    cible = chemins.sources() / entree["fichier"]
    if copier and cible.resolve() != fichier.resolve():
        chemins.sources().mkdir(parents=True, exist_ok=True)
        shutil.copy2(fichier, cible)
    journal.noter("document_remplace", entree["doc_id"],
                  {"fichier": entree["fichier"], "ancienne_empreinte": ancien, "nouvelle_empreinte": sha},
                  motif=motif.strip())
    return ancien


def importer(fichier: Path, meta_forcee: dict | None = None, copier: bool = True,
             cx: sqlite3.Connection | None = None, remplacer: bool = False, motif: str | None = None,
             prive: bool = False) -> dict:
    """Importe un fichier dans la bibliothèque. Renvoie un rapport :
    {etat: 'importe'|'doublon'|'echec'|'refuse'|'remplace', doc_id, message, ...}.
    Un fichier de sources/ dont le contenu a changé sur place n'est accepté qu'avec
    `remplacer=True` et un motif (sinon : refus, document laissé « à confirmer »).
    `prive=True` (document interne) : copie dans bibliotheque/prive/ et inscription au
    manifeste privé, jamais dans sources/ ni dans le manifeste versionné (dépôt public)."""
    fichier = Path(fichier)
    if prive:
        if remplacer:
            raise ValueError("--remplacer ne s'applique pas aux documents privés : réimporter le fichier.")
        if fichier.resolve().is_relative_to(chemins.sources().resolve()):
            raise ValueError(f"{fichier.name} est dans bibliotheque/sources/, dossier VERSIONNÉ et public : le "
                             "déplacer hors du dépôt ou dans bibliotheque/prive/, puis relancer avec --prive.")
    meta_forcee = {k: v for k, v in (meta_forcee or {}).items() if v}
    if fichier.suffix.lower() not in EXTENSIONS:
        return {"etat": "echec", "fichier": fichier.name, "message": f"format non pris en charge ({fichier.suffix})"}
    sha = empreinte(fichier)
    with verrou_manifeste():
        return _importer(fichier, sha, meta_forcee, copier, cx, remplacer, motif, prive)


def _importer(fichier: Path, sha: str, meta_forcee: dict, copier: bool, cx: sqlite3.Connection | None,
              remplacer: bool = False, motif: str | None = None, prive: bool = False) -> dict:
    manif = lire_manifeste(prive)
    autre = lire_manifeste(not prive)["documents"]
    dossier = chemins.prive() if prive else chemins.sources()
    if sha in autre:
        return {"etat": "doublon", "fichier": fichier.name, "doc_id": autre[sha]["doc_id"],
                "message": f"contenu identique (SHA-256) à {autre[sha]['doc_id']}, déjà dans la bibliothèque "
                           f"{'publique' if prive else 'privée'} — non réimporté"}
    propre = cx is None
    cx = cx or connecter()
    try:
        ancien = None
        if remplacer and sha not in manif["documents"]:
            ancien = _confirmer_remplacement(cx, manif, fichier, sha, motif, copier)
        elif not prive and sha not in manif["documents"] and \
                (chemins.sources() / fichier.name).resolve() == fichier.resolve():
            homonyme = next((e for e in manif["documents"].values() if e["fichier"] == fichier.name), None)
            if homonyme:
                return {"etat": "refuse", "fichier": fichier.name, "doc_id": homonyme["doc_id"],
                        "message": f"contenu modifié sur place (empreinte différente de celle du manifeste) : "
                                   f"{homonyme['doc_id']} reste à confirmer. Si la modification est voulue : "
                                   f"`importer {fichier} --remplacer --motif \"…\"`"}
        if sha in manif["documents"]:
            existant = manif["documents"][sha]
            cible = dossier / existant["fichier"]
            if cible.resolve() != fichier.resolve():
                if not cible.exists() and copier:  # source perdue : on la restaure
                    shutil.copy2(fichier, cible)
                return {"etat": "doublon", "fichier": fichier.name, "doc_id": existant["doc_id"],
                        "message": f"contenu identique (SHA-256) à {existant['fichier']} — non réimporté"}
            if meta_forcee:  # même fichier, métadonnées corrigées
                existant.update(meta_forcee)
                existant["champs_forces"] = sorted(set(existant.get("champs_forces", [])) | set(meta_forcee))
        ext = extraction.extraire(fichier)
        statut, message = ext.statut()
        if sha not in manif["documents"] and copier and statut not in ("ok", "partiel"):
            # Import manuel d'un fichier inexploitable (faux PDF, scan sans texte) : rien
            # n'est copié ni inscrit, la bibliothèque reste telle qu'elle était.
            return {"etat": "echec", "fichier": fichier.name, "statut_extraction": statut,
                    "message": f"{statut} : {message} — fichier ni copié ni inscrit au manifeste"}
        if sha in manif["documents"]:
            entree = manif["documents"][sha]
        else:
            meta = detecter(fichier, ext)
            meta.update(meta_forcee)
            pris = {e["doc_id"] for e in (*manif["documents"].values(), *autre.values())}
            entree = {"sha256": sha, "doc_id": _doc_id(meta, sha, pris), **meta,
                      "source_officielle": meta_forcee.get("source_officielle"),
                      "origine": meta_forcee.get("origine", "import manuel"),
                      "importe_le": datetime.now().date().isoformat(),
                      "champs_forces": sorted(meta_forcee)}
            if prive:
                entree["prive"] = True
            nom = fichier.name
            if copier:
                dossier.mkdir(parents=True, exist_ok=True)
                cible = dossier / nom
                if cible.exists() and empreinte(cible) != sha:
                    nom = f"{fichier.stem}-{sha[:6]}{fichier.suffix}"
                    cible = dossier / nom
                if cible.resolve() != fichier.resolve():
                    shutil.copy2(fichier, cible)
            entree["fichier"] = nom
            manif["documents"][sha] = entree
        n = _enregistrer(cx, entree, ext)
        notes = [n for n in calculer_versions(cx) if entree["doc_id"] in n]
        cx.commit()
        ecrire_manifeste(manif, prive)
        if ancien and statut in ("ok", "partiel"):
            message = f"remplace le contenu d'empreinte {ancien[:12]}… (historique au manifeste, journalisé) ; {message}"
        return {"etat": ("remplace" if ancien else "importe") if statut in ("ok", "partiel") else "echec",
                "fichier": fichier.name,
                "doc_id": entree["doc_id"], "passages": n, "statut_extraction": statut, "message": message,
                "versions": notes, "meta": {k: entree.get(k) for k in
                                            ("titre", "code", "type", "version", "langue", "date_publication")}}
    finally:
        if propre:
            cx.close()


def actualiser(forcer: bool = False) -> dict:
    """Synchronise l'index avec bibliotheque/sources/ : nouveaux fichiers importés,
    fichiers modifiés ou extraits par un ancien extracteur réindexés, fichiers
    disparus signalés. Ne supprime jamais un fichier source."""
    with verrou_manifeste():
        return _actualiser(forcer)


def _actualiser(forcer: bool) -> dict:
    rapport = {"importes": [], "reindexes": [], "a_confirmer": [], "inchanges": 0, "doublons": [], "absents": [],
               "echecs": [], "versions": []}
    en_attente = set()  # empreintes du manifeste dont le fichier a changé sur place
    manif = lire_manifeste()
    cx = connecter()
    try:
        connus = {r["sha256"]: dict(r) for r in cx.execute("SELECT * FROM documents")}
        presents: dict[str, str] = {}  # empreinte → fichier retenu
        dossier = chemins.sources()
        dossier.mkdir(parents=True, exist_ok=True)
        fichiers = [f for f in sorted(dossier.iterdir()) if _est_source(f)]
        empreintes = {f.name: empreinte(f) for f in fichiers}
        for f in fichiers:
            sha = empreintes[f.name]
            # Copie d'un fichier déjà connu : le fichier du manifeste reste la référence, la
            # copie est signalée en la nommant (et ne masque plus l'original).
            connu = manif["documents"].get(sha, {}).get("fichier")
            if connu and connu != f.name and empreintes.get(connu) == sha:
                rapport["doublons"].append(f"{f.name} : contenu identique à {connu}")
                continue
            if sha in presents:
                rapport["doublons"].append(f"{f.name} : contenu identique à {presents[sha]}")
                continue
            presents[sha] = f.name
            entree = manif["documents"].get(sha)
            if entree is None:
                # Même nom, contenu modifié sur place : rien ne distingue un PDF corrigé d'un
                # PDF altéré. Le document passe « à confirmer » (exclu des recherches) jusqu'à
                # une confirmation explicite et journalisée : `importer … --remplacer --motif`.
                ancien = next((k for k, e in manif["documents"].items() if e["fichier"] == f.name), None)
                if ancien:
                    attente = manif["documents"][ancien]
                    attente["a_confirmer"] = sha
                    en_attente.add(ancien)
                    cx.execute("UPDATE documents SET statut_extraction='a_confirmer', message_extraction=? "
                               "WHERE sha256=?", (f"contenu de {f.name} modifié sur place (empreinte {sha[:12]}… "
                                                  f"au lieu de {ancien[:12]}…) : exclu des recherches jusqu'à "
                                                  "confirmation", ancien))
                    rapport["a_confirmer"].append(
                        f"{attente['doc_id']} ({f.name}) : contenu modifié sur place, exclu des recherches. "
                        f"Si c'est voulu : `importer bibliotheque/sources/{f.name} --remplacer --motif \"…\"`")
                    continue
            if entree and entree["fichier"] != f.name:
                if (dossier / entree["fichier"]).exists():
                    rapport["doublons"].append(f"{f.name} = {entree['fichier']}")
                    continue
                entree["fichier"] = f.name  # fichier renommé
                cx.execute("UPDATE documents SET fichier=? WHERE sha256=?", (f.name, sha))
            doc = connus.get(sha)
            if entree and doc and not forcer and doc["version_extracteur"] == extraction.VERSION_EXTRACTEUR \
                    and doc["statut_extraction"] != "absent":
                rapport["inchanges"] += 1
                continue
            if entree:
                ext = extraction.extraire(f)
                # Détection améliorée depuis le dernier passage : on rafraîchit les champs
                # détectés, jamais ceux que l'utilisateur a corrigés (`champs_forces`).
                for k, v in detecter(f, ext).items():
                    if k not in entree.get("champs_forces", []) and v:
                        entree[k] = v
                _enregistrer(cx, entree, ext)
                # Validation document par document : une recherche lancée pendant la
                # réindexation voit l'index d'avant ou d'après, jamais un verrou de 2 minutes.
                cx.commit()
                ecrire_manifeste(manif)
                rapport["reindexes"].append(entree["doc_id"])
            else:
                # importer() relit et réécrit le manifeste : on y enregistre d'abord les
                # changements faits en mémoire (renommages, métadonnées rafraîchies).
                ecrire_manifeste(manif)
                r = importer(f, copier=False, cx=cx)
                manif = lire_manifeste()
                (rapport["importes"] if r["etat"] == "importe" else rapport["echecs"]).append(
                    f"{r.get('doc_id', f.name)} : {r['message']}")
        for sha, entree in manif["documents"].items():
            if sha not in presents and sha not in en_attente:
                rapport["absents"].append(f"{entree['doc_id']} ({entree['fichier']})")
                cx.execute("DELETE FROM passages_fts WHERE rowid IN (SELECT id FROM passages WHERE doc_id=?)",
                           (entree["doc_id"],))
                cx.execute("DELETE FROM passages WHERE doc_id=?", (entree["doc_id"],))
                cx.execute("UPDATE documents SET statut_extraction='absent', message_extraction="
                           "'fichier source introuvable dans bibliotheque/sources/' WHERE sha256=?", (sha,))
        # Métadonnées corrigées dans le manifeste versionné (niveau du catalogue, `corriger`
        # sur un autre poste) : reportées dans l'index sans réextraction.
        champs = ("titre", "code", "type", "niveau", "domaine", "version", "langue", "date_publication")
        for sha, entree in manif["documents"].items():
            cx.execute(f"UPDATE documents SET {', '.join(f'{c}=?' for c in champs)} WHERE sha256=?",
                       (*[entree.get(c) for c in champs], sha))
        # Documents internes déposés dans bibliotheque/prive/ (jamais versionné) : indexés,
        # inscrits au manifeste privé seulement.
        prives = lire_manifeste(prive=True)["documents"]
        if chemins.prive().is_dir():
            for f in sorted(chemins.prive().iterdir()):
                sha = empreinte(f) if _est_source(f) else None
                doc = connus.get(sha)
                if sha and (sha not in prives or forcer or not doc
                            or doc["version_extracteur"] != extraction.VERSION_EXTRACTEUR):
                    r = importer(f, copier=False, cx=cx, prive=True)
                    (rapport["importes"] if r["etat"] == "importe" else rapport["doublons"]
                     if r["etat"] == "doublon" else rapport["echecs"]).append(
                        f"{r.get('doc_id', f.name)} (privé) : {r['message']}")
                    prives = lire_manifeste(prive=True)["documents"]
        rapport["versions"] = calculer_versions(cx)
        maintenant = datetime.now().isoformat(timespec="seconds")
        cx.executemany("UPDATE documents SET controle_le=? WHERE sha256=?", [(maintenant, s) for s in presents])
        cx.commit()
        ecrire_manifeste(manif)
    finally:
        cx.close()
    return rapport


def _est_source(f: Path) -> bool:
    return f.is_file() and f.suffix.lower() in EXTENSIONS and not f.name.startswith(".") \
        and f.name.lower() not in IGNORES


def controle_index(cx: sqlite3.Connection | None = None) -> dict:
    """Contrôle léger, à chaque ouverture, de l'accord entre l'index et les sources (après un
    `git pull`, une suppression, une copie…) : présence des fichiers, date de modification
    postérieure au dernier contrôle (l'empreinte n'est recalculée que dans ce cas), entrées
    du manifeste non indexées, nouveaux fichiers. Renvoie {perimes: {doc_id}, messages}."""
    perimes, messages = set(), []
    if not chemins.index_db().exists():
        return {"perimes": perimes, "messages": messages}
    propre = cx is None
    cx = cx or connecter()
    try:
        docs = {r["sha256"]: dict(r) for r in cx.execute(
            "SELECT sha256, doc_id, fichier, statut_extraction, indexe_le, controle_le FROM documents")}
    finally:
        if propre:
            cx.close()
    manif = lire_manifeste()["documents"]
    prives = lire_manifeste(prive=True)["documents"]
    dossier = chemins.sources()
    for sha, e in (*manif.items(), *prives.items()):
        d = docs.get(sha)
        if d is None:
            perimes.add(e["doc_id"])
            messages.append(f"{e['doc_id']} : présent dans le manifeste mais pas dans l'index")
            continue
        if d["statut_extraction"] == "absent":
            continue  # déjà signalé par `actualiser` et `inventaire`
        if d["statut_extraction"] == "a_confirmer":
            perimes.add(d["doc_id"])  # modifié sur place : signalé, en attente de `--remplacer`
            continue
        f = (chemins.prive() if e.get("prive") else dossier) / e["fichier"]
        if not f.is_file():
            perimes.add(d["doc_id"])
            messages.append(f"{d['doc_id']} : fichier {e['fichier']} disparu de {f.parent.relative_to(chemins.racine())}/")
            continue
        repere = d["controle_le"] or d["indexe_le"]
        try:
            recent = not repere or datetime.fromtimestamp(f.stat().st_mtime) > \
                datetime.fromisoformat(repere) + timedelta(seconds=1)
        except ValueError:
            recent = True
        if recent and empreinte(f) != sha:
            perimes.add(d["doc_id"])
            messages.append(f"{d['doc_id']} : contenu de {e['fichier']} modifié depuis l'indexation")
    for sha, d in docs.items():
        if sha not in manif and sha not in prives and d["statut_extraction"] != "absent":
            perimes.add(d["doc_id"])
            messages.append(f"{d['doc_id']} : indexé mais absent du manifeste (retiré ailleurs ?)")
    if dossier.is_dir():
        connus = {e["fichier"] for e in manif.values()}
        nouveaux = sorted(f.name for f in dossier.iterdir() if _est_source(f) and f.name not in connus)
        if nouveaux:
            messages.append(f"fichiers non indexés : {', '.join(nouveaux[:5])}" + (" …" if len(nouveaux) > 5 else ""))
    return {"perimes": perimes, "messages": messages}


def avertissement_index(cx: sqlite3.Connection | None = None) -> str | None:
    """Phrase d'avertissement si l'index est périmé, sinon None."""
    c = controle_index(cx)
    if not c["messages"]:
        return None
    return "Index périmé : " + " ; ".join(c["messages"]) + " — lancer `python qa.py actualiser`."


def retirer(doc_id: str) -> dict:
    """Retire un document de la bibliothèque (manifeste + index). Le fichier source n'est
    pas supprimé : le déplacer hors de sources/ pour qu'`actualiser` ne le réimporte pas."""
    with verrou_manifeste():
        manif = lire_manifeste()
        sha = next((s for s, e in manif["documents"].items() if e["doc_id"].lower() == doc_id.lower()), None)
        if not sha:
            raise KeyError(f"Document inconnu : {doc_id}. Voir `inventaire`.")
        entree = manif["documents"].pop(sha)
        doc_id = entree["doc_id"]  # casse exacte (saisie insensible à la casse)
        ecrire_manifeste(manif)
    cx = connecter()
    try:
        cx.execute("DELETE FROM passages_fts WHERE rowid IN (SELECT id FROM passages WHERE doc_id=?)", (doc_id,))
        for table in ("passages", "sections", "documents"):
            cx.execute(f"DELETE FROM {table} WHERE doc_id=?", (doc_id,))
        calculer_versions(cx)
        cx.commit()
    finally:
        cx.close()
    return entree


def modifier_metadonnees(doc_id: str, **champs) -> dict:
    """Corrige les métadonnées d'un document (détection fautive). Les champs saisis sont
    marqués « forcés » dans le manifeste et prévalent sur la détection."""
    with verrou_manifeste():
        manif = lire_manifeste()
        cible = next((s for s, e in manif["documents"].items() if e["doc_id"].lower() == doc_id.lower()), None)
        if not cible:
            raise KeyError(f"Document inconnu : {doc_id}. Voir `inventaire`.")
        champs = {k: v for k, v in champs.items() if v is not None}
        entree = manif["documents"][cible]
        entree.update(champs)
        entree["champs_forces"] = sorted(set(entree.get("champs_forces", [])) | set(champs))
        ecrire_manifeste(manif)
    cx = connecter()
    try:
        for k, v in champs.items():
            cx.execute(f"UPDATE documents SET {k}=? WHERE sha256=?", (v, cible))
        calculer_versions(cx)
        cx.commit()
    finally:
        cx.close()
    return entree


def manquants(cx: sqlite3.Connection | None = None) -> dict:
    """Couverture du catalogue officiel : pour chaque code, version courante en anglais et
    en français (ou absence), versions remplacées et extractions à surveiller ; plus les
    documents locaux hors catalogue."""
    docs = inventaire(cx)
    lignes = []
    for e in catalogue()["documents"]:
        siens = [d for d in docs if d["code"] == e["code"] and d["statut_version"] != "absent"]
        par_langue = {}
        for langue in ("en", "fr"):
            courant = [d for d in siens if d["langue"] == langue and d["statut_version"] == "courant"]
            par_langue[langue] = courant[0]["doc_id"] if courant else None
        lignes.append({
            "code": e["code"], "titre": e["titre"], "niveau": e["niveau"],
            "version_officielle": e["version_constatee"], "en": par_langue["en"], "fr": par_langue["fr"],
            "statut_officiel": e.get("statut_officiel"), "successeur": e.get("successeur"),
            "remplaces": [d["doc_id"] for d in siens if d["statut_version"] == "remplace"],
            "a_surveiller": [f"{d['doc_id']} ({d['statut_extraction']})" for d in siens
                             if d["statut_extraction"] not in ("ok",)],
        })
    codes = {e["code"] for e in catalogue()["documents"]}
    hors = [d["doc_id"] for d in docs if d["code"] not in codes]
    return {"catalogue": lignes, "hors_catalogue": hors,
            "absents_en": [l["code"] for l in lignes if not l["en"]],
            "absents_fr": [l["code"] for l in lignes if not l["fr"]]}


def inventaire(cx: sqlite3.Connection | None = None) -> list[dict]:
    propre = cx is None
    cx = cx or connecter()
    try:
        return [dict(r) for r in cx.execute(
            "SELECT d.*, (SELECT COUNT(*) FROM passages p WHERE p.doc_id=d.doc_id) AS nb_passages "
            "FROM documents d ORDER BY d.niveau, d.code, d.langue, d.date_publication DESC")]
    finally:
        if propre:
            cx.close()
