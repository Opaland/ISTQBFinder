#!/usr/bin/env python3
"""Essais de bout en bout : pose les questions de eval/essais.json aux agents (Thomas,
Sylvie) via `claude -p`, puis contrôle automatiquement chaque réponse.

    python scripts/essais_agents.py                 # tous les essais
    python scripts/essais_agents.py T1-couverture S1-rbt   # seulement ces identifiants
    python scripts/essais_agents.py M                       # préfixe : tous les essais M…

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
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import date
from pathlib import Path

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


def racine_temporaire(source: Path = RACINE) -> Path:
    """Copie de travail des données (index, manifeste, base d'idées, journal, référentiels)
    pour `QAK_RACINE` : une écriture éventuelle de l'agent n'atteint pas le dépôt (#157).
    Les PDF sont liés (ou copiés si le lien est impossible) : seul le contrôle « index à
    jour » les lit."""
    tmp = Path(tempfile.mkdtemp(prefix="qak-essais-"))
    for dossier in ("bibliotheque", "connaissances", "referentiel"):
        (tmp / dossier).mkdir()
    for rel in ("bibliotheque/index.db", "bibliotheque/manifeste.json", "bibliotheque/vecteurs.npz",
                "connaissances/connaissances.jsonl", "connaissances/journal.jsonl",
                "referentiel/taxonomie.json", "referentiel/thesaurus.json"):
        if (source / rel).exists():
            shutil.copy2(source / rel, tmp / rel)
    try:
        (tmp / "bibliotheque" / "sources").symlink_to(source / "bibliotheque" / "sources")
    except OSError:
        shutil.copytree(source / "bibliotheque" / "sources", tmp / "bibliotheque" / "sources")
    return tmp


# Une citation = « §x.y … p. N » ou « … pp. N-M » ; elle se rattache au dernier code de
# syllabus nommé avant elle (« **CTFL v4.0.1** … (§4.2.1, p. 40) » comme « [CTAL-TM v3.0,
# §1.3, p. 29] »). Entre « § » et la page, ni « § » ni « ; » : sinon deux références
# voisines fusionnent et la page de la seconde est prêtée à la première (#142).
RE_JETON = re.compile(r"(?P<code>\b(?:CTFL(?:-AT)?|CTAL-[A-Za-z]+|CTEL-[A-Za-z]+|CT-[A-Za-z]+)\b)"
                      r"|(?P<ref>§\s?[\d.]+[^\n\]\)§;]{0,40}?\bpp?\.\s?(?P<p1>\d+)(?:\s?[-–]\s?(?P<p2>\d+))?)")
RE_CONFIANCE = re.compile(r"[Cc]onfiance\s*:?\s*\**\s*(\d{1,3})\s*/\s*100")
RE_ETAPE = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:[ÉE]tape\s*)?\d+\s*[.)—:-]", re.M)
RE_NON_COUVERT = re.compile(r"pas de syllabus|aucun syllabus|ne couvre pas|non couvert|absente? de la biblioth|"
                            r"n'est pas dans la biblioth|pas dans la biblioth|hors biblioth", re.I)


def _apres(texte: str, motif: str) -> str:
    """Texte qui suit la première occurrence de `motif` (vide si absent)."""
    m = re.search(motif, texte, re.I)
    return texte[m.end():] if m else ""


def controler(reponse: str, criteres: dict) -> dict[str, bool]:
    """Critères vérifiables d'un essai (fonction pure, testée sans réseau). Clés :
    methode (≥ 4 étapes numérotées de premier niveau après « Méthode »), etapes_sourcees
    (chaque étape, sous-puces comprises, porte « § » ou « interprétation »), exemple (exemple marqué fictif / interprétation),
    domaines et mentions (listes de motifs, tous présents), cadrage, questions_choix
    (« Questions à choix » suivi d'au moins 2 options numérotées), hypotheses,
    non_couvert (absence de syllabus dédié dite franchement), confiance."""
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


def pages_lues(sorties: str) -> set[tuple[str, int]]:
    """(code, page) affichés par `lire` / `section` / `page` (lignes « ── DOC · … · p. N »)."""
    lues = set()
    for m in re.finditer(r"── ([A-Za-z0-9.-]+?)-(?:BoK-)?[\dv.?]+(?:-[a-z]+)?-(?:en|fr) ·.*?· p\. (\d+)", sorties):
        lues.add((m.group(1).upper(), int(m.group(2))))
    return lues


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


def zones_non_lues(reponse: str) -> list[tuple[int, int]]:
    """Phrases des sections de bilan (« Confiance », « Limites », « Traçabilité »,
    « Sources retenues ») qui déclarent une référence non lue, non citée (#139) ou lue
    en partie (#181). Le reste de la réponse, et ces
    sections hors de telles phrases, restent soumis au contrôle strict."""
    zones, titres = [], [m.start() for m in RE_TITRE.finditer(reponse)] + [len(reponse)]
    for debut, fin in zip(titres, titres[1:]):
        if not RE_TITRE_BILAN.match(reponse, debut):
            continue
        for ph in RE_PHRASE.finditer(reponse, debut, fin):
            if RE_NON_LU.search(ph.group()):
                zones.append(ph.span())
    return zones


def verifier_citations(reponse: str, lues: set) -> list[dict]:
    """Chaque citation (code, pages) unique : une des pages a-t-elle été lue ?
    Une référence que l'agent déclare lui-même non lue ou non citée, dans une section
    de bilan, n'est pas une citation (#139) ; son code garde le contexte des suivantes."""
    codes_lus = {c for c, _ in lues}
    exclues = zones_non_lues(reponse)
    out, vues, code = [], set(), None
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
        code_lu = next((c for c in codes_lus if c == code), None)
        ok = bool(code_lu) and any((code_lu, p) in lues for p in range(debut, fin + 1))
        out.append({"citation": f"{code} {m.group('ref')[:60]}", "lue": ok})
    return out


def motifs_echec(bilan: dict) -> list[str]:
    """Raisons d'échec d'un essai (#127) : une citation dont la page n'a pas été lue fait
    échouer l'essai (règle « lire avant de citer »), comme un critère non satisfait."""
    if "erreur" in bilan:
        return ["erreur d'exécution"]
    motifs = [f"citation non lue : {c}" for c in bilan.get("citations_non_lues", [])]
    motifs += [f"critère : {c}" for c in bilan.get("criteres_ko", [])]
    return motifs


def lancer(essai: dict, dossier: Path, donnees: Path) -> dict:
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
    criteres_md = ""
    if bilan.get("criteres"):
        criteres_md = (f" · **critères** : {sum(bilan['criteres'].values())}/{len(bilan['criteres'])}"
                       + (f" (manquent : {', '.join(bilan['criteres_ko'])})" if bilan["criteres_ko"] else ""))
    (dossier / f"{essai['id']}.md").write_text(
        f"# {essai['id']} — {essai.get('agent') or 'skill'}\n\n**Question** : {essai['question']}\n\n"
        f"**Tours** : {bilan['tours']} · **coût** : {bilan['cout_usd']} $ · **confiance annoncée** : "
        f"{bilan['confiance']} · **verdict** : {'ÉCHEC' if bilan['echec'] else 'réussi'} · **citations** : {len(citations) - len(bilan['citations_non_lues'])}/"
        f"{len(citations)} lues · **Web** : {len(bilan['web'])}{criteres_md}\n\n## Réponse\n\n{reponse}\n\n"
        "## Commandes exécutées\n\n" + "\n".join(f"- `{c[:200]}`" for c in commandes) + "\n",
        encoding="utf-8")
    return bilan


def main() -> int:
    essais = json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]
    if sys.argv[1:]:
        demandes = sys.argv[1:]
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
            b = lancer(e, dossier, donnees)
            bilans.append(b)
            if "erreur" in b:
                b["echec"] = motifs_echec(b)
                print(f"  ERREUR : {b['erreur']}")
                continue
            print(f"  {b['tours']} tours · {b['cout_usd']} $ · confiance {b['confiance']} · citations "
                  f"{len(b['citations']) - len(b['citations_non_lues'])}/{len(b['citations'])} lues · web {len(b['web'])}"
                  + (f" · critères {sum(b['criteres'].values())}/{len(b['criteres'])} {b['criteres_ko'] or ''}" if b.get("criteres") else ""))
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
