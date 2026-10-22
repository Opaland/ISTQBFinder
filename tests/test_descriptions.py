"""Issue #21 : les descriptions (qui décident du déclenchement) départagent les skills
et les agents, et excluent le développement du dépôt."""
import re

import pytest
from conftest import RACINE_CODE

CLAUDE = RACINE_CODE / ".claude"


def description(chemin) -> str:
    texte = chemin.read_text(encoding="utf-8")
    return re.search(r"^description: (.*)$", texte, re.M).group(1)


@pytest.mark.parametrize("chemin, attendus", [
    ("skills/qa-knowledge/SKILL.md", ["Pas pour le développement de ce dépôt", "agent sylvie", "agent thomas"]),
    ("agents/thomas.md", ["recherche approfondie", "quand l'utilisateur le demande", "question simple"]),
    ("agents/sylvie.md", ["Pas pour une question de connaissance", "développement de ce dépôt"]),
    ("skills/ajouter-syllabus/SKILL.md", ["installer un fichier ou un code précis", "/bibliotheque"]),
    ("skills/bibliotheque/SKILL.md", ["détecter les nouvelles versions", "/ajouter-syllabus"]),
], ids=lambda v: v if isinstance(v, str) else "")
def test_description_departage(chemin, attendus):
    d = description(CLAUDE / chemin)
    for a in attendus:
        assert a in d, f"{chemin} : « {a} » absent de la description"


def test_qualite_generique_ne_declenche_plus_qa_knowledge():
    assert "test logiciel / qualité" not in description(CLAUDE / "skills/qa-knowledge/SKILL.md")


def test_descriptions_restent_du_yaml_valide():
    """Valeur YAML non citée : « : » ou « # » précédé d'un espace la casseraient."""
    for chemin in [*CLAUDE.glob("skills/*/SKILL.md"), *CLAUDE.glob("agents/*.md")]:
        d = description(chemin)
        assert ": " not in d and " #" not in d, chemin
