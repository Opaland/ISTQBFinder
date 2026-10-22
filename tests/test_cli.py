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
        assert "Confiance documentaire : 0/100 (nulle)" in sortie.out and not sortie.err
    assert main(["chercher", "", "--json"]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["confiance"]["score"] == 0 and "Requête vide" in r["avertissements"][0]
    assert main(["chercher", "risque", "--json"]) == 0
    assert "Bibliothèque vide" in json.loads(capsys.readouterr().out)["avertissements"][0]


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
