import json

from qak import bibliotheque, chemins, recherche
from conftest import FIXTURES


def test_import_detecte_les_metadonnees_et_ecrit_le_manifeste(bibliotheque_test):
    assert bibliotheque_test == "CTFL-9.9-en"
    doc = bibliotheque.inventaire()[0]
    assert (doc["code"], doc["version"], doc["langue"], doc["date_publication"]) == ("CTFL", "9.9", "en", "2030-03-12")
    assert doc["statut_extraction"] == "ok" and doc["nb_passages"] > 0
    manif = json.loads(chemins.manifeste().read_text(encoding="utf-8"))
    entree = next(iter(manif["documents"].values()))
    assert entree["doc_id"] == "CTFL-9.9-en" and (chemins.sources() / entree["fichier"]).exists()


def test_doublon_exact_refuse_meme_sous_un_autre_nom(bibliotheque_test, copie_fixture):
    r = bibliotheque.importer(copie_fixture("syllabus_v9.pdf", "copie (1).pdf"))
    assert r["etat"] == "doublon" and r["doc_id"] == bibliotheque_test
    assert len(bibliotheque.inventaire()) == 1


def test_nouvelle_version_remplace_l_ancienne(bibliotheque_test):
    r = bibliotheque.importer(FIXTURES / "syllabus_v10.pdf")
    assert r["doc_id"] == "CTFL-10.0-en"
    assert any("CTFL-9.9-en" in n for n in r["versions"])
    etats = {d["doc_id"]: (d["statut_version"], d["remplace_par"]) for d in bibliotheque.inventaire()}
    assert etats == {"CTFL-10.0-en": ("courant", None), "CTFL-9.9-en": ("remplace", "CTFL-10.0-en")}


def test_actualisation_incrementale_puis_source_disparue(bibliotheque_test):
    assert bibliotheque.actualiser()["inchanges"] == 1
    (chemins.sources() / "syllabus_v9.pdf").unlink()
    r = bibliotheque.actualiser()
    assert r["absents"] and "CTFL-9.9-en" in r["absents"][0]
    doc = bibliotheque.inventaire()[0]
    assert doc["statut_extraction"] == "absent" and doc["nb_passages"] == 0


def test_nouveau_fichier_depose_dans_sources_importe_par_actualiser(racine_isolee):
    chemins.sources().mkdir(parents=True)
    (chemins.sources() / "fiche.md").write_text("# 1 Revue de code\nLa revue par les pairs détecte des défauts tôt.",
                                                encoding="utf-8")
    r = bibliotheque.actualiser()
    assert len(r["importes"]) == 1 and not r["echecs"]


def test_correction_manuelle_survit_a_la_reindexation(bibliotheque_test):
    bibliotheque.modifier_metadonnees(bibliotheque_test, langue="fr", niveau="avance")
    bibliotheque.actualiser(forcer=True)
    doc = bibliotheque.inventaire()[0]
    assert (doc["langue"], doc["niveau"]) == ("fr", "avance")


def test_index_reconstructible_depuis_le_manifeste(bibliotheque_test):
    chemins.index_db().unlink()
    r = bibliotheque.actualiser()
    assert r["reindexes"] == [bibliotheque_test]
    assert recherche.chercher("equivalence partitioning")["resultats"]


def test_versions_et_dates_formats_reels():
    # Formats relevés dans les vrais syllabus (en-têtes et historiques de révision).
    assert bibliotheque._version("x.pdf", "", ["Version 2014 Page 2 of 47", "Version 2014 Page 3 of 47",
                                              "Syllabus v0.9 30JAN2014 Beta version"]) == "2014"
    assert bibliotheque._version("ISTQB_CTAL-TM_Syllabus_v3.0a_FR.pdf", "", []) == "3.0a"
    assert bibliotheque._date(["v4.0 Page 3 of 77 2025/05/02", "v4.0 Page 4 of 77 2025/05/02",
                               "v3.0 (2019) 2019/10/19 Major update"]) == "2025-05-02"
    assert bibliotheque._date(["Version 2011 Page 3 of 75 1st November 2011"]) == "2011-11-01"
    assert bibliotheque._date(["Page 2 de 63 3 mai 2019"]) == "2019-05-03"
    assert bibliotheque._cle_version("3.0a") > bibliotheque._cle_version("3.0") > bibliotheque._cle_version("2.10") \
        > bibliotheque._cle_version("2.9")


def test_codes_reconnus_sur_les_titres_reels_francais():
    titres = {
        "Testeur Certifié Extension du Niveau Fondation Testeur Agile": "CTFL-AT",
        "Syllabus 2021 Analyste Technique de Test": "CTAL-TTA",
        "Syllabus 2019 Analyste de Test": "CTAL-TA",
        "Syllabus ISTQB Expert Amélioration du Processus de Test": "CTEL-ITP",
        "Syllabus 2019 Testeur Technique Agile": "CTAL-ATT",
        "Spécialiste de Niveau Fondation Test de l'utilisabilité 2018": "CT-UT",
        "Extension du Niveau Fondation Test d'application mobile": "CT-MAT",
        "ISTQB_CTAL-ATLaS_Body-of-Knowledge_v2.0-FR": "CT-ATLaS",
        "ISTQB_CTAL-TM_Syllabus_v3.0a_FR_FINAL": "CTAL-TM",
        "ISTQB_CT-TAS_Syllabus_v1.0-FINAL": "CT-TAS",
    }
    for titre, code in titres.items():
        assert bibliotheque.entree_catalogue([titre])["code"] == code, titre
    assert bibliotheque.entree_catalogue(["Mon document interne"]) is None


def test_format_non_pris_en_charge(racine_isolee, tmp_path):
    f = tmp_path / "x.docx"
    f.write_bytes(b"PK")
    assert bibliotheque.importer(f)["etat"] == "echec"


def test_renommage_conserve_meme_si_un_nouveau_fichier_arrive(bibliotheque_test):
    # Régression : l'import d'un nouveau fichier relisait le manifeste et perdait le renommage.
    (chemins.sources() / "syllabus_v9.pdf").rename(chemins.sources() / "a_renomme.pdf")
    (chemins.sources() / "z_nouveau.md").write_text("# 1 Note\nUne note de test suffisamment longue.", encoding="utf-8")
    (chemins.sources() / "LISEZMOI.md").write_text("Notes du dossier, pas un document.", encoding="utf-8")
    r = bibliotheque.actualiser()
    assert len(r["importes"]) == 1 and not r["absents"]
    fichiers = {e["fichier"] for e in bibliotheque.lire_manifeste()["documents"].values()}
    assert fichiers == {"a_renomme.pdf", "z_nouveau.md"}
    assert {d["fichier"] for d in bibliotheque.inventaire()} == fichiers


def test_retirer_un_document(bibliotheque_test):
    bibliotheque.retirer(bibliotheque_test)
    assert bibliotheque.inventaire() == [] and not bibliotheque.lire_manifeste()["documents"]
    assert (chemins.sources() / "syllabus_v9.pdf").exists()


def test_manquants_par_langue(bibliotheque_test):
    r = bibliotheque.manquants()
    ctfl = next(l for l in r["catalogue"] if l["code"] == "CTFL")
    assert (ctfl["en"], ctfl["fr"]) == ("CTFL-9.9-en", None)
    assert "CTFL" not in r["absents_en"] and "CTFL" in r["absents_fr"]
    assert "CTAL-TM" in r["absents_en"] and len(r["absents_en"]) == len(r["catalogue"]) - 1


def test_index_perime_detecte_avant_actualiser(capsys, monkeypatch, bibliotheque_test):
    """#36 : après suppression d'un PDF (git pull), `chercher` avertit, `verifier-refs` et
    `idee ajouter` refusent la référence, sans attendre `actualiser`."""
    import io
    from qak import connaissances
    from qak.cli import main
    assert bibliotheque.controle_index()["messages"] == []
    idee = {"titre": "Matrice des risques produit", "resume": "Probabilité × impact.",
            "probleme": "Effort uniforme.", "principe": "Calculer le niveau de risque.", "theme_principal": "rbt",
            "references": [{"type": "istqb", "doc_id": bibliotheque_test, "pages": "6"}]}
    assert connaissances.ajouter(dict(idee), forcer=True, motif="t")["etat"] != "refuse"
    entree = next(iter(bibliotheque.lire_manifeste()["documents"].values()))
    (chemins.sources() / entree["fichier"]).unlink()
    assert main(["chercher", "valeurs", "limites"]) == 0
    assert "Index périmé" in capsys.readouterr().out
    assert any(r["problemes"] for r in connaissances.verifier_references())
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps({**idee, "titre": "Autre matrice des risques"})))
    assert main(["idee", "ajouter"]) == 2
    assert "index périmé" in capsys.readouterr().err
    bibliotheque.actualiser()
    assert bibliotheque.controle_index()["messages"] == []


def test_contenu_modifie_ou_nouveau_fichier_signales(bibliotheque_test, tmp_path):
    import os
    import time
    entree = next(iter(bibliotheque.lire_manifeste()["documents"].values()))
    f = chemins.sources() / entree["fichier"]
    with open(f, "ab") as fh:
        fh.write(b"\n% altere\n")
    futur = time.time() + 5
    os.utime(f, (futur, futur))
    (chemins.sources() / "nouveau.md").write_text("# 1 Note\nTexte.", encoding="utf-8")
    c = bibliotheque.controle_index()
    assert c["perimes"] == {bibliotheque_test}
    assert any("modifié" in m for m in c["messages"]) and any("nouveau.md" in m for m in c["messages"])


def test_copie_d_un_source_nommee_sans_masquer_l_original(bibliotheque_test):
    entree = next(iter(bibliotheque.lire_manifeste()["documents"].values()))
    shutil = __import__("shutil")
    shutil.copy2(chemins.sources() / entree["fichier"], chemins.sources() / "a_copie.pdf")
    r = bibliotheque.actualiser()
    assert r["doublons"] == [f"a_copie.pdf : contenu identique à {entree['fichier']}"]
    assert r["inchanges"] == 1 and not r["absents"]
