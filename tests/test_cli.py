import json

from qak.cli import main
from conftest import FIXTURES


def test_parcours_complet_en_ligne_de_commande(capsys, monkeypatch, racine_isolee):
    assert main(["importer", str(FIXTURES / "syllabus_v9.pdf")]) == 0
    assert "CTFL-9.9-en" in capsys.readouterr().out
    assert main(["chercher", "valeurs", "limites"]) == 0
    sortie = capsys.readouterr().out
    assert "CTFL-9.9-en" in sortie and "passage #" in sortie
    assert main(["section", "CTFL", "2.1"]) == 0
    assert "Risk level is determined" in capsys.readouterr().out
    assert main(["inventaire"]) == 0 and "CTFL-9.9-en" in capsys.readouterr().out

    idee = {"titre": "Matrice des risques", "resume": "Probabilité × impact.", "probleme": "Effort uniforme.",
            "principe": "Calculer le niveau de risque.", "theme_principal": "rbt",
            "references": [{"type": "istqb", "doc_id": "CTFL", "pages": "6"}]}
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps(idee)))
    assert main(["idee", "ajouter"]) == 0
    q1 = capsys.readouterr().out.split("Idée créée : ")[1].split()[0]
    assert main(["idee", "chercher", "matrice", "risques"]) == 0
    assert q1 in capsys.readouterr().out
    assert main(["idee", "statut", q1, "validee"]) == 2  # motif obligatoire
    assert "motif" in capsys.readouterr().err
    assert main(["idee", "statut", q1, "validee", "--motif", "adopté par l'équipe"]) == 0
    assert main(["journal"]) == 0 and "statut_change" in capsys.readouterr().out


def test_erreurs_lisibles_en_francais(capsys):
    assert main(["idee", "voir", "QA-0404"]) == 2
    assert "Idée inconnue" in capsys.readouterr().err
    assert main(["plan", "INCONNU"]) == 2
    assert "Document inconnu" in capsys.readouterr().err


def test_chercher_sans_notion_ni_bibliotheque_ne_plante_pas(capsys, racine_isolee):
    # Issue #53 : requête vide, emoji seuls ou bibliothèque vide → « Erreur : confiance », rc=2.
    for requete in (["chercher", "le la"], ["chercher", ""], ["chercher", "😀🧪"], ["chercher", "risque"]):
        assert main(requete) == 0, requete
        sortie = capsys.readouterr()
        assert "Couverture lexicale : 0/100 (nulle)" in sortie.out and not sortie.err
    assert main(["chercher", "", "--json"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["couverture_lexicale"]["score"] == 0 and "Requête vide" in r["avertissements"][0]
    assert main(["chercher", "risque", "--json"]) == 0
    assert "Bibliothèque vide" in json.loads(capsys.readouterr().out)["avertissements"][0]


def test_codes_retour_et_validations(capsys, racine_isolee, tmp_path):
    """#58 : import en échec ni copié ni inscrit (rc=2), pages et métadonnées validées en
    français, doc_id insensible à la casse, identifiant d'idée manquant → rc=2."""
    import pytest
    from qak import bibliotheque, chemins
    faux = tmp_path / "faux.pdf"
    faux.write_text("ceci n'est pas un PDF", encoding="utf-8")
    assert main(["importer", str(faux)]) == 2
    assert "ni copié ni inscrit" in capsys.readouterr().out
    assert not (chemins.sources() / "faux.pdf").exists() and not bibliotheque.lire_manifeste()["documents"]
    assert main(["importer", str(tmp_path / "absent.pdf")]) == 2
    assert main(["importer", str(FIXTURES / "syllabus_v9.pdf")]) == 0
    capsys.readouterr()
    for pages in ("abc", "0", "5-3"):
        assert main(["page", "CTFL", pages]) == 2
        assert "Pages attendues" in capsys.readouterr().err
    for options in (["--date", "hier soir"], ["--niveau", "n'importe"], ["--langue", "klingon"], ["--type", "x"]):
        with pytest.raises(SystemExit) as exc:  # argparse : rc=2, message d'usage
            main(["corriger", "CTFL-9.9-en", *options])
        assert exc.value.code == 2
    assert "AAAA-MM-JJ" in capsys.readouterr().err
    assert main(["corriger", "ctfl-9.9-EN"]) == 2  # rien à corriger
    assert main(["corriger", "ctfl-9.9-EN", "--date", "2030-03-13", "--langue", "en"]) == 0
    assert bibliotheque.inventaire()[0]["date_publication"] == "2030-03-13"
    assert main(["idee", "modifier"]) == 2
    assert "attend un identifiant" in capsys.readouterr().err
    assert main(["retirer", "CTFL-9.9-EN"]) == 0 and bibliotheque.inventaire() == []


def test_idee_refusee_pour_doublon_rc2(capsys, monkeypatch, racine_isolee):
    import io
    idee = {"titre": "Matrice des risques produit", "resume": "Probabilité × impact.",
            "probleme": "Effort de test uniforme.", "principe": "Calculer le niveau de risque.",
            "theme_principal": "rbt"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(idee)))
    assert main(["idee", "ajouter"]) == 0
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(idee)))
    assert main(["idee", "ajouter"]) == 2
    assert "REFUSÉ" in capsys.readouterr().out


def test_entree_standard_et_fichiers_utf8_sous_windows(capsys, monkeypatch, racine_isolee, tmp_path):
    """#57 : console Windows (cp1252) → accents corrompus ; JSON enregistré avec BOM refusé."""
    import io
    from qak import connaissances
    idee = {"titre": "Évaluer la qualité des données de test", "resume": "Contrôles à prévoir.",
            "probleme": "Données non représentatives.", "principe": "Échantillonner et vérifier.",
            "theme_principal": "rbt"}
    octets = "﻿".encode() + json.dumps(idee, ensure_ascii=False).encode("utf-8")
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO(octets), encoding="cp1252"))
    assert main(["idee", "ajouter"]) == 0, capsys.readouterr().err
    assert connaissances.lister()[0]["titre"] == "Évaluer la qualité des données de test"
    # Même chose depuis un fichier JSON avec BOM (Bloc-notes).
    f = tmp_path / "idee.json"
    f.write_bytes("﻿".encode() + json.dumps({**idee, "titre": "Échantillonnage des données de recette"},
                                                ensure_ascii=False).encode("utf-8"))
    assert main(["idee", "ajouter", "--fichier", str(f)]) == 0, capsys.readouterr().err
    assert any(i["titre"] == "Échantillonnage des données de recette" for i in connaissances.lister())
    # Octets non UTF-8 : message français, rc=2.
    monkeypatch.setattr("sys.stdin", io.TextIOWrapper(io.BytesIO("{\"titre\": \"é\"}".encode("cp1252"))))
    assert main(["idee", "ajouter"]) == 2
    assert "UTF-8" in capsys.readouterr().err


def test_lecture_pendant_une_ecriture_et_base_occupee(capsys, monkeypatch, bibliotheque_test):
    # Issue #52 : `chercher` pendant `actualiser` → « database is locked », traceback, rc=1.
    from qak import bibliotheque, chemins
    ecrivain = bibliotheque.connecter()
    try:
        assert ecrivain.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
        ecrivain.execute("BEGIN IMMEDIATE")  # un autre processus est en train d'écrire
        ecrivain.execute("UPDATE documents SET titre=titre")
        assert main(["chercher", "valeurs", "limites"]) == 0  # la lecture n'est pas bloquée
        assert "CTFL-9.9-en" in capsys.readouterr().out
        # Deux écritures : la seconde attend, puis abandonne avec un message français (rc=2).
        monkeypatch.setattr(bibliotheque, "ATTENTE_VERROU", 0.2)
        assert main(["corriger", bibliotheque_test, "--version", "9.9"]) == 2
        err = capsys.readouterr().err
        assert "base est occupée" in err and "Traceback" not in err
    finally:
        ecrivain.rollback()
        ecrivain.close()
    assert chemins.index_db().exists()


def test_section_et_page_bornees_indiquent_la_suite(capsys, racine_isolee):
    # Issue #22 : sortie bornée par --max-caracteres, terminée par ce qui reste à lire.
    assert main(["importer", str(FIXTURES / "syllabus_v9.pdf")]) == 0
    capsys.readouterr()
    assert main(["section", "CTFL", "1", "--max-caracteres", "100"]) == 0
    sortie = capsys.readouterr().out
    assert "Sortie tronquée" in sortie and "Ne citer que ce qui précède" in sortie
    assert "`section CTFL-9.9-en 1.2`" in sortie
    affiche = sortie.split("✂")[0]
    assert "divides data into partitions" not in affiche  # §1.2 non affichée…
    assert main(["section", "CTFL", "1", "--max-caracteres", "0"]) == 0
    assert "divides data into partitions" in capsys.readouterr().out  # … mais présente sans borne
    assert main(["page", "CTFL", "3-6", "--max-caracteres", "100"]) == 0
    assert "pages restantes : `page CTFL-9.9-en" in capsys.readouterr().out
    assert main(["section", "CTFL", "1", "--max-caracteres", "100", "--json"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["tronque"] and any("section CTFL-9.9-en 1.2" in l for l in r["reste_a_lire"])
    # Par défaut (15 000 caractères), une petite section n'est pas tronquée.
    assert main(["section", "CTFL", "1"]) == 0
    assert "Sortie tronquée" not in capsys.readouterr().out


def test_lire_borne_comme_section_et_page(capsys, racine_isolee):
    # Issue #156 : `lire --max-caracteres N`, prescrit par le skill et les agents, était refusé.
    assert main(["importer", str(FIXTURES / "syllabus_v9.pdf")]) == 0
    capsys.readouterr()
    assert main(["chercher", "valeurs", "limites", "--json"]) == 0
    pid = json.loads(capsys.readouterr().out)["resultats"][0]["id"]
    assert main(["lire", str(pid), "--contexte", "50", "--max-caracteres", "100"]) == 0
    sortie = capsys.readouterr().out
    assert "Sortie tronquée" in sortie and "Ne citer que ce qui précède" in sortie
    assert main(["lire", str(pid), "--contexte", "50", "--max-caracteres", "100", "--json"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["tronque"] and r["reste_a_lire"] and r["document"]["doc_id"] == "CTFL-9.9-en"
    assert main(["lire", str(pid), "--contexte", "50", "--max-caracteres", "0"]) == 0
    assert "Sortie tronquée" not in capsys.readouterr().out
    assert main(["lire", str(pid)]) == 0  # défaut 15 000 : un passage seul n'est pas tronqué
    sortie = capsys.readouterr().out
    assert f"passage #{pid}" in sortie and "Sortie tronquée" not in sortie


def test_doublons_en_une_ligne_sans_json(capsys, monkeypatch, racine_isolee):
    """#128 : `idee doublons --titre … --resume … --theme …` sans entrée standard."""
    idee = {"titre": "Matrice des risques probabilité impact", "resume": "Prioriser les tests par probabilité × impact.",
            "probleme": "Effort uniforme.", "principe": "Calculer le niveau de risque.", "theme_principal": "rbt"}
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps(idee)))
    assert main(["idee", "ajouter"]) == 0
    q1 = capsys.readouterr().out.split("Idée créée : ")[1].split()[0]
    monkeypatch.setattr("sys.stdin", __import__("io").StringIO(""))  # rien sur l'entrée standard
    assert main(["idee", "doublons", "--titre", "Matrice des risques : probabilité et impact",
                 "--resume", "Prioriser les tests selon probabilité × impact.", "--theme", "rbt"]) == 0
    sortie = capsys.readouterr().out
    assert q1 in sortie and "DOUBLON PROBABLE" in sortie
    assert main(["idee", "doublons", "--titre", "x", "--theme", "inconnu"]) == 2
