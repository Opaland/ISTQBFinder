"""Critères automatiques des essais de bout en bout (scripts/essais_agents.py, #91).

`controler()` est une fonction pure : on la vérifie sur des réponses écrites à la main,
sans lancer la CLI `claude`."""
import importlib.util
import json

import pytest
from conftest import RACINE_CODE as RACINE

_spec = importlib.util.spec_from_file_location("essais_agents", RACINE / "scripts" / "essais_agents.py")
essais_agents = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(essais_agents)

BONNE = """Hypothèse de contexte : équipe Scrum, domaine non précisé.

**Méthode pas à pas**
1. Identifier les risques en planification de release — PO + équipe [CTFL-AT 2014 EN, §3.2.1, p. 32]
2. Évaluer probabilité × impact en planification d'itération [CTFL-AT 2014 EN, §3.2.1, p. 32]
3. Choisir techniques et profondeur par niveau de risque [CTAL-TM v3.0 FR, §1.3.5, p. 33]
4. Mettre les critères dans la DoD (interprétation)
5. Revoir les risques à la rétrospective [CTAL-TA v4.0 FR, §2.2, p. 28]

**Exemple de mise en œuvre** (fictif — interprétation)
Dans une équipe Scrum de 6 personnes…

| Domaine | Ce qui change |
|---|---|
| Santé / réglementé | pas de syllabus santé dans la bibliothèque |
| Web | … |
| Embarqué | … |
| Mobile | CT-MAT |
| API | tests de contrat |

**Confiance : 78/100** (élevée)

**Questions à choix**
1. Quel domaine ? a) santé b) web c) API
2. Quelle taille d'équipe ?
"""


def test_controler_reponse_mise_en_place_complete():
    criteres = {"methode": True, "etapes_sourcees": True, "exemple": True, "cadrage": True,
                "questions_choix": True, "hypotheses": True, "non_couvert": True, "confiance": True,
                "domaines": ["sant[ée]", "web", "embarqu", "mobile", "API"], "mentions": ["contrat"]}
    resultat = essais_agents.controler(BONNE, criteres)
    assert all(resultat.values()), [c for c, ok in resultat.items() if not ok]


@pytest.mark.parametrize("critere, alteration", [
    ("methode", lambda t: t.replace("3. ", "- ").replace("4. ", "- ")),
    ("etapes_sourcees", lambda t: t.replace("(interprétation)", "")),
    ("exemple", lambda t: t.replace("(fictif — interprétation)", "")),
    ("questions_choix", lambda t: t.split("**Questions à choix**")[0]),
    ("hypotheses", lambda t: t.replace("Hypothèse de contexte :", "Contexte")),
    ("non_couvert", lambda t: t.replace("pas de syllabus santé dans la bibliothèque", "IEC 62304")),
    ("confiance", lambda t: t.replace("**Confiance : 78/100**", "")),
    ("domaines:API", lambda t: t.replace("API", "")),
])
def test_controler_detecte_chaque_manque(critere, alteration):
    criteres = {"methode": True, "etapes_sourcees": True, "exemple": True, "questions_choix": True,
                "hypotheses": True, "non_couvert": True, "confiance": True, "domaines": ["API"]}
    resultat = essais_agents.controler(alteration(BONNE), criteres)
    assert resultat[critere] is False


def test_essais_par_domaine_presents():
    """#91 : les questions de mise en place couvrent les domaines demandés, avec critères."""
    essais = {e["id"]: e for e in json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]}
    for ident in ("M1-rbt-agile", "M2-sante", "M3-web", "M4-embarque", "M5-mobile", "M6-api",
                  "S3-reglemente", "C1-ambigu"):
        assert ident in essais and essais[ident].get("criteres"), ident
    assert set(essais["M1-rbt-agile"]["criteres"]["domaines"]) >= {"web", "mobile", "API"}
    assert essais["C1-ambigu"]["criteres"]["questions_choix"] and "agent" not in essais["C1-ambigu"]
    # Tous les critères déclarés sont connus de controler().
    connus = {"methode", "etapes_sourcees", "exemple", "cadrage", "questions_choix", "hypotheses",
              "non_couvert", "confiance", "domaines", "mentions"}
    for e in essais.values():
        assert set(e.get("criteres", {})) <= connus, e["id"]
