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
`--` = à faire, non bloquant (par exemple la CLI d'un assistant pas encore installée).

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

## Ce qui a été essayé

- `installer.sh` : exécuté sur un clone propre (Linux, Python 3.13) puis relancé
  (idempotence : 1,5 s, aucun fichier versionné modifié) ; la CI le rejoue à chaque push
  avec Python 3.10 (job `installation-linux`).
- `installer.ps1` : exécuté par la CI sous Windows PowerShell 5.1 (job `installation-windows`) ;
  non essayé sur un poste Windows réel.
- Assistants : chargement des fichiers vérifié avec Copilot CLI 1.0.102 et Gemini CLI 0.65.0 ;
  **aucune réponse obtenue de Copilot ni de Gemini**, faute de compte dans l'environnement
  de développement (voir README).

Documentation consultée (2026-10-22) :
[Claude Code — installation](https://code.claude.com/docs/en/setup) ·
[Claude Code — CLAUDE.md et AGENTS.md](https://code.claude.com/docs/en/memory) ·
[Copilot CLI — skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) ·
[VS Code — Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) ·
[Gemini CLI — skills](https://geminicli.com/docs/cli/skills/).
