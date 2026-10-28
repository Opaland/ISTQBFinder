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
                "--non-couvert", "--autorite"):
        assert opt in grille


# Jeu de cas tiré de l'étude par personas du 2026-10-28 (#226) : entrées de `confiance`
# relevées dans les réponses (tableau de #226) → bande attendue.
# « autorite » : la section qui fait autorité sur la notion (syllabus dédié, titre qui la
# nomme) a été lue en entier ; l'exemple qui applique directement la définition lue n'est
# pas un « raisonnement sans source ».
CAS_DEFINITION = [
    pytest.param(dict(base=70, lus=1, concordants=1, autorite=True), "élevée",
                 id="P2b valeurs limites 18-65, CTFL §4.2.2 lue en entier"),
    pytest.param(dict(base=70, lus=1, concordants=1, autorite=True, raisonnement=True), "moyenne",
                 id="P2b, avec une partie réellement sans source"),
    pytest.param(dict(base=84, lus=1, concordants=1, autorite=True), "élevée",
                 id="P2a erreur / défaut / défaillance, CTFL §1.2.3"),
    pytest.param(dict(base=70, lus=2, concordants=1, autorite=True, raisonnement=True), "moyenne",
                 id="P2c table de décision / transitions, CTFL §4.2.3-4.2.4, critère de choix raisonné"),
    pytest.param(dict(base=97, lus=5, concordants=1, autorite=True, raisonnement=True), "élevée",
                 id="P5b TAA et couches, CTAL-TAE §3.1.1-3.1.5"),
]
# Questions larges ou sans section qui fait autorité : score inchangé, au point près.
CAS_INCHANGES = [
    pytest.param(dict(base=79, lus=6, concordants=3), 87, id="P3c rôle du testeur, 3 syllabus"),
    pytest.param(dict(base=85, lus=5, concordants=2), 81, id="P1a plan de test"),
    pytest.param(dict(base=82, lus=8, concordants=3, web=True, raisonnement=True), 69, id="P5a pyramide, flaky"),
    pytest.param(dict(base=75, lus=4, concordants=4, raisonnement=True, non_couvert=True), 60,
                 id="P6b bugs du vendredi, notion non couverte"),
    pytest.param(dict(base=70, lus=1, concordants=1, raisonnement=True), 42,
                 id="P2b tel que calculé, autorité non revendiquée"),
]


@pytest.mark.parametrize("entrees, bande", CAS_DEFINITION)
def test_question_de_definition_sourcee_par_la_section_qui_fait_autorite(entrees, bande):
    assert confiance.calculer(**entrees)["libelle"] == bande


@pytest.mark.parametrize("entrees, score", CAS_INCHANGES)
def test_questions_larges_inchangees(entrees, score):
    assert confiance.calculer(**entrees)["score"] == score


def test_autorite_ne_leve_pas_le_plafond_et_exige_une_lecture():
    assert confiance.calculer(90, 1, 1, autorite=True, non_couvert=True)["score"] == confiance.PLAFOND_NON_COUVERT
    with pytest.raises(ValueError, match="autorit"):
        confiance.calculer(90, 0, 0, autorite=True)
    assert "section de référence lue" in "\n".join(confiance.calculer(70, 1, 1, autorite=True)["calcul"])
