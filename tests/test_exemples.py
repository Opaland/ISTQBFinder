"""docs/exemples-conversations.md : chaque exemple est tiré d'une sortie réelle versionnée
et reste d'accord avec elle (#47, #91, #159)."""
import json
import re

import pytest

from conftest import RACINE_CODE

EXEMPLES = (RACINE_CODE / "docs" / "exemples-conversations.md").read_text(encoding="utf-8")
SECTIONS = {m.group(1): m.group(2) for m in
            re.finditer(r"^## (\d)\. (.*?)(?=^## \d\. |\Z)", EXEMPLES, re.M | re.S)}
SORTIE_CLI = "eval/sorties-cli/2026-10-22/exemples-cli.md"


def normaliser(texte):
    return re.sub(r"\s+", " ", texte).strip()


def sources(section):
    """Fichiers versionnés cités par la section (hors essais « avant correctif »)."""
    chemins = sorted(set(re.findall(r"`(eval/[^`]+\.md)`", section)))
    return [c for c in chemins if "avant-correctif" not in c]


def texte_sources(section):
    return normaliser("\n".join((RACINE_CODE / c).read_text(encoding="utf-8")
                                for c in sources(section)))


def blocs_reponse(section):
    """Réponses d'agent : citations « > **Thomas** : … » jusqu'à la fin de la citation."""
    blocs = re.findall(r"^> \*\*(?:Thomas|Sylvie)\*\* : .*?(?=^(?!>)|\Z)", section, re.M | re.S)
    return [re.sub(r"^> ?", "", b, flags=re.M).split(" : ", 1)[1] for b in blocs]


def fragments(texte):
    """Morceaux non coupés d'un extrait : « […] », « … » et fins de ligne les séparent."""
    for ligne in texte.splitlines():
        for morceau in re.split(r"\[…\]|…", ligne):
            morceau = morceau.strip()
            if len(morceau) >= 12 and not re.fullmatch(r"[|\s-]+", morceau):
                yield morceau


def lignes_cli(section):
    """Lignes des blocs ```text : commandes et sorties, sans heredoc ni étiquettes."""
    for bloc in re.findall(r"```text\n(.*?)```", section, re.S):
        dans_heredoc = False
        for ligne in bloc.splitlines():
            if dans_heredoc:
                dans_heredoc = ligne != "JSON"
                continue
            if ligne.endswith("<<'JSON'"):
                dans_heredoc = True
                ligne = ligne[: -len(" <<'JSON'")]
            if ligne.strip() in ("", "…") or ligne.endswith(" :"):
                continue
            yield ligne


def test_toutes_les_sections_citent_une_sortie_versionnee():
    assert set(SECTIONS) == set("123456789")
    for numero, section in SECTIONS.items():
        assert sources(section), f"§{numero} sans sortie réelle citée"
        for chemin in sources(section):
            assert (RACINE_CODE / chemin).exists(), chemin


@pytest.mark.parametrize("numero", sorted(SECTIONS))
def test_extraits_d_agent_non_retouches(numero):
    section = SECTIONS[numero]
    reference = texte_sources(section)
    for bloc in blocs_reponse(section):
        for morceau in fragments(bloc):
            assert normaliser(morceau) in reference, f"§{numero} : « {morceau} » absent de {sources(section)}"


@pytest.mark.parametrize("numero", sorted(SECTIONS))
def test_commandes_et_sorties_cli_reelles(numero):
    section = SECTIONS[numero]
    reference = texte_sources(section)
    for ligne in lignes_cli(section):
        for morceau in fragments(ligne):
            assert normaliser(morceau.removeprefix("$ ")) in reference, f"§{numero} : {ligne}"


@pytest.mark.parametrize("numero", sorted(SECTIONS))
def test_chiffres_de_l_essai_cite(numero):
    """Tours, coût, citations et confiance : ceux du fichier cité, pas des chiffres figés."""
    section = SECTIONS[numero]
    for chemin in sources(section):
        if not chemin.startswith("eval/essais-resultats/"):
            continue
        entete = (RACINE_CODE / chemin).read_text(encoding="utf-8")
        tours = re.search(r"\*\*Tours\*\* : (\d+)", entete).group(1)
        cout = re.search(r"\*\*coût\*\* : ([\d.]+) \$", entete).group(1).replace(".", ",")
        citations = re.search(r"\*\*citations\*\* : (\d+/\d+) lues", entete).group(1)
        confiance = re.search(r"\*\*confiance annoncée\*\* : (\d+)", entete).group(1)
        for attendu in (f"{tours} tours", f"{cout} $", f"{citations} citations",
                        f"Confiance : {confiance}/100"):
            assert attendu in normaliser(section), f"§{numero} ({chemin}) : « {attendu} » attendu"


def test_exemple_1_est_une_sortie_reelle_de_mise_en_place():
    """#91 : l'exemple 1 (RBT en agile) vient d'un essai réel au format « mise en place »."""
    assert "eval/essais-resultats/2026-10-22/M1-rbt-agile.md" in SECTIONS["1"]
    for attendu in ("Méthode pas à pas", "fictif, interprétation", "Adaptation par domaine",
                    "Questions à choix", "Par quoi je commencerais"):
        assert attendu in SECTIONS["1"], attendu


def test_capitalisation_rejouee_identifiants_reels_et_contexte_anonyme():
    """#159 : identifiants QA-AAAAMMJJ-xxxx de la sortie rejouée, contexte anonymisé."""
    assert "QA-0001" not in EXEMPLES
    for numero in "34":
        assert SORTIE_CLI in SECTIONS[numero]
    sortie = (RACINE_CODE / SORTIE_CLI).read_text(encoding="utf-8")
    cree = re.search(r"Idée créée : (QA-\d{8}-[0-9a-f]{4})", sortie).group(1)
    assert set(re.findall(r"QA-\d[\w-]*", EXEMPLES)) == {cree}
    # Le JSON montré est celui réellement passé à `idee ajouter`.
    montre = json.loads(re.search(r"```json\n(.*?)```", SECTIONS["3"], re.S).group(1))
    passe = json.loads(re.search(r"\$ python qa\.py idee ajouter\n\(entrée standard : (.*)\)\n"
                                 r"Idée créée", sortie).group(1))
    assert montre == passe
    for nominatif in ("Release 3.2", "release 3.2", "équipe paiement"):
        assert nominatif not in EXEMPLES


def test_couches_citees_au_paragraphe_3_1_3():
    # #47 : la superposition en couches du TAF est au §3.1.3, pas aux §4.3 / §3.1.5.
    for m in re.finditer(r"[Cc]ouches[^\[]{0,200}\[([^\]]+)\]", EXEMPLES):
        assert "§3.1.3" in m.group(1), m.group(0)
