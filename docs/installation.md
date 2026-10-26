# Installation

Deux temps : **1. le dépôt** (Python, index, contrôle), commun à tous les assistants ;
**2. l'assistant** de votre choix : Claude Code, GitHub Copilot ou Gemini CLI. La CLI
`python qa.py` ne dépend d'aucun assistant.

## 1. Le dépôt (une fois par poste)

Prérequis : **Git** et **Python ≥ 3.10** ([python.org](https://www.python.org/downloads/) ;
sous Windows, cocher « Add python.exe to PATH » ; Debian/Ubuntu : `sudo apt install python3 python3-venv`).

```bash
git clone https://github.com/Opaland/ISTQBFinder && cd ISTQBFinder
./installer.sh                         # Linux / macOS
```

```powershell
git clone https://github.com/Opaland/ISTQBFinder; cd ISTQBFinder
powershell -ExecutionPolicy Bypass -File installer.ps1     # Windows
```

Le script, relançable sans risque (rien n'est refait inutilement) :

1. vérifie Python ≥ 3.10 ;
2. crée l'environnement virtuel `.venv` (ou réutilise l'existant) ;
3. installe `requirements.txt` (`pypdf`, `pytest`) ;
4. indexe les PDF de `bibliotheque/sources/` (`qa.py actualiser` : ≈ 3 min la première fois,
   quelques secondes ensuite) ;
5. lance `qa.py diagnostic` et affiche une ligne par contrôle (sortie réelle du 2026-10-22,
   Linux, Python 3.13 ; versions et nombres varient selon le poste et l'index) :

```
OK  Python                     3.13.16
OK  SQLite FTS5                3.45.1
OK  pypdf                      installé
OK  Index                      42 documents, 6743 passages
OK  Recherche témoin           « risk-based testing » → CTAL-TA-4.0-fr p. 26
OK  Base d'idées               0 idées
OK  Fichiers d'intégration     à jour

Diagnostic : OK
```

`KO` = bloquant (le script s'arrête, code retour 1, avec la commande qui répare) ;
`--` = à faire, non bloquant (par exemple la CLI d'un assistant pas encore installée, ou
« Fichiers d'intégration … à régénérer » après une permission ajoutée à `.claude/settings.json` :
`python scripts/generer_integrations.py` les réaligne pour Copilot et Gemini).

Option `--assistant claude|copilot|gemini|tous` (Windows : `-Assistant gemini`) : contrôle
en plus les fichiers d'intégration de l'assistant et la présence de sa CLI dans le `PATH`.
Le diagnostic se relance seul à tout moment : `python qa.py diagnostic --assistant tous`.

**Toujours lancer l'assistant venv activé**, depuis la racine du dépôt :
`source .venv/bin/activate` (Windows : `.\.venv\Scripts\Activate.ps1`). Les commandes
de recherche marchent avec n'importe quel Python ≥ 3.10, mais `actualiser`, `importer` et
`telecharger` ont besoin de `pypdf`, installé dans le venv.

## 2. L'assistant

### Claude Code (référence)

Tout est prévu pour lui : skills `.claude/skills/`, agents Thomas et Sylvie, permissions en
lecture seule `.claude/settings.json`. Compte Claude Pro, Max, Team, Enterprise ou Console requis.

| Interface | Installation | Lancement |
|---|---|---|
| **Ligne de commande** | `curl -fsSL https://claude.ai/install.sh \| bash` (Windows : `irm https://claude.ai/install.ps1 \| iex`) | `claude` à la racine du dépôt |
| **Appli de bureau, onglet Code** | [claude.com/download](https://claude.com/download) | onglet **Code**, ouvrir le dossier du dépôt |
| **Extension VS Code** | extension « Claude Code » de la marketplace VS Code | ouvrir le dossier du dépôt, panneau Claude Code |

Vérifier : `./installer.sh --assistant claude`. Agents : `@agent-thomas <question>`,
`@agent-sylvie <démarche>`, ou `claude --agent thomas`.

Au premier lancement, **ouvrir le clone une fois en interactif** (`claude` à la racine) et
accepter le dossier : tant qu'il n'est pas approuvé, `claude -p` ignore les permissions de
`.claude/settings.json` et refuse les `python qa.py …`. Pour un usage scripté sans cette
étape, passer les outils explicitement (`--allowedTools`), comme `scripts/essais_agents.py`.

**claude.ai** (Web ou appli, onglet Chat) : **non pris en charge**. Un skill importé (zip)
n'y emporte ni la CLI `qa.py` ni la bibliothèque, et ne garde rien d'une conversation à
l'autre (voir README, « Où l'utiliser »).

### Plugin Claude Code (hors du clone)

Pour utiliser les skills, Thomas et Sylvie depuis **n'importe quel projet**, après
l'installation du clone et du SDK MCP (`.venv/bin/python -m pip install -r requirements-mcp.txt`,
sous Windows `.venv\Scripts\python -m pip install -r requirements-mcp.txt`) :

```bash
claude plugin marketplace add /chemin/ISTQBFinder/plugin
claude plugin install istqbfinder@istqbfinder-local
```

Le plugin se charge en place depuis le clone (aucune copie, ni des PDF ni de la CLI) :
`/istqbfinder:qa-knowledge`, `@agent-istqbfinder:thomas`, `@agent-istqbfinder:sylvie`, outils
MCP en lecture seule. Choix, permissions à ajouter et limites :
[docs/plugin.md](plugin.md).

### GitHub Copilot

Skills lus directement dans `.claude/skills/`, agents `.github/agents/*.agent.md` et consignes
`AGENTS.md` versionnés : rien à copier. Abonnement GitHub Copilot requis.

- **VS Code + Copilot Chat** : installer VS Code et l'extension GitHub Copilot Chat, ouvrir le
  dossier du dépôt (venv activé : `code .` depuis le terminal), passer le chat en **mode
  agent**, choisir `thomas` ou `sylvie` dans le sélecteur d'agents.
- **Copilot CLI** : `npm install -g @github/copilot`, puis `copilot` à la racine du dépôt
  (`copilot login` la première fois) ; `/agent` pour choisir Thomas ou Sylvie, ou
  `copilot --agent thomas -p "<question>"`.
- Permissions : voir README, « Utiliser avec GitHub Copilot » (`chat.tools.terminal.autoApprove`,
  `--allow-tool`) ; ne jamais pré-approuver les commandes qui écrivent.

Vérifier : `./installer.sh --assistant copilot`.

### Gemini CLI

- Installer : `npm install -g @google/gemini-cli` (Node.js 20 ou plus), puis `gemini` à la
  racine du dépôt et se connecter (compte Google ou clé `GEMINI_API_KEY`).
- Au premier lancement, **faire confiance au dossier** : sans cela, Gemini ignore
  `.gemini/settings.json`, les sous-agents et les commandes du projet.
- Skills : actifs par défaut (`skills.enabled`, pas d'activation à faire en 0.65) ; contrôle :
  `gemini skills list` (trois skills attendus).
- Thomas et Sylvie : `/thomas <question>`, `/sylvie <démarche>` (commandes), ou
  `@thomas` / `@sylvie` (sous-agents).

Vérifier : `./installer.sh --assistant gemini`. Limites : README, « Utiliser avec Gemini CLI ».

### Serveur MCP local en lecture seule (optionnel)

`python qa.py mcp` lance un serveur [MCP](https://modelcontextprotocol.io) sur stdio. Il
expose les commandes de **lecture** à tout client MCP (Claude Code, Claude Desktop, VS Code…),
y compris quand l'assistant n'est pas ouvert dans le clone :

| Outil MCP | Commande équivalente |
|---|---|
| `chercher` | `chercher <notions> [--doc] [--langue] [--section] [--theme] …` |
| `lire`, `section`, `page` | mêmes commandes ; la sortie garde la ligne `Citer : […]` à recopier et la borne `max_caracteres` |
| `plan` | `plan <doc>` |
| `idee_chercher`, `idee_voir` | `idee chercher`, `idee voir` |
| `confiance` | `confiance --base … --lus … --concordants …` ; rappelle en plus combien de passages le serveur a vu lire |
| `passages_lus` | propre au serveur : références lues dans la session, ou « LU / NON LU » pour une citation donnée |

Chaque outil appelle la CLI (`qak/cli.py`) : mêmes vérifications, mêmes messages d'erreur
en français. Le serveur **n'écrit rien** : capitaliser une idée, importer ou télécharger un
document reste dans la CLI, avec l'accord de l'utilisateur. Il relève chaque passage
affiché par `lire`, `section` ou `page` (en mémoire, pour la durée de la session, et une
ligne sur stderr, c'est-à-dire dans le journal du client MCP) : « lire avant de citer » se
vérifie avec `passages_lus`.

Installation (dans le venv du clone ; le SDK `mcp` ≥ 2.3 est **optionnel**, `pypdf` reste
la seule dépendance obligatoire) :

```bash
.venv/bin/python -m pip install -r requirements-mcp.txt     # Windows : .venv\Scripts\python -m pip …
.venv/bin/python qa.py mcp                                   # test : attend un client sur stdio (Ctrl+C)
```

Sans le SDK, `python qa.py mcp` répond « Le serveur MCP demande le SDK Python `mcp` … » et
s'arrête (code 2).

**Claude Code** — chemins **absolus** vers le Python du venv et vers `qa.py` (le serveur
trouve la bibliothèque à côté de `qa.py`, quel que soit le dossier ouvert) :

```bash
claude mcp add istqbfinder --scope user -- /chemin/ISTQBFinder/.venv/bin/python /chemin/ISTQBFinder/qa.py mcp
claude mcp list                     # « istqbfinder: … - ✓ Connected »
```

`--scope user` : disponible dans tous les projets ; `--scope local` (défaut) : ce projet
seulement ; `--scope project` écrit un `.mcp.json` à la racine du projet, de la forme :

```json
{"mcpServers": {"istqbfinder": {"command": "/chemin/ISTQBFinder/.venv/bin/python",
                                "args": ["/chemin/ISTQBFinder/qa.py", "mcp"]}}}
```

Claude Code demande d'approuver un serveur de `.mcp.json` au premier lancement interactif.
Les outils apparaissent sous les noms `mcp__istqbfinder__chercher`, `mcp__istqbfinder__lire`…
(à autoriser à la demande, ou par une règle `allow` qui ne nomme que ces outils de lecture).
Dans le clone lui-même, la CLI suffit : le serveur sert surtout **hors du clone**.

**Claude Desktop** (onglet Chat de l'appli de bureau) — menu Claude → Settings… → Developer
→ Edit Config, qui ouvre `claude_desktop_config.json`
(macOS : `~/Library/Application Support/Claude/claude_desktop_config.json` ;
Windows : `%APPDATA%\Claude\claude_desktop_config.json`), puis quitter et relancer l'appli :

```json
{
  "mcpServers": {
    "istqbfinder": {
      "command": "C:\\chemin\\ISTQBFinder\\.venv\\Scripts\\python.exe",
      "args": ["C:\\chemin\\ISTQBFinder\\qa.py", "mcp"]
    }
  }
}
```

(macOS : `"/chemin/ISTQBFinder/.venv/bin/python"` et `"/chemin/ISTQBFinder/qa.py"`.) Le journal
du serveur, dont le relevé des lectures, est dans `mcp-server-istqbfinder.log` (macOS :
`~/Library/Logs/Claude`, Windows : `%APPDATA%\Claude\logs`). Sans le skill, Claude Desktop
reçoit les règles (ordre de recherche, lire avant de citer, confiance) par les
`instructions` du serveur MCP ; il ne connaît ni Thomas ni Sylvie. **Non essayé en réel** :
pas d'appli de bureau dans l'environnement de développement.

**Paquet `.mcpb`** (extension Claude Desktop installable en un clic) : non produit pour
l'instant. Il ne peut pas embarquer les PDF (autorisation propre à ce dépôt, voir
`NOTICE.md`), devrait donc pointer vers un clone installé, et n'a pas pu être essayé dans
Claude Desktop : voir #200.

## Ce qui a été essayé

- `installer.sh` : exécuté sur un clone propre (Linux, Python 3.13) puis relancé
  (idempotence : 1,5 s, aucun fichier versionné modifié) ; la CI le rejoue à chaque push
  avec Python 3.10 (job `installation-linux`).
- `installer.ps1` : exécuté par la CI sous Windows PowerShell 5.1 (job `installation-windows`) ;
  non essayé sur un poste Windows réel.
- Serveur MCP : dialogue stdio réel avec le client du SDK officiel `mcp` 2.3.0
  (`tests/test_mcp.py`, job `tests` de la CI) et avec Claude Code (voir la PR #153).
- Assistants : chargement des fichiers vérifié avec Copilot CLI 1.0.102 et Gemini CLI 0.65.0 ;
  **aucune réponse obtenue de Copilot ni de Gemini**, faute de compte dans l'environnement
  de développement (voir README).

Documentation consultée (2026-10-22) :
[Claude Code — installation](https://code.claude.com/docs/en/setup) ·
[Claude Code — CLAUDE.md et AGENTS.md](https://code.claude.com/docs/en/memory) ·
[Copilot CLI — skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) ·
[VS Code — Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) ·
[Gemini CLI — skills](https://geminicli.com/docs/cli/skills/).

Serveur MCP (2026-10-26) :
[Claude Code — MCP](https://code.claude.com/docs/en/mcp) ·
[Claude Desktop — serveurs locaux](https://modelcontextprotocol.io/docs/develop/connect-local-servers) ·
[SDK Python v2 — migration (FastMCP → MCPServer)](https://py.sdk.modelcontextprotocol.io/v2/migration/) ·
[MCPB — manifeste](https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md).
