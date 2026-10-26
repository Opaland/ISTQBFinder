# Plugin Claude Code (#184)

But : utiliser les skills (`qa-knowledge`, `bibliotheque`, `ajouter-syllabus`), les agents
Thomas et Sylvie et la bibliothèque ISTQB depuis **n'importe quel projet**, sans ouvrir
l'assistant dans le clone, et sans perdre les garanties de la CLI (citations vérifiées,
écritures soumises à l'accord de l'utilisateur).

Ce document décrit le format réel, puis les choix retenus. Il signale aussi les décisions
laissées à l'utilisateur. Relevé du 2026-10-26, avec Claude Code 2.1.310
(`claude plugin --help`, `claude plugin validate --help`) et la documentation officielle
citée en fin de page.

## 1. Le format réel

### Plugin

- Racine du plugin : un dossier. Le manifeste `.claude-plugin/plugin.json` est
  optionnel ; seul son champ `name` est obligatoire. Il est en kebab-case et sert d'espace
  de noms : l'agent `thomas` du plugin `istqbfinder` s'appelle `istqbfinder:thomas`, le skill
  `istqbfinder:qa-knowledge`.
- Emplacements par défaut, à la racine du plugin et non dans `.claude-plugin/` :
  - `skills/<nom>/SKILL.md` ;
  - `agents/*.md` ;
  - `commands/` ;
  - `hooks/hooks.json` ;
  - `.mcp.json` (serveurs MCP, aussi déclarables dans `plugin.json` sous `mcpServers`) ;
  - `bin/` : ses fichiers sont dans le `PATH` de l'outil Bash tant que le plugin est actif ;
  - `settings.json`, où seules les clés `agent` et `subagentStatusLine` sont lues.
- **Un plugin ne transporte pas de règles de permission.** `settings` ne garde que `agent`
  et `subagentStatusLine`. Le seul levier est l'en-tête `allowed-tools` d'un skill, qui
  pré-approuve des outils pendant que le skill est actif.
- **Confinement** : tout chemin de composant commence par `./` et reste dans la racine du
  plugin. `..` et les liens symboliques qui en sortent sont refusés (« path escapes plugin
  directory »). Les skills et les agents doivent donc être **copiés** dans le plugin : on ne
  peut pas pointer vers `.claude/skills/`.
- Variables :
  - `${CLAUDE_PLUGIN_ROOT}` : dossier installé du plugin ;
  - `${CLAUDE_PLUGIN_DATA}` : données persistantes, `~/.claude/plugins/data/<id>/` ;
  - `${CLAUDE_PROJECT_DIR}` : racine du projet ouvert.

  Elles sont remplacées dans `command`, `args` et `env` des serveurs MCP stdio, et dans le
  corps des skills, agents et commandes. Elles ne le sont pas dans les fichiers lus ensuite
  avec `Read`, ni dans l'environnement de l'outil Bash.
- `userConfig` : valeurs demandées à l'activation (`string`, `number`, `boolean`,
  `directory`, `file`), référencées par `${user_config.CLE}`.
- Outils d'un serveur MCP fourni par un plugin : `mcp__plugin_<plugin>_<serveur>__<outil>`.
  Une règle d'autorisation couvre tout le serveur : `mcp__plugin_<plugin>_<serveur>__*`.
- Contrôle : `claude plugin validate [--strict] <dossier>`. `--strict` traite les
  avertissements comme des erreurs, pour la CI.

### Marketplace

- `.claude-plugin/marketplace.json`, avec `name`, `owner` et `plugins`. Chaque entrée a un
  `name` et une `source` : chemin relatif `./…` (ou `"./"`, la racine elle-même), `github`,
  `url`, `git-subdir`, `npm`, `archive` ou `command`.
- Ajout : `claude plugin marketplace add <owner/repo | URL | chemin>`. Installation :
  `claude plugin install <plugin>@<marketplace>`.
- **Où vont les fichiers** :
  - marketplace ajoutée **depuis un chemin local** : rien n'est copié. Le plugin à source
    relative se charge **en place**, et `${CLAUDE_PLUGIN_ROOT}` désigne le dossier source ;
  - marketplace **GitHub** : le dépôt entier est cloné dans
    `~/.claude/plugins/marketplaces/<nom>/` (sauf `--sparse`), puis le plugin est copié dans
    `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Un script du plugin ne voit
    plus rien au-dessus de sa racine.
- `version` dans `plugin.json` fige la version installée jusqu'à son changement ; un
  plugin chargé en place relit ses fichiers à chaque session, quelle que soit la version.

## 2. Contraintes du projet

- **Droits** (NOTICE.md, #149) : l'autorisation de l'ISTQB, du CFTL et de la TMMi
  Foundation vaut pour **ce dépôt** et ne se transmet pas. Le plugin ne doit donc jamais
  contenir ni recopier les PDF : il pointe vers un clone de ce dépôt, ou fait télécharger
  les documents à la source.
- Garanties portées par la CLI `qa.py` : lire avant de citer, références vérifiées,
  déduplication, journal. Aucune écriture sans l'accord de l'utilisateur.
- `pypdf` reste la seule dépendance obligatoire ; le serveur MCP (#153) est optionnel
  (`requirements-mcp.txt`).
- Téléchargement depuis istqb.org seulement.

## 3. Choix

### 3.1 Où vivent la CLI et la bibliothèque

| Option | Pour | Contre |
|---|---|---|
| A. Le plugin localise un **clone installé** (`installer.sh`) | Rien de neuf à distribuer ; PDF, index, base d'idées et CLI restent là où ils sont ; les garanties sont intactes | Il faut un clone par poste |
| B. Le plugin **embarque la CLI** et télécharge la bibliothèque au premier usage | Installation en une commande | Les traductions françaises ne se téléchargent pas automatiquement (seul istqb.org est autorisé) ; il faudrait dupliquer `qak/` dans le plugin, avec `pypdf` à installer dans `${CLAUDE_PLUGIN_DATA}` |
| C. Le plugin s'appuie sur le **serveur MCP** (#153) | Lecture sans commande shell ; une seule règle `allow` couvre un serveur en lecture seule | Le serveur doit tourner quelque part : dans un clone (A) ou dans une CLI embarquée (B) |

**Choix : A + C.** Le plugin vit dans ce dépôt (`plugin/`), **généré** depuis `.claude/`
par `scripts/generer_integrations.py`, comme les intégrations Copilot et Gemini. Il se
charge en place depuis le clone, par une marketplace locale. Les lectures passent par le
serveur MCP du clone, et le reste par un lanceur `qa` :

- `plugin/bin/qa` : `qa <commande>` = `python qa.py <commande>` du clone, avec le Python de
  son `.venv`. Le dossier `bin/` étant dans le `PATH` de l'outil Bash, les skills l'appellent
  depuis n'importe quel dossier. Sous Windows, `plugin/bin/qa.cmd` joue le même rôle (#203) :
  l'outil PowerShell trouve `qa.cmd`, l'outil Bash (Git Bash) trouve `qa`.
- Serveur MCP `istqbfinder` déclaré dans `plugin.json` : `${CLAUDE_PLUGIN_ROOT}/bin/qa mcp`,
  une seule déclaration pour les trois systèmes. Sous Windows, Claude Code résout ce chemin
  sans extension vers `bin/qa.cmd`, avec ou sans Git Bash (voir « Ce qui a été essayé »).
- Skills et agents recopiés. `python qa.py` y devient `qa`, et un en-tête signale les outils
  MCP. Les agents reçoivent les outils MCP dans `tools:` et le skill
  `istqbfinder:qa-knowledge` dans `skills:`.

### 3.2 Comment les PDF sont obtenus

Ils ne sont jamais dans le plugin. `plugin/` ne contient que du texte généré, ce qu'un test
vérifie. Le plugin lit la bibliothèque du clone (`${CLAUDE_PLUGIN_ROOT}/..`). La
marketplace est dans `plugin/.claude-plugin/` et **pas à la racine du dépôt** :
`claude plugin marketplace add Opaland/ISTQBFinder` ne trouve donc rien. On ne l'ajoute
que depuis un clone (`claude plugin marketplace add <clone>/plugin`), sans aucune copie.

Une marketplace GitHub à la racine clonerait au contraire tout le dépôt, PDF compris, dans
`~/.claude/plugins/marketplaces/`, puis copierait le plugin dans le cache, hors du clone,
où le lanceur ne trouverait plus `qa.py`. C'est une décision de diffusion (§ 5, question 1).

### 3.3 Chemins et permissions

- Commandes : `qa <commande>` grâce à `bin/`. L'en-tête `allowed-tools` des skills est
  réécrit (`Bash(qa chercher:*)`…), sans aucune écriture, ce que vérifie le test, et
  complété par `mcp__plugin_istqbfinder_istqbfinder__*`.
- Le plugin ne peut pas livrer l'allowlist de `.claude/settings.json`. Pour les agents
  Thomas et Sylvie, qui ne profitent pas de l'`allowed-tools` du skill, ajouter dans
  `~/.claude/settings.json` (lecture seule) :

  ```json
  {"permissions": {"allow": ["mcp__plugin_istqbfinder_istqbfinder__*",
                              "Bash(qa chercher:*)", "Bash(qa lire:*)", "Bash(qa section:*)",
                              "Bash(qa page:*)", "Bash(qa plan:*)", "Bash(qa idee chercher:*)",
                              "Bash(qa idee voir:*)", "Bash(qa confiance:*)"]}}
  ```

  Jamais de règle `allow` pour `qa idee ajouter`, `qa importer`, `qa actualiser`… : ces
  commandes écrivent et restent soumises à l'accord de l'utilisateur.
- Lecture de fichiers du clone (`referentiel/grille-maturite.md`, `reference/*.md`) hors du
  projet ouvert : Claude Code demande une autorisation `Read`. Elle peut être accordée une
  fois pour le dossier du clone.

### 3.4 Base d'idées

Celle du clone : `connaissances/` (variable `QAK_RACINE` absente), comme aujourd'hui. C'est
une base par clone, donc par utilisateur. Rien n'est écrit dans `${CLAUDE_PLUGIN_DATA}`.
`QAK_RACINE` reste disponible pour pointer vers une autre racine de données. Une base
**partagée** entre plusieurs personnes est une décision de l'utilisateur (§ 5, question 3).

### 3.5 Autres assistants

Gemini CLI a ses extensions et Copilot l'équivalent qu'il proposera. Le même générateur
pourra les produire. Ce n'est pas fait ici : les essais réels sont impossibles sans compte
(#114).

## 4. Version minimale livrée

Prérequis : un clone installé (`./installer.sh`) et le SDK MCP dans son venv
(`.venv/bin/python -m pip install -r requirements-mcp.txt`).

```bash
claude plugin marketplace add /chemin/ISTQBFinder/plugin
claude plugin install istqbfinder@istqbfinder-local
claude plugin list                       # istqbfinder@istqbfinder-local … enabled
```

Ensuite, dans n'importe quel projet :

- `/istqbfinder:qa-knowledge <question>` ;
- `@agent-istqbfinder:thomas <question>`, `@agent-istqbfinder:sylvie <démarche>` ;
- les outils MCP `chercher`, `lire`…

Dans le clone lui-même, le plugin fait doublon avec `.claude/` : le désactiver
(`claude plugin disable istqbfinder@istqbfinder-local`) ou ne pas l'installer.

Contrôles :

- `tests/test_integrations.py` vérifie que `plugin/` est à jour ;
- `tests/test_plugin.py` vérifie :
  - aucune écriture pré-approuvée ;
  - aucun PDF ni fichier binaire ;
  - le lanceur réel (`bin/qa`, ou `bin/qa.cmd` sous Windows), qui démarre la CLI du clone et
    transmet son code retour ;
  - le serveur MCP démarré par ce lanceur, qui répond à `tools/list` (SDK `mcp` requis) ;
  - `claude plugin validate --strict plugin` quand la CLI `claude` est présente. La CI
    l'installe dans les jobs `tests` et `plugin-windows`.
- Job CI `plugin-windows` (#203) : les mêmes tests sous Windows, puis Git Bash retiré du
  runner, `claude plugin install` et `claude mcp list`, qui doit montrer le serveur
  `plugin:istqbfinder:istqbfinder` connecté. Ce contrôle ne demande aucun compte Claude.

Limites :

- **Windows** : le lanceur cherche le Python du `.venv` du clone, puis `python`, puis
  `py -3` (3.10 ou plus). L'alias `python` du Microsoft Store, sans Python installé, est
  écarté par ce contrôle de version. Une question posée à Claude par le plugin sous
  Windows n'a pas été essayée (pas de compte sur le runner) : seuls le démarrage du
  serveur et `tools/list` le sont.
- Le plugin installé **depuis GitHub** (copie dans le cache) ne trouve pas le clone. Le
  lanceur l'explique et s'arrête.

### Ce qui a été essayé (2026-10-26, Claude Code 2.1.310, Linux)

- `HOME=<vide> claude plugin marketplace add <clone>/plugin` puis
  `claude plugin install istqbfinder@istqbfinder-local` : installé, `Read from: <clone>/plugin`
  (chargé en place), 3 skills, 2 agents, 1 serveur MCP (`claude plugin details`).
- Depuis un dossier vide, `claude -p … --plugin-dir <clone>/plugin --model haiku` : les outils
  `mcp__plugin_istqbfinder_istqbfinder__chercher` et `…__lire` répondent (« Citer :
  [CT-AcT 2019 FR, §2.3.1, p. 19] ») et `qa confiance …` passe par le lanceur `bin/qa`
  (0,006 $).
- `claude --agent istqbfinder:thomas -p …` (haiku) : Thomas cherche, lit un passage, cite
  `[CTAL-TA v4.0 FR, §3.4.1, p. 39]` et refuse de citer une section qu'il n'a pas lue
  (0,004 $).
- Windows, 2026-10-26, Claude Code 2.1.310, runner `windows-latest` (essai jetable, puis job
  `plugin-windows`) : un plugin déclarant plusieurs formes de commande MCP, chacune
  traçant la forme réellement lancée. `${CLAUDE_PLUGIN_ROOT}/bin/qa` démarre **`bin/qa.cmd`**,
  avec Git Bash comme après son retrait ; `bin/qa.cmd` et `cmd /c …\qa.cmd` aussi. Un fichier
  `.cmd` polyglotte commençant par `#!/bin/sh` échoue sans Git Bash (ligne recopiée sur
  stdout). Sous Linux et macOS, la même déclaration lance `bin/qa` (sh) ; un `.cmd` y échoue
  (`ENOEXEC`).
- Non essayé : une conversation complète sous Windows ou macOS, Claude Desktop.

## 5. Décisions laissées à l'utilisateur

1. **Diffusion publique** : déplacer la marketplace à la racine du dépôt
   (`claude plugin marketplace add Opaland/ISTQBFinder`) ou la soumettre à un catalogue
   public. *Recommandation* : pas avant d'avoir réglé la copie des PDF. Une marketplace
   GitHub clone le dépôt entier, PDF compris, sur chaque poste, ce qui revient à
   redistribuer hors de ce dépôt (#149). Alternative sans PDF : un dépôt dédié au plugin,
   qui demande un clone de ce dépôt par `userConfig` (`type: directory`) ou qui télécharge
   les syllabus anglais à la source (istqb.org), sans les traductions françaises.
2. **Domaines de téléchargement** : autoriser cftl.fr ou tmmi.org pour que le plugin
   obtienne seul les traductions françaises. *Recommandation* : non pour l'instant. La
   règle « istqb.org uniquement » tient, et les traductions restent fournies par
   l'utilisateur.
3. **Base d'idées partagée** entre plusieurs utilisateurs : dépôt Git commun, ou
   `QAK_RACINE` sur un dossier partagé. *Recommandation* : garder une base par clone. Le
   partage passe déjà par Git (commit de `connaissances/` puis `git pull`). Un dossier
   partagé en écriture concurrente n'est pas prévu par la base SQLite.

## Documentation consultée (2026-10-26)

- [Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference.md)
- [Plugin loading reference](https://code.claude.com/docs/en/plugins/loading.md)
- [MCP dans Claude Code](https://code.claude.com/docs/en/mcp) (serveurs fournis par un plugin)
- [Permissions](https://code.claude.com/docs/en/permissions) (règles `mcp__…__*`, `allowed-tools`)
- `claude plugin --help`, `claude plugin validate --help` (Claude Code 2.1.310)
