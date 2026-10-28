"""Mesure de la reformulation de la question par l'agent avant `chercher` (issue #151).

La consigne « Reformuler avant de chercher » du skill qa-knowledge (lue dans
`.claude/skills/qa-knowledge/SKILL.md`, source unique) est donnée à `claude -p`, qui produit
2-3 requêtes en vocabulaire ISTQB pour chaque question d'un jeu d'évaluation. Chaque requête
(plus la question telle quelle) passe par `recherche.chercher` ; les listes sont fusionnées
par rang réciproque (RRF) et l'on garde 5 passages, comme `evaluer` : même budget de lecture.
Indicateur secondaire « une requête suffit » : la section attendue est dans les 5 premiers
résultats d'au moins une requête (l'agent lit chaque liste ; budget 5 par requête).

Non déterministe et payant : plusieurs passages (`--passages`), moyenne et extrêmes ; les
reformulations sont enregistrées (`--sortie`) pour pouvoir recalculer sans repayer
(`--rejouer`). Budget plafonné (`--budget`, en dollars, coût lu dans la sortie JSON de
`claude -p`). Prérequis : CLI `claude` connectée, index construit (`python qa.py actualiser`).

    python scripts/mesure_reformulation.py --jeux eloigne controle reglage --passages 3 \\
        --sortie eval/reformulation-resultats/AAAA-MM-JJ.json
    python scripts/mesure_reformulation.py --rejouer eval/reformulation-resultats/AAAA-MM-JJ.json
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))

from qak import bibliotheque, evaluation, recherche  # noqa: E402

SKILL = RACINE / ".claude" / "skills" / "qa-knowledge" / "SKILL.md"
TAILLE_LOT = 20
K_RRF = 60


def consigne(texte: str | None = None) -> str:
    """Paragraphe « Reformuler avant de chercher » du skill (jusqu'à la ligne vide ou à
    l'étape numérotée suivante)."""
    texte = SKILL.read_text(encoding="utf-8") if texte is None else texte
    m = re.search(r"^[ \t]*\*\*Reformuler avant de chercher\*\*.*?(?=\n[ \t]*(?:\d+\.\s|\n)|\Z)", texte, re.S | re.M)
    if not m:
        raise SystemExit("Consigne « Reformuler avant de chercher » introuvable dans " + str(SKILL))
    return re.sub(r"\s+", " ", m.group(0)).strip()


def invite(questions: list[str]) -> str:
    lignes = "\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1))
    return ("Pour chacune des questions numérotées ci-dessous, applique la consigne et donne seulement "
            "les requêtes `chercher` que tu lancerais (sans la question d'origine). Réponds uniquement par "
            'un objet JSON {"1": ["requête", ...], "2": [...]}, sans autre texte.\n\n' + lignes)


def lire_reponse(texte: str, nombre: int) -> list[list[str]]:
    """Requêtes par question depuis la réponse du modèle (objet JSON, éventuellement entouré
    de texte ou d'une clôture ```). Question absente → liste vide (comptée sans reformulation)."""
    m = re.search(r"\{.*\}", texte, re.S)
    d = json.loads(m.group(0)) if m else {}
    return [[str(r).strip() for r in d.get(str(i), []) if str(r).strip()][:3] for i in range(1, nombre + 1)]


def reformuler(questions: list[str], regle: str, modele: str | None) -> tuple[list[list[str]], float]:
    cmd = ["claude", "-p", invite(questions), "--output-format", "json", "--tools", "",
           "--no-session-persistence", "--system-prompt",
           "Tu es l'assistant QA du skill qa-knowledge (syllabus ISTQB locaux FR/EN). Consigne à appliquer : "
           + regle]
    if modele:
        cmd += ["--model", modele]
    with tempfile.TemporaryDirectory() as vide:  # aucun CLAUDE.md ni réglage du dépôt
        p = subprocess.run(cmd, cwd=vide, capture_output=True, text=True, encoding="utf-8", timeout=600)
    if p.returncode:
        raise SystemExit(f"claude -p a échoué ({p.returncode}) : {p.stderr.strip()[:300]}")
    sortie = json.loads(p.stdout)
    return lire_reponse(sortie.get("result", ""), len(questions)), float(sortie.get("total_cost_usd") or 0)


def fusion_rrf(listes: list[list[dict]], n: int = 5) -> list[dict]:
    """Fusion par rang réciproque (somme de 1/(60 + rang)) ; ex æquo : ordre de première apparition."""
    scores, premiers = {}, {}
    for liste in listes:
        for rang, r in enumerate(liste, 1):
            scores[r["id"]] = scores.get(r["id"], 0.0) + 1 / (K_RRF + rang)
            premiers.setdefault(r["id"], r)
    ordre = sorted(premiers, key=lambda i: -scores[i])
    return [premiers[i] for i in ordre[:n]]


def rang(resultats: list[dict], attendus: list[dict]) -> int | None:
    return next((i for i, r in enumerate(resultats, 1) if any(
        r["code"] == a["code"] and evaluation._dans_section(r["section_num"], a.get("section", ""))
        for a in attendus)), None)


def cas_du_jeu(nom: str) -> list[dict]:
    fichier = evaluation.fichier_jeu(nom) or RACINE / "eval" / "requetes.json"
    cas = json.loads(fichier.read_text(encoding="utf-8-sig"))["cas"]
    if nom == "examens":
        return cas
    return [c for c in cas if bool(c.get("eloigne")) == (nom == "eloigne")
            and (nom == "eloigne" or bool(c.get("controle")) == (nom == "controle"))]


def noter(cas: list[dict], reformulations: list[list[str]], cx, codes: set[str], k: int = 5) -> dict:
    base = fusion = une = total = 0
    for c, reqs in zip(cas, reformulations):
        attendus = [a for a in c["attendus"] if a["code"] in codes]
        if not attendus:
            continue
        total += 1
        listes = [recherche.chercher(q, n=k, cx=cx, **c.get("filtres", {}))["resultats"] for q in [c["requete"], *reqs]]
        base += rang(listes[0], attendus) is not None
        fusion += rang(fusion_rrf(listes, k), attendus) is not None
        une += any(rang(lst, attendus) is not None for lst in listes)
    return {"total": total, "base": base, "fusion": fusion, "une_requete": une}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--jeux", nargs="+", default=["eloigne"], choices=["eloigne", "controle", "reglage", "examens"])
    p.add_argument("--passages", type=int, default=3)
    p.add_argument("--budget", type=float, default=2.0, help="plafond en dollars pour cet appel (défaut 2)")
    p.add_argument("--modele", help="modèle de `claude -p` (défaut : celui de la CLI)")
    p.add_argument("--sortie", type=Path, help="fichier JSON où enregistrer les reformulations")
    p.add_argument("--rejouer", type=Path, help="recalculer à partir de reformulations enregistrées")
    a = p.parse_args(argv)

    if a.rejouer:
        donnees = json.loads(a.rejouer.read_text(encoding="utf-8"))
    else:
        regle, depense = consigne(), 0.0
        donnees = {"consigne": regle, "modele": a.modele or "défaut de la CLI", "passages": []}
        for _ in range(a.passages):
            passage = {}
            for nom in a.jeux:
                questions = [c["requete"] for c in cas_du_jeu(nom)]
                reqs = []
                for i in range(0, len(questions), TAILLE_LOT):
                    if depense >= a.budget:
                        raise SystemExit(f"Budget atteint ({depense:.2f} $) : mesure interrompue.")
                    lot, cout = reformuler(questions[i:i + TAILLE_LOT], regle, a.modele)
                    reqs += lot
                    depense += cout
                passage[nom] = reqs
            donnees["passages"].append(passage)
        donnees["cout_usd"] = round(depense, 4)
        if a.sortie:
            a.sortie.parent.mkdir(parents=True, exist_ok=True)
            a.sortie.write_text(json.dumps(donnees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    cx = bibliotheque.connecter()
    try:
        codes = {r["code"] for r in cx.execute("SELECT DISTINCT code FROM documents WHERE statut_version='courant'")}
        for nom in donnees["passages"][0]:
            cas = cas_du_jeu(nom)
            notes = [noter(cas, passage[nom], cx, codes) for passage in donnees["passages"]]
            t = notes[0]["total"]
            fus = [n["fusion"] for n in notes]
            une = [n["une_requete"] for n in notes]
            print(f"{nom:9} ({t} q.) · question seule {notes[0]['base']}/{t} ({notes[0]['base'] / t:.0%})"
                  f" · reformulation (RRF, 5 passages) moyenne {sum(fus) / len(fus) / t:.0%}"
                  f" [{min(fus)}-{max(fus)}/{t}] · une requête suffit {sum(une) / len(une) / t:.0%}"
                  f" [{min(une)}-{max(une)}/{t}] · {len(notes)} passage(s)")
    finally:
        cx.close()
    if "cout_usd" in donnees:
        print(f"Coût claude -p : {donnees['cout_usd']:.2f} $")
    return 0


if __name__ == "__main__":
    sys.exit(main())
