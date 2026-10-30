#!/usr/bin/env python3
"""Essais de bout en bout : pose les questions de eval/essais.json aux agents (Thomas,
Sylvie) via `claude -p`, puis contrôle automatiquement chaque réponse.

    python scripts/essais_agents.py                 # tous les essais
    python scripts/essais_agents.py T1-couverture S1-rbt   # seulement ces identifiants
    python scripts/essais_agents.py M                       # préfixe : tous les essais M…
    python scripts/essais_agents.py --fidelite S1-rbt       # + contrôle de fond de fidélité (#152)

Prérequis : CLI `claude` connectée, index construit (`python qa.py actualiser`).
Les essais tournent avec les permissions réelles du dépôt (règles `allow` de
`.claude/settings.json`, aucune écriture pré-approuvée) sur une COPIE temporaire des
données (`QAK_RACINE`) : la base d'idées et le journal versionnés ne bougent pas (#157).
Coût indicatif : 0,10 à 0,50 $ par question. Résultats : eval/essais-resultats/<date>/.

Contrôles automatiques (le jugement de fond reste humain, voir docs/essais-reponses.md) ;
un essai ÉCHOUE (code retour 1) dès qu'une citation n'a pas été lue ou qu'un critère
manque (#127) :
- commandes `qa.py` réellement exécutées par l'agent (lues dans le transcript) ;
- citations `[DOC …, §x.y, p. N]` : la page N du document a-t-elle été LUE pendant la
  conversation (présente dans la sortie d'un `lire`, `section` ou `page`), dans ce document
  (sigle, version et langue, #280) ? Une référence
  que l'agent déclare lui-même non lue, non citée ou lue en partie dans « Confiance »,
  « Limites », « Traçabilité » ou « Sources retenues » n'est pas une citation (#139, #181) ;
- présence d'un score de confiance « Confiance : NN/100 » ;
- recours au Web ;
- sur tout essai : un bloc JSON d'idée exige `qa.py idee modele` parmi les commandes (#264) ;
  une confiance annoncée exige `qa.py confiance --base …` parmi les commandes et son
  calcul « base N × 0,6 » recopié (#262) ;
- critères propres à l'essai (`"criteres"` dans eval/essais.json, voir `controler()`) :
  méthode en étapes, étapes sourcées, exemple fictif, domaines, questions de cadrage ou à
  choix, hypothèses explicites, couverture absente signalée, mentions attendues.

Contrôle de fond OPTIONNEL `--fidelite` (#152) : chaque citation lue est jugée par un juge
LLM (méthode RAGAS faithfulness, `scripts/etude_juge.py`) contre le texte de la page lue
pendant la conversation : chaque ligne qui porte des citations est-elle soutenue par les
pages qu'elle cite ? Indicateur seulement (score de fidélité moyen et lignes jugées
contradictoires dans le bilan, jamais un échec) : le juge est de la même famille de
modèle que l'agent (biais d'auto-évaluation), étalonnage dans docs/architecture.md.
Coût : ≈ 0,03 $ par ligne citée, en plus de l'essai.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import commun  # noqa: E402
import etude_juge  # noqa: E402
from qak import citations as regle_citations  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
# Outils hors Bash dont les agents ont besoin (lecture, skill, Web) ; les commandes Bash
# viennent toutes des règles `allow` du dépôt, rien de plus (#157).
OUTILS_HORS_BASH = ["Read", "Skill", "WebSearch", "WebFetch"]


def outils_autorises(reglages: Path = RACINE / ".claude" / "settings.json") -> list[str]:
    """`--allowedTools` des essais : les règles `allow` de `.claude/settings.json` (celles
    qu'un utilisateur a réellement), plus les outils hors Bash. Aucune règle ajoutée."""
    allow = json.loads(reglages.read_text(encoding="utf-8"))["permissions"]["allow"]
    return [*allow, *(o for o in OUTILS_HORS_BASH if o not in allow)]


def autorise(commande: str, outils: list[str]) -> bool:
    """La commande Bash est-elle pré-approuvée par une règle `Bash(préfixe:*)` ou `Bash(cmd)` ?"""
    for regle in outils:
        if not (regle.startswith("Bash(") and regle.endswith(")")):
            continue
        motif = regle[5:-1]
        if motif.endswith(":*") and (commande == motif[:-2] or commande.startswith(motif[:-2] + " ")):
            return True
        if commande == motif:
            return True
    return False


# Copiés dans la racine temporaire des essais : une écriture de l'agent n'atteint pas le dépôt (#157).
FICHIERS_ESSAIS = ("bibliotheque/index.db", "bibliotheque/manifeste.json", "bibliotheque/vecteurs.npz",
                   "connaissances/connaissances.jsonl", "connaissances/journal.jsonl",
                   "referentiel/taxonomie.json", "referentiel/thesaurus.json")


def racine_temporaire(source: Path = RACINE) -> Path:
    """Copie de travail des données (index, manifeste, base d'idées, journal, référentiels)
    pour `QAK_RACINE` (#157), voir `commun.racine_temporaire()`."""
    return commun.racine_temporaire(source, FICHIERS_ESSAIS, "qak-essais-")


# Une citation = « §x.y … p. N » ou « … pp. N-M » ; elle se rattache au dernier code de
# syllabus nommé avant elle (« **CTFL v4.0.1** … (§4.2.1, p. 40) » comme « [CTAL-TM v3.0,
# §1.3, p. 29] »). Entre « § » et la page, ni « § » ni « ; » : sinon deux références
# voisines fusionnent et la page de la seconde est prêtée à la première (#142).
# Le document cité garde sa version et sa langue quand l'agent les écrit après le sigle
# (« CT-MAT v2019 FR », « CTFL-4.0.1 EN », « CT-ATLaS BoK v2.0 FR ») (#280) ; langue en
# majuscules seulement : « le CTFL en parle » ne nomme pas une langue.
RE_JETON = re.compile(r"(?P<code>\b(?:CTFL(?:-AT)?|CTAL-[A-Za-z]+|CTEL-[A-Za-z]+|CT-[A-Za-z]+)\b"
                      r"(?:[ -]BoK\b)?(?:[ -]v?\d+(?:\.\d+)*\b)?(?:[ -](?:EN|FR)\b)?)"
                      r"|(?P<ref>§\s?[\d.]+[^\n\]\)§;]{0,40}?\bpp?\.\s?(?P<p1>\d+)(?:\s?[-–]\s?(?P<p2>\d+))?)")
RE_CONFIANCE = re.compile(r"[Cc]onfiance\s*:?\s*\**\s*(\d{1,3})\s*/\s*100")
RE_ETAPE = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:[ÉE]tape\s*)?\d+\s*[.)—:-]", re.M)
# Calcul de la confiance recopié de `qa.py confiance` (#227) : « base 70 × 0,6 = 42 ».
RE_CALCUL_CONFIANCE = re.compile(r"\d{1,3}\s*[×x*]\s*0[,.]6\b", re.I)
# Appel réel de l'outil, paramètres compris (`confiance --help` ne calcule rien) (#262).
RE_CMD_CONFIANCE = re.compile(r"qa\.py\s+confiance\b[^;&|\n]*--base")
# Titre « Niveau atteint : N » de Sylvie (#228) : le niveau retenu, sans réserve.
RE_NIVEAU_ATTEINT = re.compile(r"niveau\s+atteint\W{0,6}(\d)(?P<suite>[^\n]*)", re.I)
RE_NIVEAU_RETENU = re.compile(r"(?:je\s+retiens|niveau\s+retenu)\W{0,6}(?:le\s+)?(?:niveau\s+)?(\d)", re.I)
RE_NIVEAU_RESERVE = re.compile(r"non\s+d[ée]montr|provisoire|probable|en\s+partie|partiel", re.I)
# Phrase de déroulé en tête de réponse (#232) : « Je finalise le rapport… », « J'ai fini de lire… ».
RE_DEROULE = re.compile(r"^\W*(?:je\s+(?:finalise|r[ée]dige|termine|rends|n['’]ai\s+plus)"
                        r"|j['’]ai\s+(?:fini|termin[ée]|maintenant)|voici\s+(?:l['’]avis|le\s+rapport|ma\s+r[ée]ponse))", re.I)
# Bloc JSON d'idée proposé « À capitaliser » (#264) : il exige `idee modele` dans la session.
RE_BLOC_IDEE = re.compile(r"```(?:json)?\s*\n[^`]*?\"titre\"\s*:", re.I)
RE_IDEE_MODELE = re.compile(r"qa\.py\s+idee\s+modele\b")
RE_NON_COUVERT = re.compile(r"pas de syllabus|aucun syllabus|ne couvre pas|non couvert|absente? de la biblioth|"
                            r"n'est pas dans la biblioth|pas dans la biblioth|hors biblioth", re.I)


def _apres(texte: str, motif: str) -> str:
    """Texte qui suit la première occurrence de `motif` (vide si absent)."""
    m = re.search(motif, texte, re.I)
    return texte[m.end():] if m else ""


def niveau_coherent(reponse: str) -> bool:
    """#228 : chaque « Niveau atteint : N » donne le même N, sans réserve (« provisoire »,
    « non démontré »…) avant « niveau visé », et « je retiens le niveau M » dit M = N."""
    atteints = list(RE_NIVEAU_ATTEINT.finditer(reponse))
    if not atteints:
        return False
    niveaux = {m.group(1) for m in atteints} | {m.group(1) for m in RE_NIVEAU_RETENU.finditer(reponse)}
    # Le titre seul : jusqu'à « niveau visé » ou la fin de la première phrase.
    reserve = any(RE_NIVEAU_RESERVE.search(re.split(r"niveau\s+vis[ée]|\.(?:\*\*)?\s", m.group("suite"),
                                                    maxsplit=1, flags=re.I)[0][:100])
                  for m in atteints)
    return len(niveaux) == 1 and not reserve


def controler(reponse: str, criteres: dict, commandes: list[str] | None = None) -> dict[str, bool]:
    """Critères vérifiables d'un essai (fonction pure, testée sans réseau). Clés :
    methode (≥ 4 étapes numérotées de premier niveau après « Méthode »), etapes_sourcees
    (chaque étape, sous-puces comprises, porte « § » ou « interprétation »), exemple (exemple marqué fictif / interprétation),
    domaines et mentions (listes de motifs, tous présents), cadrage, questions_choix
    (« Questions à choix » suivi d'au moins 2 options numérotées), hypotheses,
    non_couvert (absence de syllabus dédié dite franchement), confiance, calcul_confiance
    (le calcul « base N × 0,6 » de `qa.py confiance` est recopié, #227), niveau_coherent
    (« Niveau atteint : N » porte le niveau retenu, sans réserve ni second chiffre, #228),
    debut_direct (la première ligne n'est pas une phrase de déroulé, #232) et en_tete
    (Sylvie : la première ligne est l'en-tête « Avis indicatif… », #232).
    Avec `commandes` (commandes exécutées, lues dans le transcript), critères posés sur TOUT
    essai : json_apres_idee_modele (un bloc JSON d'idée exige `qa.py idee modele` parmi
    les commandes, #264) et calcul_confiance dès qu'une confiance est annoncée (calcul
    recopié ET `qa.py confiance --base …` parmi les commandes, #262)."""
    out = {}
    methode = _apres(reponse, r"m[ée]thode")
    # La méthode s'arrête au titre de l'exemple (« ## Exemple… », « **Exemple… »), pas à un
    # « par exemple » dans une étape.
    methode = re.split(r"\n(?:#+\s*|\*\*)exemple", methode, maxsplit=1, flags=re.I)[0]
    # Étape = ligne numérotée de premier niveau + ses sous-puces (source souvent en dessous).
    etapes, courante = [], None
    for ligne in methode.splitlines():
        if RE_ETAPE.match(ligne) and not ligne.startswith((" ", "\t")):
            courante = [ligne]
            etapes.append(courante)
        elif courante is not None and (ligne.startswith((" ", "\t", "|")) or not ligne.strip()):
            courante.append(ligne)
        else:
            courante = None
    etapes = ["\n".join(e) for e in etapes]
    if criteres.get("methode"):
        out["methode"] = len(etapes) >= 4
    if criteres.get("etapes_sourcees"):
        out["etapes_sourcees"] = bool(etapes) and all(
            "§" in l or re.search(r"interpr[ée]tation|hypoth[èe]se", l, re.I) for l in etapes)
    if criteres.get("exemple"):
        out["exemple"] = bool(re.search(r"exemple[^\n]{0,80}(fictif|interpr[ée]tation)", reponse, re.I))
    for cle in ("domaines", "mentions"):
        for motif in criteres.get(cle, []):
            out[f"{cle}:{motif}"] = bool(re.search(motif, reponse, re.I))
    if criteres.get("cadrage"):
        out["cadrage"] = bool(re.search(r"questions? (de cadrage|à choix)", reponse, re.I))
    if criteres.get("questions_choix"):
        suite = _apres(reponse, r"questions? à choix")
        out["questions_choix"] = len(RE_ETAPE.findall(suite)) + len(re.findall(r"^\s*[-*]\s*[a-c][.)]", suite, re.M)) >= 2
    if criteres.get("hypotheses"):
        out["hypotheses"] = bool(re.search(r"hypoth[èe]se[^\n:]{0,25}:", reponse, re.I))
    if criteres.get("non_couvert"):
        out["non_couvert"] = bool(RE_NON_COUVERT.search(reponse))
    if criteres.get("confiance"):
        out["confiance"] = bool(RE_CONFIANCE.search(reponse))
    if criteres.get("niveau_coherent"):
        out["niveau_coherent"] = niveau_coherent(reponse)
    premiere = next((l for l in reponse.splitlines() if l.strip()), "")
    if criteres.get("debut_direct"):
        out["debut_direct"] = bool(premiere) and not RE_DEROULE.match(premiere)
    if criteres.get("en_tete"):
        out["en_tete"] = "avis indicatif" in premiere.lower()
    # #262 : avec les commandes, toute réponse qui annonce une confiance doit l'avoir fait
    # calculer par `qa.py confiance` ET recopier son calcul (Thomas estimait à la main).
    if criteres.get("calcul_confiance") or (commandes is not None and RE_CONFIANCE.search(reponse)):
        out["calcul_confiance"] = bool(RE_CALCUL_CONFIANCE.search(reponse)) and (
            commandes is None or any(RE_CMD_CONFIANCE.search(c) for c in commandes))
    if commandes is not None and RE_BLOC_IDEE.search(reponse):
        out["json_apres_idee_modele"] = any(RE_IDEE_MODELE.search(c) for c in commandes)
    return out


def transcript(session_id: str) -> list[dict]:
    """Transcript JSONL de la session (dossier projet de Claude Code). L'identifiant est
    imposé par le harnais (`--session-id`) : lancé depuis une session Claude Code, le
    processus enfant hériterait sinon de l'identifiant (et du transcript) du parent."""
    for f in (Path.home() / ".claude" / "projects").glob(f"*/{session_id}.jsonl"):
        return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    return []


def outils_utilises(evenements: list[dict]) -> tuple[list[str], str]:
    commandes, sorties = [], []
    for e in evenements:
        contenu = (e.get("message") or {}).get("content")
        if not isinstance(contenu, list):
            continue
        for c in contenu:
            if c.get("type") == "tool_use":
                commandes.append(c["input"].get("command") or f"{c['name']} {json.dumps(c['input'], ensure_ascii=False)[:120]}")
            elif c.get("type") == "tool_result":
                t = c.get("content")
                sorties.append(t if isinstance(t, str) else json.dumps(t, ensure_ascii=False))
    return commandes, "\n".join(sorties)


# En-tête de passage : « ── DOC · titre · version · p. N [(imprimée M)] · §x.y Titre (passage #id) ».
RE_ENTETE = re.compile(r"── ([A-Za-z0-9.-]+?-(?:BoK-)?[\dv.?]+(?:-[a-z]+)?-(?:en|fr)) ·.*?· p\. (\d+)"
                       r"(?: \(imprimée [^)\n]*\))?(?: · §(\S*))?")


def pages_lues(sorties: str) -> set[tuple[str, int, str]]:
    """(document, page, section) affichés par `lire` / `section` / `page` (lignes
    « ── DOC · … · p. N · §x.y … ») : la section compte, comme dans `passages_lus` (#275), et
    le document est l'identifiant complet (`CT-MAT-2019-fr`), version et langue comprises (#280)."""
    return {(m.group(1), int(m.group(2)), regle_citations.numero_section(m.group(3) or ""))
            for m in RE_ENTETE.finditer(sorties)}


def textes_lus(sorties: str, maximum: int = 4000) -> dict[tuple[str, int], str]:
    """Texte affiché sous chaque en-tête « ── DOC · … · p. N » (jusqu'à l'en-tête suivant,
    `maximum` caractères au plus), par (document, page) : le passage réellement lu (#152)."""
    entetes = list(RE_ENTETE.finditer(sorties))
    lus: dict[tuple[str, int], str] = {}
    for m, suivant in zip(entetes, [*entetes[1:], None]):
        bloc = sorties[m.end():suivant.start() if suivant else len(sorties)][:maximum].strip()
        cle = (m.group(1), int(m.group(2)))
        if bloc and bloc not in lus.get(cle, ""):
            lus[cle] = f"{lus[cle]}\n{bloc}" if cle in lus else bloc
    return lus


# Sections de bilan (#139) : l'agent y déclare ce qu'il n'a PAS lu ou PAS cité ;
# « Sources retenues » en fait partie (#181) : on y déclare aussi une lecture partielle.
RE_TITRE = re.compile(r"^(?:#{1,6}\s|\*\*)", re.M)
RE_TITRE_BILAN = re.compile(r"^(?:#{1,6}\s*|\*\*)\s*(?:limites?|tra[çc]abilit[ée]|confiance|sources?\s+retenues?)\b",
                            re.I | re.M)
RE_PHRASE = re.compile(r"[^\n]+?(?:[.!?](?=\s+[A-ZÀ-Ý«*])|$)", re.M)
RE_NON_LU = re.compile(r"\bn['’](?:ai|a|ont|est|sont)\s+(?:donc\s+|pas\s+non\s+plus\s+|jamais\s+)?"
                       r"(?:pas\s+(?:non\s+plus\s+|été\s+|encore\s+)?)?(?:lue?s?|consult[ée]e?s?|ouvert|affich[ée]e?s?|cit[ée]e?s?)\b"
                       r"|\bnon\s+(?:lue?s?|consult[ée]e?s?|cit[ée]e?s?)\b|\bpas\s+(?:été\s+)?(?:lue?s?|cit[ée]e?s?)\b"
                       # Lecture partielle déclarée (#181) : « lu en partie (le reste est à la p. 35) ».
                       r"|\blue?s?\s+(?:en\s+partie|partiellement)\b|\ble\s+reste\s+(?:est\s+)?(?:à|a)\s+la\s+p\.", re.I)


def sections_bilan(reponse: str) -> list[tuple[int, int]]:
    """Étendue de chaque section de bilan (« Confiance », « Limites », « Traçabilité »,
    « Sources retenues ») : du titre au titre suivant."""
    titres = [m.start() for m in RE_TITRE.finditer(reponse)] + [len(reponse)]
    return [(d, f) for d, f in zip(titres, titres[1:]) if RE_TITRE_BILAN.match(reponse, d)]


def zones_non_lues(reponse: str) -> list[tuple[int, int]]:
    """Phrases des sections de bilan (« Confiance », « Limites », « Traçabilité »,
    « Sources retenues ») qui déclarent une référence non lue, non citée (#139) ou lue
    en partie (#181). Le reste de la réponse, et ces
    sections hors de telles phrases, restent soumis au contrôle strict."""
    zones = []
    for debut, fin in sections_bilan(reponse):
        for ph in RE_PHRASE.finditer(reponse, debut, fin):
            if RE_NON_LU.search(ph.group()):
                zones.append(ph.span())
    return zones


# Début de plage de sections juste avant une référence : « §4.3.1 à §4.3.2, p. 42 » (le
# jeton `ref` commence au dernier « § ») (#275).
RE_DEBUT_PLAGE = re.compile(r"§\s?([\d.]*\d)\.?\s*(?:à|au|-|–)\s*$")


def section_citee(reponse: str, m: re.Match) -> str:
    """Section(s) d'une référence, plage comprise : « §1.3.1 à 1.3.5 » est dans le jeton,
    « §4.3.1 à §4.3.2 » a sa première borne juste avant (#275)."""
    avant = RE_DEBUT_PLAGE.search(reponse, max(0, m.start() - 30), m.start())
    return f"{avant[1]} à {m.group('ref')}" if avant else m.group("ref")


# Référence qui ne nomme pas son document sur sa ligne (#247) : « (§3.2.2, p. 36) ».
SANS_DOCUMENT = "sans document"


def references(reponse: str, uniques: bool = True):
    """(code, première page, dernière page, correspondance) de chaque citation unique
    (document, section, pages : deux sections sœurs d'une même page restent deux
    citations, #275 ; `uniques=False` : chaque occurrence, pour juger chaque ligne qui cite, #255).
    Une référence que l'agent déclare lui-même non lue ou non citée, dans une section
    de bilan, n'est pas une citation (#139) ; son code garde le contexte des suivantes.
    Rattachement explicite seulement (#247) : une référence prend le dernier sigle nommé
    sur SA ligne, à défaut le premier qui la suit sur cette ligne ; sinon elle est
    orpheline (code None) — jamais rattachée au sigle d'une autre ligne. Une orpheline
    d'une section de bilan (« Sections lues : §1.3 (p. 29) ») n'est pas une citation.
    Le code rendu est le document tel que nommé (`CT-MAT v2019 FR`, `CTFL`), version et
    langue comprises quand l'agent les écrit (#280)."""
    exclues, bilans = zones_non_lues(reponse), sections_bilan(reponse)
    jetons = list(RE_JETON.finditer(reponse))
    vues, code, pos_code = set(), None, -1
    for i, m in enumerate(jetons):
        if m.group("code"):
            code, pos_code = " ".join(m.group("code").split()), m.start()
            continue
        if any(a <= m.start() < b for a, b in exclues):
            continue
        debut_ligne = reponse.rfind("\n", 0, m.start()) + 1
        fin_ligne = reponse.find("\n", m.end())
        fin_ligne = len(reponse) if fin_ligne < 0 else fin_ligne
        sigle = code if pos_code >= debut_ligne else next(
            (" ".join(j.group("code").split()) for j in jetons[i + 1:] if j.start() < fin_ligne and j.group("code")), None)
        if sigle is None and any(a <= m.start() < b for a, b in bilans):
            continue
        debut, fin = int(m.group("p1")), int(m.group("p2") or m.group("p1"))
        cle = (sigle and regle_citations.identite_document(sigle), regle_citations.bornes_section(section_citee(reponse, m)), debut, fin)  # section comprise (#275)
        if uniques and cle in vues:
            continue
        vues.add(cle)
        yield sigle, debut, fin, m


def verifier_citations(reponse: str, lues: set[tuple[str, int, str]]) -> list[dict]:
    """Chaque citation (code, section, pages) unique est-elle lue ? Même règle que
    `passages_lus` du serveur MCP, même code (`qak.citations`, #275) : chaque page citée
    (`pp. N-M` : chaque page de l'intervalle, #272) affichée dans la section citée ou
    l'une de ses sous-sections — une page lue sous une section sœur ne suffit pas.
    Une plage de sections (« §1.3.1 à §1.3.5, pp. 29-34 ») couvre chaque section de la
    plage. Le document lu doit être celui qui est cité : même sigle, et même version et
    même langue quand la citation les nomme (`regle_citations.meme_document`, #280).
    `lues` vient de `pages_lues` (document, page, section). Une référence sans document
    (#247) n'est rattachée à aucun syllabus : elle est signalée comme telle
    (« sans document §… »), non lue par construction."""
    lectures = [(code, sec, page, None) for code, page, sec in lues]
    return [{"citation": f"{code or SANS_DOCUMENT} {m.group('ref')[:60]}",
             "lue": code is not None and bool(regle_citations.lectures_couvrantes(
                 code, section_citee(reponse, m), debut, fin, lectures))}
            for code, debut, fin, m in references(reponse)]


def ligne_citee(reponse: str, position: int) -> tuple[int, str]:
    """(début, texte sans puce) de la ligne de la réponse qui porte la citation."""
    debut = reponse.rfind("\n", 0, position) + 1
    fin = reponse.find("\n", position)
    ligne = reponse[debut:fin if fin >= 0 else len(reponse)]
    return debut, re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", ligne).strip()


def controle_fidelite(reponse: str, sorties: str, juge=etude_juge.juger) -> list[dict]:
    """Contrôle de fond (#152), par LIGNE de la réponse qui porte des citations lues : le
    juge reçoit la ligne (une puce, une ligne de tableau…) et le texte lu de toutes les
    pages qu'elle cite, car une affirmation s'appuie souvent sur plusieurs références de
    la même ligne. `juge(passage, phrase)` renvoie au moins `cout_usd` et, s'il a abouti,
    `predit`, `fidelite` et `affirmations`. Les citations non lues sont déjà un échec de
    l'essai : elles ne sont pas jugées, pas plus que les sections de bilan. Le
    dédoublonnage se fait par ligne (#255) : une page déjà citée plus haut est rejugée
    sur chaque nouvelle ligne qui la cite (une réutilisation peut être à contresens)."""
    lus, lignes, bilans = textes_lus(sorties), {}, sections_bilan(reponse)
    for code, debut, fin, m in references(reponse, uniques=False):
        if any(a <= m.start() < b for a, b in bilans):
            continue  # liste des sources lues, limites : pas une affirmation sur le contenu
        textes = [t for (doc, p), t in sorted(lus.items(), key=lambda x: x[0][1])
                  if debut <= p <= fin and regle_citations.meme_document(code or "", doc)]
        if textes:
            cle, phrase = ligne_citee(reponse, m.start())
            ligne = lignes.setdefault(cle, {"phrase": phrase, "citations": [], "textes": [], "vues": set()})
            if (code, debut, fin) in ligne["vues"]:
                continue  # même citation répétée sur la même ligne : un seul jugement
            ligne["vues"].add((code, debut, fin))
            ligne["citations"].append(f"{code} {m.group('ref')[:60]}")
            ligne["textes"] += [t for t in textes if t not in ligne["textes"]]
    out = []
    for ligne in lignes.values():
        r = juge("\n\n".join(ligne["textes"]), ligne["phrase"][:1500])
        out.append({"citations": ligne["citations"], "phrase": ligne["phrase"][:200],
                    "verdict": r.get("predit", "erreur"), "fidelite": r.get("fidelite"),
                    "cout_usd": round(r.get("cout_usd") or 0, 4), "affirmations": r.get("affirmations", [])})
    return out


def alertes_fidelite(jugements: list[dict]) -> list[str]:
    """Lignes jugées contradictoires avec les passages lus (citation à contresens) : 0 fausse
    alerte et 12 contradictions sur 12 à l'étalonnage. « non soutenue » n'alerte pas : une
    ligne mêle souvent le passage cité et le contexte de l'utilisateur ou un raisonnement."""
    return [f"{', '.join(j['citations'])} : {j['phrase'][:80]}" for j in jugements if j["verdict"] == "contradictoire"]


def motifs_echec(bilan: dict) -> list[str]:
    """Raisons d'échec d'un essai (#127) : une citation dont la page n'a pas été lue fait
    échouer l'essai (règle « lire avant de citer »), comme un critère non satisfait ; une
    référence qui ne nomme pas son document (#247) aussi, sous son vrai motif."""
    if "erreur" in bilan:
        return ["erreur d'exécution"]
    motifs = [f"référence sans document : {c.removeprefix(SANS_DOCUMENT).strip()}" if c.startswith(SANS_DOCUMENT)
              else f"citation non lue : {c}" for c in bilan.get("citations_non_lues", [])]
    motifs += [f"critère : {c}" for c in bilan.get("criteres_ko", [])]
    return motifs


def lancer(essai: dict, dossier: Path, donnees: Path, fidelite: bool = False) -> dict:
    session = str(uuid.uuid4())
    cmd = ["claude", "-p", essai["question"], "--output-format", "json", "--session-id", session,
           "--allowedTools", *outils_autorises()]
    if essai.get("agent"):
        cmd[1:1] = ["--agent", essai["agent"]]
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION")}
    env["PATH"] = f"{RACINE / '.venv' / 'bin'}{os.pathsep}{env['PATH']}"
    env["QAK_RACINE"] = str(donnees)
    proc = subprocess.run(cmd, cwd=RACINE, capture_output=True, text=True, timeout=900, env=env)
    try:
        res = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"id": essai["id"], "erreur": (proc.stderr or proc.stdout)[-800:]}
    commandes, sorties = outils_utilises(transcript(session))
    reponse = res.get("result", "")
    citations = verifier_citations(reponse, pages_lues(sorties))
    conf = RE_CONFIANCE.search(reponse)
    bilan = {
        "id": essai["id"], "agent": essai.get("agent"), "question": essai["question"],
        "tours": res.get("num_turns"), "cout_usd": round(res.get("total_cost_usd") or 0, 3),
        "commandes_qa": [c for c in commandes if "qa.py" in c],
        "web": [c for c in commandes if c.startswith(("WebSearch", "WebFetch"))],
        "citations": citations,
        "citations_non_lues": [c["citation"] for c in citations if not c["lue"]],
        "confiance": int(conf.group(1)) if conf else None,
    }
    bilan["criteres"] = controler(reponse, essai.get("criteres") or {}, commandes)
    bilan["criteres_ko"] = [c for c, ok in bilan["criteres"].items() if not ok]
    bilan["echec"] = motifs_echec(bilan)
    fidelite_md = ""
    if fidelite:
        bilan["fidelite"] = controle_fidelite(reponse, sorties)
        bilan["fidelite_alertes"] = alertes_fidelite(bilan["fidelite"])
        notes = [j["fidelite"] for j in bilan["fidelite"] if j["fidelite"] is not None]
        bilan["fidelite_moyenne"] = round(sum(notes) / len(notes), 2) if notes else None
        bilan["cout_usd"] = round(bilan["cout_usd"] + sum(j["cout_usd"] for j in bilan["fidelite"]), 3)
        fidelite_md = (f" · **fidélité** (juge LLM, indicatif) : {bilan['fidelite_moyenne']} sur "
                       f"{len(bilan['fidelite'])} lignes citées, {len(bilan['fidelite_alertes'])} contradiction(s)"
                       + (f" ({' ; '.join(bilan['fidelite_alertes'])})" if bilan["fidelite_alertes"] else ""))
    criteres_md = ""
    if bilan.get("criteres"):
        criteres_md = (f" · **critères** : {sum(bilan['criteres'].values())}/{len(bilan['criteres'])}"
                       + (f" (manquent : {', '.join(bilan['criteres_ko'])})" if bilan["criteres_ko"] else ""))
    (dossier / f"{essai['id']}.md").write_text(
        f"# {essai['id']} — {essai.get('agent') or 'skill'}\n\n**Question** : {essai['question']}\n\n"
        f"**Tours** : {bilan['tours']} · **coût** : {bilan['cout_usd']} $ · **confiance annoncée** : "
        f"{bilan['confiance']} · **verdict** : {'ÉCHEC' if bilan['echec'] else 'réussi'} · **citations** : {len(citations) - len(bilan['citations_non_lues'])}/"
        f"{len(citations)} lues · **Web** : {len(bilan['web'])}{criteres_md}{fidelite_md}\n\n## Réponse\n\n{reponse}\n\n"
        "## Commandes exécutées\n\n" + "\n".join(f"- `{c[:200]}`" for c in commandes) + "\n",
        encoding="utf-8")
    return bilan


def main() -> int:
    essais = json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]
    fidelite = "--fidelite" in sys.argv[1:]
    demandes = [a for a in sys.argv[1:] if a != "--fidelite"]
    if demandes:
        essais = [e for e in essais if any(e["id"] == d or e["id"].startswith(d) for d in demandes)]
    dossier = RACINE / "eval" / "essais-resultats" / date.today().isoformat()
    if not (RACINE / "bibliotheque" / "index.db").exists():
        sys.exit("Index absent : lancer d'abord `python qa.py actualiser`.")
    dossier.mkdir(parents=True, exist_ok=True)
    bilans = []
    donnees = racine_temporaire()
    try:
        for e in essais:
            print(f"… {e['id']}", flush=True)
            b = lancer(e, dossier, donnees, fidelite)
            bilans.append(b)
            if "erreur" in b:
                b["echec"] = motifs_echec(b)
                print(f"  ERREUR : {b['erreur']}")
                continue
            print(f"  {b['tours']} tours · {b['cout_usd']} $ · confiance {b['confiance']} · citations "
                  f"{len(b['citations']) - len(b['citations_non_lues'])}/{len(b['citations'])} lues · web {len(b['web'])}"
                  + (f" · critères {sum(b['criteres'].values())}/{len(b['criteres'])} {b['criteres_ko'] or ''}" if b.get("criteres") else ""))
            if fidelite:
                print(f"  fidélité (indicatif) : {b['fidelite_moyenne']} sur {len(b['fidelite'])} lignes citées · "
                      f"contradictions : {len(b['fidelite_alertes'])}"
                      + (f" — {' ; '.join(b['fidelite_alertes'])}" if b["fidelite_alertes"] else ""))
            print("  ÉCHEC — " + " ; ".join(b["echec"]) if b["echec"] else "  réussi")
    finally:
        shutil.rmtree(donnees, ignore_errors=True)
    # Un lancement partiel complète le bilan du jour au lieu de l'écraser.
    fichier = dossier / "bilan.json"
    anciens = json.loads(fichier.read_text(encoding="utf-8")) if fichier.exists() else []
    nouveaux = {b["id"] for b in bilans}
    bilans = [b for b in anciens if b.get("id") not in nouveaux] + bilans
    fichier.write_text(json.dumps(bilans, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Résultats : {dossier}")
    echecs = [b["id"] for b in bilans if b.get("id") in nouveaux and b.get("echec")]
    if echecs:
        print(f"Essais en échec : {', '.join(echecs)}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
