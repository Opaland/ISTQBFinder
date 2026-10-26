#!/usr/bin/env python3
"""Génère les fichiers d'intégration des autres assistants depuis la source unique `.claude/`.

    python scripts/generer_integrations.py              # (ré)écrit les fichiers générés
    python scripts/generer_integrations.py --verifier   # code 1 si un fichier n'est pas à jour

Source unique (à modifier) : `.claude/agents/*.md` et `.claude/skills/*/` ; consignes
communes dans `AGENTS.md`. Fichiers générés (à ne jamais modifier à la main) :

- GitHub Copilot : `.github/agents/<agent>.agent.md`. Les skills n'ont pas besoin de copie :
  Copilot (VS Code et Copilot CLI) lit `.claude/skills/` directement.
- Gemini CLI (qui ne lit pas `.claude/`) : `.gemini/skills/<skill>/` (copie, liens relatifs
  conservés), `.gemini/agents/<agent>.md` (sous-agents, `@thomas`), `.gemini/commands/<agent>.toml`
  (`/thomas <question>`) et `.gemini/settings.json` (contexte `AGENTS.md`, commandes `qa.py`
  en lecture seule pré-approuvées, reprises de `.claude/settings.json`).
  `.gemini/skills/` plutôt que `.agents/skills/`, que Copilot lit aussi (skills en double).

- Plugin Claude Code (#184, `docs/plugin.md`) : `plugin/` — manifeste et marketplace locale
  (`.claude-plugin/`), skills et agents recopiés avec `qa <commande>` à la place de
  `python qa.py <commande>`, lanceur `bin/qa` (la CLI du clone, avec le Python de son venv)
  et serveur MCP en lecture seule déclaré. Le plugin ne contient ni la CLI ni les PDF : il
  se charge en place depuis un clone installé (`installer.sh`).

Le test `tests/test_integrations.py` échoue si un fichier généré n'est pas à jour.
"""
import json
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
AGENTS_CLAUDE = RACINE / ".claude" / "agents"
SKILLS_CLAUDE = RACINE / ".claude" / "skills"
REGLAGES_CLAUDE = RACINE / ".claude" / "settings.json"
MARQUE = "Fichier généré par scripts/generer_integrations.py"

# Outils Claude Code → alias Copilot (docs.github.com/en/copilot/reference/custom-agents-configuration).
OUTILS_COPILOT = {"Bash": "execute", "Read": "read", "Grep": "search", "Glob": "search",
                  "WebSearch": "web", "WebFetch": "web"}

# Outils Claude Code → outils intégrés de Gemini CLI (geminicli.com/docs/reference/tools).
OUTILS_GEMINI = {"Bash": "run_shell_command", "Read": "read_file", "Grep": "grep_search", "Glob": "glob",
                 "WebSearch": "google_web_search", "WebFetch": "web_fetch"}


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


def agent_gemini(chemin: Path) -> str:
    champs, corps = lire_entete(chemin.read_text(encoding="utf-8"))
    entete = ["---",
              f"name: {champs['name']}",
              f"description: {json.dumps(champs['description'], ensure_ascii=False)}",
              "kind: local",
              "tools:", *[f"  - {o}" for o in outils(champs, OUTILS_GEMINI)],
              "---", ""]
    return "\n".join(entete) + preambule(chemin.name, champs, "Gemini CLI", "read_file") + corps


def chaine_toml(texte: str) -> str:
    """Chaîne TOML multiligne « basique » (échappe \\ et \")."""
    return '"""\n' + texte.replace("\\", "\\\\").replace('"', '\\"') + '"""'


def commande_gemini(chemin: Path) -> str:
    """`/thomas <question>` : le prompt de l'agent joué dans la conversation principale."""
    champs, corps = lire_entete(chemin.read_text(encoding="utf-8"))
    nom = champs["name"]
    # Le marqueur est déjà en commentaire TOML : inutile de l'envoyer au modèle.
    prompt = (preambule(chemin.name, champs, "Gemini CLI (commande /" + nom + ")", "read_file").split("\n", 2)[2]
              + "> Ici tu réponds directement dans la conversation (pas en sous-agent) : tu peux poser "
              "toi-même les questions de cadrage. Pour une délégation en sous-agent : `@" + nom + "`.\n\n"
              + corps.rstrip("\n") + "\n\n## Demande de l'utilisateur\n\n{{args}}\n")
    description = champs["description"].split(". ")[0].rstrip(".") + "."
    return (f"# {MARQUE} depuis .claude/agents/{chemin.name} : ne pas modifier, relancer le script.\n"
            f"description = {json.dumps(description, ensure_ascii=False)}\n"
            f"prompt = {chaine_toml(prompt)}\n")


def skill_gemini(dossier: Path) -> dict[str, str]:
    """Copie du skill : en-tête réduit à name/description (allowed-tools, argument-hint sont
    propres à Claude Code), arborescence conservée pour que les liens relatifs restent valides."""
    fichiers = {}
    for f in sorted(p for p in dossier.rglob("*") if p.is_file()):
        rel = f.relative_to(dossier).as_posix()
        source = f".claude/skills/{dossier.name}/{rel}"
        texte = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        marque = f"<!-- {MARQUE} depuis {source} : ne pas modifier, relancer le script. -->\n"
        if rel == "SKILL.md":
            champs, corps = lire_entete(texte)
            texte = ("---\n"
                     f"name: {champs['name']}\n"
                     f"description: {json.dumps(champs['description'], ensure_ascii=False)}\n"
                     "---\n" + marque + "\n" + corps)
        elif f.suffix == ".md":
            texte = marque + "\n" + texte
        fichiers[f".gemini/skills/{dossier.name}/{rel}"] = texte
    return fichiers


def commandes_lecture() -> list[str]:
    """Commandes pré-approuvées de `.claude/settings.json` au format Gemini (préfixes)."""
    regles = json.loads(REGLAGES_CLAUDE.read_text(encoding="utf-8"))["permissions"]["allow"]
    commandes = []
    for regle in regles:
        if regle.startswith("Bash(") and regle.endswith(")"):
            commande = regle[5:-1].removesuffix(":*").strip()
            commandes.append(f"run_shell_command({commande})")
    return commandes


def reglages_gemini() -> str:
    reglages = {"context": {"fileName": ["AGENTS.md"]},
                "tools": {"allowed": commandes_lecture()}}
    return json.dumps(reglages, ensure_ascii=False, indent=2) + "\n"


# ---------------------------------------------------------------- plugin Claude Code (#184)

PLUGIN = "plugin"
NOM_PLUGIN = "istqbfinder"
MARKETPLACE = "istqbfinder-local"
SERVEUR_MCP = "istqbfinder"
# Nom complet des outils d'un serveur MCP fourni par un plugin :
# mcp__plugin_<plugin>_<serveur>__<outil> (code.claude.com/docs/en/mcp).
PREFIXE_MCP = f"mcp__plugin_{NOM_PLUGIN}_{SERVEUR_MCP}__"
OUTILS_MCP = ("chercher", "lire", "section", "page", "plan", "idee_chercher", "idee_voir", "confiance",
              "passages_lus")
DEPOT = "https://github.com/Opaland/ISTQBFinder"
EXECUTABLES = {f"{PLUGIN}/bin/qa"}  # fichiers générés à rendre exécutables

LANCEUR = """#!/bin/sh
# {marque} : ne pas modifier, relancer le script.
# Lanceur du plugin ISTQBFinder : `qa <commande>` = `python qa.py <commande>` du clone,
# avec le Python de son venv, depuis n'importe quel dossier (bin/ du plugin est dans le PATH
# de l'outil Bash ; le serveur MCP du plugin est `qa mcp`).
RACINE=$(cd "$(dirname "$0")/../.." && pwd)
if [ ! -f "$RACINE/qa.py" ]; then
  echo "ISTQBFinder : qa.py introuvable dans $RACINE. Le plugin se charge en place depuis un clone" >&2
  echo "installé : claude plugin marketplace add <clone>/plugin, puis claude plugin install {plugin}@{marketplace}." >&2
  exit 2
fi
for PY in "$RACINE/.venv/bin/python" "$RACINE/.venv/Scripts/python.exe"; do
  if [ -x "$PY" ]; then exec "$PY" "$RACINE/qa.py" "$@"; fi
done
for PY in python3 python; do
  if command -v "$PY" >/dev/null 2>&1; then exec "$PY" "$RACINE/qa.py" "$@"; fi
done
echo "ISTQBFinder : ni venv ($RACINE/.venv) ni Python dans le PATH. Lancer $RACINE/installer.sh." >&2
exit 2
"""


def vers_plugin(texte: str) -> str:
    """`python qa.py …` / `python3 qa.py …` → `qa …` (lanceur du plugin)."""
    return re.sub(r"\bpython3? qa\.py\b", "qa", texte)


def outils_skill_plugin(ligne: str) -> str:
    """`allowed-tools` du skill : règles Bash réécrites pour `qa`, doublons python/python3
    retirés, outils MCP en lecture seule ajoutés (pré-approuvés pendant le skill)."""
    regles = []
    for r in re.findall(r"Bash\([^)]*\)|[A-Za-z_][\w*]*", ligne):
        r = vers_plugin(r)
        if r not in regles:
            regles.append(r)
    return ", ".join(regles + [PREFIXE_MCP + "*"])


def avertissement_plugin(source: str, avec_racine: bool = True) -> str:
    lignes = [f"<!-- {MARQUE} depuis {source} : ne pas modifier, relancer le script. -->", "",
              "> **Version plugin** d'ISTQBFinder (Claude Code hors du clone ; source unique : "
              f"`{source}` du dépôt).",
              "> - `qa <commande>` remplace `python qa.py <commande>` : lanceur fourni par le plugin, "
              "utilisable depuis n'importe quel dossier (CLI du clone, Python de son venv).",
              "> - Lecture : les outils MCP `" + "`, `".join(OUTILS_MCP) + f"` du serveur `{SERVEUR_MCP}` "
              "donnent les mêmes sorties que les commandes du même nom (`idee_chercher` = `idee chercher`) ; "
              "`passages_lus` dit si une référence a été lue dans la session. Toute écriture passe par "
              "`qa`, avec l'accord explicite de l'utilisateur."]
    if avec_racine:
        lignes.append("> - Les chemins `bibliotheque/`, `referentiel/`, `connaissances/`, `docs/` sont "
                      "relatifs au clone : `${CLAUDE_PLUGIN_ROOT}/..`.")
    return "\n".join(lignes) + "\n\n"


def skill_plugin(dossier: Path) -> dict[str, str]:
    fichiers = {}
    for f in sorted(p for p in dossier.rglob("*") if p.is_file()):
        rel = f.relative_to(dossier).as_posix()
        source = f".claude/skills/{dossier.name}/{rel}"
        texte = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        if rel == "SKILL.md":
            lignes = texte.split("\n")
            fin = lignes.index("---", 1)
            entete = [f"allowed-tools: {outils_skill_plugin(l.split(':', 1)[1])}" if l.startswith("allowed-tools:")
                      else l for l in lignes[1:fin]]
            corps = "\n".join(lignes[fin + 1:]).lstrip("\n")
            texte = "\n".join(["---", *entete, "---"]) + "\n" + avertissement_plugin(source) + vers_plugin(corps)
        elif f.suffix == ".md":
            # Lus avec Read : ${CLAUDE_PLUGIN_ROOT} n'y serait pas remplacé.
            texte = avertissement_plugin(source, avec_racine=False) + vers_plugin(texte)
        fichiers[f"{PLUGIN}/skills/{dossier.name}/{rel}"] = texte
    return fichiers


def agent_plugin(chemin: Path) -> str:
    lignes = chemin.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    fin = lignes.index("---", 1)
    entete = []
    for l in lignes[1:fin]:
        if l.startswith("tools:"):
            # Un sous-agent n'a que les outils listés : on y ajoute ceux du serveur MCP.
            l += ", " + ", ".join(PREFIXE_MCP + o for o in OUTILS_MCP)
        elif l.startswith("  - ") and entete and entete[-1].startswith(("skills:", "  - ")):
            l = f"  - {NOM_PLUGIN}:{l[4:].strip()}"  # skills d'un plugin : <plugin>:<skill>
        entete.append(l)
    corps = "\n".join(lignes[fin + 1:]).lstrip("\n")
    corps = corps.replace(".claude/skills/", "${CLAUDE_PLUGIN_ROOT}/skills/")
    return ("\n".join(["---", *entete, "---"]) + "\n"
            + avertissement_plugin(f".claude/agents/{chemin.name}") + vers_plugin(corps))


def manifeste_plugin() -> str:
    manifeste = {
        "name": NOM_PLUGIN,
        "displayName": "ISTQBFinder",
        "version": "0.1.0",
        "description": "Assistant de connaissances QA : syllabus ISTQB locaux (FR/EN) cités page et section, "
                       "base d'idées QA capitalisées, agents Thomas (chercheur) et Sylvie (auditrice). "
                       "Se charge en place depuis un clone installé du dépôt (installer.sh).",
        "author": {"name": "Opaland", "url": "https://github.com/Opaland"},
        "homepage": f"{DEPOT}/blob/main/docs/plugin.md",
        "repository": DEPOT,
        "license": "MIT",
        "keywords": ["istqb", "qa", "test", "syllabus", "tmmi"],
        "mcpServers": {SERVEUR_MCP: {"command": "${CLAUDE_PLUGIN_ROOT}/bin/qa", "args": ["mcp"]}},
    }
    return json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n"


def marketplace_plugin() -> str:
    """Marketplace LOCALE : dans `plugin/`, pas à la racine du dépôt, pour qu'elle ne s'ajoute
    que depuis un clone (`claude plugin marketplace add <clone>/plugin`), jamais depuis GitHub."""
    m = {"name": MARKETPLACE,
         "owner": {"name": "Opaland", "url": "https://github.com/Opaland"},
         "description": "Marketplace locale d'ISTQBFinder, à ajouter depuis un clone installé.",
         "plugins": [{"name": NOM_PLUGIN, "source": "./",
                      "description": "Syllabus ISTQB cités, base d'idées QA, agents Thomas et Sylvie (lecture "
                                     "par serveur MCP, écritures soumises à l'accord de l'utilisateur)."}]}
    return json.dumps(m, ensure_ascii=False, indent=2) + "\n"


def lisez_moi_plugin() -> str:
    return f"""<!-- {MARQUE} : ne pas modifier, relancer le script. -->

# Plugin Claude Code ISTQBFinder

Skills `qa-knowledge`, `bibliotheque` et `ajouter-syllabus`, agents Thomas (chercheur) et
Sylvie (auditrice), et serveur MCP local en lecture seule d'ISTQBFinder, utilisables dans
Claude Code depuis **n'importe quel projet**. Généré depuis `.claude/` par
`scripts/generer_integrations.py`. Choix, limites et décisions en attente :
[docs/plugin.md](../docs/plugin.md).

Le plugin ne contient ni la CLI ni les syllabus : il se charge **en place** depuis un clone
installé avec `installer.sh` (les PDF restent dans ce dépôt, voir `NOTICE.md`).

```bash
cd /chemin/ISTQBFinder && ./installer.sh
.venv/bin/python -m pip install -r requirements-mcp.txt
claude plugin marketplace add /chemin/ISTQBFinder/plugin
claude plugin install {NOM_PLUGIN}@{MARKETPLACE}
```

Licence : MIT (code et documentation), comme le dépôt ; les syllabus n'en relèvent pas.
"""


def fichiers_plugin() -> dict[str, str]:
    fichiers = {f"{PLUGIN}/.claude-plugin/plugin.json": manifeste_plugin(),
                f"{PLUGIN}/.claude-plugin/marketplace.json": marketplace_plugin(),
                f"{PLUGIN}/README.md": lisez_moi_plugin(),
                f"{PLUGIN}/bin/qa": LANCEUR.replace("{marque}", MARQUE).replace("{plugin}", NOM_PLUGIN)
                                           .replace("{marketplace}", MARKETPLACE)}
    for chemin in sorted(AGENTS_CLAUDE.glob("*.md")):
        fichiers[f"{PLUGIN}/agents/{chemin.name}"] = agent_plugin(chemin)
    for dossier in sorted(d for d in SKILLS_CLAUDE.iterdir() if (d / "SKILL.md").exists()):
        fichiers.update(skill_plugin(dossier))
    return fichiers


def fichiers_attendus() -> dict[str, str]:
    """Chemin relatif (POSIX) → contenu attendu de chaque fichier généré."""
    attendus = {}
    for chemin in sorted(AGENTS_CLAUDE.glob("*.md")):
        attendus[f".github/agents/{chemin.stem}.agent.md"] = agent_copilot(chemin)
        attendus[f".gemini/agents/{chemin.stem}.md"] = agent_gemini(chemin)
        attendus[f".gemini/commands/{chemin.stem}.toml"] = commande_gemini(chemin)
    for dossier in sorted(d for d in SKILLS_CLAUDE.iterdir() if (d / "SKILL.md").exists()):
        attendus.update(skill_gemini(dossier))
    attendus[".gemini/settings.json"] = reglages_gemini()
    attendus.update(fichiers_plugin())
    return attendus


def dossiers_geres() -> list[Path]:
    return [RACINE / ".github" / "agents", RACINE / ".gemini", RACINE / PLUGIN]


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
        if rel in EXECUTABLES and os.name != "nt" and not os.access(f, os.X_OK):
            f.chmod(0o755)
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
