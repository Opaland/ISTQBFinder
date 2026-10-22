"""Issue #73 : `qa.py diagnostic` et scripts d'installation. L'installation complète
(venv, dépendances, indexation) est exécutée par la CI sur un clone propre (job
« installation ») ; ici, les contrôles rapides."""
import shutil
import subprocess

import pytest
from conftest import RACINE_CODE

from qak import diagnostic
from qak.cli import main


def _etat(etats, sujet):
    return next(e for e in etats if e[1] == sujet)


def test_diagnostic_index_vide_ko(capsys):
    with pytest.raises(SystemExit) as fin:
        main(["diagnostic"])
    assert fin.value.code == 1
    sortie = capsys.readouterr().out
    assert "KO  Index" in sortie and "python qa.py actualiser" in sortie
    assert "Diagnostic : KO" in sortie


def test_diagnostic_bibliotheque_ok(bibliotheque_test, monkeypatch):
    monkeypatch.setattr(diagnostic, "REQUETE_TEMOIN", "valeurs limites")
    etats = diagnostic.diagnostic()
    assert _etat(etats, "Index")[0] == "OK"
    assert _etat(etats, "Recherche témoin")[0] == "OK"
    assert "CTFL-9.9-en" in _etat(etats, "Recherche témoin")[2]
    assert _etat(etats, "Base d'idées") == ("OK", "Base d'idées", "0 idées")
    assert _etat(etats, "Fichiers d'intégration")[0] == "OK"
    assert not [e for e in etats if e[0] == "KO"]


def test_recherche_temoin_sans_resultat_ko(bibliotheque_test, monkeypatch):
    monkeypatch.setattr(diagnostic, "REQUETE_TEMOIN", "zzzintrouvable")
    assert _etat(diagnostic.diagnostic(), "Recherche témoin")[0] == "KO"


def test_cli_assistant_absente_non_bloquante(monkeypatch):
    """Une CLI d'assistant absente est « à faire » (--), pas un échec d'installation."""
    monkeypatch.setenv("PATH", "")
    etats = diagnostic.diagnostic(diagnostic.ASSISTANTS)
    for nom in diagnostic.ASSISTANTS:
        assert _etat(etats, f"{nom} : fichiers")[0] == "OK"
        assert _etat(etats, f"{nom} : CLI")[0] == "--"


@pytest.mark.skipif(not shutil.which("bash"), reason="bash absent")
def test_installer_sh_options():
    script = RACINE_CODE / "installer.sh"
    assert subprocess.run(["bash", "-n", str(script)]).returncode == 0
    r = subprocess.run(["bash", str(script), "--assistant", "inconnu"], capture_output=True, text=True)
    assert r.returncode == 2 and "claude, copilot, gemini ou tous" in r.stderr
    r = subprocess.run(["bash", str(script), "--help"], capture_output=True, text=True)
    assert r.returncode == 0 and "--assistant" in r.stdout


def test_installer_ps1_coherent():
    texte = (RACINE_CODE / "installer.ps1").read_bytes()
    assert texte.startswith(b"\xef\xbb\xbf"), "BOM UTF-8 requis : PowerShell 5.1 lirait les accents en ANSI"
    texte = texte.decode("utf-8")
    assert '[ValidateSet("", "claude", "copilot", "gemini", "tous")]' in texte
    for etape in ("-m venv .venv", "requirements.txt", "qa.py actualiser", "qa.py diagnostic"):
        assert etape in texte
