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


def test_citation_non_lue_fait_echouer_l_essai():
    """#127 : une citation dont la page n'a pas été lue n'est plus un simple indicateur."""
    lues = {("CTAL-TM", 29)}
    reponse = "Pistes [CTAL-TM v3.0 FR, §1.3.2, p. 29] et [CTAL-TAE v2.0 EN, §4.2.1, p. 32]."
    citations = essais_agents.verifier_citations(reponse, lues)
    bilan = {"citations": citations, "citations_non_lues": [c["citation"] for c in citations if not c["lue"]],
             "criteres_ko": []}
    motifs = essais_agents.motifs_echec(bilan)
    assert len(motifs) == 1 and "CTAL-TAE" in motifs[0]
    assert essais_agents.motifs_echec({"citations_non_lues": [], "criteres_ko": []}) == []
    assert essais_agents.motifs_echec({"erreur": "x"}) == ["erreur d'exécution"]


def test_consigne_controle_avant_d_envoyer():
    """#127 : liste de contrôle des références avant la réponse finale (skill et agents)."""
    from test_agents import AGENTS, SKILL, corps
    assert "Contrôle avant d'envoyer" in corps(SKILL) and "retire la" in corps(SKILL)
    for nom in ("thomas", "sylvie"):
        assert "contrôle avant" in corps(AGENTS / f"{nom}.md"), nom


# Extrait réel : eval/essais-resultats/2026-10-22/S1-rbt.md (Sylvie, relance sur a9ddcd7).
S1_RBT = """| **P2** Tester d'abord | Intention | Aligné | … | [CTAL-TM v3.0 FR, §1.3, p. 29 ; §1.3.1, p. 29 ; §1.3.4, p. 32] |

## Confiance : 72/100

- **Ce qui l'appuie :** j'ai lu le §1.3 de CTAL-TM v3.0 FR (sous-sections 1.3.1 à 1.3.4 et 1.3.6), version courante. Il est cohérent avec les passages de CTAL-TA v4.0 vus en recherche.
- **Ce qui la limite :** je n'ai pas lu la §1.3.5 (p. 33). Je n'ai pas non plus consulté le contexte agile de la release, ni CTAL-TA §2 ni CTFL §5.2. Le niveau dépend entièrement de ce que tu m'as décrit.

## Limites

- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable ici.

## Traçabilité

- **Document lu :** `CTAL-TM-3.0-fr`, ISTQB Advanced Level Test Management, v3.0 (2024-03-28)
- **Requête `chercher` :** `"risk-based testing" identification évaluation atténuation`. Le résultat CTAL-TA §2 (p. 26-27) ne figure qu'en extrait et n'est donc pas cité.
"""


def test_reference_declaree_non_lue_n_est_pas_une_citation():
    """#139 : « je n'ai pas lu la §1.3.5 (p. 33) » et « … n'est donc pas cité » dans les
    sections de bilan ne sont pas des citations non lues (faux positif sur S1-rbt)."""
    citations = essais_agents.verifier_citations(S1_RBT, {("CTAL-TM", 29), ("CTAL-TM", 32)})
    assert citations and all(c["lue"] for c in citations), citations
    assert not any("CTAL-TA" in c["citation"] or "33" in c["citation"] for c in citations)


@pytest.mark.parametrize("reponse", [
    # Dans la réponse elle-même, une négation n'excuse rien : contrôle strict.
    "## Pratiques\n\nLe §1.3.5, que je n'ai pas lu, impose ceci [CTAL-TM v3.0 FR, §1.3.5, p. 33].",
    # Dans une section de bilan, une vraie citation (sans déclaration de non-lecture) compte.
    "## Limites\n\nLe syllabus exclut ce cas [CTAL-TM v3.0 FR, §1.3.5, p. 33].",
    "## Traçabilité\n\n- Document lu : CTAL-TM v3.0 FR. Sections lues : §1.3.5 (p. 33).\n",
])
def test_controle_strict_hors_declaration_de_non_lecture(reponse):
    citations = essais_agents.verifier_citations(reponse, {("CTAL-TM", 29)})
    assert [c["lue"] for c in citations] == [False], citations
