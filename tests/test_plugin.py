"""#184 : plugin Claude Code généré dans `plugin/` (docs/plugin.md).

À jour : `test_integrations.py` (même générateur). Ici : aucune écriture pré-approuvée,
aucun document tiers dans le plugin, lanceur réel, et validation par la CLI `claude`
quand elle est installée (la CI l'installe dans le job `tests`)."""
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


@pytest.mark.skipif(os.name == "nt", reason="lanceur sh : Linux / macOS")
def test_lanceur_demarre_la_cli_du_clone(tmp_path):
    lanceur = PLUGIN / "bin" / "qa"
    assert os.access(lanceur, os.X_OK)
    r = subprocess.run([str(lanceur), "confiance", "--base", "60", "--lus", "1", "--concordants", "1"],
                       capture_output=True, text=True, cwd=tmp_path, timeout=60)
    assert r.returncode == 0, r.stderr
    assert "Confiance : " in r.stdout
    # Copié hors du clone (cache d'une marketplace GitHub) : message clair, pas de pile Python.
    copie = tmp_path / "cache" / "istqbfinder" / "bin"
    copie.mkdir(parents=True)
    shutil.copy2(lanceur, copie / "qa")
    r = subprocess.run([str(copie / "qa"), "--help"], capture_output=True, text=True, timeout=30)
    assert r.returncode == 2 and "qa.py introuvable" in r.stderr and "marketplace add" in r.stderr


@pytest.mark.skipif(not shutil.which("claude"), reason="CLI `claude` absente : `claude plugin validate` non lancé")
def test_claude_plugin_validate_strict():
    r = subprocess.run(["claude", "plugin", "validate", "--strict", str(PLUGIN)],
                       capture_output=True, text=True, timeout=120, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Validation passed" in r.stdout
