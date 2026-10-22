"""Score de confiance déterministe (issue #18) : `qa.py confiance` et grille du skill."""
import re

import pytest

from conftest import RACINE_CODE
from qak import confiance
from qak.cli import main


def test_calcul_deterministe_et_detaille():
    r = confiance.calculer(79, lus=3, concordants=2, web=True)
    assert (r["score"], r["libelle"]) == (47 + 20 + 10 - 10, "moyenne")
    assert any("× 0.6" in l for l in r["calcul"]) and any("-10" in l for l in r["calcul"])
    assert confiance.calculer(100, 0, 0)["score"] == 60  # sans lecture : jamais « élevée »
    assert confiance.calculer(100, 1, 1)["score"] == 70
    assert confiance.calculer(100, 5, 4)["score"] == 100
    assert confiance.calculer(10, 0, 0, ancien=True, contradiction=True, web=True, raisonnement=True)["score"] == 0


def test_plafond_si_une_notion_n_est_couverte_ni_par_la_lecture_ni_par_le_web():
    r = confiance.calculer(100, 4, 3, non_couvert=True)
    assert r["score"] == confiance.PLAFOND_NON_COUVERT and "plafond" in r["calcul"][-1]
    assert confiance.calculer(20, 0, 0, non_couvert=True)["score"] == 12  # sous le plafond : inchangé


@pytest.mark.parametrize("args", [(101, 1, 0), (50, -1, 0), (50, 1, 2)])
def test_entrees_incoherentes_refusees(args):
    with pytest.raises(ValueError):
        confiance.calculer(*args)


def test_commande_confiance(capsys):
    assert main(["confiance", "--base", "79", "--lus", "3", "--concordants", "2", "--web", "1"]) == 0
    sortie = capsys.readouterr().out
    assert "Confiance : 67/100 (moyenne)" in sortie and "total borné" in sortie
    assert main(["confiance", "--base", "50", "--lus", "1", "--concordants", "2"]) == 2
    assert "ne peut dépasser" in capsys.readouterr().err


def test_grille_du_skill_identique_au_code():
    # SKILL.md est le seul texte préchargé chez les agents : sa grille doit être celle du code.
    skill = (RACINE_CODE / ".claude" / "skills" / "qa-knowledge" / "SKILL.md").read_text(encoding="utf-8")
    grille = skill[skill.index("## Score de confiance"):]
    assert "× 0,6" in grille and confiance.PART_BASE == 0.6
    assert f"plafond {confiance.PLAFOND_NON_COUVERT}" in grille
    assert "1 → +10 · ≥ 2 → +20" in grille and (confiance.BONUS_LUS[1], confiance.BONUS_LUS_MAX) == (10, 20)
    assert "2 → +10 · ≥ 3 → +20" in grille and (confiance.BONUS_CONCORDANTS[2], confiance.BONUS_CONCORDANTS_MAX) == (10, 20)
    malus = sorted(int(m) for m in re.findall(r"− (\d+)", grille))
    assert malus == sorted(v for v, _ in confiance.MALUS.values())
    for opt in ("--base", "--lus", "--concordants", "--ancien", "--contradiction", "--web", "--raisonnement",
                "--non-couvert"):
        assert opt in grille
