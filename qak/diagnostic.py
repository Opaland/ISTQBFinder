"""Diagnostic d'installation (`python qa.py diagnostic`) : environnement, index, recherche
témoin, base d'idées et fichiers d'intégration des assistants. Lecture seule.

Chaque contrôle rend (état, sujet, détail) : OK, KO (bloquant : code retour 1) ou
« -- » (à faire, non bloquant : par exemple une CLI d'assistant non installée, ou des
fichiers d'intégration à régénérer après une permission ajoutée)."""
import importlib.util
import shutil
import sqlite3
import sys

from . import bibliotheque, chemins, connaissances, recherche

ASSISTANTS = ("claude", "copilot", "gemini")
REQUETE_TEMOIN = "risk-based testing"


def _environnement() -> list[tuple]:
    v = sys.version_info
    etats = [("OK" if v >= (3, 10) else "KO", "Python", f"{v.major}.{v.minor}.{v.micro}"
              + ("" if v >= (3, 10) else " : Python 3.10 ou plus récent est requis"))]
    try:
        sqlite3.connect(":memory:").execute("CREATE VIRTUAL TABLE t USING fts5(x)")
        etats.append(("OK", "SQLite FTS5", sqlite3.sqlite_version))
    except sqlite3.OperationalError:
        etats.append(("KO", "SQLite FTS5", "absent de ce Python : la recherche est impossible"))
    pypdf = importlib.util.find_spec("pypdf") is not None
    etats.append(("OK" if pypdf else "KO", "pypdf",
                  "installé" if pypdf else "absent : `pip install -r requirements.txt` (dans le venv)"))
    return etats


def _bibliotheque() -> list[tuple]:
    docs = bibliotheque.inventaire()
    if not docs:
        return [("KO", "Index", "vide : lancer `python qa.py actualiser` (≈ 3 min sur un clone neuf)")]
    defauts = [d["doc_id"] for d in docs if d["statut_extraction"] != "ok"]
    etats = [("OK", "Index", f"{len(docs)} documents, {sum(d['nb_passages'] for d in docs)} passages"
              + (f" ; à surveiller : {', '.join(defauts)}" if defauts else ""))]
    trouves = recherche.chercher(REQUETE_TEMOIN, n=3)["resultats"]
    etats.append(("OK" if trouves else "KO", "Recherche témoin",
                  f"« {REQUETE_TEMOIN} » → {trouves[0]['doc_id']} p. {trouves[0]['page']}" if trouves
                  else f"« {REQUETE_TEMOIN} » sans résultat : relancer `python qa.py actualiser`"))
    return etats


def _base_idees() -> list[tuple]:
    try:
        n = len(connaissances.lister())
    except (sqlite3.Error, ValueError) as exc:
        return [("KO", "Base d'idées", f"illisible ({exc})")]
    return [("OK", "Base d'idées", f"{n} idées")]


def _integrations() -> list[tuple]:
    script = chemins.CODE / "scripts" / "generer_integrations.py"
    if not script.exists():
        return []
    spec = importlib.util.spec_from_file_location("generer_integrations", script)
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    ecarts = gen.ecarts()
    # Maintenance du dépôt, pas de l'installation (#163) : une permission ajoutée par
    # l'utilisateur (`/permissions`, portée projet) suffit à périmer `.gemini/settings.json`.
    # Avertissement « -- » ici ; la CI reste bloquante (tests/test_integrations.py).
    if not ecarts:
        return [("OK", "Fichiers d'intégration", "à jour")]
    return [("--", "Fichiers d'intégration",
             f"{len(ecarts)} à régénérer ({', '.join(ecarts)}), non bloquant : `.claude/` a changé "
             "(une permission ajoutée, par exemple). Pour aligner Copilot et Gemini : "
             "`python scripts/generer_integrations.py` ; sinon, rien à faire.")]


def _assistant(nom: str) -> list[tuple]:
    racine = chemins.CODE
    if nom == "claude":
        fichiers = [racine / ".claude" / "skills" / "qa-knowledge" / "SKILL.md", racine / ".claude" / "agents"]
        clis, aide = ["claude"], "installer Claude Code (ou utiliser l'appli de bureau, onglet Code)"
    elif nom == "copilot":
        fichiers = [racine / "AGENTS.md", racine / ".github" / "agents" / "thomas.agent.md"]
        clis, aide = ["code", "copilot"], "installer VS Code + GitHub Copilot Chat, ou Copilot CLI"
    else:
        fichiers = [racine / ".gemini" / "settings.json", racine / ".gemini" / "commands" / "thomas.toml"]
        clis, aide = ["gemini"], "npm install -g @google/gemini-cli"
    absents = [f.relative_to(racine).as_posix() for f in fichiers if not f.exists()]
    etats = [("KO" if absents else "OK", f"{nom} : fichiers",
              f"absents : {', '.join(absents)}" if absents else "présents")]
    trouvees = [c for c in clis if shutil.which(c)]
    etats.append(("OK", f"{nom} : CLI", ", ".join(trouvees)) if trouvees
                 else ("--", f"{nom} : CLI", f"{' / '.join(clis)} introuvable dans le PATH : {aide}"))
    return etats


def diagnostic(assistants: list[str] | tuple = ()) -> list[tuple]:
    etats = _environnement() + _bibliotheque() + _base_idees() + _integrations()
    for nom in assistants:
        etats += _assistant(nom)
    return etats
