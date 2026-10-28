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
  conversation (présente dans la sortie d'un `lire`, `section` ou `page`) ? Une référence
  que l'agent déclare lui-même non lue, non citée ou lue en partie dans « Confiance »,
  « Limites », « Traçabilité » ou « Sources retenues » n'est pas une citation (#139, #181) ;
- présence d'un score de confiance « Confiance : NN/100 » ;
- recours au Web ;
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
import commun  # noqa: E402
import etude_juge  # noqa: E402

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
RE_JETON = re.compile(r"(?P<code>\b(?:CTFL(?:-AT)?|CTAL-[A-Za-z]+|CTEL-[A-Za-z]+|CT-[A-Za-z]+)\b)"
                      r"|(?P<ref>§\s?[\d.]+[^\n\]\)§;]{0,40}?\bpp?\.\s?(?P<p1>\d+)(?:\s?[-–]\s?(?P<p2>\d+))?)")
RE_CONFIANCE = re.compile(r"[Cc]onfiance\s*:?\s*\**\s*(\d{1,3})\s*/\s*100")
RE_ETAPE = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:[ÉE]tape\s*)?\d+\s*[.)—:-]", re.M)
# Calcul de la confiance recopié de `qa.py confiance` (#227) : « base 70 × 0,6 = 42 ».
RE_CALCUL_CONFIANCE = re.compile(r"\d{1,3}\s*[×x*]\s*0[,.]6\b", re.I)
# Titre « Niveau atteint : N » de Sylvie (#228) : le niveau retenu, sans réserve.
RE_NIVEAU_ATTEINT = re.compile(r"niveau\s+atteint\W{0,6}(\d)(?P<suite>[^\n]*)", re.I)
RE_NIVEAU_RETENU = re.compile(r"(?:je\s+retiens|niveau\s+retenu)\W{0,6}(?:le\s+)?(?:niveau\s+)?(\d)", re.I)
RE_NIVEAU_RESERVE = re.compile(r"non\s+d[ée]montr|provisoire|probable|en\s+partie|partiel", re.I)
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


def controler(reponse: str, criteres: dict) -> dict[str, bool]:
    """Critères vérifiables d'un essai (fonction pure, testée sans réseau). Clés :
    methode (≥ 4 étapes numérotées de premier niveau après « Méthode »), etapes_sourcees
    (chaque étape, sous-puces comprises, porte « § » ou « interprétation »), exemple (exemple marqué fictif / interprétation),
    domaines et mentions (listes de motifs, tous présents), cadrage, questions_choix
    (« Questions à choix » suivi d'au moins 2 options numérotées), hypotheses,
    non_couvert (absence de syllabus dédié dite franchement), confiance, calcul_confiance
    (le calcul « base N × 0,6 » de `qa.py confiance` est recopié, #227), niveau_coherent
    (« Niveau atteint : N » porte le niveau retenu, sans réserve ni second chiffre, #228)."""
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
    if criteres.get("calcul_confiance"):
        out["calcul_confiance"] = bool(RE_CALCUL_CONFIANCE.search(reponse))
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


RE_ENTETE = re.compile(r"── ([A-Za-z0-9.-]+?)-(?:BoK-)?[\dv.?]+(?:-[a-z]+)?-(?:en|fr) ·.*?· p\. (\d+)")


def pages_lues(sorties: str) -> set[tuple[str, int]]:
    """(code, page) affichés par `lire` / `section` / `page` (lignes « ── DOC · … · p. N »)."""
    return {(m.group(1).upper(), int(m.group(2))) for m in RE_ENTETE.finditer(sorties)}


def textes_lus(sorties: str, maximum: int = 4000) -> dict[tuple[str, int], str]:
    """Texte affiché sous chaque en-tête « ── DOC · … · p. N » (jusqu'à l'en-tête suivant,
    `maximum` caractères au plus), par (code, page) : le passage réellement lu (#152)."""
    entetes = list(RE_ENTETE.finditer(sorties))
    lus: dict[tuple[str, int], str] = {}
    for m, suivant in zip(entetes, [*entetes[1:], None]):
        bloc = sorties[m.end():suivant.start() if suivant else len(sorties)][:maximum].strip()
        cle = (m.group(1).upper(), int(m.group(2)))
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


def references(reponse: str):
    """(code, première page, dernière page, correspondance) de chaque citation unique.
    Une référence que l'agent déclare lui-même non lue ou non citée, dans une section
    de bilan, n'est pas une citation (#139) ; son code garde le contexte des suivantes."""
    exclues = zones_non_lues(reponse)
    vues, code = set(), None
    for m in RE_JETON.finditer(reponse):
        if m.group("code"):
            code = m.group("code").upper()
            continue
        if not code or any(a <= m.start() < b for a, b in exclues):
            continue
        debut, fin = int(m.group("p1")), int(m.group("p2") or m.group("p1"))
        if (code, debut, fin) in vues:
            continue
        vues.add((code, debut, fin))
        yield code, debut, fin, m


def verifier_citations(reponse: str, lues: set) -> list[dict]:
    """Chaque citation (code, pages) unique : une des pages a-t-elle été lue ?"""
    return [{"citation": f"{code} {m.group('ref')[:60]}",
             "lue": any((code, p) in lues for p in range(debut, fin + 1))}
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
    l'essai : elles ne sont pas jugées, pas plus que les sections de bilan."""
    lus, lignes, bilans = textes_lus(sorties), {}, sections_bilan(reponse)
    for code, debut, fin, m in references(reponse):
        if any(a <= m.start() < b for a, b in bilans):
            continue  # liste des sources lues, limites : pas une affirmation sur le contenu
        textes = [lus[(code, p)] for p in range(debut, fin + 1) if (code, p) in lus]
        if textes:
            cle, phrase = ligne_citee(reponse, m.start())
            ligne = lignes.setdefault(cle, {"phrase": phrase, "citations": [], "textes": []})
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
    échouer l'essai (règle « lire avant de citer »), comme un critère non satisfait."""
    if "erreur" in bilan:
        return ["erreur d'exécution"]
    motifs = [f"citation non lue : {c}" for c in bilan.get("citations_non_lues", [])]
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
    if essai.get("criteres"):
        bilan["criteres"] = controler(reponse, essai["criteres"])
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
