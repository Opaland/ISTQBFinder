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


def test_confiance_documentaire(bibliotheque_test):
    bonne = recherche.chercher("equivalence partitioning")["confiance"]
    assert bonne["score"] >= 75 and bonne["libelle"] == "élevée"
    assert "une section est consacrée à la notion" in bonne["raisons"]
    partielle = recherche.chercher("equivalence partitioning blockchain")["confiance"]
    assert partielle["score"] < bonne["score"]
    assert recherche.chercher("blockchain quantique")["confiance"] == {
        "score": 0, "libelle": "nulle", "raisons": ["aucun passage trouvé"]}


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
