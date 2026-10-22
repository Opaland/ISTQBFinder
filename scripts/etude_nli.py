#!/usr/bin/env python3
"""Étude (issue #108) : un modèle NLI multilingue détecte-t-il qu'une citation ne soutient pas
l'affirmation qu'on lui attribue ?

    pip install --index-url https://download.pytorch.org/whl/cpu torch   # dépendances OPTIONNELLES
    pip install transformers sentencepiece protobuf
    python scripts/etude_nli.py [--modele NOM] [--passages]

Lit eval/nli/paires.json, retrouve le passage cité dans l'index local (page + section, le
plus proche de l'affirmation soutenue), applique le modèle et affiche exactitude, matrice de
confusion, précision / rappel de la détection « pas soutenue » et temps CPU par paire.
Script d'étude : il n'est pas utilisé par qa.py.
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE))

from qak import bibliotheque  # noqa: E402
from qak.textes import mots  # noqa: E402

MODELE = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
ETIQUETTES = {"entailment": "soutenue", "neutral": "non_soutenue", "contradiction": "contradictoire"}


def passage(cx, p: dict, reference: str) -> str:
    rows = cx.execute("SELECT texte FROM passages WHERE doc_id=? AND page=? AND section_num=?",
                      (p["doc_id"], p["page"], p["section"])).fetchall()
    if not rows:
        raise SystemExit(f"Passage introuvable : {p['doc_id']} p. {p['page']} §{p['section']} (index à jour ?)")
    ref = set(mots(reference))
    return max((r[0] for r in rows), key=lambda t: len(ref & set(mots(t))))


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--modele", default=MODELE)
    a.add_argument("--passages", action="store_true", help="afficher le début des passages retenus")
    args = a.parse_args()
    from transformers import pipeline

    jeu = json.loads((RACINE / "eval" / "nli" / "paires.json").read_text(encoding="utf-8"))["paires"]
    cx = bibliotheque.connecter()
    soutenues = {(p["doc_id"], p["page"], p["section"]): p["affirmation"] for p in jeu if p["etiquette"] == "soutenue"}
    debut = time.perf_counter()
    nli = pipeline("text-classification", model=args.modele, device=-1)
    chargement = time.perf_counter() - debut
    resultats, durees = [], []
    for p in jeu:
        premisse = passage(cx, p, soutenues[(p["doc_id"], p["page"], p["section"])])
        if args.passages and p["etiquette"] == "soutenue":
            print(f"--- {p['doc_id']} p. {p['page']} §{p['section']} : {' '.join(premisse.split())[:300]}")
        t = time.perf_counter()
        sortie = nli({"text": premisse, "text_pair": p["affirmation"]}, truncation=True, top_k=None)
        durees.append(time.perf_counter() - t)
        scores = {ETIQUETTES[s["label"].lower()]: s["score"] for s in sortie}
        resultats.append((p["etiquette"], max(scores, key=scores.get), scores))
    ok = sum(e == pr for e, pr, _ in resultats)
    print(f"Modèle : {args.modele} · chargement {chargement:.1f} s · {sum(durees) / len(durees):.2f} s CPU par paire")
    print(f"Exactitude (3 classes) : {ok}/{len(resultats)} = {ok / len(resultats):.0%}")
    confusion = Counter((e, pr) for e, pr, _ in resultats)
    classes = ["soutenue", "non_soutenue", "contradictoire"]
    print("attendu \\ prédit  " + "  ".join(f"{c[:12]:>12}" for c in classes))
    for e in classes:
        print(f"{e:17}" + "  ".join(f"{confusion[(e, pr)]:>12}" for pr in classes))
    # Usage visé : avertir quand le passage NE soutient PAS (non soutenue ou contradictoire).
    vp = sum(e != "soutenue" and pr != "soutenue" for e, pr, _ in resultats)
    fp = sum(e == "soutenue" and pr != "soutenue" for e, pr, _ in resultats)
    fn = sum(e != "soutenue" and pr == "soutenue" for e, pr, _ in resultats)
    print(f"Détection « pas soutenue » : précision {vp / max(1, vp + fp):.0%} · rappel {vp / max(1, vp + fn):.0%} "
          f"(faux avertissements sur une citation juste : {fp}/{sum(e == 'soutenue' for e, _, _ in resultats)})")
    for e, pr, s in resultats:
        if e != pr:
            print(f"  erreur : attendu {e}, prédit {pr} ({', '.join(f'{k} {v:.2f}' for k, v in s.items())})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
