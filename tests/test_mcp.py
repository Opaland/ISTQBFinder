"""#153 : serveur MCP local en lecture seule (`python qa.py mcp`).

Les fonctions d'outil se testent sans le SDK ; le dialogue MCP réel (sous-processus stdio,
client du SDK officiel) est ignoré, avec la raison, si `mcp` n'est pas installé — la CI
l'installe dans le job `tests` (requirements-mcp.txt)."""
import asyncio
import re
import sys

import pytest

from conftest import RACINE_CODE
from qak import cli, serveur_mcp
from qak.connaissances import ErreurValidation

ECRITURES = ("ajouter", "modifier", "statut", "retour", "lier", "retirer", "telecharger", "importer",
             "actualiser", "corriger", "obsolete")


@pytest.fixture(autouse=True)
def session_vierge(monkeypatch):
    monkeypatch.setattr(serveur_mcp, "_LUS", [])


def test_outils_reutilisent_la_cli_et_tracent_les_passages_lus(bibliotheque_test):
    trouve = serveur_mcp.chercher("valeurs limites")
    pid = int(re.search(r"passage #(\d+)", trouve)[1])
    assert "Aucun passage lu" in serveur_mcp.passages_lus()

    lu = serveur_mcp.lire(pid)
    citer = re.search(r"Citer : (\[[^\]]+\])", lu)[1]
    assert citer.startswith("[CTFL v9.9 EN, ")
    assert cli.LECTURES is None  # le relevé ne reste pas actif pour la CLI
    assert f"LU dans cette session : {citer}" in serveur_mcp.passages_lus(citer)
    assert "NON LU" in serveur_mcp.passages_lus("[CTFL v9.9 EN, §8.8, p. 99]")

    sec = serveur_mcp.section("CTFL", "2.1")
    assert "Risk level is determined" in sec and "Citer : [CTFL v9.9 EN, §2.1" in sec
    assert "Citer : " in serveur_mcp.page("CTFL", "1")
    assert "2.1" in serveur_mcp.plan("CTFL")
    assert "référence(s) lue(s)" in serveur_mcp.passages_lus()


def test_confiance_compare_les_lectures_annoncees_au_releve(bibliotheque_test):
    r = serveur_mcp.confiance(base=70, lus=2, concordants=1)
    assert "Confiance : " in r and "ATTENTION : lus=2 annoncé, 0 relevé(s)" in r
    serveur_mcp.section("CTFL", "2.1")
    assert "ATTENTION" not in serveur_mcp.confiance(base=70, lus=1, concordants=1)


def test_erreurs_en_francais_et_arguments_jamais_pris_pour_des_options(bibliotheque_test):
    with pytest.raises(ErreurValidation, match="Document inconnu"):
        serveur_mcp.section("INCONNU", "1.1")
    with pytest.raises(ErreurValidation, match="Idée inconnue"):
        serveur_mcp.idee_voir("QA-0404")
    with pytest.raises(ErreurValidation):  # « --forcer » est un texte, jamais une option
        serveur_mcp.idee_voir("--forcer")
    assert "Aucune idée" in serveur_mcp.idee_chercher("--json matrice")


def test_sans_sdk_message_d_installation(monkeypatch, capsys):
    monkeypatch.setattr(serveur_mcp, "sdk_present", lambda: False)
    assert cli.main(["mcp"]) == 2
    err = capsys.readouterr().err
    assert "requirements-mcp.txt" in err and "SDK" in err


def test_dependance_optionnelle():
    """pypdf reste la seule dépendance obligatoire ; le SDK MCP a son fichier, installé en CI."""
    assert "mcp" not in (RACINE_CODE / "requirements.txt").read_text(encoding="utf-8")
    assert re.search(r"^mcp>=2\.3", (RACINE_CODE / "requirements-mcp.txt").read_text(encoding="utf-8"), re.M)
    assert "requirements-mcp.txt" in (RACINE_CODE / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")


def test_dialogue_mcp_reel_en_stdio(bibliotheque_test, racine_isolee):
    pytest.importorskip("mcp.server.mcpserver", reason="SDK `mcp` absent : pip install -r requirements-mcp.txt")
    from mcp import Client, StdioServerParameters

    async def dialogue():
        params = StdioServerParameters(command=sys.executable, args=[str(RACINE_CODE / "qa.py"), "mcp"],
                                       env={"QAK_RACINE": str(racine_isolee)}, cwd=str(racine_isolee))
        async with Client(params) as c:
            outils = (await c.list_tools()).tools
            noms = {t.name for t in outils}
            assert noms == {"chercher", "lire", "section", "page", "plan", "idee_chercher", "idee_voir",
                            "confiance", "passages_lus"}
            assert not [n for n in noms if any(e in n for e in ECRITURES)]
            assert all(t.annotations.read_only_hint and not t.annotations.destructive_hint for t in outils)
            texte = (await c.call_tool("chercher", {"requete": "valeurs limites"})).content[0].text
            pid = int(re.search(r"passage #(\d+)", texte)[1])
            lu = (await c.call_tool("lire", {"passage": pid})).content[0].text
            citer = re.search(r"Citer : (\[[^\]]+\])", lu)[1]
            verif = (await c.call_tool("passages_lus", {"citation": citer})).content[0].text
            assert verif.startswith("LU dans cette session")
            erreur = await c.call_tool("section", {"doc": "INCONNU", "numero": "1"})
            assert erreur.is_error and "Document inconnu" in erreur.content[0].text
            # #207 : hors du document → erreur d'outil, même message que la CLI
            hors = await c.call_tool("section", {"doc": "CTFL", "numero": "99.9"})
            assert hors.is_error and "Section 99.9 introuvable" in hors.content[0].text
            hors = await c.call_tool("page", {"doc": "CTFL", "pages": "999"})
            assert hors.is_error and "Page 999 inexistante" in hors.content[0].text

    asyncio.run(asyncio.wait_for(dialogue(), 60))
    assert not (racine_isolee / "connaissances" / "journal.jsonl").exists()  # rien n'a été écrit


def test_qa_py_mcp_documente():
    doc = (RACINE_CODE / "docs" / "installation.md").read_text(encoding="utf-8")
    assert "claude mcp add" in doc and "qa.py mcp" in doc and "claude_desktop_config.json" in doc
