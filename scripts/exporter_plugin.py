#!/usr/bin/env python3
"""Exporte le plugin Claude Code ISTQBFinder **autonome** (#184), sans aucun syllabus.

    python scripts/exporter_plugin.py <dossier_cible> [--version X.Y.Z]

Produit l'arborescence complète du dépôt dédié `Opaland/ISTQBFinder-plugin` (docs/plugin.md,
§ 6) :

- manifeste `.claude-plugin/plugin.json` (serveur MCP `istqbfinder` = `${CLAUDE_PLUGIN_ROOT}/bin/qa
  mcp`) et marketplace `.claude-plugin/marketplace.json` à la racine, pour
  `claude plugin marketplace add Opaland/ISTQBFinder-plugin` ;
- skills et agents de `.claude/` (version plugin, avec l'en-tête « autonome »), plus le skill
  `installer` (premier usage) ;
- lanceurs `bin/qa` (sh), `bin/qa.cmd` (Windows) et `lanceur.py` : venv et données dans
  `${CLAUDE_PLUGIN_DATA}`, jamais dans le dossier du plugin ;
- le code (`qa.py`, `qak/`, `requirements*.txt`, `catalogue/`, `referentiel/`), un README
  d'installation, `LICENSE` (MIT, code seulement) et `NOTICE.md`.

**Aucun PDF, aucun fichier de `bibliotheque/sources/`** : `verifier()` le contrôle après
écriture (extension et empreinte SHA-256 de chaque fichier), et l'export échoue sinon.

Le dossier cible doit être vide, un export précédent ou un clone du dépôt du plugin : tout y est
remplacé, sauf `.git/`. La version vaut par défaut `VERSION+<commit court>`, pour que chaque
export publié soit vu comme une mise à jour (`version` fige la version installée).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MODELES = Path(__file__).resolve().parent / "plugin_autonome"

_spec = importlib.util.spec_from_file_location("generer_integrations", RACINE / "scripts" / "generer_integrations.py")
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

NOM = gen.NOM_PLUGIN                   # istqbfinder : espace de noms des skills et agents
MARKETPLACE = "istqbfinder"            # claude plugin install istqbfinder@istqbfinder
DEPOT_PLUGIN = "https://github.com/Opaland/ISTQBFinder-plugin"
VERSION = "1.0.0"
CODE_DOSSIERS = ("qak", "catalogue", "referentiel")
EXECUTABLES = ("bin/qa", "lanceur.py")
REQUIS = (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", "README.md", "LICENSE", "NOTICE.md",
          "bin/qa", "bin/qa.cmd", "lanceur.py", "qa.py", "qak/cli.py", "qak/serveur_mcp.py", "requirements.txt",
          "requirements-mcp.txt", "catalogue/istqb.json", "referentiel/taxonomie.json",
          "skills/qa-knowledge/SKILL.md", "skills/bibliotheque/SKILL.md", "skills/ajouter-syllabus/SKILL.md",
          "skills/installer/SKILL.md", "agents/thomas.md", "agents/sylvie.md")
DESCRIPTION = ("Assistant de connaissances QA : syllabus ISTQB (téléchargés au premier usage depuis istqb.org) "
               "cités page et section, base d'idées QA, agents Thomas (chercheur) et Sylvie (auditrice), "
               "serveur MCP local en lecture seule. Aucun syllabus n'est inclus.")


def commit_source() -> str:
    try:
        r = subprocess.run(["git", "-C", str(RACINE), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else "inconnu"
    except (OSError, subprocess.SubprocessError):
        return "inconnu"


def avertissement_autonome(source: str, avec_chemins: bool = True) -> str:
    lignes = [f"<!-- {gen.MARQUE} depuis {source} (dépôt Opaland/ISTQBFinder), exporté par "
              "scripts/exporter_plugin.py : ne pas modifier, réexporter. -->", "",
              "> **Version plugin autonome** d'ISTQBFinder (source unique : `" + source + "` du dépôt "
              "Opaland/ISTQBFinder).",
              "> - `qa <commande>` remplace `python qa.py <commande>` : lanceur du plugin, utilisable depuis "
              "n'importe quel dossier. `qa emplacements` montre le dossier de données (venv, bibliothèque, "
              "base d'idées), jamais celui du plugin.",
              "> - Lecture : les outils MCP `" + "`, `".join(gen.OUTILS_MCP) + f"` du serveur `{gen.SERVEUR_MCP}` "
              "donnent les mêmes sorties que les commandes du même nom (`idee_chercher` = `idee chercher`) ; "
              "`passages_lus` dit si une référence a été lue dans la session. Toute écriture passe par "
              "`qa`, avec l'accord explicite de l'utilisateur.",
              "> - Bibliothèque vide (`qa inventaire`) : proposer à l'utilisateur `/istqbfinder:installer` "
              "(syllabus anglais téléchargés depuis istqb.org). Les traductions françaises ne sont pas "
              "téléchargées : l'utilisateur les dépose avec `qa importer --prive <fichier>`.",
              "> - Base d'idées : celle du dossier de données (une base par installation). Ce dossier n'est "
              "pas un dépôt Git : les consignes de commit, de branche ou de PR ne s'appliquent pas."]
    if avec_chemins:
        lignes.append("> - Chemins : `bibliotheque/` et `connaissances/` sont dans le dossier de données "
                      "(`qa emplacements`) ; `referentiel/` est `${CLAUDE_PLUGIN_ROOT}/referentiel/` ; "
                      "`docs/` est en ligne : " + gen.DEPOT + "/tree/main/docs.")
    return "\n".join(lignes) + "\n\n"


def _source(rel: str) -> str:
    """plugin/skills/<s>/<f> → .claude/skills/<s>/<f> ; plugin/agents/<a> → .claude/agents/<a>."""
    return ".claude/" + rel.split("/", 1)[1]


def _corps_autonome(texte: str) -> str:
    """Chemins du clone réécrits dans le corps (après l'en-tête YAML, où rien n'est remplacé)."""
    entete, sep, corps = texte.partition("\n---\n") if texte.startswith("---\n") else ("", "", texte)
    corps = re.sub(r"(?<![\w/{}.])referentiel/", "${CLAUDE_PLUGIN_ROOT}/referentiel/", corps)
    corps = re.sub(r"(?<![\w/])docs/([\w-]+\.md)", gen.DEPOT + r"/blob/main/docs/\1", corps)
    return entete + sep + corps


def composants() -> dict[str, str]:
    """Skills et agents : ceux du plugin du clone (même générateur), en-tête « autonome »."""
    fichiers = {}
    for rel, texte in gen.fichiers_plugin().items():
        if not rel.startswith((f"{gen.PLUGIN}/skills/", f"{gen.PLUGIN}/agents/")):
            continue
        source = _source(rel)
        lu_par_read = rel.startswith(f"{gen.PLUGIN}/skills/") and not rel.endswith("/SKILL.md")
        ancien = gen.avertissement_plugin(source, avec_racine=not lu_par_read)
        if ancien not in texte:
            raise RuntimeError(f"en-tête du plugin introuvable dans {rel} : générateur modifié ?")
        repere = "\x00EN-TETE\x00"
        texte = texte.replace(ancien, repere)
        # Lus avec Read, les fichiers reference/ ne profitent pas du remplacement de ${CLAUDE_PLUGIN_ROOT}.
        texte = texte if lu_par_read else _corps_autonome(texte)
        fichiers[rel.split("/", 1)[1]] = texte.replace(repere, avertissement_autonome(source, not lu_par_read))
    fichiers["skills/installer/SKILL.md"] = (MODELES / "installer.md").read_text(encoding="utf-8")
    return fichiers


def manifeste(version: str, commit: str) -> str:
    m = {"name": NOM,
         "displayName": "ISTQBFinder",
         "version": version,
         "description": DESCRIPTION,
         "author": {"name": "Opaland", "url": "https://github.com/Opaland"},
         "homepage": f"{DEPOT_PLUGIN}#readme",
         "repository": DEPOT_PLUGIN,
         "license": "MIT",
         "keywords": ["istqb", "qa", "test", "syllabus", "tmmi"],
         "mcpServers": {gen.SERVEUR_MCP: {"command": "${CLAUDE_PLUGIN_ROOT}/bin/qa", "args": ["mcp"]}},
         "metadata": {"source": gen.DEPOT, "commit": commit}}
    return json.dumps(m, ensure_ascii=False, indent=2) + "\n"


def marketplace() -> str:
    m = {"name": MARKETPLACE,
         "owner": {"name": "Opaland", "url": "https://github.com/Opaland"},
         "description": "Marketplace du plugin ISTQBFinder (dépôt dédié, sans aucun syllabus).",
         "plugins": [{"name": NOM, "source": "./", "description": DESCRIPTION}]}
    return json.dumps(m, ensure_ascii=False, indent=2) + "\n"


def fichiers_texte(version: str, commit: str) -> dict[str, str]:
    """Chemin relatif (POSIX) → contenu, pour tout le dépôt du plugin."""
    def modele(nom: str) -> str:
        return (MODELES / nom).read_text(encoding="utf-8").replace("{commit}", commit).replace("{version}", version)

    fichiers = {".claude-plugin/plugin.json": manifeste(version, commit),
                ".claude-plugin/marketplace.json": marketplace(),
                "README.md": modele("README.md"),
                "NOTICE.md": modele("NOTICE.md"),
                "LICENSE": (RACINE / "LICENSE").read_text(encoding="utf-8"),
                "bin/qa": (MODELES / "qa.sh").read_text(encoding="utf-8"),
                "bin/qa.cmd": (MODELES / "qa.cmd").read_text(encoding="utf-8"),
                "lanceur.py": (MODELES / "lanceur.py").read_text(encoding="utf-8"),
                ".gitattributes": "* text=auto eol=lf\n",
                ".gitignore": "__pycache__/\n*.pyc\n# Aucun document dans ce dépôt (NOTICE.md)\n*.pdf\n"}
    fichiers.update(composants())
    code = [RACINE / "qa.py", *sorted(RACINE.glob("requirements*.txt"))]
    for dossier in CODE_DOSSIERS:
        code += sorted(f for f in (RACINE / dossier).rglob("*")
                       if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc")
    for f in code:
        fichiers[f.relative_to(RACINE).as_posix()] = f.read_text(encoding="utf-8")
    return fichiers


def _vider(cible: Path) -> None:
    """Accepte un dossier vide, un export précédent ou un clone du dépôt du plugin ; garde `.git/`."""
    contenu = [p for p in cible.iterdir() if p.name != ".git"] if cible.exists() else []
    if contenu:
        try:
            ancien = json.loads((cible / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["name"]
        except (OSError, ValueError, KeyError):
            ancien = None
        if ancien != NOM:
            raise SystemExit(f"{cible} n'est ni vide ni un export du plugin {NOM} : rien n'est écrit.")
    for p in contenu:
        shutil.rmtree(p) if p.is_dir() and not p.is_symlink() else p.unlink()


def empreintes_sources() -> set[str]:
    sources = RACINE / "bibliotheque" / "sources"
    return {hashlib.sha256(f.read_bytes()).hexdigest() for f in sources.rglob("*") if f.is_file()} \
        if sources.exists() else set()


def verifier(cible: Path) -> list[str]:
    """Problèmes de l'export (liste vide = conforme)."""
    problemes = []
    interdits = empreintes_sources()
    for f in sorted(p for p in cible.rglob("*") if p.is_file() and ".git" not in p.relative_to(cible).parts):
        rel = f.relative_to(cible).as_posix()
        donnees = f.read_bytes()
        if f.suffix.lower() == ".pdf" or donnees.startswith(b"%PDF"):
            problemes.append(f"PDF interdit : {rel}")
        # Aucun dossier de données (bibliotheque/, connaissances/) ; le skill « bibliotheque » est permis.
        if rel.startswith(("bibliotheque/", "connaissances/")) or hashlib.sha256(donnees).hexdigest() in interdits:
            problemes.append(f"fichier de bibliotheque/ interdit : {rel}")
    problemes += [f"fichier requis absent : {r}" for r in REQUIS if not (cible / r).is_file()]
    for r in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        try:
            json.loads((cible / r).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            problemes.append(f"{r} illisible : {exc}")
    return problemes


def exporter(cible: Path, version: str | None = None) -> list[str]:
    """Écrit l'export dans `cible` ; renvoie les problèmes de `verifier()` (vide = conforme)."""
    commit = commit_source()
    version = version or f"{VERSION}+{commit[:12]}"
    fichiers = fichiers_texte(version, commit)
    _vider(cible)
    for rel, contenu in fichiers.items():
        f = cible / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(contenu, encoding="utf-8", newline="\n")
    if os.name != "nt":
        for rel in EXECUTABLES:
            (cible / rel).chmod(0o755)
    return verifier(cible)


def main(args: list[str]) -> int:
    p = argparse.ArgumentParser(description="Exporte le plugin ISTQBFinder autonome (sans aucun syllabus).")
    p.add_argument("cible", type=Path, help="dossier du dépôt du plugin (vide, export précédent ou clone)")
    p.add_argument("--version", help=f"version du plugin (défaut : {VERSION}+<commit court>)")
    a = p.parse_args(args)
    problemes = exporter(a.cible.resolve(), a.version)
    for pb in problemes:
        print(pb, file=sys.stderr)
    if problemes:
        print("Export NON conforme : ne pas publier.", file=sys.stderr)
        return 1
    n = sum(1 for f in a.cible.rglob("*") if f.is_file() and ".git" not in f.relative_to(a.cible).parts)
    print(f"Plugin exporté dans {a.cible} ({n} fichiers, aucun PDF). "
          f"Contrôle : claude plugin validate --strict {a.cible}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
