from qak import bibliotheque, recherche
from conftest import FIXTURES


def test_question_francaise_trouve_le_passage_anglais(bibliotheque_test):
    r = recherche.chercher("partitions d'équivalence")
    premier = r["resultats"][0]
    assert premier["section_num"] == "1.2" and premier["page"] == 5
    assert r["groupes"] == ["partition-equivalence"]


def test_couverture_des_notions_prime_sur_un_mot_isole(bibliotheque_test):
    r = recherche.chercher("priorisation des tests selon le niveau de risque")
    premier = r["resultats"][0]
    assert premier["section_num"] == "2.1" and not premier["partiel"]


def test_sommaires_et_index_exclus_par_defaut(bibliotheque_test):
    pages = {x["page"] for x in recherche.chercher("equivalence partitioning", n=20, par_doc=20)["resultats"]}
    assert 2 not in pages and 7 not in pages
    avec = {x["page"] for x in recherche.chercher("equivalence partitioning", n=20, par_doc=20, inclure_sommaires=True)["resultats"]}
    assert 7 in avec


def test_filtre_section_inclut_les_sous_sections(bibliotheque_test):
    r = recherche.chercher("partition", section="1.2")
    assert {x["section_num"] for x in r["resultats"]} <= {"1.2", "1.2.1"} and r["resultats"]
    assert not recherche.chercher("partition", section="2")["resultats"]


def test_version_remplacee_exclue_sauf_demande(bibliotheque_test):
    bibliotheque.importer(FIXTURES / "syllabus_v10.pdf")
    docs = {x["doc_id"] for x in recherche.chercher("test objectives", n=10)["resultats"]}
    assert docs == {"CTFL-10.0-en"}
    docs = {x["doc_id"] for x in recherche.chercher("test objectives", n=10, toutes_versions=True)["resultats"]}
    assert docs == {"CTFL-10.0-en", "CTFL-9.9-en"}


def test_lire_passage_avec_contexte_et_section(bibliotheque_test):
    pid = recherche.chercher("equivalence partitioning")["resultats"][0]["id"]
    autour = recherche.lire_passage(pid, contexte=1)
    assert len(autour) == 3 and any(p["id"] == pid for p in autour)
    section = recherche.lire_section(bibliotheque_test, "1.2")
    assert {p["section_num"] for p in section["passages"]} == {"1.2", "1.2.1"}
    assert recherche.lire_pages("CTFL", 5)["passages"]


def test_bibliotheque_vide_et_requete_vide(racine_isolee):
    assert "Bibliothèque vide" in recherche.chercher("risque")["avertissements"][0]
    assert recherche.chercher("le la les de")["resultats"] == []


def test_aucun_resultat_suggere_reformulation_ou_web(bibliotheque_test):
    r = recherche.chercher("blockchain quantique")
    assert not r["resultats"] and "Web" in r["avertissements"][0]


def test_filtre_par_theme(bibliotheque_test):
    r = recherche.chercher("tests", theme="rbt")
    assert r["resultats"] and all(x["section_num"] in ("2.1", "1.1") for x in r["resultats"])


def test_filtre_qui_exclut_un_document_le_dit(bibliotheque_test):
    # Issue #2 : « CTFL en français » n'existe pas, mais le CTFL est bien là (en anglais).
    r = recherche.chercher("equivalence partitioning", docs=["CTFL"], langue="fr")
    assert not r["resultats"]
    assert any("seulement en : en" in w for w in r["avertissements"])
    assert not any("absent de la bibliothèque" in w for w in r["avertissements"])
    r = recherche.chercher("equivalence partitioning", docs=["CTFL"], niveau="expert")
    assert any("exclu par `--niveau expert`" in w for w in r["avertissements"])
    r = recherche.chercher("equivalence partitioning", docs=["CTAL-TM"])
    assert any("CTAL-TM : absent" in w for w in r["avertissements"])


def test_couverture_lexicale(bibliotheque_test):
    bonne = recherche.chercher("equivalence partitioning")["couverture_lexicale"]
    assert bonne["libelle"] in ("élevée", "moyenne")
    assert any("nomment une notion dans leur titre" in r for r in bonne["raisons"])
    partielle = recherche.chercher("equivalence partitioning blockchain")["couverture_lexicale"]
    assert partielle["score"] < bonne["score"]
    assert recherche.chercher("blockchain quantique")["couverture_lexicale"] == {
        "score": 0, "libelle": "nulle", "raisons": ["aucun passage trouvé"]}


def test_couverture_lexicale_ne_sature_pas_sur_des_sujets_disperses():
    # Issue #18 (Claire) : notions toutes présentes, mais dans des sections qui ne les traitent
    # pas (titres sans la notion) et d'un syllabus ancien → bien en dessous d'un socle pertinent.
    def res(titre, date):
        return {"doc_id": "CTFL-4.0-en", "couverture": 1.0, "partiel": False, "notion_en_titre": titre > 0,
                "couverture_titre": titre, "date_publication": date}
    pertinent = recherche.couverture_lexicale([res(1.0, "2023-05-01")] * 5)
    disperse = recherche.couverture_lexicale([res(0.0, "2012-10-19")] * 5)
    assert pertinent["score"] == 100 - 10  # un seul syllabus complet : 5/15
    assert disperse["score"] == pertinent["score"] - 30 - 15
    assert any("sujets dispersés" in r for r in disperse["raisons"])


def test_notions_des_candidats_identiques_au_match_sur_l_index(bibliotheque_test):
    # Issue #59 : le calcul restreint aux candidats (index FTS5 en mémoire, même tokeniseur)
    # doit donner exactement ce que donnait un MATCH sur tout l'index (porter compris).
    from qak import bibliotheque
    cx = bibliotheque.connecter()
    try:
        for q in ("equivalence partitioning risques", "valeurs limites tests", "risk level determined"):
            gs = recherche.groupes(q)
            cand = cx.execute("SELECT id, texte, section_titre FROM passages").fetchall()
            trouves, en_titre = recherche._notions_des_candidats(cand, gs)
            for k, g in enumerate(gs):
                attendu = {r for (r,) in cx.execute("SELECT rowid FROM passages_fts WHERE passages_fts MATCH ?",
                                                    (g.fts(),))}
                assert {i for i, ks in trouves.items() if k in ks} == attendu, (q, g.libelle)
                attendu = {r for (r,) in cx.execute("SELECT rowid FROM passages_fts WHERE passages_fts MATCH ?",
                                                    (f"section_titre : {g.fts()}",))}
                assert {i for i, ks in en_titre.items() if k in ks} == attendu, (q, g.libelle)
            assert any(trouves.values())
    finally:
        cx.close()


def test_faute_de_frappe_corrigee_et_signalee(bibliotheque_test):
    # Issue #106 : un mot inconnu de l'index et du thésaurus, proche d'un mot connu, est corrigé.
    r = recherche.chercher("equivalnce partitioning")
    assert r["resultats"] and r["resultats"][0]["section_num"].startswith("1.2")
    assert any("« equivalnce » compris comme « equivalence »" in a for a in r["avertissements"])
    # Un mot connu n'est jamais « corrigé » ; un mot sans voisin proche reste tel quel.
    assert not recherche.chercher("equivalence partitioning")["avertissements"]
    assert not any("Faute" in a for a in recherche.chercher("blockchain quantique")["avertissements"])


def test_chapitre_0_d_introduction_retrograde(bibliotheque_test):
    # Issue #25 : les §0.x (objet du syllabus, examen, parcours de carrière) citent les notions
    # sans les traiter ; à couverture égale ils passent après les sections de fond.
    from qak import bibliotheque
    cx = bibliotheque.connecter()
    try:
        doc = cx.execute("SELECT doc_id FROM passages LIMIT 1").fetchone()[0]
        cx.execute("INSERT INTO passages(doc_id, ordre, page, section_num, section_titre, texte, sommaire) "
                   "VALUES (?, 999, 1, '0.2', 'About this syllabus', 'equivalence partitioning equivalence "
                   "partitioning equivalence partitioning', 0)", (doc,))
        rid = cx.execute("SELECT max(id) FROM passages").fetchone()[0]
        cx.execute("INSERT INTO passages_fts(rowid, texte, section_titre) SELECT id, texte, section_titre "
                   "FROM passages WHERE id=?", (rid,))
        cx.commit()
        res = recherche.chercher("equivalence partitioning", cx=cx)["resultats"]
        assert res[-1]["section_num"] == "0.2" and res[0]["section_num"] != "0.2"
    finally:
        cx.close()


def test_section_au_titre_identique_a_la_requete_d_abord(bibliotheque_test):
    # Issue #165 : « Exploratory Testing » (CTFL §4.4.2) arrivait au rang 11, derrière des
    # sections dont le titre nomme le même concept du thésaurus (« Session-Based Test
    # Management ») et que BM25 classait plus haut. À couverture et titre égaux, le titre qui
    # EST la question passe devant ; une question en français vise la même section anglaise.
    from qak import bibliotheque
    cx = bibliotheque.connecter()
    try:
        doc = cx.execute("SELECT doc_id FROM passages LIMIT 1").fetchone()[0]
        for ordre, num, titre, texte in (
                (997, "7.1", "Session-Based Test Management (SBTM)", "exploratory testing sessions " * 6),
                (998, "7.2", "Exploratory Testing", "exploratory testing is an approach where tests are "
                                                    "designed and executed while learning about the object")):
            cx.execute("INSERT INTO passages(doc_id, ordre, page, section_num, section_titre, texte, sommaire) "
                       "VALUES (?, ?, ?, ?, ?, ?, 0)", (doc, ordre, ordre, num, titre, texte))
        cx.execute("INSERT INTO passages_fts(rowid, texte, section_titre) SELECT id, texte, section_titre "
                   "FROM passages WHERE ordre IN (997, 998)")
        cx.commit()
        for q in ("exploratory testing", "tests exploratoires"):
            res = recherche.chercher(q, cx=cx)["resultats"]
            assert [r["section_num"] for r in res[:2]] == ["7.2", "7.1"], q
    finally:
        cx.close()


def test_faute_de_frappe_sur_un_mot_de_quatre_lettres(bibliotheque_test):
    # Issue #166 : « tets » n'était pas corrigé (mots de moins de 5 lettres exclus). Une seule
    # édition vers un mot du thésaurus suffit, la plus proche l'emporte (« tests », pas « test »).
    r = recherche.chercher("tets equivalence partitioning")
    assert any("« tets » compris comme « tests »" in a for a in r["avertissements"])
    assert recherche._une_edition("tets", "test") and recherche._une_edition("tets", "tests")
    assert recherche._une_edition("tset", "test") and not recherche._une_edition("tset", "tests")
    assert recherche._a_une_edition("tets", {"test", "tests"}) == ["tests"]
    assert recherche._a_une_edition("abcd", {"abce", "abcf"}) == []  # ex æquo : pas de choix arbitraire
    assert not any("Faute" in a for a in recherche.chercher("zzqx equivalence")["avertissements"])


def test_passage_introuvable_message_actionnable(bibliotheque_test):
    """#211 : le message dit pourquoi (numéro périmé) et quoi faire (relancer `chercher`)."""
    import pytest
    with pytest.raises(KeyError) as exc:
        recherche.lire_passage(999999)
    assert exc.value.args[0] == ("Passage 999999 introuvable : numéro périmé si l'index a été reconstruit "
                                 "depuis la recherche ; relancer `chercher` pour obtenir des numéros à jour.")
