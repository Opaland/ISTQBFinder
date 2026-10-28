"""#200 : paquet `.mcpb` (extension Claude Desktop) du serveur MCP en lecture seule.

Hors réseau : le manifeste et le paquet produit par `scripts/produire_mcpb.py`. Le format
lui-même est validé en CI par `npx @anthropic-ai/mcpb validate` et `mcpb pack` (job `mcpb`)."""
import copy
import importlib.util
import json
import zipfile

import pytest

from conftest import RACINE_CODE

_spec = importlib.util.spec_from_file_location("produire_mcpb", RACINE_CODE / "scripts" / "produire_mcpb.py")
mcpb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mcpb)


@pytest.fixture
def manifeste():
    return json.loads(mcpb.MANIFESTE.read_text(encoding="utf-8"))


def test_manifeste_conforme_sans_pdf(manifeste):
    assert mcpb.verifier(manifeste) == []
    texte = mcpb.MANIFESTE.read_text(encoding="utf-8").lower()
    assert ".pdf" not in texte and "bibliotheque" not in texte
    assert manifeste["server"]["mcp_config"]["args"][-1] == "mcp"
    # Venv réellement créé par les installeurs : .venv/bin/python et .venv\Scripts\python.exe.
    assert "VPY=.venv/bin/python" in (RACINE_CODE / "installer.sh").read_text(encoding="utf-8")
    assert '".venv\\Scripts\\python.exe"' in (RACINE_CODE / "installer.ps1").read_text(encoding="utf-8")


@pytest.mark.parametrize("abimer, motif", [
    (lambda m: m["user_config"]["clone"].update(default="${HOME}/bibliotheque/sources/CTFL.pdf"), "PDF"),
    (lambda m: m["server"]["mcp_config"].update(command="python"), "commande par défaut"),
    (lambda m: m["server"]["mcp_config"]["platform_overrides"].pop("win32"), "commande win32"),
    (lambda m: m["user_config"]["clone"].update(type="string"), "directory"),
    (lambda m: m["tools"].pop(), "outils déclarés"),
    (lambda m: m.update(version="1.0"), "semver"),
])
def test_verifier_refuse_un_manifeste_abime(manifeste, abimer, motif):
    m = copy.deepcopy(manifeste)
    abimer(m)
    assert any(motif in e for e in mcpb.verifier(m)), mcpb.verifier(m)


def test_paquet_produit_sans_pdf_ni_code(tmp_path, manifeste):
    paquet = mcpb.produire(tmp_path / "istqbfinder.mcpb")
    with zipfile.ZipFile(paquet) as z:
        assert z.namelist() == ["manifest.json"]
        assert json.loads(z.read("manifest.json")) == manifeste
    assert mcpb.verifier_paquet(paquet) == []
    # Production reproductible : même octets à chaque fois.
    assert mcpb.produire(tmp_path / "bis.mcpb").read_bytes() == paquet.read_bytes()


def test_version_choisie_et_paquet_abime_refuse(tmp_path):
    paquet = mcpb.produire(tmp_path / "v.mcpb", version="0.2.0")
    with zipfile.ZipFile(paquet) as z:
        assert json.loads(z.read("manifest.json"))["version"] == "0.2.0"
    with pytest.raises(SystemExit, match="semver"):
        mcpb.produire(tmp_path / "x.mcpb", version="deux")
    with zipfile.ZipFile(paquet, "a") as z:
        z.writestr("syllabus/CTFL.PDF", b"%PDF")
    erreurs = mcpb.verifier_paquet(paquet)
    assert any("PDF dans le paquet" in e for e in erreurs) and any("inattendu" in e for e in erreurs)


def test_mcpb_documente_et_valide_en_ci():
    doc = (RACINE_CODE / "docs" / "installation.md").read_text(encoding="utf-8")
    assert "scripts/produire_mcpb.py" in doc and "Install Extension" in doc
    ci = (RACINE_CODE / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "@anthropic-ai/mcpb@" in ci and " validate mcpb/manifest.json" in ci
    assert "scripts/produire_mcpb.py" in ci


def test_commande_par_plateforme(manifeste, tmp_path):
    assert mcpb.commande(manifeste, tmp_path, "linux") == [f"{tmp_path}/.venv/bin/python", f"{tmp_path}/qa.py", "mcp"]
    assert mcpb.commande(manifeste, tmp_path, "darwin")[0] == f"{tmp_path}/.venv/bin/python"
    assert mcpb.commande(manifeste, tmp_path, "win32") == [
        f"{tmp_path}\\.venv\\Scripts\\python.exe", f"{tmp_path}\\qa.py", "mcp"]
    with pytest.raises(SystemExit, match="installer.sh"):
        mcpb.essayer(tmp_path)  # pas de venv : message qui dit quoi faire
