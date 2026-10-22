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
