"""Mesure de la reformulation par l'agent (scripts/mesure_reformulation.py, #151).

Les fonctions pures (consigne lue dans le skill, lecture de la réponse du modèle, fusion RRF,
choix des questions d'un jeu) se vérifient sans lancer la CLI `claude`."""
import importlib.util

from conftest import RACINE_CODE as RACINE

_spec = importlib.util.spec_from_file_location("mesure_reformulation", RACINE / "scripts" / "mesure_reformulation.py")
mesure = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mesure)


def test_consigne_lue_dans_le_skill_sans_deborder():
    texte = mesure.consigne()
    assert texte.startswith("**Reformuler avant de chercher**") and "anglais" in texte
    assert "Lire avant de citer" not in texte  # s'arrête avant l'étape suivante
    faux = "2. **Syllabus** : x\n   **Reformuler avant de chercher** : a\n   b\n3. **Lire** : c\n"
    assert mesure.consigne(faux) == "**Reformuler avant de chercher** : a b"


def test_lire_reponse_tolere_texte_autour_et_questions_manquantes():
    reponse = 'Voici :\n```json\n{"1": ["exit criteria", " ", "critères de sortie"], "3": ["a", "b", "c", "d"]}\n```'
    assert mesure.lire_reponse(reponse, 3) == [["exit criteria", "critères de sortie"], [], ["a", "b", "c"]]
    assert mesure.lire_reponse("pas de JSON", 2) == [[], []]


def test_fusion_rrf_garde_le_budget_et_favorise_l_accord():
    a, b, c, d = ({"id": i} for i in "abcd")
    fus = mesure.fusion_rrf([[a, b, c], [b, d], [b, a]], n=2)
    assert [r["id"] for r in fus] == ["b", "a"]
    assert len(mesure.fusion_rrf([[a, b, c, d]] * 3, n=5)) == 4


def test_rang_section_prefixe():
    res = [{"code": "CTFL", "section_num": "4.2"}, {"code": "CTFL", "section_num": "5.1.3"}]
    assert mesure.rang(res, [{"code": "CTFL", "section": "5.1"}]) == 2
    assert mesure.rang(res, [{"code": "CTAL-TM", "section": "5.1"}]) is None


def test_cas_des_jeux_disjoints():
    eloigne, controle, reglage = (mesure.cas_du_jeu(n) for n in ("eloigne", "controle", "reglage"))
    assert len(eloigne) >= 20 and all(c.get("eloigne") for c in eloigne)
    assert not {c["requete"] for c in controle} & {c["requete"] for c in reglage}
    assert len(mesure.cas_du_jeu("examens")) >= 100
