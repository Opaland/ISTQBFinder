"""Base de connaissances QA : idées et techniques capitalisées.

Stockage :
- `connaissances/base.db` (SQLite, non versionné) : copie de travail, recherche FTS5 ;
- `connaissances/connaissances.jsonl` (versionné) : miroir lisible, une idée par ligne,
  réécrit après chaque modification. Après un `git pull`, la base est reconstruite
  automatiquement depuis ce fichier s'il a changé (empreinte comparée).
- `connaissances/journal.jsonl` (versionné, append-only) : traçabilité des changements.
"""
import hashlib
import json
import os
import re
import secrets
import sqlite3
from datetime import date, datetime

from . import bibliotheque, chemins, journal, taxonomie
from .textes import (MOTS_VIDES, jaccard, mots, motif_sous_sections, normaliser, recouvrement, signature,
                     termes_thesaurus)

STATUTS = {
    "a_explorer": "à explorer — piste repérée, pas encore étudiée",
    "a_evaluer": "à évaluer — étudiée, à confronter au contexte",
    "validee": "validée — retenue après analyse (motif obligatoire)",
    "experimentee": "expérimentée — mise en pratique, retour d'expérience enregistré",
    "abandonnee": "abandonnée — écartée (motif obligatoire)",
}
MATURITES = {
    "hypothese": "intuition ou idée non étayée",
    "documentee": "décrite dans une source fiable (syllabus, norme, publication)",
    "pratiquee": "pratique reconnue et répandue dans l'industrie",
    "eprouvee": "éprouvée dans notre propre contexte",
}
RELATIONS = {
    "complementaire": "se combinent utilement",
    "contradictoire": "s'opposent ou se concurrencent",
    "variante": "variante ou cas particulier",
    "prerequis": "la source est un prérequis de la cible",
    "remplace": "la source remplace la cible (obsolète)",
}
TYPES_REFERENCE = ("istqb", "norme", "web", "livre", "article", "interne", "conversation")
CHAMPS_TEXTE = ("titre", "resume", "probleme", "principe", "domaine_application", "prerequis",
                "benefices", "limites")
SEUIL_DOUBLON, SEUIL_PROCHE = 0.6, 0.35
# Seuls champs qu'une saisie (`idee ajouter` / `idee modifier`) peut fournir. Identifiant,
# dates, relations et retours sont gérés par l'outil ou par leurs commandes dédiées
# (`idee lier`, `idee retour`) : les accepter ici permettrait d'écraser une autre idée
# ou de falsifier l'historique.
CHAMPS_SAISIE = (*CHAMPS_TEXTE, "theme_principal", "themes_secondaires", "maturite", "statut",
                 "provenance", "references")
CHAMPS_GERES = {"id": "attribué par l'outil", "cree_le": "daté par l'outil", "maj_le": "daté par l'outil",
                "relations": "passer par `idee lier`", "retours": "passer par `idee retour`"}

SCHEMA = """
CREATE TABLE IF NOT EXISTS idees (
    id TEXT PRIMARY KEY, titre TEXT NOT NULL, resume TEXT NOT NULL, probleme TEXT NOT NULL,
    principe TEXT NOT NULL, theme_principal TEXT NOT NULL, domaine_application TEXT, prerequis TEXT,
    benefices TEXT, limites TEXT, maturite TEXT NOT NULL, statut TEXT NOT NULL, provenance TEXT,
    cree_le TEXT NOT NULL, maj_le TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS idee_themes (
    idee_id TEXT NOT NULL, theme TEXT NOT NULL, principal INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (idee_id, theme)
);
CREATE TABLE IF NOT EXISTS refs (
    idee_id TEXT NOT NULL, ordre INTEGER NOT NULL, type TEXT NOT NULL, titre TEXT, doc_id TEXT,
    version TEXT, pages TEXT, section TEXT, url TEXT, extrait TEXT, consulte_le TEXT, note TEXT,
    PRIMARY KEY (idee_id, ordre)
);
CREATE TABLE IF NOT EXISTS relations (
    source TEXT NOT NULL, cible TEXT NOT NULL, type TEXT NOT NULL, note TEXT, cree_le TEXT,
    PRIMARY KEY (source, cible, type)
);
CREATE TABLE IF NOT EXISTS retours (
    idee_id TEXT NOT NULL, ordre INTEGER NOT NULL, date TEXT, contexte TEXT, resultat TEXT,
    enseignement TEXT, PRIMARY KEY (idee_id, ordre)
);
CREATE TABLE IF NOT EXISTS meta (cle TEXT PRIMARY KEY, valeur TEXT);
CREATE VIRTUAL TABLE IF NOT EXISTS idees_fts USING fts5(
    id UNINDEXED, titre, contenu, tokenize='porter unicode61 remove_diacritics 2'
);
"""


class ErreurValidation(ValueError):
    pass


# ---------------------------------------------------------------- stockage

def _empreinte_fichier() -> str | None:
    p = chemins.connaissances_jsonl()
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def ouvrir() -> sqlite3.Connection:
    """Ouvre la base ; la reconstruit depuis le JSONL versionné s'il a changé."""
    db = chemins.base_db()
    db.parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(db)
    cx.row_factory = sqlite3.Row
    cx.executescript(SCHEMA)
    try:
        if _action_miroir(cx):
            # Verrou d'écriture puis second contrôle : un autre processus peut être en
            # train d'exporter ; reconstruire sans verrou depuis un état intermédiaire
            # effaçait les idées qu'il venait d'ajouter.
            cx.execute("BEGIN IMMEDIATE")
            action = _action_miroir(cx)
            if action == "reconstruire":
                _reconstruire(cx)
            elif action == "exporter":
                _exporter(cx)  # base sans miroir (première version) : on crée le miroir
            else:
                cx.rollback()
    except BaseException:
        cx.close()
        raise
    return cx


def _action_miroir(cx) -> str | None:
    """« reconstruire » si le JSONL a changé, « exporter » si la base n'a pas encore de
    miroir, None si tout est à jour."""
    h = _empreinte_fichier()
    if h:
        connu = cx.execute("SELECT valeur FROM meta WHERE cle='hash_jsonl'").fetchone()
        return None if connu and connu[0] == h else "reconstruire"
    return "exporter" if cx.execute("SELECT 1 FROM idees LIMIT 1").fetchone() else None


COLONNES_REQUISES = ("id", "titre", "resume", "probleme", "principe", "theme_principal", "maturite", "statut",
                     "cree_le", "maj_le")
_AVERTISSEMENTS: list[str] = []


def avertissements() -> list[str]:
    """Avertissements produits à l'ouverture (reconstruction depuis un JSONL modifié hors
    de l'outil) ; la liste est vidée à la lecture. La CLI les affiche après chaque commande."""
    out = list(_AVERTISSEMENTS)
    _AVERTISSEMENTS.clear()
    return out


def _lire_jsonl() -> list[dict]:
    p = chemins.connaissances_jsonl()
    idees = []
    for n, ligne in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not ligne.strip():
            continue
        try:
            idee = json.loads(ligne)
        except json.JSONDecodeError as exc:
            raise ErreurValidation(f"{p.name}, ligne {n} : JSON invalide ({exc.msg}). Corriger la ligne "
                                   "à la main (ou `git checkout` du fichier), puis relancer.") from exc
        manquants = [c for c in COLONNES_REQUISES if not isinstance(idee, dict) or not idee.get(c)]
        if manquants:
            raise ErreurValidation(f"{p.name}, ligne {n} : champ(s) obligatoire(s) absent(s) : "
                                   f"{', '.join(manquants)}. Compléter la ligne, puis relancer.")
        idees.append(idee)
    return idees


def _anomalies(idee: dict, ids: set[str]) -> list[str]:
    """Règles que l'outil applique à l'écriture, recontrôlées sur une idée relue depuis le
    JSONL (qui peut avoir été modifié à la main) : rien n'interdit de reconstruire, mais
    l'écart doit être vu et tracé."""
    out = []
    inconnus = sorted(k for k in idee if k not in CHAMPS_SAISIE and k not in CHAMPS_GERES)
    if inconnus:
        out.append(f"champ(s) inconnu(s) : {', '.join(inconnus)}")
    saisie = {k: v for k, v in idee.items() if k in CHAMPS_SAISIE and k != "statut"}
    try:
        valider(saisie)
    except (ErreurValidation, KeyError) as exc:
        out.append(exc.args[0] if exc.args else str(exc))
    statut = idee.get("statut")
    if statut not in STATUTS:
        out.append(f"statut invalide : {statut}")
    elif statut == "experimentee" and not idee.get("retours"):
        out.append("« expérimentée » sans retour d'expérience")
    elif statut == "validee" and not idee.get("references") and not idee.get("retours"):
        out.append("« validée » sans référence ni retour d'expérience")
    for r in idee.get("relations", []):
        if not isinstance(r, dict) or r.get("type") not in RELATIONS:
            out.append(f"relation invalide : {r}")
        elif r.get("cible") not in ids:
            out.append(f"relation {r.get('type')} vers {r.get('cible')} : idée cible inexistante (orpheline)")
    return [f"{idee['id']} : {m}" for m in out]


def _differentiel(avant: dict[str, dict], apres: dict[str, dict]) -> dict:
    """Changements que le journal n'explique pas : idée ajoutée sans `idee_creee`, retirée
    sans `idee_retiree`, modifiée sans entrée de journal à sa date de mise à jour
    (une modification par l'outil, même sur un autre poste, met à jour `maj_le` et journalise)."""
    entrees = journal.lire(limite=10 ** 9)
    actions = {(e["cible"], e["action"]) for e in entrees}
    dernieres = {}
    for e in entrees:
        dernieres[e["cible"]] = max(dernieres.get(e["cible"], ""), e["horodatage"][:19])
    diff = {}
    ajoutees = sorted(i for i in apres.keys() - avant.keys() if (i, "idee_creee") not in actions)
    supprimees = sorted(i for i in avant.keys() - apres.keys() if (i, "idee_retiree") not in actions)
    modifiees = {}
    for i in sorted(avant.keys() & apres.keys()):
        a, b = avant[i], apres[i]
        champs = {k: {"avant": a.get(k), "apres": b.get(k)} for k in sorted(a.keys() | b.keys())
                  if k != "maj_le" and _forme(a.get(k)) != _forme(b.get(k))}
        if not champs:
            continue
        explique = b.get("maj_le") != a.get("maj_le") and dernieres.get(i, "") >= str(b.get("maj_le"))[:19]
        if not explique:
            modifiees[i] = champs
    for cle, val in (("ajoutees", ajoutees), ("supprimees", supprimees), ("modifiees", modifiees)):
        if val:
            diff[cle] = val
    return diff


def _forme(v):
    """Valeur comparable : listes vides et absences sont équivalentes."""
    return None if v in (None, "", []) else json.dumps(v, sort_keys=True, ensure_ascii=False)


def _reconstruire(cx: sqlite3.Connection) -> None:
    idees = _lire_jsonl()
    vus, doubles = set(), set()
    for i in idees:
        (doubles if i["id"] in vus else vus).add(i["id"])
    if doubles:
        # Typiquement un conflit Git résolu en gardant les deux côtés : reconstruire
        # garderait une seule des deux lignes et la perte deviendrait définitive au
        # prochain export. On refuse et on laisse l'arbitrage à l'utilisateur.
        raise ErreurValidation(
            f"Identifiants en double dans {chemins.connaissances_jsonl().name} : {', '.join(sorted(doubles))}. "
            "Fusionner ou renuméroter ces lignes à la main (conflit Git ?), puis relancer.")
    base_connue = cx.execute("SELECT 1 FROM meta WHERE cle='hash_jsonl'").fetchone() is not None
    avant = {r["id"]: _charger(cx, r["id"]) for r in cx.execute("SELECT id FROM idees")} if base_connue else {}
    anomalies = [m for i in idees for m in _anomalies(i, vus)]
    for t in ("idees", "idee_themes", "refs", "relations", "retours", "idees_fts"):
        cx.execute(f"DELETE FROM {t}")
    for idee in idees:
        _inserer(cx, idee, relations=True)
    cx.execute("INSERT OR REPLACE INTO meta VALUES ('hash_jsonl', ?)", (_empreinte_fichier(),))
    cx.commit()
    diff = _differentiel(avant, {i["id"]: _charger(cx, i["id"]) for i in idees}) if base_connue else {}
    if diff or anomalies:
        if diff:
            # Seul un changement inexpliqué est journalisé : une base neuve (clone) ou un
            # `git pull` d'ajouts faits avec l'outil ne produit pas d'entrée.
            journal.noter("modification_externe", chemins.connaissances_jsonl().name,
                          {**diff, **({"anomalies": anomalies} if anomalies else {})},
                          "JSONL modifié hors de l'outil (édition manuelle, fusion ou revert Git)")
        libelles = {"ajoutees": "ajoutée(s)", "supprimees": "supprimée(s)", "modifiees": "modifiée(s)"}
        resume = ", ".join(f"{len(v)} idée(s) {libelles[k]}" for k, v in diff.items())
        if diff:
            _AVERTISSEMENTS.append(f"{chemins.connaissances_jsonl().name} modifié hors de l'outil ({resume}) : "
                                   "écart tracé dans le journal (`journal --cible connaissances.jsonl`).")
        _AVERTISSEMENTS.extend(f"anomalie {a}" for a in anomalies)


def _inserer(cx, idee: dict, relations: bool = False, nouvelle: bool = False) -> None:
    cols = ("id", *CHAMPS_TEXTE, "theme_principal", "maturite", "statut", "provenance", "cree_le", "maj_le")
    cx.execute(f"INSERT {'' if nouvelle else 'OR REPLACE '}INTO idees({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
               [idee.get(c) for c in cols])
    cx.execute("DELETE FROM idee_themes WHERE idee_id=?", (idee["id"],))
    cx.execute("INSERT INTO idee_themes VALUES (?,?,1)", (idee["id"], idee["theme_principal"]))
    for t in idee.get("themes_secondaires", []):
        if t != idee["theme_principal"]:
            cx.execute("INSERT OR IGNORE INTO idee_themes VALUES (?,?,0)", (idee["id"], t))
    cx.execute("DELETE FROM refs WHERE idee_id=?", (idee["id"],))
    for i, r in enumerate(idee.get("references", [])):
        cx.execute("INSERT INTO refs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                   (idee["id"], i, r.get("type"), r.get("titre"), r.get("doc_id"), r.get("version"),
                    r.get("pages"), r.get("section"), r.get("url"), r.get("extrait"), r.get("consulte_le"),
                    r.get("note")))
    cx.execute("DELETE FROM retours WHERE idee_id=?", (idee["id"],))
    for i, r in enumerate(idee.get("retours", [])):
        cx.execute("INSERT INTO retours VALUES (?,?,?,?,?,?)",
                   (idee["id"], i, r.get("date"), r.get("contexte"), r.get("resultat"), r.get("enseignement")))
    if relations:
        for r in idee.get("relations", []):
            cx.execute("INSERT OR REPLACE INTO relations VALUES (?,?,?,?,?)",
                       (idee["id"], r["cible"], r["type"], r.get("note"), r.get("cree_le")))
    cx.execute("DELETE FROM idees_fts WHERE id=?", (idee["id"],))
    contenu = " ".join(str(idee.get(c) or "") for c in CHAMPS_TEXTE[1:])
    cx.execute("INSERT INTO idees_fts(id, titre, contenu) VALUES (?,?,?)", (idee["id"], idee["titre"], contenu))


def _exporter(cx: sqlite3.Connection) -> None:
    """Réécrit le miroir JSONL (tri stable par identifiant : diffs Git lisibles)."""
    p = chemins.connaissances_jsonl()
    p.parent.mkdir(parents=True, exist_ok=True)
    lignes = [json.dumps(_charger(cx, r["id"]), ensure_ascii=False, sort_keys=False)
              for r in cx.execute("SELECT id FROM idees ORDER BY id")]
    # Écriture atomique : un lecteur concurrent voit l'ancien fichier ou le nouveau,
    # jamais un fichier tronqué (qui déclenchait une reconstruction à vide).
    tmp = p.with_name(f".{p.name}.{os.getpid()}.tmp")
    tmp.write_text("".join(l + "\n" for l in lignes), encoding="utf-8")
    os.replace(tmp, p)
    cx.execute("INSERT OR REPLACE INTO meta VALUES ('hash_jsonl', ?)", (_empreinte_fichier(),))
    cx.commit()


def _charger(cx, idee_id: str) -> dict:
    r = cx.execute("SELECT * FROM idees WHERE id=?", (idee_id,)).fetchone()
    if not r:
        raise KeyError(f"Idée inconnue : {idee_id}. Voir `idee lister` ou `idee chercher`.")
    idee = {k: r[k] for k in r.keys() if r[k] is not None}
    idee["themes_secondaires"] = [x["theme"] for x in cx.execute(
        "SELECT theme FROM idee_themes WHERE idee_id=? AND principal=0 ORDER BY theme", (idee_id,))]
    idee["references"] = [{k: x[k] for k in x.keys() if x[k] is not None and k not in ("idee_id", "ordre")}
                          for x in cx.execute("SELECT * FROM refs WHERE idee_id=? ORDER BY ordre", (idee_id,))]
    idee["retours"] = [{k: x[k] for k in x.keys() if x[k] is not None and k not in ("idee_id", "ordre")}
                       for x in cx.execute("SELECT * FROM retours WHERE idee_id=? ORDER BY ordre", (idee_id,))]
    idee["relations"] = [{k: x[k] for k in ("cible", "type", "note", "cree_le") if x[k] is not None}
                         for x in cx.execute("SELECT * FROM relations WHERE source=? ORDER BY cible, type",
                                             (idee_id,))]
    return idee


# ---------------------------------------------------------------- validation

FORMAT_PAGES = re.compile(r"\d+(\s*[-–]\s*\d+)?(\s*,\s*\d+(\s*[-–]\s*\d+)?)*")
FORMAT_SECTION = re.compile(r"\d+(\.\d+)*")
MOTS_EXTRAIT_MIN = 6


def _pages(texte: str) -> set[int]:
    """« 31 », « 31-33 », « 4, 6 » → ensemble de pages. Tout autre format (« -5 »,
    « p. 4 », « 0 », plage inversée) est refusé plutôt qu'interprété."""
    texte = texte.strip()
    if not FORMAT_PAGES.fullmatch(texte):
        raise ErreurValidation(f"Pages « {texte} » : format attendu « 31 », « 31-33 » ou « 4, 6 ».")
    pages = set()
    for a, b in re.findall(r"(\d+)\s*(?:[-–]\s*(\d+))?", texte):
        a, b = int(a), int(b or a)
        if a < 1 or b < a:
            raise ErreurValidation(f"Pages « {texte} » : numéros de page à partir de 1, plages croissantes.")
        pages |= set(range(a, b + 1)) if b - a < 200 else {a}
    return pages


def _compacter(texte: str) -> str:
    """Texte normalisé sans aucun espace : recolle les fragments que les PDF découpent
    (« êtr e », « perme ttant », coupures de fin de ligne) sans tolérer le moindre
    changement d'ordre, de mot ni de négation."""
    return normaliser(texte).replace(" ", "")


def _verifier_extrait(extrait: str, texte_source: str, lieu: str) -> None:
    """L'extrait doit être une suite CONTIGUË du texte cité (après normalisation) et
    compter au moins MOTS_EXTRAIT_MIN mots significatifs : un sac de mots à 70 %
    acceptait des citations inversées, inventées ou en vrac (#28)."""
    significatifs = mots(extrait)
    if len(significatifs) < MOTS_EXTRAIT_MIN:
        raise ErreurValidation(
            f"Extrait trop court ({len(significatifs)} mot(s) significatif(s), minimum {MOTS_EXTRAIT_MIN}) : "
            "recopier une phrase entière du passage lu.")
    if _compacter(extrait) not in _compacter(texte_source):
        raise ErreurValidation(
            f"L'extrait cité n'apparaît pas mot pour mot {lieu} : recopier une suite continue du passage "
            "lu (`lire` / `page`), sans reformuler ni couper au milieu.")


MARQUEURS_LANGUE = {
    "fr": {"le", "la", "les", "des", "est", "et", "pour", "une", "dans", "du", "sont", "qui", "par", "au"},
    "en": {"the", "and", "of", "is", "to", "for", "in", "with", "are", "be", "which", "by", "that"},
}


def _langue_extrait(extrait: str | None) -> str | None:
    """Langue d'un extrait d'après ses mots-outils ; None si rien ne la départage."""
    toks = normaliser(extrait or "").split()
    fr, en = (sum(t in MARQUEURS_LANGUE[l] for t in toks) for l in ("fr", "en"))
    return None if fr == en else "fr" if fr > en else "en"


def _document_reference(cx, doc: str, extrait: str | None):
    """Document désigné par `doc` : identifiant exact, sinon code ISTQB. Un code peut
    désigner plusieurs documents courants (EN et FR, syllabus et BoK) : on départage par
    la langue de l'extrait, sinon on exige l'identifiant exact plutôt que de choisir au
    hasard (une vraie citation FR était vérifiée contre la version EN, #37)."""
    exact = cx.execute("SELECT * FROM documents WHERE doc_id=? COLLATE NOCASE", (doc,)).fetchone()
    if exact:
        return exact
    docs = cx.execute("SELECT * FROM documents WHERE code=? COLLATE NOCASE ORDER BY doc_id", (doc,)).fetchall()
    candidats = [x for x in docs if x["statut_version"] == "courant"] or docs
    if len(candidats) > 1:
        langue = _langue_extrait(extrait)
        candidats = [x for x in candidats if x["langue"] == langue] or candidats
    if len(candidats) > 1:
        raise ErreurValidation(
            f"Code « {doc} » ambigu ({', '.join(x['doc_id'] for x in candidats)}) : préciser le doc_id exact"
            + (" (la langue de l'extrait ne suffit pas à départager)." if extrait else "."))
    return candidats[0] if candidats else None


def _verifier_reference_istqb(ref: dict) -> list[str]:
    """Contrôle une référence ISTQB contre la bibliothèque indexée : document présent,
    pages existantes, section du plan présente sur les pages citées, extrait recopié
    mot pour mot (suite contiguë) des pages ou de la section citées."""
    problemes = []
    if not chemins.index_db().exists():
        return ["bibliothèque non indexée : référence ISTQB non vérifiable"]
    cx = bibliotheque.connecter()
    try:
        doc = ref.get("doc_id")
        d = _document_reference(cx, doc, ref.get("extrait")) if doc else None
        if not d:
            return [f"document « {doc} » absent de la bibliothèque : référence non vérifiable"]
        ref["doc_id"] = d["doc_id"]
        ref.setdefault("version", d["version"])
        ref.setdefault("titre", d["titre"])
        if d["statut_version"] == "absent":
            problemes.append(f"{d['doc_id']} : fichier source absent de la bibliothèque (référence non relisible)")
        elif d["statut_version"] == "remplace":
            problemes.append(f"{d['doc_id']} est une version remplacée (par {d['remplace_par']})")
        pages = _pages(str(ref["pages"])) if str(ref.get("pages") or "").strip() else set()
        section = str(ref.get("section") or "").strip().rstrip(".")
        if not pages and not section:
            raise ErreurValidation(f"Référence ISTQB {d['doc_id']} sans page ni section : impossible à vérifier.")
        if section and not FORMAT_SECTION.fullmatch(section):
            raise ErreurValidation(f"Section « {section} » : numéro attendu (ex. 3.1.2), voir `plan {d['doc_id']}`.")
        for p in sorted(pages):
            if p > (d["nb_pages"] or 0):
                raise ErreurValidation(f"Page {p} inexistante dans {d['doc_id']} ({d['nb_pages']} pages).")
        dans_section = "(section_num=? OR section_num LIKE ? ESCAPE '\\')"
        if section and not cx.execute(f"SELECT 1 FROM sections WHERE doc_id=? AND (numero=? OR numero LIKE ? ESCAPE '\\')",
                                      (d["doc_id"], section, motif_sous_sections(section))).fetchone():
            raise ErreurValidation(f"Section {section} absente du plan de {d['doc_id']} (voir `plan {d['doc_id']}`).")
        place = f" AND page IN ({', '.join('?' * len(pages))})"
        if section and pages and d["statut_version"] != "absent" and not cx.execute(
                f"SELECT 1 FROM passages WHERE doc_id=? AND {dans_section}{place}",
                (d["doc_id"], section, motif_sous_sections(section), *sorted(pages))).fetchone():
            raise ErreurValidation(
                f"La section {section} de {d['doc_id']} ne figure pas aux pages {ref.get('pages')} : "
                f"vérifier la page ou la section (`section {d['doc_id']} {section}`).")
        if ref.get("extrait") and d["statut_version"] != "absent":
            sql, params = "SELECT texte FROM passages WHERE doc_id=?", [d["doc_id"]]
            if pages:  # exactement les pages citées
                sql += place
                params += sorted(pages)
            else:      # sinon, la section citée et ses sous-sections
                sql += f" AND {dans_section}"
                params += [section, motif_sous_sections(section)]
            texte = " ".join(x["texte"] for x in cx.execute(sql + " ORDER BY ordre", params))
            lieu = f"aux pages {ref.get('pages')}" if pages else f"dans la section {section}"
            _verifier_extrait(ref["extrait"], texte, f"{lieu} de {d['doc_id']}")
    finally:
        cx.close()
    return problemes


CHAMPS_CHAINE = (*CHAMPS_TEXTE, "theme_principal", "maturite", "statut", "provenance")


def _controler_types(donnees) -> None:
    """Types attendus du JSON saisi : un message français plutôt qu'une trace Python."""
    if not isinstance(donnees, dict):
        raise ErreurValidation("L'idée doit être un objet JSON ({…}) : voir `idee modele`.")
    for champ in CHAMPS_CHAINE:
        if donnees.get(champ) is not None and not isinstance(donnees[champ], str):
            raise ErreurValidation(f"Champ {champ} : texte attendu (reçu {type(donnees[champ]).__name__}).")
    t = donnees.get("themes_secondaires")
    if t is not None and not (isinstance(t, list) and all(isinstance(x, str) for x in t)):
        raise ErreurValidation("Champ themes_secondaires : liste de codes de thème attendue "
                               "(ex. [\"metriques\"]).")
    refs = donnees.get("references")
    if refs is not None and not (isinstance(refs, list) and all(isinstance(r, dict) for r in refs)):
        raise ErreurValidation("Champ references : liste d'objets attendue (ex. [{\"type\": \"web\", …}]).")
    for r in refs or []:
        for k, v in r.items():
            if v is not None and not isinstance(v, str) and not (k == "pages" and isinstance(v, int)
                                                                 and not isinstance(v, bool)):
                raise ErreurValidation(f"Champ references.{k} : texte attendu (reçu {type(v).__name__}).")


def valider(donnees: dict, partiel: bool = False) -> tuple[dict, list[str]]:
    """Normalise et contrôle une idée. Renvoie (idée, avertissements)."""
    _controler_types(donnees)
    avert = []
    geres = [f"« {k} » ({CHAMPS_GERES[k]})" for k in donnees if k in CHAMPS_GERES]
    if geres:
        raise ErreurValidation(f"Champ(s) non modifiable(s) par saisie : {', '.join(geres)}.")
    inconnus = sorted(k for k in donnees if k not in CHAMPS_SAISIE)
    if inconnus:
        raise ErreurValidation(f"Champ(s) inconnu(s) : {', '.join(inconnus)} (voir `idee modele`).")
    d = {k: (v.strip() if isinstance(v, str) else v) for k, v in donnees.items() if v not in (None, "", [])}
    if not partiel:
        manquants = [c for c in ("titre", "resume", "probleme", "principe", "theme_principal") if not d.get(c)]
        if manquants:
            raise ErreurValidation(f"Champs obligatoires manquants : {', '.join(manquants)}.")
    for champ in ("theme_principal",):
        if champ in d:
            code = taxonomie.resoudre(d[champ])
            if code != d[champ]:
                avert.append(f"thème {d[champ]} obsolète → {code}")
            d[champ] = code
    if "themes_secondaires" in d:
        d["themes_secondaires"] = sorted({taxonomie.resoudre(t) for t in d["themes_secondaires"]})
    if not partiel:
        d.setdefault("statut", "a_explorer")
        d.setdefault("maturite", "hypothese")
    for champ, permis in (("statut", STATUTS), ("maturite", MATURITES)):
        if champ in d and d[champ] not in permis:
            raise ErreurValidation(f"{champ} invalide : {d[champ]} (valeurs : {', '.join(permis)}).")
    if not partiel and d["statut"] in ("validee", "experimentee"):
        raise ErreurValidation("Une nouvelle idée ne peut pas être créée « validée » ou « expérimentée » : "
                               "la créer puis utiliser `idee statut` avec un motif (et un retour d'expérience).")
    refs = []
    for r in d.get("references", []):
        r = {k: (str(v) if k == "pages" else v.strip()) for k, v in r.items() if v not in (None, "")}
        if r.get("type") not in TYPES_REFERENCE:
            raise ErreurValidation(f"Type de référence invalide : {r.get('type')} ({', '.join(TYPES_REFERENCE)}).")
        if r["type"] == "web" and not r.get("url"):
            raise ErreurValidation("Une référence web doit avoir une URL.")
        if r["type"] == "istqb":
            avert += [f"référence {r.get('doc_id')} : {p}" for p in _verifier_reference_istqb(r)]
        if r["type"] in ("web", "article") and not r.get("consulte_le"):
            r["consulte_le"] = date.today().isoformat()
        refs.append(r)
    if "references" in d:
        d["references"] = refs
    if not partiel:
        _exiger_source(d)
    return d, avert


MOTIF_MIN = 10

# Dépôt public : ce qui ressemble à une donnée personnelle ou confidentielle bloque
# l'enregistrement (sauf --forcer --motif). Les noms de clients, de personnes ou de projets
# ne sont pas détectables : la règle d'anonymisation du skill les couvre.
_ESPACE = r"[ \u00a0\u202f]"
MOTIFS_SENSIBLES = {
    "adresse e-mail": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "montant": re.compile(
        rf"(?<![\w.,])\d+(?:[.,{_ESPACE[1:-1]}]\d+)*{_ESPACE}?(?:[kKM]{_ESPACE}?)?(?:€|\$|£|euros?\b|EUR\b|USD\b|dollars?\b)"
        rf"|[€$£]{_ESPACE}?\d+(?:[.,]\d+)*{_ESPACE}?[kKM]?\b"),
    "numéro de téléphone": re.compile(
        rf"(?<![\w+])(?:\+\d{{2,3}}{_ESPACE}?(?:\(0\))?{_ESPACE}?\d|0\d)(?:[{_ESPACE[1:-1]}.-]?\d{{2}}){{4}}(?!\d)"),
}


def _textes_libres(d: dict) -> list[tuple[str, str]]:
    out = [(c, d[c]) for c in (*CHAMPS_TEXTE, "provenance") if isinstance(d.get(c), str)]
    for i, r in enumerate(d.get("references", [])):
        out += [(f"references[{i}].{k}", v) for k, v in r.items() if isinstance(v, str) and k != "url"]
    for i, r in enumerate(d.get("retours", [])):
        out += [(f"retours[{i}].{k}", v) for k, v in r.items() if isinstance(v, str)]
    return out


def _controler_confidentialite(d: dict, forcer: bool, motif: str | None) -> tuple[list[str], list[str]]:
    """Renvoie (avertissements, types forcés). Lève si une donnée sensible est trouvée sans
    `--forcer --motif` ; avertit sur les références « interne »."""
    trouves = [(nature, champ, m.group().strip()) for champ, texte in _textes_libres(d)
               for nature, rx in MOTIFS_SENSIBLES.items() for m in rx.finditer(texte)]
    avert = [f"référence « interne » ({r.get('titre', 'sans titre')}) : le dépôt est public, vérifier qu'elle "
             "ne révèle ni client, ni personne, ni projet, ni montant" for r in d.get("references", [])
             if r.get("type") == "interne"]
    if trouves and not (forcer and (motif or "").strip()):
        detail = "; ".join(f"{n} « {v} » ({c})" for n, c, v in trouves)
        raise ErreurValidation(
            f"Donnée personnelle ou confidentielle probable : {detail}. Le dépôt est PUBLIC : anonymiser "
            "(ni client, ni personne, ni montant, ni projet nommé). Si c'est voulu : --forcer --motif \"…\".")
    if trouves:
        avert.append("donnée sensible conservée sur décision explicite (--forcer) : "
                     + ", ".join(sorted({n for n, _, _ in trouves})))
    return avert, sorted({n for n, _, _ in trouves})


def _exiger_source(idee: dict) -> None:
    """« documentée » / « pratiquée » affirment une source : sans référence, c'est faux."""
    if idee.get("maturite") in ("documentee", "pratiquee") and not idee.get("references"):
        raise ErreurValidation(
            f"Maturité « {idee['maturite']} » sans aucune référence : ajouter la source (syllabus, norme, "
            "publication) dans `references`, ou garder « hypothese ».")


# ---------------------------------------------------------------- déduplication

def _sig_titre(i: dict) -> set:
    return signature(i.get("titre", ""))


def _sig_contenu(i: dict) -> set:
    return signature(" ".join(str(i.get(c) or "") for c in ("titre", "resume", "probleme", "principe")))


TERMES_BANALS = {"qa", "istqb", "test", "tests", "testeur", "testeurs", "tester"}


def _termes_distinctifs(texte: str) -> set[str]:
    """Noms propres et sigles d'un texte (Herzberg, TMMi, IDEAL) : un sigle (au moins deux
    majuscules) partout ; un mot capitalisé seulement hors début de phrase et s'il n'apparaît
    jamais en minuscules dans le texte (« Équipe … équipe » n'est pas un nom propre)."""
    minuscules = set(re.findall(r"\b[^\W\d_]+\b", texte))
    out = set()
    for m in re.finditer(r"[^\W\d_]+", texte):
        mot = m.group()
        if len(mot) < 3:
            continue
        avant = texte[:m.start()].rstrip()
        sigle = sum(c.isupper() for c in mot) >= 2
        nom_propre = (mot[0].isupper() and mot[1:].islower() and avant and avant[-1] not in ".!?:;"
                      and mot.lower() not in minuscules)
        n = normaliser(mot)
        if (sigle or nom_propre) and n not in MOTS_VIDES and n not in TERMES_BANALS:
            out.add(n)
    return out


def _termes_idee(i: dict, champs=("titre", "resume", "probleme", "principe")) -> set[str]:
    return set().union(*(_termes_distinctifs(str(i.get(c) or "")) for c in champs))


def similarite(a: dict, b: dict) -> float:
    """Signatures du thésaurus (titre, contenu), plus deux indices qui manquaient pour une
    même idée reformulée ou traduite (#27) : le thème principal commun et les noms
    propres / sigles partagés absents du thésaurus (Herzberg), surtout s'ils figurent dans les
    deux titres."""
    st, sb = _sig_titre(a), _sig_titre(b)
    titre = max(jaccard(st, sb), 0.8 * recouvrement(st, sb))
    contenu = jaccard(_sig_contenu(a), _sig_contenu(b))
    score = 0.55 * titre + 0.45 * min(1.0, contenu * 1.6)
    if a.get("theme_principal") and a.get("theme_principal") == b.get("theme_principal"):
        score += 0.1
    # Les sigles du thésaurus (TMMi, IDEAL, API) pèsent déjà dans les signatures :
    # seuls les termes qu'il ignore (Herzberg, Maslow…) reçoivent ce bonus.
    communs = {t for t in _termes_idee(a) & _termes_idee(b) if t not in termes_thesaurus()}
    titres = set(normaliser(a.get("titre", "")).split()) & set(normaliser(b.get("titre", "")).split())
    score += 0.3 if communs & titres else 0.15 if communs else 0.0
    return round(min(1.0, score), 2)


def doublons(candidat: dict, exclure: str | None = None, cx: sqlite3.Connection | None = None) -> list[dict]:
    propre = cx is None
    cx = cx or ouvrir()
    try:
        out = []
        for r in cx.execute("SELECT id FROM idees"):
            if r["id"] == exclure:
                continue
            autre = _charger(cx, r["id"])
            s = similarite(candidat, autre)
            if s >= SEUIL_PROCHE:
                out.append({"id": autre["id"], "titre": autre["titre"], "statut": autre["statut"], "score": s,
                            "verdict": "doublon probable" if s >= SEUIL_DOUBLON else "proche"})
        return sorted(out, key=lambda x: -x["score"])
    finally:
        if propre:
            cx.close()


# ---------------------------------------------------------------- écriture

def _nouvel_id(cx) -> str:
    """Identifiant daté et aléatoire, QA-AAAAMMJJ-xxxx : jamais réattribué, même après un
    `git revert` qui efface l'idée ET sa trace dans le journal (un compteur séquentiel
    redonnait alors le même numéro à une autre idée, #34). Les anciens QA-0001… restent
    valides. Unicité vérifiée contre les idées, les cibles de relations et le journal."""
    vus = {r[0] for r in cx.execute("SELECT id FROM idees UNION SELECT cible FROM relations")}
    vus |= {e["cible"] for e in journal.lire(limite=10 ** 9)}
    while True:
        candidat = f"QA-{date.today():%Y%m%d}-{secrets.token_hex(2)}"
        if candidat not in vus:
            return candidat


def ajouter(donnees: dict, forcer: bool = False, motif: str | None = None) -> dict:
    """Crée une idée après validation et contrôle des doublons.
    Un doublon probable bloque, sauf `forcer` avec un motif (journalisé)."""
    idee, avert = valider(donnees)
    avert_conf, forces = _controler_confidentialite(idee, forcer, motif)
    avert += avert_conf
    cx = ouvrir()
    try:
        # Verrou d'écriture AVANT de lire les doublons et le dernier identifiant : deux
        # ajouts simultanés ne peuvent pas obtenir le même identifiant.
        cx.execute("BEGIN IMMEDIATE")
        sim = doublons(idee, cx=cx)
        probables = [s for s in sim if s["verdict"] == "doublon probable"]
        if probables and not forcer:
            cx.rollback()
            return {"etat": "refuse", "doublons": sim, "avertissements": avert,
                    "message": "Doublon probable : compléter l'idée existante (`idee modifier`) ou la lier "
                               "(`idee lier`) plutôt que d'en créer une nouvelle."}
        if probables and not motif:
            raise ErreurValidation("--forcer exige --motif : expliquer en quoi l'idée diffère de l'existante.")
        maintenant = datetime.now().isoformat(timespec="seconds")
        idee.update(id=_nouvel_id(cx), cree_le=maintenant, maj_le=maintenant)
        idee.setdefault("provenance", "saisie conversationnelle")
        _inserer(cx, idee, nouvelle=True)
        _exporter(cx)
        journal.noter("idee_creee", idee["id"], {"titre": idee["titre"], "doublons_signales": sim,
                                                 **({"donnees_sensibles_forcees": forces} if forces else {})}, motif)
        return {"etat": "cree", "id": idee["id"], "doublons": sim, "avertissements": avert}
    finally:
        cx.close()


def modifier(idee_id: str, donnees: dict, remplacer_listes: bool = False, motif: str | None = None,
             forcer: bool = False) -> dict:
    """Met à jour une idée. Par défaut les références et thèmes secondaires sont AJOUTÉS
    (rien n'est perdu) ; `remplacer_listes` les remplace."""
    cx = ouvrir()
    try:
        avant = _charger(cx, idee_id)
        if "statut" in donnees:
            raise ErreurValidation("Changer le statut passe par `idee statut` (motif et contrôles dédiés).")
        maj, avert = valider(donnees, partiel=True)
        avert_conf, forces = _controler_confidentialite(maj, forcer, motif)
        avert += avert_conf
        apres = dict(avant)
        for k, v in maj.items():
            if k in ("references", "themes_secondaires") and not remplacer_listes:
                existant = avant.get(k, [])
                cle = (lambda x: json.dumps(x, sort_keys=True)) if k == "references" else (lambda x: x)
                vus = {cle(x) for x in existant}
                apres[k] = existant + [x for x in v if cle(x) not in vus]
            else:
                apres[k] = v
        _exiger_source(apres)
        apres["maj_le"] = datetime.now().isoformat(timespec="seconds")
        changes = {k: {"avant": avant.get(k), "apres": apres.get(k)} for k in maj if avant.get(k) != apres.get(k)}
        if not changes:
            return {"etat": "inchange", "id": idee_id, "avertissements": avert}
        _inserer(cx, apres)
        _exporter(cx)
        journal.noter("idee_modifiee", idee_id, {**changes, **({"donnees_sensibles_forcees": forces} if forces else {})},
                      motif)
        return {"etat": "modifie", "id": idee_id, "champs": sorted(changes), "avertissements": avert}
    finally:
        cx.close()


def changer_statut(idee_id: str, statut: str, motif: str | None) -> dict:
    if statut not in STATUTS:
        raise ErreurValidation(f"Statut invalide : {statut} ({', '.join(STATUTS)}).")
    cx = ouvrir()
    try:
        idee = _charger(cx, idee_id)
        motif = (motif or "").strip()
        if statut in ("validee", "abandonnee", "experimentee") and len(motif) < MOTIF_MIN:
            raise ErreurValidation(f"Le statut « {statut} » exige un motif d'au moins {MOTIF_MIN} caractères "
                                   "(--motif) : sur quoi repose la décision ?")
        if statut == "validee" and not idee["references"] and not idee["retours"]:
            raise ErreurValidation("« validée » exige au moins une référence (`idee modifier`) ou un retour "
                                   "d'expérience (`idee retour`) : sur quelle source repose la validation ?")
        if statut == "experimentee" and not idee["retours"]:
            raise ErreurValidation("« expérimentée » exige au moins un retour d'expérience (`idee retour`).")
        avant = idee["statut"]
        cx.execute("UPDATE idees SET statut=?, maj_le=? WHERE id=?",
                   (statut, datetime.now().isoformat(timespec="seconds"), idee_id))
        _exporter(cx)
        journal.noter("statut_change", idee_id, {"avant": avant, "apres": statut}, motif)
        return {"etat": "modifie", "id": idee_id, "avant": avant, "apres": statut}
    finally:
        cx.close()


def ajouter_retour(idee_id: str, contexte: str, resultat: str, enseignement: str | None = None,
                   quand: str | None = None, forcer: bool = False, motif: str | None = None) -> dict:
    retour = {k: v for k, v in {"date": quand or date.today().isoformat(), "contexte": contexte,
                                "resultat": resultat, "enseignement": enseignement}.items() if v}
    _controler_confidentialite({"retours": [retour]}, forcer, motif)
    cx = ouvrir()
    try:
        idee = _charger(cx, idee_id)
        idee["retours"].append(retour)
        idee["maj_le"] = datetime.now().isoformat(timespec="seconds")
        _inserer(cx, idee)
        _exporter(cx)
        journal.noter("retour_ajoute", idee_id, idee["retours"][-1])
        return {"etat": "modifie", "id": idee_id, "retours": len(idee["retours"])}
    finally:
        cx.close()


def lier(source: str, cible: str, type_: str, note: str | None = None) -> dict:
    if type_ not in RELATIONS:
        raise ErreurValidation(f"Type de relation invalide : {type_} ({', '.join(RELATIONS)}).")
    if source == cible:
        raise ErreurValidation("Une idée ne peut pas être liée à elle-même.")
    cx = ouvrir()
    try:
        _charger(cx, source), _charger(cx, cible)
        cx.execute("INSERT OR REPLACE INTO relations VALUES (?,?,?,?,?)",
                   (source, cible, type_, note, date.today().isoformat()))
        cx.execute("UPDATE idees SET maj_le=? WHERE id=?", (datetime.now().isoformat(timespec="seconds"), source))
        _exporter(cx)
        journal.noter("relation_ajoutee", source, {"cible": cible, "type": type_, "note": note})
        return {"etat": "lie", "source": source, "cible": cible, "type": type_}
    finally:
        cx.close()


def retirer(idee_id: str, motif: str | None) -> dict:
    """Supprime proprement une idée (au lieu d'effacer sa ligne du JSONL) : relations
    sortantes et entrantes retirées, instantané complet conservé dans le journal (l'idée
    reste restaurable et son identifiant n'est jamais réattribué)."""
    motif = (motif or "").strip()
    if len(motif) < 10:
        raise ErreurValidation("Retirer une idée exige un motif d'au moins 10 caractères (--motif) : "
                               "pourquoi la supprimer plutôt que l'« abandonner » (`idee statut … abandonnee`) ?")
    cx = ouvrir()
    try:
        cx.execute("BEGIN IMMEDIATE")
        idee = _charger(cx, idee_id)
        entrantes = [dict(r) for r in cx.execute("SELECT source, type FROM relations WHERE cible=?", (idee_id,))]
        for t, col in (("idees", "id"), ("idee_themes", "idee_id"), ("refs", "idee_id"), ("retours", "idee_id"),
                       ("idees_fts", "id"), ("relations", "source"), ("relations", "cible")):
            cx.execute(f"DELETE FROM {t} WHERE {col}=?", (idee_id,))
        maintenant = datetime.now().isoformat(timespec="seconds")
        for r in entrantes:
            cx.execute("UPDATE idees SET maj_le=? WHERE id=?", (maintenant, r["source"]))
        _exporter(cx)
        journal.noter("idee_retiree", idee_id, {"idee": idee, "relations_entrantes_retirees": entrantes}, motif)
        for r in entrantes:
            journal.noter("relation_retiree", r["source"], {"cible": idee_id, "type": r["type"]}, motif)
        return {"etat": "retire", "id": idee_id, "relations_entrantes_retirees": entrantes}
    finally:
        cx.close()


# ---------------------------------------------------------------- lecture

def voir(idee_id: str) -> dict:
    cx = ouvrir()
    try:
        idee = _charger(cx, idee_id)
        idee["relations_entrantes"] = [dict(r) for r in cx.execute(
            "SELECT r.source, r.type, r.note, i.titre FROM relations r JOIN idees i ON i.id=r.source "
            "WHERE r.cible=?", (idee_id,))]
        titres = {r["id"]: r["titre"] for r in cx.execute("SELECT id, titre FROM idees")}
        for r in idee["relations"]:
            r["titre"] = titres.get(r["cible"], "?")
        idee["journal"] = journal.lire(idee_id, limite=10)
        return idee
    finally:
        cx.close()


def _descendants(code: str) -> set[str]:
    out = {code}
    change = True
    while change:
        change = False
        for t in taxonomie.themes():
            if t.get("parent") in out and t["code"] not in out:
                out.add(t["code"])
                change = True
    return out


def lister(theme: str | None = None, statut: str | None = None) -> list[dict]:
    cx = ouvrir()
    try:
        sql, params = "SELECT DISTINCT i.* FROM idees i JOIN idee_themes t ON t.idee_id=i.id WHERE 1=1", []
        if theme:
            codes = _descendants(taxonomie.resoudre(theme))
            sql += f" AND t.theme IN ({', '.join('?' * len(codes))})"
            params += sorted(codes)
        if statut:
            sql += " AND i.statut=?"
            params.append(statut)
        return [dict(r) for r in cx.execute(sql + " ORDER BY i.theme_principal, i.id", params)]
    finally:
        cx.close()


def chercher(requete: str, n: int = 10, theme: str | None = None) -> list[dict]:
    """Recherche plein texte dans les idées, avec l'expansion FR/EN du thésaurus."""
    from .recherche import groupes
    gs = groupes(requete)
    if not gs:
        return []
    expr = " OR ".join(g.fts() for g in gs)
    filtre, params = "", []
    if theme:
        codes = sorted(_descendants(taxonomie.resoudre(theme)))
        filtre = f" AND i.id IN (SELECT idee_id FROM idee_themes WHERE theme IN ({', '.join('?' * len(codes))}))"
        params = codes
    cx = ouvrir()
    try:
        return [dict(r) for r in cx.execute(
            "SELECT i.*, bm25(idees_fts, 0, 3.0, 1.0) AS score, "
            "snippet(idees_fts, 2, '«', '»', ' … ', 20) AS extrait FROM idees_fts "
            f"JOIN idees i ON i.id = idees_fts.id WHERE idees_fts MATCH ?{filtre} ORDER BY score LIMIT ?",
            (expr, *params, n))]
    finally:
        cx.close()


def couverture() -> list[dict]:
    """Par thème actif : idées capitalisées et matière disponible dans la bibliothèque.
    Un thème riche en passages mais pauvre en idées est une piste d'exploration."""
    cx = ouvrir()
    try:
        compte = {}
        for r in cx.execute("SELECT theme, COUNT(*) AS n, SUM(principal) AS p FROM idee_themes GROUP BY theme"):
            compte[r["theme"]] = (r["n"], r["p"])
    finally:
        cx.close()
    bib = bibliotheque.connecter() if chemins.index_db().exists() else None
    from .recherche import compter_theme
    out = []
    try:
        for niveau, t in taxonomie.arbre():
            if t["statut"] != "actif":
                continue
            n, p = compte.get(t["code"], (0, 0))
            passages = compter_theme(t["code"], bib) if bib else None
            etat = "vide" if n == 0 else "pauvre" if n < 3 else "correct"
            out.append({"code": t["code"], "libelle": t["libelle"], "niveau": niveau, "idees": n,
                        "principales": p or 0, "passages": passages, "etat": etat})
    finally:
        if bib:
            bib.close()
    return out


def verifier_references() -> list[dict]:
    """Recontrôle toutes les références ISTQB des idées (après une actualisation de la
    bibliothèque : version remplacée, document disparu, pagination changée)."""
    out = []
    cx = ouvrir()
    try:
        ids = [r["id"] for r in cx.execute("SELECT id FROM idees ORDER BY id")]
        idees = [_charger(cx, i) for i in ids]
    finally:
        cx.close()
    for idee in idees:
        for ref in idee["references"]:
            if ref.get("type") != "istqb":
                continue
            try:
                problemes = _verifier_reference_istqb(dict(ref))
            except ErreurValidation as exc:
                problemes = [str(exc)]
            out.append({"idee": idee["id"], "doc_id": ref.get("doc_id"), "pages": ref.get("pages"),
                        "problemes": problemes})
    return out
