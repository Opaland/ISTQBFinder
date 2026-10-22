"""Recherche plein texte dans la bibliothèque (SQLite FTS5, classement BM25).

Une question en langage naturel devient une liste de « groupes » :
- chaque concept du thésaurus repéré donne un groupe OU de tous ses termes FR/EN
  (« partitions d'équivalence » cherche aussi « equivalence partitioning ») ;
- chaque mot restant (hors mots vides et mots génériques) forme son propre groupe.
Les candidats (OU de tous les groupes, classés BM25) sont reclassés par COUVERTURE :
part pondérée des notions de la question présentes dans le passage (un concept du
thésaurus pèse 2, un mot isolé 1), BM25 départageant les ex æquo. Un passage qui ne
couvre pas toutes les notions est marqué « partiel ».
Ce choix a été mesuré sur eval/requetes.json (voir docs/architecture.md) : le mode
« ET strict puis OU » échouait dès qu'un mot secondaire de la question manquait.
"""
import json
import re
import sqlite3
from dataclasses import dataclass

from . import bibliotheque, taxonomie
from .textes import MOTS_GENERIQUES, normaliser, reperer_concepts

CANDIDATS = 300  # passages BM25 reclassés par couverture
# Sections périphériques (annexes, notes de version, bibliographie, matrices de traçabilité) :
# elles citent beaucoup de notions sans les traiter. Rétrogradées à couverture égale.
RE_PERIPHERIQUE = re.compile(r"\b(appendi|annexe|release notes|notes de (version|release)|references|bibliograph|"
                             r"business outcomes|objectifs metier|tracabilite|traceability matrix|index)", re.I)


@dataclass
class Groupe:
    libelle: str
    termes: list[str]
    poids: int = 1

    def fts(self) -> str:
        phrases = sorted({normaliser(t) for t in self.termes if normaliser(t)})
        return "(" + " OR ".join(f'"{p}"' for p in phrases) + ")"


def sigles(requete: str) -> set[str]:
    """Sigles écrits en majuscules (SQL, GUI, ISO, API) : courts mais porteurs de sens."""
    return {normaliser(m) for m in re.findall(r"\b[A-Z][A-Z0-9]{1,5}\b", requete)}


def groupes(requete: str) -> list[Groupe]:
    concepts, reste = reperer_concepts(requete)
    garder = sigles(requete)
    out = [Groupe(cid, list(termes), 1 if cid.startswith("lex-") else 2) for cid, termes in concepts]
    out += [Groupe(m, [m]) for m in reste if m not in MOTS_GENERIQUES and (len(m) > 3 or m in garder)]
    return out


def mots_ignores(requete: str) -> list[str]:
    _, reste = reperer_concepts(requete)
    garder = sigles(requete)
    return [m for m in reste if m not in MOTS_GENERIQUES and len(m) <= 3 and m not in garder and not m.isdigit()]


def chercher(requete: str, n: int = 8, docs: list[str] | None = None, niveau: str | None = None,
             langue: str | None = None, section: str | None = None, theme: str | None = None,
             toutes_versions: bool = False, inclure_sommaires: bool = False, par_doc: int = 3,
             cx: sqlite3.Connection | None = None) -> dict:
    """Renvoie {requete_fts, groupes, resultats:[...], avertissements:[...]}."""
    gs = groupes(requete)
    avert = []
    obligatoire = None
    if theme:
        th = taxonomie.theme(theme)
        obligatoire = Groupe(f"thème {th['code']}", th["mots_cles"])
    if not gs and not obligatoire:
        return _sans_resultat([], "Requête vide après retrait des mots vides : préciser les notions cherchées.")
    filtres, params = [], []
    if not toutes_versions:
        # Un doc_id précis demandé explicitement (même remplacé) reste cherchable.
        exacts = [d for d in (docs or []) if "-" in d and any(c.isdigit() for c in d)]
        filtres.append("(d.statut_version = 'courant'"
                       + (f" OR d.doc_id COLLATE NOCASE IN ({', '.join('?' * len(exacts))})" if exacts else "") + ")")
        params += exacts
    if not inclure_sommaires:
        filtres.append("p.sommaire = 0")
    if docs:
        conds = []
        for d in docs:
            conds.append("(d.doc_id = ? COLLATE NOCASE OR d.code = ? COLLATE NOCASE)")
            params += [d, d]
        filtres.append("(" + " OR ".join(conds) + ")")
    if niveau:
        filtres.append("d.niveau = ?")
        params.append(niveau)
    if langue:
        filtres.append("d.langue = ?")
        params.append(langue)
    if section:
        filtres.append("(p.section_num = ? OR p.section_num LIKE ?)")
        params += [section, section.rstrip(".") + ".%"]
    where = (" AND " + " AND ".join(filtres)) if filtres else ""

    def executer(expr: str, limite: int) -> list[sqlite3.Row]:
        sql = ("SELECT p.id, p.doc_id, p.page, p.page_imprimee, p.section_num, p.section_titre, p.texte, "
               "d.titre, d.code, d.version, d.langue, d.date_publication, d.statut_version, d.type, "
               "snippet(passages_fts, 0, '«', '»', ' … ', 32) AS extrait, "
               "bm25(passages_fts, 1.0, 4.0) AS score "
               "FROM passages_fts JOIN passages p ON p.id = passages_fts.rowid "
               "JOIN documents d ON d.doc_id = p.doc_id "
               f"WHERE passages_fts MATCH ?{where} ORDER BY score LIMIT ?")
        return cx.execute(sql, [expr, *params, limite]).fetchall()

    propre = cx is None
    cx = cx or bibliotheque.connecter()
    try:
        if not cx.execute("SELECT 1 FROM passages LIMIT 1").fetchone():
            return _sans_resultat([g.libelle for g in gs],
                                  "Bibliothèque vide : lancer `actualiser` ou `telecharger` d'abord.")
        prefixe = f"{obligatoire.fts()} AND " if obligatoire else ""
        ou = prefixe + "(" + " OR ".join(g.fts() for g in gs) + ")" if gs else obligatoire.fts()
        candidats = executer(ou, CANDIDATS)
        ids = [r["id"] for r in candidats]
        trouves: dict[int, set[int]] = {i: set() for i in ids}
        marque = ",".join("?" * len(ids))
        for k, g in enumerate(gs):
            for (rid,) in cx.execute(f"SELECT rowid FROM passages_fts WHERE passages_fts MATCH ? "
                                     f"AND rowid IN ({marque})", [g.fts(), *ids]) if ids else []:
                trouves[rid].add(k)
        # Notions nommées dans le TITRE de la section : une section dédiée à la notion passe
        # devant une section qui ne fait que l'évoquer (issue #4 : « Shift Left » §2.1.5).
        en_titre: dict[int, set[int]] = {i: set() for i in ids}
        for k, g in enumerate(gs):
            for (rid,) in cx.execute(f"SELECT rowid FROM passages_fts WHERE passages_fts MATCH ? "
                                     f"AND rowid IN ({marque})", [f"section_titre : {g.fts()}", *ids]) if ids else []:
                en_titre[rid].add(k)
        total = sum(g.poids for g in gs) or 1

        def couverture(r) -> float:
            return sum(gs[k].poids for k in trouves[r["id"]]) / total

        def peripherique(r) -> bool:
            return bool(RE_PERIPHERIQUE.search(normaliser(r["section_titre"] or "")))

        def titre(r) -> float:
            return sum(gs[k].poids for k in en_titre[r["id"]]) / total

        # tri stable : couverture décroissante, sections de fond d'abord, puis sections dont le
        # titre nomme les notions, puis l'ordre BM25
        classes = sorted(candidats, key=lambda r: (-couverture(r), peripherique(r), -titre(r)))
        vus, resultats, par = set(), [], {}
        for r in classes:
            cle = (r["doc_id"], r["page"])
            if cle in vus or par.get(r["doc_id"], 0) >= par_doc:
                continue
            vus.add(cle)
            par[r["doc_id"]] = par.get(r["doc_id"], 0) + 1
            c = couverture(r)
            resultats.append({**{k: r[k] for k in r.keys() if k not in ("texte", "score")},
                              "score": round(-r["score"], 2), "couverture": round(c, 2),
                              "partiel": c < 1 and bool(gs),
                              "groupes_trouves": [gs[k].libelle for k in sorted(trouves[r["id"]])],
                              "notion_en_titre": bool(en_titre[r["id"]]),
                              "couverture_titre": round(titre(r), 2)})
            if len(resultats) >= n:
                break
        ignores = mots_ignores(requete)
        if ignores:
            avert.append(f"Mots trop courts ignorés : {', '.join(ignores)} (écrire un sigle en MAJUSCULES pour le garder).")
        if not resultats:
            avert.append("Aucun passage trouvé dans la bibliothèque locale : reformuler (termes anglais des "
                         "syllabus), élargir les filtres, ou justifier une recherche Web.")
        elif all(r["partiel"] for r in resultats) and len(gs) > 1:
            avert.append("Aucun passage ne couvre toutes les notions : résultats partiels.")
        avert += _diagnostic_filtres(cx, docs, langue, niveau, toutes_versions)
        return {"requete_fts": ou, "groupes": [g.libelle for g in gs], "resultats": resultats,
                "couverture_lexicale": couverture_lexicale(resultats),
                "avertissements": avert}
    finally:
        if propre:
            cx.close()


def _sans_resultat(libelles: list[str], avertissement: str) -> dict:
    """Retour anticipé (requête vide, bibliothèque vide) : même forme qu'un résultat normal,
    clé « couverture_lexicale » comprise (issue #53 : la CLI la lit toujours)."""
    return {"requete_fts": "", "groupes": libelles, "resultats": [], "couverture_lexicale": couverture_lexicale([]),
            "avertissements": [avertissement]}


ANNEE_RECENTE = 2017  # syllabus publiés avant : « anciens » (cohérent avec la grille du skill)


def libelle(score: int) -> str:
    return "élevée" if score >= 75 else "moyenne" if score >= 50 else "faible" if score >= 25 else "très faible"


def couverture_lexicale(resultats: list[dict]) -> dict:
    """Indice 0-100 du socle documentaire trouvé par la recherche. Ce n'est PAS une confiance
    (issue #18) : il dit si les notions de la question figurent dans des passages pertinents,
    pas si la réponse est juste — `qa.py confiance` en part, avec ce qui a été réellement lu.
    Présence lexicale (55) : couverture du meilleur passage (25), syllabus couvrant TOUTES
    les notions (15), part de résultats complets dans les 5 premiers (15).
    Pertinence (45) : part des notions nommées par le TITRE de section des 5 premiers (30 ;
    des sujets dispersés — sections qui ne font qu'évoquer la notion — la font chuter),
    part des 5 premiers issus d'un syllabus publié depuis ANNEE_RECENTE (15)."""
    if not resultats:
        return {"score": 0, "libelle": "nulle", "raisons": ["aucun passage trouvé"]}
    top = resultats[:5]
    complets = {r["doc_id"].rsplit("-", 2)[0] for r in resultats if not r["partiel"]}  # par code
    nb_complets = sum(not r["partiel"] for r in top)
    titres = sum(r.get("couverture_titre", 0) for r in top) / len(top)
    recents = sum(int((r.get("date_publication") or "0")[:4] or 0) >= ANNEE_RECENTE for r in top)
    a = 25 * top[0]["couverture"]
    b = {0: 0, 1: 5, 2: 10}.get(len(complets), 15)
    c = 15 * nb_complets / len(top)
    d = 30 * titres
    e = 15 * recents / len(top)
    score = round(a + b + c + d + e)
    en_titre = sum(bool(r.get("notion_en_titre")) for r in top)
    raisons = [f"meilleur passage : {round(100 * top[0]['couverture'])} % des notions",
               f"{len(complets)} syllabus couvrent toutes les notions",
               f"{nb_complets}/{len(top)} premiers résultats complets",
               f"{en_titre}/{len(top)} premières sections nomment une notion dans leur titre"
               + (" (sujets dispersés)" if en_titre * 5 < 2 * len(top) else ""),
               f"{recents}/{len(top)} premiers résultats issus d'un syllabus publié depuis {ANNEE_RECENTE}"]
    return {"score": score, "libelle": libelle(score), "raisons": raisons}


def _diagnostic_filtres(cx, docs, langue, niveau, toutes_versions) -> list[str]:
    """Explique quand un filtre écarte un document demandé : « absent » et « exclu par
    --langue » ne doivent jamais se confondre (sinon on affirme à tort qu'un syllabus
    manque à la bibliothèque)."""
    out = []
    for d in docs or []:
        lignes = cx.execute("SELECT doc_id, langue, niveau, statut_version FROM documents "
                            "WHERE (doc_id=? COLLATE NOCASE OR code=? COLLATE NOCASE) AND statut_version!='absent'",
                            (d, d)).fetchall()
        if not lignes:
            out.append(f"{d} : absent de la bibliothèque (voir `inventaire` et `catalogue`).")
            continue
        langues = sorted({r["langue"] for r in lignes})
        if langue and langue not in langues:
            out.append(f"{d} existe, mais seulement en : {', '.join(langues)} — retirer `--langue {langue}` "
                       "pour le chercher.")
        if niveau and all(r["niveau"] != niveau for r in lignes):
            out.append(f"{d} est de niveau « {lignes[0]['niveau']} » : exclu par `--niveau {niveau}`.")
        if not toutes_versions and all(r["statut_version"] == "remplace" for r in lignes):
            out.append(f"{d} : seules des versions remplacées sont présentes — ajouter `--toutes-versions`.")
    return out


def lire_passage(pid: int, contexte: int = 0, cx: sqlite3.Connection | None = None) -> list[dict]:
    """Le passage `pid` et ses `contexte` voisins de part et d'autre (même document)."""
    propre = cx is None
    cx = cx or bibliotheque.connecter()
    try:
        r = cx.execute("SELECT doc_id, ordre FROM passages WHERE id=?", (pid,)).fetchone()
        if not r:
            raise KeyError(f"Passage {pid} introuvable (index reconstruit depuis ? relancer la recherche).")
        return [dict(x) for x in cx.execute(
            "SELECT p.*, d.titre, d.code, d.version, d.langue, d.statut_version, d.date_publication "
            "FROM passages p JOIN documents d ON d.doc_id=p.doc_id "
            "WHERE p.doc_id=? AND p.ordre BETWEEN ? AND ? ORDER BY p.ordre",
            (r["doc_id"], r["ordre"] - contexte, r["ordre"] + contexte))]
    finally:
        if propre:
            cx.close()


def _doc(cx, doc: str) -> sqlite3.Row:
    r = cx.execute("SELECT * FROM documents WHERE doc_id=? COLLATE NOCASE", (doc,)).fetchone() or \
        cx.execute("SELECT * FROM documents WHERE code=? COLLATE NOCASE ORDER BY statut_version='courant' DESC, "
                   "date_publication DESC", (doc,)).fetchone()
    if not r:
        raise KeyError(f"Document inconnu : {doc}. Voir `inventaire`.")
    return r


def lire_pages(doc: str, debut: int, fin: int | None = None, cx: sqlite3.Connection | None = None) -> dict:
    propre = cx is None
    cx = cx or bibliotheque.connecter()
    try:
        d = _doc(cx, doc)
        rows = [dict(x) for x in cx.execute(
            "SELECT * FROM passages WHERE doc_id=? AND page BETWEEN ? AND ? ORDER BY ordre",
            (d["doc_id"], debut, fin or debut))]
        return {"document": dict(d), "passages": rows}
    finally:
        if propre:
            cx.close()


def lire_section(doc: str, numero: str, cx: sqlite3.Connection | None = None) -> dict:
    """Tous les passages d'une section et de ses sous-sections (« 4.2 » inclut « 4.2.1 »)."""
    propre = cx is None
    cx = cx or bibliotheque.connecter()
    try:
        d = _doc(cx, doc)
        rows = [dict(x) for x in cx.execute(
            "SELECT * FROM passages WHERE doc_id=? AND sommaire=0 AND (section_num=? OR section_num LIKE ?) "
            "ORDER BY ordre", (d["doc_id"], numero, numero.rstrip(".") + ".%"))]
        return {"document": dict(d), "passages": rows}
    finally:
        if propre:
            cx.close()


def plan(doc: str, cx: sqlite3.Connection | None = None) -> dict:
    propre = cx is None
    cx = cx or bibliotheque.connecter()
    try:
        d = _doc(cx, doc)
        return {"document": dict(d), "sections": [dict(x) for x in cx.execute(
            "SELECT numero, titre, page FROM sections WHERE doc_id=? ORDER BY ordre", (d["doc_id"],))]}
    finally:
        if propre:
            cx.close()


def compter_theme(code: str, cx: sqlite3.Connection) -> int:
    """Nombre de passages (versions courantes, hors sommaires) qui évoquent le thème."""
    th = taxonomie.theme(code)
    expr = Groupe(code, th["mots_cles"]).fts()
    return cx.execute("SELECT COUNT(*) FROM passages_fts JOIN passages p ON p.id=passages_fts.rowid "
                      "JOIN documents d ON d.doc_id=p.doc_id WHERE passages_fts MATCH ? "
                      "AND d.statut_version='courant' AND p.sommaire=0", (expr,)).fetchone()[0]


def en_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, default=str)
