#!/usr/bin/env python3
"""Essais de bout en bout : pose les questions de eval/essais.json aux agents (Thomas,
Sylvie) via `claude -p`, puis contrôle automatiquement chaque réponse.

    python scripts/essais_agents.py                 # tous les essais
    python scripts/essais_agents.py T1-couverture S1-rbt

Prérequis : CLI `claude` connectée, index construit (`python qa.py actualiser`).
Coût indicatif : 0,10 à 0,50 $ par question. Résultats : eval/essais-resultats/<date>/.

Contrôles automatiques (le jugement de fond reste humain, voir docs/essais-reponses.md) :
- commandes `qa.py` réellement exécutées par l'agent (lues dans le transcript) ;
- citations `[DOC …, §x.y, p. N]` : la page N du document a-t-elle été LUE pendant la
  conversation (présente dans la sortie d'un `lire`, `section` ou `page`) ? ;
- présence d'un score de confiance « Confiance : NN/100 » ;
- recours au Web.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
OUTILS = ["Bash(python qa.py:*)", "Bash(python3 qa.py:*)", "Read", "Skill", "WebSearch", "WebFetch"]
RE_CITATION = re.compile(r"\[[^\]]*?\b((?:CT|CTAL|CTFL|CTEL)[A-Za-z-]*)[^\]]*?\bp\.\s*(\d+)(?:\s*[-–]\s*(\d+))?[^\]]*\]")
RE_CONFIANCE = re.compile(r"[Cc]onfiance\s*:?\s*\**\s*(\d{1,3})\s*/\s*100")


def transcript(session_id: str) -> list[dict]:
    """Transcript JSONL de la session (dossier projet de Claude Code)."""
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


def verifier_citations(reponse: str, lues: set) -> list[dict]:
    codes_lus = {c for c, _ in lues}
    out = []
    for m in RE_CITATION.finditer(reponse):
        code = m.group(1).upper().rstrip("-")
        debut, fin = int(m.group(2)), int(m.group(3) or m.group(2))
        code_lu = next((c for c in codes_lus if c == code or c.startswith(code) or code.startswith(c)), None)
        ok = bool(code_lu) and any((code_lu, p) in lues for p in range(debut, fin + 1))
        out.append({"citation": m.group(0)[:120], "lue": ok})
    return out


def lancer(essai: dict, dossier: Path) -> dict:
    cmd = ["claude", "-p", essai["question"], "--output-format", "json", "--allowedTools", *OUTILS]
    if essai.get("agent"):
        cmd[1:1] = ["--agent", essai["agent"]]
    proc = subprocess.run(cmd, cwd=RACINE, capture_output=True, text=True, timeout=900,
                          env={**os.environ, "PATH": f"{RACINE / '.venv' / 'bin'}:{os.environ['PATH']}"})
    try:
        res = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"id": essai["id"], "erreur": (proc.stderr or proc.stdout)[-800:]}
    commandes, sorties = outils_utilises(transcript(res.get("session_id", "")))
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
    (dossier / f"{essai['id']}.md").write_text(
        f"# {essai['id']} — {essai.get('agent') or 'skill'}\n\n**Question** : {essai['question']}\n\n"
        f"**Tours** : {bilan['tours']} · **coût** : {bilan['cout_usd']} $ · **confiance annoncée** : "
        f"{bilan['confiance']} · **citations** : {len(citations) - len(bilan['citations_non_lues'])}/"
        f"{len(citations)} lues · **Web** : {len(bilan['web'])}\n\n## Réponse\n\n{reponse}\n\n"
        "## Commandes exécutées\n\n" + "\n".join(f"- `{c[:200]}`" for c in commandes) + "\n",
        encoding="utf-8")
    return bilan


def main() -> int:
    essais = json.loads((RACINE / "eval" / "essais.json").read_text(encoding="utf-8"))["essais"]
    if sys.argv[1:]:
        essais = [e for e in essais if e["id"] in sys.argv[1:]]
    dossier = RACINE / "eval" / "essais-resultats" / date.today().isoformat()
    dossier.mkdir(parents=True, exist_ok=True)
    bilans = []
    for e in essais:
        print(f"… {e['id']}", flush=True)
        b = lancer(e, dossier)
        bilans.append(b)
        if "erreur" in b:
            print(f"  ERREUR : {b['erreur']}")
            continue
        print(f"  {b['tours']} tours · {b['cout_usd']} $ · confiance {b['confiance']} · citations "
              f"{len(b['citations']) - len(b['citations_non_lues'])}/{len(b['citations'])} lues · web {len(b['web'])}")
    (dossier / "bilan.json").write_text(json.dumps(bilans, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Résultats : {dossier}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
