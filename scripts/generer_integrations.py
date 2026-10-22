#!/usr/bin/env python3
"""Génère les fichiers d'intégration des autres assistants depuis la source unique `.claude/`.

    python scripts/generer_integrations.py              # (ré)écrit les fichiers générés
    python scripts/generer_integrations.py --verifier   # code 1 si un fichier n'est pas à jour

Source unique (à modifier) : `.claude/agents/*.md` et `.claude/skills/*/` ; consignes
communes dans `AGENTS.md`. Fichiers générés (à ne jamais modifier à la main) :

- GitHub Copilot : `.github/agents/<agent>.agent.md`. Les skills n'ont pas besoin de copie :
  Copilot (VS Code et Copilot CLI) lit `.claude/skills/` directement.

Le test `tests/test_integrations.py` échoue si un fichier généré n'est pas à jour.
"""
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
AGENTS_CLAUDE = RACINE / ".claude" / "agents"
MARQUE = "Fichier généré par scripts/generer_integrations.py"

# Outils Claude Code → alias Copilot (docs.github.com/en/copilot/reference/custom-agents-configuration).
OUTILS_COPILOT = {"Bash": "execute", "Read": "read", "Grep": "search", "Glob": "search",
                  "WebSearch": "web", "WebFetch": "web"}


def lire_entete(texte: str) -> tuple[dict, str]:
    """Sépare l'en-tête YAML minimal (« clé: valeur » et listes « - x ») du corps."""
    lignes = texte.replace("\r\n", "\n").split("\n")
    if lignes[0] != "---":
        raise ValueError("en-tête YAML absent")
    fin = lignes.index("---", 1)
    champs, cle = {}, None
    for ligne in lignes[1:fin]:
        if ligne.startswith("  - ") and cle:
            if not isinstance(champs.get(cle), list):
                champs[cle] = []
            champs[cle].append(ligne[4:].strip())
        elif ":" in ligne and not ligne.startswith(" "):
            cle, valeur = ligne.split(":", 1)
            cle = cle.strip()
            champs[cle] = valeur.strip().strip('"')
    return champs, "\n".join(lignes[fin + 1:]).lstrip("\n")


def outils(champs: dict, table: dict) -> list[str]:
    """Outils autorisés par l'agent Claude, traduits ; les outils d'écriture ne passent jamais."""
    noms = [o.strip() for o in str(champs.get("tools", "")).split(",") if o.strip()]
    interdits = {o.strip() for o in str(champs.get("disallowedTools", "")).split(",")}
    resultat = []
    for nom in noms:
        cible = table.get(nom)
        if nom not in interdits and cible and cible not in resultat:
            resultat.append(cible)
    return resultat


def preambule(nom_source: str, champs: dict, assistant: str, outil_lecture: str) -> str:
    skills = champs.get("skills") or []
    lignes = [f"<!-- {MARQUE} depuis .claude/agents/{nom_source} : ne pas modifier, relancer le script. -->", "",
              f"> **Version {assistant}** de l'agent défini dans `.claude/agents/{nom_source}` (source unique)."]
    for skill in skills:
        lignes.append(f"> Ta méthode est le skill `{skill}` : **avant toute recherche, lis en entier "
                      f"`.claude/skills/{skill}/SKILL.md`** puis les fichiers `reference/` qu'il cite ; "
                      f"cette lecture remplace le « déjà chargé » écrit plus bas.")
    lignes.append(f"> Outils : « `Read` » désigne ici `{outil_lecture}` ; les commandes `python qa.py …` "
                  "passent par le terminal (`python3` si `python` est absent), lancées depuis la racine du dépôt.")
    return "\n".join(lignes) + "\n\n"


def agent_copilot(chemin: Path) -> str:
    champs, corps = lire_entete(chemin.read_text(encoding="utf-8"))
    entete = ["---",
              f"name: {champs['name']}",
              f"description: {json.dumps(champs['description'], ensure_ascii=False)}",
              f"tools: {json.dumps(outils(champs, OUTILS_COPILOT))}",
              "---", ""]
    return "\n".join(entete) + preambule(chemin.name, champs, "GitHub Copilot", "read") + corps


def fichiers_attendus() -> dict[str, str]:
    """Chemin relatif (POSIX) → contenu attendu de chaque fichier généré."""
    attendus = {}
    for chemin in sorted(AGENTS_CLAUDE.glob("*.md")):
        attendus[f".github/agents/{chemin.stem}.agent.md"] = agent_copilot(chemin)
    return attendus


def dossiers_geres() -> list[Path]:
    return [RACINE / ".github" / "agents"]


def orphelins(attendus: dict[str, str]) -> list[str]:
    """Fichiers générés autrefois (marqués) dont la source a disparu."""
    trouves = []
    for dossier in dossiers_geres():
        for f in dossier.rglob("*") if dossier.exists() else []:
            rel = f.relative_to(RACINE).as_posix()
            if f.is_file() and rel not in attendus and MARQUE in f.read_text(encoding="utf-8", errors="ignore"):
                trouves.append(rel)
    return trouves


def ecarts() -> list[str]:
    """Fichiers absents, périmés ou orphelins (liste vide = tout est à jour)."""
    attendus = fichiers_attendus()
    resultat = []
    for rel, contenu in attendus.items():
        f = RACINE / rel
        if not f.exists():
            resultat.append(f"absent : {rel}")
        elif f.read_text(encoding="utf-8").replace("\r\n", "\n") != contenu:
            resultat.append(f"périmé : {rel}")
    resultat += [f"orphelin : {rel}" for rel in orphelins(attendus)]
    return resultat


def generer() -> list[str]:
    attendus = fichiers_attendus()
    ecrits = []
    for rel, contenu in attendus.items():
        f = RACINE / rel
        if not f.exists() or f.read_text(encoding="utf-8").replace("\r\n", "\n") != contenu:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(contenu, encoding="utf-8", newline="\n")
            ecrits.append(rel)
    for rel in orphelins(attendus):
        (RACINE / rel).unlink()
        ecrits.append(f"{rel} (supprimé)")
    return ecrits


def main(args: list[str]) -> int:
    if "--verifier" in args:
        problemes = ecarts()
        for p in problemes:
            print(p)
        if problemes:
            print("Intégrations à régénérer : python scripts/generer_integrations.py")
            return 1
        print("Intégrations à jour.")
        return 0
    ecrits = generer()
    print("\n".join(ecrits) if ecrits else "Rien à régénérer : intégrations à jour.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
