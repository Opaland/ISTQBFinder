"""Issues #70 (Copilot) et #71 (Gemini) : les intégrations des autres assistants sont
générées depuis la source unique `.claude/` et restent synchronisées."""
import importlib.util
import json
import re

import pytest
from conftest import RACINE_CODE

_spec = importlib.util.spec_from_file_location("generer_integrations",
                                               RACINE_CODE / "scripts" / "generer_integrations.py")
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

SKILLS = sorted((RACINE_CODE / ".claude" / "skills").glob("*/SKILL.md"))
AGENTS = sorted((RACINE_CODE / ".claude" / "agents").glob("*.md"))


def test_fichiers_generes_a_jour():
    ecarts = gen.ecarts()
    assert not ecarts, "Lancer « python scripts/generer_integrations.py » :\n" + "\n".join(ecarts)


@pytest.mark.parametrize("skill", SKILLS, ids=lambda s: s.parent.name)
def test_skill_lisible_par_copilot(skill):
    """Copilot lit `.claude/skills/` tel quel : un nom invalide ou différent du dossier
    fait ignorer le skill sans message (doc VS Code « Agent Skills »)."""
    champs, _ = gen.lire_entete(skill.read_text(encoding="utf-8"))
    assert re.fullmatch(r"[a-z0-9-]{1,64}", champs["name"])
    assert champs["name"] == skill.parent.name
    assert 0 < len(champs["description"]) <= 1024


@pytest.mark.parametrize("agent", AGENTS, ids=lambda a: a.stem)
def test_agent_copilot(agent):
    source, corps_source = gen.lire_entete(agent.read_text(encoding="utf-8"))
    genere = (RACINE_CODE / ".github" / "agents" / f"{agent.stem}.agent.md").read_text(encoding="utf-8")
    champs, corps = gen.lire_entete(genere)
    assert champs["name"] == source["name"]
    entete = genere.split("---", 2)[1]
    description = re.search(r"^description: (.*)$", entete, re.M).group(1)
    assert json.loads(description) == source["description"]  # chaîne YAML entre guillemets, valide
    outils = json.loads(re.search(r"^tools: (.*)$", entete, re.M).group(1))
    assert "edit" not in outils and "execute" in outils and "read" in outils
    assert ("web" in outils) == ("WebSearch" in source["tools"])
    assert corps.endswith(corps_source)  # même prompt que la source
    assert ".claude/skills/qa-knowledge/SKILL.md" in corps  # la méthode n'est pas préchargée


def test_agent_sans_web_n_a_pas_le_web():
    assert gen.outils({"tools": "Bash, Read", "disallowedTools": "Write, Edit, WebSearch"},
                      gen.OUTILS_COPILOT) == ["execute", "read"]
    assert gen.outils({"tools": "Bash, Edit"}, gen.OUTILS_COPILOT) == ["execute"]


def test_source_modifiee_detectee(tmp_path, monkeypatch):
    """Une source modifiée sans régénération est signalée, puis réparée par generer()."""
    agents = tmp_path / ".claude" / "agents"
    agents.mkdir(parents=True)
    (agents / "essai.md").write_text("---\nname: essai\ndescription: Essai.\ntools: Bash, Read\n---\n\nCorps.\n",
                                     encoding="utf-8")
    monkeypatch.setattr(gen, "RACINE", tmp_path)
    monkeypatch.setattr(gen, "AGENTS_CLAUDE", agents)
    (tmp_path / ".claude" / "skills").mkdir()
    monkeypatch.setattr(gen, "SKILLS_CLAUDE", tmp_path / ".claude" / "skills")
    (tmp_path / ".claude" / "settings.json").write_text('{"permissions": {"allow": []}}', encoding="utf-8")
    monkeypatch.setattr(gen, "REGLAGES_CLAUDE", tmp_path / ".claude" / "settings.json")
    generes = {".github/agents/essai.agent.md", ".gemini/agents/essai.md", ".gemini/commands/essai.toml",
               "plugin/agents/essai.md"}
    fixes = {".gemini/settings.json", "plugin/.claude-plugin/plugin.json", "plugin/.claude-plugin/marketplace.json",
             "plugin/README.md", "plugin/bin/qa"}
    assert set(gen.ecarts()) == {f"absent : {g}" for g in generes | fixes}
    gen.generer()
    assert gen.ecarts() == []
    (agents / "essai.md").write_text("---\nname: essai\ndescription: Essai 2.\ntools: Bash\n---\n\nCorps.\n",
                                     encoding="utf-8")
    assert set(gen.ecarts()) == {f"périmé : {g}" for g in generes}
    (agents / "essai.md").unlink()
    assert set(gen.ecarts()) == {f"orphelin : {g}" for g in generes}
    gen.generer()
    assert gen.ecarts() == [] and not any((tmp_path / g).exists() for g in generes)


def test_agents_md_importe_par_claude():
    claude = (RACINE_CODE / "CLAUDE.md").read_text(encoding="utf-8")
    agents = (RACINE_CODE / "AGENTS.md").read_text(encoding="utf-8")
    assert re.search(r"^@AGENTS\.md$", claude, re.M)
    for regle in ("Lire avant de citer", "Confiance : NN/100", "Closes #n", "VERSION_EXTRACTEUR"):
        assert regle in agents


# --- Gemini CLI (#71) -------------------------------------------------------------------

GEMINI = RACINE_CODE / ".gemini"


@pytest.mark.parametrize("skill", SKILLS, ids=lambda s: s.parent.name)
def test_skill_gemini_copie_complete(skill):
    """Copie fidèle (même corps, mêmes fichiers annexes) et liens relatifs valides."""
    copie = GEMINI / "skills" / skill.parent.name
    champs_source, corps_source = gen.lire_entete(skill.read_text(encoding="utf-8"))
    champs, corps = gen.lire_entete((copie / "SKILL.md").read_text(encoding="utf-8"))
    assert champs.keys() == {"name", "description"}  # allowed-tools : propre à Claude Code
    assert champs["name"] == champs_source["name"]
    assert corps.endswith(corps_source)
    annexes = {f.relative_to(skill.parent) for f in skill.parent.rglob("*") if f.is_file()}
    assert {f.relative_to(copie) for f in copie.rglob("*") if f.is_file()} == annexes
    for f in copie.rglob("*.md"):
        for lien in re.findall(r"\]\(([^)#]+)\)", f.read_text(encoding="utf-8")):
            if not lien.startswith("http"):
                assert (f.parent / lien).exists(), f"{f.relative_to(RACINE_CODE)} : lien cassé {lien}"


@pytest.mark.parametrize("agent", AGENTS, ids=lambda a: a.stem)
def test_agent_et_commande_gemini(agent):
    tomllib = pytest.importorskip("tomllib", reason="Python < 3.11 : lecture TOML non vérifiée")
    source, corps_source = gen.lire_entete(agent.read_text(encoding="utf-8"))
    champs, corps = gen.lire_entete((GEMINI / "agents" / agent.name).read_text(encoding="utf-8"))
    assert champs["name"] == source["name"] and champs["kind"] == "local"
    assert "write_file" not in champs["tools"] and "replace" not in champs["tools"]
    assert ("google_web_search" in champs["tools"]) == ("WebSearch" in source["tools"])
    assert corps.endswith(corps_source)
    commande = tomllib.loads((GEMINI / "commands" / f"{agent.stem}.toml").read_text(encoding="utf-8"))
    assert commande["prompt"].rstrip().endswith("{{args}}")
    assert corps_source.rstrip() in commande["prompt"]
    # @{…} et !{…} seraient exécutés par Gemini (injection de fichier / commande shell).
    assert "@{" not in commande["prompt"] and "!{" not in commande["prompt"]


def test_reglages_gemini_lecture_seule():
    import test_permissions
    reglages = json.loads((GEMINI / "settings.json").read_text(encoding="utf-8"))
    assert reglages["context"]["fileName"] == ["AGENTS.md"]
    autorises = reglages["tools"]["allowed"]
    assert "run_shell_command(python qa.py chercher)" in autorises
    for regle in autorises:
        commande = re.fullmatch(r"run_shell_command\((.+)\)", regle).group(1)
        assert not test_permissions._ecrit(f"Bash({commande}:*)"), regle
    assert "run_shell_command" not in autorises  # jamais tout le terminal
