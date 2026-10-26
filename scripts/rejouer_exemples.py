#!/usr/bin/env python3
"""Rejoue les commandes CLI des exemples (docs/exemples-conversations.md, §3 à §5) dans une
racine temporaire (QAK_RACINE) et fige leur sortie réelle (#159).

    python scripts/rejouer_exemples.py      # → eval/sorties-cli/<date>/exemples-cli.md

Prérequis : index construit (`python qa.py actualiser`). Rien n'est écrit dans la vraie
base d'idées : l'index et le manifeste sont copiés dans la racine temporaire (les PDF y
sont liés), qui est supprimée à la fin. L'identifiant de l'idée créée (QA-AAAAMMJJ-xxxx)
change à chaque exécution : reprendre dans la page celui de la sortie figée.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import commun  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent

IDEE = {
    "titre": "Matrice probabilité × impact pour prioriser les tests",
    "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver "
              "l'effort et l'ordre de test.",
    "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.",
    "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de "
                "risque, allouer profondeur et ordre de test.",
    "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee",
    "provenance": "Exemple rejoué par scripts/rejouer_exemples.py",
    "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "30", "section": "1.3.3",
                    "extrait": "pour chaque élément de risque, de la probabilité du risque et de "
                               "l'impact du risque"}],
}


def variante(**changements):
    idee = json.loads(json.dumps(IDEE))
    for cle, valeur in changements.items():
        if cle == "reference":
            idee["references"][0].update(valeur)
        else:
            idee[cle] = valeur
    return json.dumps(idee, ensure_ascii=False)


def etapes():
    """(titre, arguments, entrée standard). « {id} » = identifiant de l'idée créée."""
    return [
        ("§3 — préparer la capitalisation", None, None),
        ("", ["section", "CTAL-TM-3.0-fr", "1.3.3"], None),
        ("", ["theme", "proposer", "prioriser les tests selon probabilité et impact des risques"], None),
        ("", ["idee", "doublons", "--titre", IDEE["titre"], "--resume", IDEE["resume"],
              "--theme", "rbt"], None),
        ("", ["idee", "ajouter"], json.dumps(IDEE, ensure_ascii=False)),
        ("§3 — ce que l'outil refuse", None, None),
        ("Référence vers une page inexistante", ["idee", "ajouter"],
         variante(titre="Variante page 300", reference={"pages": "300"})),
        ("Extrait reformulé", ["idee", "ajouter"],
         variante(titre="Variante extrait reformulé",
                  # Ordre inversé : probabilité et impact permutés.
                  reference={"extrait": "pour chaque élément de risque, de l'impact du risque "
                                        "en cas de survenance et de la probabilité du risque"})),
        ("Même idée reformulée", ["idee", "ajouter"],
         variante(titre="Matrice impact × probabilité pour prioriser les tests")),
        ("Statut validée sans motif", ["idee", "statut", "{id}", "validee"], None),
        ("Expérimentée sans retour d'expérience", ["idee", "statut", "{id}", "experimentee",
                                                   "--motif", "appliquée sur une release"], None),
        ("§4 — retrouver et faire évoluer", None, None),
        ("", ["idee", "chercher", "probabilité", "impact"], None),
        ("", ["idee", "lister", "--theme", "rbt"], None),
        ("", ["idee", "retour", "{id}", "--contexte", "Release web, équipe produit de 6 personnes",
              "--resultat", "2 défauts critiques trouvés avant la recette",
              "--enseignement", "atelier d'1 h suffisant"], None),
        ("", ["idee", "statut", "{id}", "experimentee", "--motif", "appliquée sur une release"], None),
        ("§5 — couverture", None, None),
        ("", ["couverture"], None),
    ]


def affichage(args):
    return " ".join(a if re.fullmatch(r"[\w.:/{}§-]+", a) else f'"{a}"' for a in args)


def main():
    if not (RACINE / "bibliotheque" / "index.db").exists():
        sys.exit("Index absent : lancer d'abord `python qa.py actualiser`.")
    # Base d'idées vide : seuls l'index et le manifeste sont copiés.
    tmp = commun.racine_temporaire(RACINE, ("bibliotheque/index.db", "bibliotheque/manifeste.json"),
                                   "qak-exemples-")
    try:
        env = dict(os.environ, QAK_RACINE=str(tmp), PYTHONIOENCODING="utf-8")
        ident = None
        lignes = [f"# Sorties CLI des exemples — {date.today().isoformat()}", "",
                  "Généré par `python scripts/rejouer_exemples.py` dans une racine temporaire "
                  "(QAK_RACINE) : sortie brute, non retouchée. Référencé par "
                  "`docs/exemples-conversations.md` (§3 à §5).", ""]
        for titre, args, entree in etapes():
            if args is None:
                lignes += [f"## {titre}", ""]
                continue
            args = [a.replace("{id}", ident or "{id}") for a in args]
            r = subprocess.run([sys.executable, "qa.py", *args], cwd=RACINE, env=env, input=entree,
                               capture_output=True, text=True, encoding="utf-8")
            sortie = (r.stdout + r.stderr).rstrip()
            m = re.search(r"Idée créée : (QA-[\w-]+)", sortie)
            if m and ident is None:
                ident = m.group(1)
            if titre:
                lignes += [f"### {titre}", ""]
            lignes += ["```text", f"$ python qa.py {affichage(args)}"]
            if entree:
                lignes.append(f"(entrée standard : {entree})")
            lignes += [sortie, f"[code retour {r.returncode}]", "```", ""]
        cible = RACINE / "eval" / "sorties-cli" / date.today().isoformat() / "exemples-cli.md"
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text("\n".join(lignes), encoding="utf-8")
        print(f"Sorties figées : {cible.relative_to(RACINE)} (idée créée : {ident})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
