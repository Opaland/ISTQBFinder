"""Recherche sémantique optionnelle (issue #107) : tout fonctionne sans ses dépendances."""
import pytest

from qak import recherche, semantique
from qak.cli import main


@pytest.fixture
def sans_dependances(monkeypatch):
    monkeypatch.setattr(semantique, "dependances_presentes", lambda: False)


def test_sans_dependances_resultats_lexicaux_identiques(bibliotheque_test, sans_dependances):
    lexical = recherche.chercher("equivalence partitioning")
    hybride = recherche.chercher("equivalence partitioning", semantique=True)
    assert hybride["resultats"] == lexical["resultats"]
    assert any("requirements-semantique.txt" in a for a in hybride["avertissements"])
    assert not any("sémantique" in a for a in lexical["avertissements"])


def test_sans_vecteurs_avertissement(bibliotheque_test, monkeypatch):
    monkeypatch.setattr(semantique, "dependances_presentes", lambda: True)
    r = recherche.chercher("equivalence partitioning", semantique=True)
    assert r["resultats"] and any("actualiser --semantique" in a for a in r["avertissements"])


def test_cli_sans_dependances(capsys, bibliotheque_test, sans_dependances):
    assert main(["chercher", "equivalence", "partitioning", "--semantique"]) == 0
    assert "résultats lexicaux seuls" in capsys.readouterr().out
    assert main(["actualiser", "--semantique"]) == 2
    assert "requirements-semantique.txt" in capsys.readouterr().err
    assert main(["evaluer", "--semantique", "-k", "3"]) == 0


def test_installation_par_defaut_sans_modele():
    # La CI et requirements.txt n'installent pas les dépendances lourdes.
    from conftest import RACINE_CODE
    assert "sentence" not in (RACINE_CODE / "requirements.txt").read_text(encoding="utf-8")
    assert "sentence-transformers" in (RACINE_CODE / "requirements-semantique.txt").read_text(encoding="utf-8")
