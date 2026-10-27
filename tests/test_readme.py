"""Issue #24 : le README dit où l'outil fonctionne (Claude Code) et pourquoi pas claude.ai."""
from conftest import RACINE_CODE

README = (RACINE_CODE / "README.md").read_text(encoding="utf-8")


def test_section_ou_l_utiliser():
    assert "## Où l'utiliser" in README
    section = README.split("## Où l'utiliser", 1)[1].split("\n## ", 1)[0]
    assert "Claude Code en ligne de commande" in section
    assert "onglet Code" in section
    assert "claude.ai" in section and "**non**" in section
    assert "Pourquoi pas claude.ai" in section


def test_chiffres_de_la_documentation_a_jour():
    """#211 : le nombre de thèmes annoncé suit `referentiel/taxonomie.json`."""
    import json
    import re
    themes = json.loads((RACINE_CODE / "referentiel" / "taxonomie.json").read_text(encoding="utf-8"))["themes"]
    archi = (RACINE_CODE / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert re.search(r"taxonomie\.json\s+(\d+) thèmes", archi)[1] == str(len(themes))
