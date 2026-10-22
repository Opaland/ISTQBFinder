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


def outils(valeur: str) -> set:
    return {o.strip() for o in valeur.split(",") if o.strip()}


def test_agents_sans_skill_et_sans_ecriture():
    """#23 : le skill est préchargé (pas d'outil Skill) ; aucun agent n'écrit de fichier."""
    thomas = frontmatter(AGENTS / "thomas.md")
    sylvie = frontmatter(AGENTS / "sylvie.md")
    assert outils(thomas["tools"]) == {"Bash", "Read", "WebSearch", "WebFetch", "AskUserQuestion"}
    assert outils(sylvie["tools"]) == {"Bash", "Read", "AskUserQuestion"}
    assert {"Write", "Edit"} <= outils(thomas["disallowedTools"])
    assert {"Write", "Edit", "WebSearch", "WebFetch"} <= outils(sylvie["disallowedTools"])


@pytest.mark.parametrize("nom", ["thomas", "sylvie"])
def test_agents_savent_qu_ils_sont_sous_agents(nom):
    texte = corps(AGENTS / f"{nom}.md")
    assert "déjà chargé" in texte and "ne l'invoque pas" in texte
    assert "sous-agent" in texte and "ni poser de question" in texte
    assert "JSON" in texte and "prêt à l'emploi" in texte


def test_sylvie_n_ajoute_aucune_pratique_et_rend_seulement_ses_questions():
    texte = corps(AGENTS / "sylvie.md")
    assert "aucune pratique déduite ou ajoutée" in texte
    assert "**seulement** 2-3 questions" in texte


def test_capitalisation_par_entree_standard():
    """#23 : pas de fichier temporaire idee.json dans les procédures."""
    for chemin in (SKILL, SKILL.parent / "reference" / "capitalisation.md",
                   RACINE / "docs" / "exemples-conversations.md", AGENTS / "thomas.md"):
        texte = chemin.read_text(encoding="utf-8")
        assert "--fichier idee.json" not in texte and "--fichier <json>" not in texte, chemin.name
    capitalisation = (SKILL.parent / "reference" / "capitalisation.md").read_text(encoding="utf-8")
    assert "idee ajouter <<'JSON'" in capitalisation
    # #128 : `idee doublons` en une ligne, sans JSON (heredoc JSON bloqué en `claude -p`).
    assert "idee doublons <<" not in capitalisation and "idee doublons --titre" in capitalisation


def test_web_obligatoire_pour_un_outil_absent_des_syllabus():
    """#49 : la recherche Web est faite (pas proposée) quand l'outil nommé est introuvable."""
    for chemin in (SKILL, AGENTS / "thomas.md"):
        texte = corps(chemin)
        assert "fait partie de" in texte and "ne la propose pas" in texte, chemin.name
        assert "60/100" in texte, chemin.name
    strategie = (SKILL.parent / "reference" / "strategie.md").read_text(encoding="utf-8")
    assert "ne dépasse pas **60**" in strategie


def test_contexte_projet_et_par_quoi_je_commencerais():
    """#31 : contexte utilisé ou signalé comme hypothèse ; pistes classées impact / effort."""
    strategie = (SKILL.parent / "reference" / "strategie.md").read_text(encoding="utf-8")
    for texte in (corps(SKILL), strategie, corps(AGENTS / "thomas.md")):
        assert "Par quoi je commencerais" in texte and "impact / effort" in texte
        assert "questions de cadrage" in texte
    assert "Hypothèse de contexte" in strategie


def test_exemples_contiennent_un_extrait_reel_de_thomas_et_de_sylvie():
    exemples = (RACINE / "docs" / "exemples-conversations.md").read_text(encoding="utf-8")
    assert "> **Thomas** :" in exemples and "> **Sylvie** :" in exemples
    assert "eval/essais-resultats/2026-10-22/" in exemples
    assert (RACINE / "eval" / "essais-resultats" / "2026-10-22" / "S1-rbt.md").exists()


def test_gabarit_mise_en_place():
    """#90 : une question « comment mettre en place » reçoit méthode, exemple, domaines."""
    strategie = (SKILL.parent / "reference" / "strategie.md").read_text(encoding="utf-8")
    gabarit = strategie.split("## Format « mise en place »", 1)[1].split("## Score de confiance", 1)[0]
    for attendu in ("Méthode pas à pas", "Exemple de mise en œuvre", "fictif", "interprétation",
                    "Adaptation par domaine", "Questions de cadrage", "Où creuser ensuite",
                    "Confiance : NN/100"):
        assert attendu in gabarit, attendu
    for domaine in ("Santé / réglementé", "Web", "embarqué", "Mobile", "API"):
        assert domaine.lower() in gabarit.lower(), domaine
    # Les domaines sans syllabus dédié sont signalés honnêtement.
    assert "Pas de syllabus santé" in gabarit and "Pas de syllabus web dédié" in gabarit
    assert "M — mise en place" in strategie
    for chemin in (SKILL, AGENTS / "thomas.md"):
        texte = corps(chemin)
        assert "mise en place" in texte and "interprétation" in texte, chemin.name
    thomas = corps(AGENTS / "thomas.md")
    assert "méthode pas à pas" in thomas and "adaptation par domaine" in thomas


def test_gabarit_mise_en_place_renvoie_a_des_syllabus_presents():
    """#90 : les codes cités dans le tableau des domaines existent dans le catalogue."""
    import json
    import re
    strategie = (SKILL.parent / "reference" / "strategie.md").read_text(encoding="utf-8")
    gabarit = strategie.split("## Format « mise en place »", 1)[1].split("## Score de confiance", 1)[0]
    catalogue = json.loads((RACINE / "catalogue" / "istqb.json").read_text(encoding="utf-8"))
    connus = set(re.findall(r'"code"\s*:\s*"([^"]+)"', json.dumps(catalogue)))
    cites = set(re.findall(r"\b(CT(?:FL|AL|EL)?-[A-Za-z]+(?:-[A-Za-z]+)?)\b", gabarit))
    assert cites, "aucun syllabus cité"
    assert cites <= connus, cites - connus


def test_mode_conversationnel():
    """#92 : questions à choix, plan de recherche montré, suites dont /ajouter-syllabus,
    jamais bloquant hors session interactive ; AskUserQuestion déclaré partout."""
    conversation = (SKILL.parent / "reference" / "conversation.md").read_text(encoding="utf-8")
    for attendu in ("AskUserQuestion", "liste numérotée", "Ne jamais bloquer", "Hypothèse :",
                    "Plan de recherche", "langue", "version", "/ajouter-syllabus",
                    "manquants --langue fr", "3 options au plus", "Ne pas questionner une question claire"):
        assert attendu in conversation, attendu
    assert "reference/conversation.md" in corps(SKILL)
    assert "AskUserQuestion" in frontmatter(SKILL)["allowed-tools"]
    for nom in ("thomas", "sylvie"):
        texte = corps(AGENTS / f"{nom}.md")
        assert "Questions à choix" in texte and "AskUserQuestion" in texte, nom
        assert "/ajouter-syllabus" in texte, nom
    assert "Hypothèse : " in corps(AGENTS / "thomas.md")
