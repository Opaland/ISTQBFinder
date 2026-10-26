"""#184 : plugin Claude Code généré dans `plugin/` (docs/plugin.md).

À jour : `test_integrations.py` (même générateur). Ici : aucune écriture pré-approuvée,
aucun document tiers dans le plugin, lanceurs réels (`bin/qa` en sh, `bin/qa.cmd` sous
Windows, #203), dialogue MCP réel par le lanceur, et validation par la CLI `claude` quand
elle est installée (la CI l'installe dans les jobs `tests` et `plugin-windows`)."""
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

from conftest import RACINE_CODE
from test_permissions import ECRITURE

PLUGIN = RACINE_CODE / "plugin"


def _regles_skills() -> list[str]:
    regles = []
    for f in PLUGIN.glob("skills/*/SKILL.md"):
        ligne = next(l for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("allowed-tools:"))
        regles += re.findall(r"Bash\([^)]*\)", ligne)
    return regles


def test_aucune_ecriture_preapprouvee_par_les_skills_du_plugin():
    regles = _regles_skills()
    assert "Bash(qa chercher:*)" in regles and "Bash(qa confiance:*)" in regles
    commandes = [re.match(r"Bash\(qa (.*?):?\*?\)$", r).group(1) for r in regles if r.startswith("Bash(qa")]
    assert not [c for c in commandes if any(c.startswith(e) or (e.startswith(c) and len(c) < len(e))
                                            for e in ECRITURE)]
    assert not [r for r in regles if "python" in r]  # tout passe par le lanceur du plugin


def test_ni_pdf_ni_fichier_binaire_dans_le_plugin():
    """Droits (#149, NOTICE.md) : le plugin ne recopie aucun document de bibliotheque/."""
    for f in PLUGIN.rglob("*"):
        if f.is_file():
            f.read_text(encoding="utf-8")  # texte seulement
            assert f.suffix.lower() not in (".pdf", ".db", ".npz"), f
    assert sum(f.stat().st_size for f in PLUGIN.rglob("*") if f.is_file()) < 200_000


def test_manifeste_marketplace_locale_et_serveur_mcp():
    manifeste = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifeste["name"] == "istqbfinder" and manifeste["license"] == "MIT"
    assert manifeste["mcpServers"]["istqbfinder"] == {"command": "${CLAUDE_PLUGIN_ROOT}/bin/qa", "args": ["mcp"]}
    marche = json.loads((PLUGIN / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert marche["plugins"][0]["source"] == "./"
    # Marketplace locale seulement : rien à la racine du dépôt (docs/plugin.md, § 3.2).
    assert not (RACINE_CODE / ".claude-plugin").exists()
    for agent in PLUGIN.glob("agents/*.md"):
        texte = agent.read_text(encoding="utf-8")
        assert "mcp__plugin_istqbfinder_istqbfinder__lire" in texte and "  - istqbfinder:qa-knowledge" in texte


LANCEUR = PLUGIN / "bin" / ("qa.cmd" if os.name == "nt" else "qa")


def _python_du_lanceur() -> str | None:
    """Le Python que le lanceur choisira : celui du venv du clone, sinon celui du PATH."""
    for venv in (RACINE_CODE / ".venv" / "bin" / "python", RACINE_CODE / ".venv" / "Scripts" / "python.exe"):
        if venv.exists():
            return str(venv)
    return shutil.which("python3" if os.name != "nt" else "python") or shutil.which("python")


def test_lanceur_demarre_la_cli_du_clone(tmp_path):
    if os.name != "nt":
        assert os.access(LANCEUR, os.X_OK)
    r = subprocess.run([str(LANCEUR), "confiance", "--base", "60", "--lus", "1", "--concordants", "1"],
                       capture_output=True, text=True, cwd=tmp_path, timeout=60)
    assert r.returncode == 0, r.stderr
    assert "Confiance : " in r.stdout
    # Code retour de qa.py transmis tel quel (2 : argument refusé par argparse).
    r = subprocess.run([str(LANCEUR), "commande-inconnue"], capture_output=True, text=True, cwd=tmp_path, timeout=60)
    assert r.returncode == 2
    # Copié hors du clone (cache d'une marketplace GitHub) : message clair, pas de pile Python.
    copie = tmp_path / "cache" / "istqbfinder" / "bin"
    copie.mkdir(parents=True)
    shutil.copy2(LANCEUR, copie / LANCEUR.name)
    r = subprocess.run([str(copie / LANCEUR.name), "--help"], capture_output=True, text=True, timeout=30)
    assert r.returncode == 2 and "qa.py introuvable" in r.stderr and "marketplace add" in r.stderr


def test_lanceur_windows_sans_etiquette_ni_chemin_dans_un_bloc():
    """bin/qa.cmd est en LF (.gitattributes) : ni `goto` ni étiquette ; une « ) » dans le
    chemin d'installation fermerait un bloc qui développe %RACINE%."""
    texte = (PLUGIN / "bin" / "qa.cmd").read_text(encoding="utf-8")
    assert texte.startswith("@echo off\n") and "\r" not in texte
    assert not re.search(r"^\s*:|goto", texte, re.M)
    blocs = re.findall(r"\(\n(.*?)\n\)", texte, re.S)
    assert blocs and not [b for b in blocs if "%RACINE%" in b or "%PY%" in b]


def test_serveur_mcp_par_le_lanceur_repond_a_tools_list(tmp_path):
    """#203 : la commande déclarée dans plugin.json démarre le serveur et répond (stdio réel)."""
    pytest.importorskip("mcp.server.mcpserver", reason="SDK `mcp` absent : pip install -r requirements-mcp.txt")
    py = _python_du_lanceur()
    if not py or subprocess.run([py, "-c", "import mcp.server.mcpserver"], capture_output=True).returncode:
        pytest.skip(f"le Python du lanceur ({py}) n'a pas le SDK `mcp` (requirements-mcp.txt)")
    from mcp import Client, StdioServerParameters

    async def dialogue():
        params = StdioServerParameters(command=str(LANCEUR), args=["mcp"], cwd=str(tmp_path),
                                       env={**os.environ, "QAK_RACINE": str(tmp_path)})
        async with Client(params) as c:
            noms = {t.name for t in (await c.list_tools()).tools}
            assert {"chercher", "lire", "passages_lus"} <= noms

    asyncio.run(asyncio.wait_for(dialogue(), 90))


@pytest.mark.skipif(not shutil.which("claude"), reason="CLI `claude` absente : `claude plugin validate` non lancé")
def test_claude_plugin_validate_strict():
    # shutil.which : sous Windows, npm installe `claude.cmd`, que subprocess ne trouve pas seul.
    r = subprocess.run([shutil.which("claude"), "plugin", "validate", "--strict", str(PLUGIN)],
                       capture_output=True, text=True, timeout=120, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Validation passed" in r.stdout
