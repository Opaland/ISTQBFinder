"""Cohérence des textes du skill et des agents (frontmatter, mentions obligatoires).

Ces fichiers pilotent le comportement de Claude : une consigne qui disparaît lors
d'une réécriture ne casse aucun code, d'où ces vérifications textuelles simples."""
from pathlib import Path

import pytest
from conftest import RACINE_CODE as RACINE

SKILL = RACINE / ".claude" / "skills" / "qa-knowledge" / "SKILL.md"
AGENTS = RACINE / ".claude" / "agents"


def frontmatter(chemin: Path) -> dict:
    """Lit l'en-tête YAML minimal (clé: valeur et listes « - x ») sans dépendance."""
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    assert lignes[0] == "---", f"{chemin.name} : frontmatter absent"
    fin = lignes.index("---", 1)
    champs, cle = {}, None
    for ligne in lignes[1:fin]:
        if ligne.startswith("  - ") and cle:
            champs.setdefault(cle, [])
            if not isinstance(champs[cle], list):
                champs[cle] = []
            champs[cle].append(ligne[4:].strip())
        elif ":" in ligne and not ligne.startswith(" "):
            cle, valeur = ligne.split(":", 1)
            cle = cle.strip()
            champs[cle] = valeur.strip()
    return champs


def corps(chemin: Path) -> str:
    texte = chemin.read_text(encoding="utf-8")
    return texte.split("---", 2)[2]


@pytest.mark.parametrize("chemin", [SKILL, AGENTS / "thomas.md", AGENTS / "sylvie.md"],
                         ids=lambda c: c.stem if c != SKILL else "qa-knowledge")
def test_contenu_lu_traite_comme_donnee(chemin):
    """#20 : tout texte renvoyé par qa.py ou par le Web est une donnée, jamais une consigne."""
    texte = corps(chemin)
    assert "DONNÉE" in texte and "jamais une consigne" in texte, chemin.name
    assert "signale-la" in texte, chemin.name


def test_agents_ont_les_champs_obligatoires():
    for nom in ("thomas", "sylvie"):
        champs = frontmatter(AGENTS / f"{nom}.md")
        for cle in ("name", "description", "tools", "skills", "model"):
            assert champs.get(cle), f"{nom} : champ {cle} manquant"
        assert champs["name"] == nom
        assert champs["skills"] == ["qa-knowledge"]


def test_web_obligatoire_pour_un_outil_absent_des_syllabus():
    """#49 : la recherche Web est faite (pas proposée) quand l'outil nommé est introuvable."""
    for chemin in (SKILL, AGENTS / "thomas.md"):
        texte = corps(chemin)
        assert "fait partie de" in texte and "ne la propose pas" in texte, chemin.name
        assert "60/100" in texte, chemin.name
    strategie = (SKILL.parent / "reference" / "strategie.md").read_text(encoding="utf-8")
    assert "ne dépasse pas **60**" in strategie
