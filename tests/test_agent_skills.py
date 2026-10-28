"""Issue #154 : les skills respectent le standard Agent Skills (agentskills.io/specification),
vérifié par le validateur de référence `skills-ref` (CLI `agentskills validate`).

Un seul écart est toléré, et seulement dans les skills lus par Claude Code (`.claude/skills/`,
`plugin/skills/`, skill `installer` de l'export) : les champs propres à Claude Code
`argument-hint` (indice d'autocomplétion de `/skill`) et `disable-model-invocation`. Claude Code
ne les lit qu'à la racine de l'en-tête : les ranger sous `metadata:` les ferait ignorer
(« Claude Code doesn't act on its contents », code.claude.com/docs/en/skills). Les copies
Gemini (`.gemini/skills/`) sont validées sans aucune tolérance.

`allowed-tools` (virgules, motifs `Bash(python qa.py chercher:*)`) n'est pas contrôlé par
`skills-ref` 0.1.1 : écart documenté dans docs/architecture.md (« Standard Agent Skills »).

`skills-ref` exige Python 3.11+ : absent, le test est ignoré avec la raison ; le job CI
`tests` l'installe et pose QAK_EXIGER_SKILLS_REF=1, qui transforme l'absence en échec.
"""
import os

import pytest
from conftest import RACINE_CODE

try:
    from skills_ref.parser import parse_frontmatter
    from skills_ref.validator import validate, validate_metadata
except ImportError:  # pragma: no cover - dépend de l'environnement
    if os.environ.get("QAK_EXIGER_SKILLS_REF") == "1":
        raise
    pytest.skip("skills-ref absent (pip install skills-ref, Python 3.11+) : conformité Agent Skills "
                "non vérifiée", allow_module_level=True)

PROPRES_A_CLAUDE_CODE = {"argument-hint", "disable-model-invocation"}

STRICTS = sorted((RACINE_CODE / ".gemini" / "skills").glob("*/SKILL.md"))
CLAUDE_CODE = sorted([*(RACINE_CODE / ".claude" / "skills").glob("*/SKILL.md"),
                      *(RACINE_CODE / "plugin" / "skills").glob("*/SKILL.md")])
INSTALLER = RACINE_CODE / "scripts" / "plugin_autonome" / "installer.md"


def _id(chemin):
    return chemin.relative_to(RACINE_CODE).as_posix()


def erreurs_tolerantes(skill_md, dossier) -> list[str]:
    """Erreurs de `skills-ref` une fois retirés les seuls champs propres à Claude Code."""
    entete, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    for champ in PROPRES_A_CLAUDE_CODE:
        entete.pop(champ, None)
    return validate_metadata(entete, dossier)


def test_skills_trouves():
    assert len(STRICTS) == 3 and len(CLAUDE_CODE) == 6


@pytest.mark.parametrize("skill", STRICTS, ids=_id)
def test_copie_gemini_strictement_conforme(skill):
    assert validate(skill.parent) == []


@pytest.mark.parametrize("skill", CLAUDE_CODE, ids=_id)
def test_skill_claude_code_conforme_hors_champs_claude(skill):
    assert erreurs_tolerantes(skill, skill.parent) == []


def test_skill_installer_de_l_export_conforme():
    # Le modèle est copié en skills/installer/SKILL.md par scripts/exporter_plugin.py.
    assert erreurs_tolerantes(INSTALLER, INSTALLER.parent / "installer") == []


@pytest.mark.parametrize("skill", CLAUDE_CODE, ids=_id)
def test_compatibilite_declaree(skill):
    entete, _ = parse_frontmatter(skill.read_text(encoding="utf-8"))
    assert "Python 3.10+" in entete.get("compatibility", "")


def test_la_tolerance_ne_couvre_que_les_champs_claude(tmp_path):
    """Un champ inconnu ou un nom invalide reste une erreur malgré la tolérance."""
    dossier = tmp_path / "essai"
    dossier.mkdir()
    (dossier / "SKILL.md").write_text("---\nname: essai\ndescription: Essai.\n"
                                      "argument-hint: \"[x]\"\nversion: \"1\"\n---\nCorps\n",
                                      encoding="utf-8")
    erreurs = erreurs_tolerantes(dossier / "SKILL.md", dossier)
    assert len(erreurs) == 1 and "version" in erreurs[0] and "argument-hint" not in erreurs[0]
    assert erreurs_tolerantes(dossier / "SKILL.md", tmp_path / "autre")[-1].startswith("Directory name")
