# Plugin Claude Code (#184)

But : utiliser les skills (`qa-knowledge`, `bibliotheque`, `ajouter-syllabus`), les agents
Thomas et Sylvie et la bibliothèque ISTQB depuis **n'importe quel projet**, sans ouvrir
l'assistant dans le clone, et sans perdre les garanties de la CLI (citations vérifiées,
écritures soumises à l'accord de l'utilisateur).

Deux plugins sortent de la même source `.claude/` :

- `plugin/` (§ 3 et 4) : il se charge **en place depuis un clone** et lit sa bibliothèque ;
- le **plugin autonome** (§ 6), exporté par `scripts/exporter_plugin.py` pour le dépôt dédié
  `Opaland/ISTQBFinder-plugin`. Il ne contient aucun PDF et télécharge les syllabus anglais
  au premier usage.

Ce document décrit le format réel, les choix retenus, les décisions de l'utilisateur (§ 5),
puis la publication (§ 7). Relevé du 2026-10-26, avec Claude Code 2.1.310
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

## 5. Décisions de l'utilisateur (2026-10-26, #184)

Les questions posées ici dans la première version (#202) ont reçu ces réponses :

1. **Diffusion** : un **dépôt dédié au plugin**, sans aucun PDF, diffusable publiquement. Les
   documents s'obtiennent au premier usage, à la source. La marketplace de ce dépôt-ci
   reste locale (`plugin/`).
2. **Domaines de téléchargement** : **istqb.org seulement**. Les traductions CFTL et les
   documents TMMi se déposent à la main, ou s'obtiennent par un clone de ce dépôt.
3. **Base d'idées** : **une base par clone**, partagée par Git, comme aujourd'hui. Pour le
   plugin autonome, c'est la base de son dossier de données : une par installation.

## 6. Plugin autonome (dépôt dédié `Opaland/ISTQBFinder-plugin`)

### 6.1 Contenu de l'export

`python scripts/exporter_plugin.py <dossier>` écrit l'arborescence complète du dépôt :

| Chemin | Rôle |
|---|---|
| `.claude-plugin/plugin.json` | manifeste. `version` vaut `1.0.0+<commit court>` par défaut, `--version` pour la fixer. Serveur MCP `istqbfinder` = `${CLAUDE_PLUGIN_ROOT}/bin/qa mcp`. `metadata.commit` donne le commit source |
| `.claude-plugin/marketplace.json` | marketplace `istqbfinder` **à la racine**, plugin `source: "./"`. `claude plugin marketplace add Opaland/ISTQBFinder-plugin`, puis `claude plugin install istqbfinder@istqbfinder` |
| `skills/`, `agents/` | skills et agents de `.claude/`, produits par le même générateur que `plugin/`, avec un en-tête « autonome » : données dans le dossier de données, `referentiel/` sous `${CLAUDE_PLUGIN_ROOT}`, `docs/` en ligne, pas de commit. S'y ajoute le skill `installer` (premier usage, `disable-model-invocation`) |
| `bin/qa`, `bin/qa.cmd`, `lanceur.py` | lanceurs (§ 6.3) |
| `qa.py`, `qak/`, `requirements*.txt`, `catalogue/`, `referentiel/` | le code, tel quel |
| `README.md`, `LICENSE`, `NOTICE.md` | installation, licence MIT (code seulement), droits des documents téléchargés |
| `.gitattributes`, `.gitignore` | fins de ligne LF ; `*.pdf` ignoré par sécurité |

**Aucun PDF, aucun fichier de `bibliotheque/sources/`.** Après écriture, `verifier()` contrôle
l'extension, la signature `%PDF` et l'empreinte SHA-256 de chaque fichier, comparée à celles
de `bibliotheque/sources/`. Il vérifie aussi les fichiers requis et la validité des JSON. Un
écart fait échouer l'export, avec le code 1. Le dossier cible doit être vide, un export
précédent ou un clone du dépôt du plugin. Tout y est remplacé, sauf `.git/`.

### 6.2 Données : `${CLAUDE_PLUGIN_DATA}`, jamais le dossier du plugin

D'après la documentation officielle, relevée le 2026-10-26 (*Plugin manifest reference*,
« Environment variables » ; *Plugins components*, « Reference plugin paths and store
data ») :

- `${CLAUDE_PLUGIN_ROOT}` change à chaque mise à jour : « Don't write state there ».
- `${CLAUDE_PLUGIN_DATA}` vaut `~/.claude/plugins/data/<id>/`. Il est créé au premier usage,
  **gardé d'une mise à jour à l'autre** et prévu « for `node_modules`, virtual environments,
  and caches ». Dans `<id>` = `plugin@marketplace`, tout caractère autre que lettre, chiffre,
  `_` ou `-` devient `-`.
- La variable est passée au processus d'un serveur MCP stdio, mais **pas à l'outil Bash**.
- Ce dossier est **supprimé à la désinstallation**, sauf avec
  `claude plugin uninstall … --keep-data`.

Le lanceur suit ces règles :

- dossier de données : `CLAUDE_PLUGIN_DATA`, sinon le même chemin **recalculé** pour l'outil
  Bash. La configuration vient de `CLAUDE_CONFIG_DIR` ou de `~/.claude`. La marketplace se
  lit dans le chemin du cache (`plugins/cache/<marketplace>/istqbfinder/<version>/`), ou
  dans `.claude-plugin/marketplace.json` pour un plugin chargé en place. Un test vérifie ce
  calcul. L'essai réel montre que le serveur MCP et l'outil Bash tombent sur le même
  dossier ;
- `venv/` (pypdf et SDK MCP) et `donnees/` (`QAK_RACINE` : bibliothèque, index, base
  d'idées, journal, taxonomie modifiée). Python est lancé avec `PYTHONDONTWRITEBYTECODE=1`,
  donc il n'y a pas de `__pycache__` dans le plugin ;
- `QAK_RACINE`, défini par l'utilisateur dans le bloc `env` de `~/.claude/settings.json`,
  remplace `donnees/`. C'est utile pour garder la base hors du dossier que la
  désinstallation supprime, ou pour pointer vers un clone de ce dépôt (traductions,
  base d'idées) ;
- `qa emplacements` affiche ces chemins.

### 6.3 Lanceurs (Linux, macOS, Windows ; #203)

- `bin/qa` (sh) et `bin/qa.cmd` (Windows) cherchent un Python 3.10 ou plus dans le PATH :
  `python3` puis `python` avec sh, `python` puis `py -3` avec cmd. Ils passent la main à
  `lanceur.py` (bibliothèque standard), qui fait le reste. La déclaration MCP unique
  `${CLAUDE_PLUGIN_ROOT}/bin/qa` vaut pour les trois systèmes (§ 4, essais #203).
- Premier appel : création du venv dans le dossier de données (`python -m venv`, puis pip).
  Un verrou de fichier tenu par le **processus** (fcntl ou msvcrt) évite deux préparations
  simultanées et disparaît si le processus meurt. Un essai l'a montré nécessaire : arrêté
  par Claude Code, un serveur trop lent laissait un verrou en dossier, et `qa installer`
  attendait 15 minutes. Une empreinte des `requirements*.txt` relance pip après une mise à
  jour qui change les dépendances.
- `qa mcp` sans venv : Claude Code abandonne un serveur au bout de 30 s, et pip dure
  souvent plus longtemps (environ une minute à froid). La préparation part donc dans un
  processus détaché (journal `preparation.log`), attendue 20 s. Au-delà, le lanceur
  s'arrête avec un message. Le serveur se reconnecte dans `/mcp` une fois le venv prêt.
- Premier usage : `qa installer [codes…]`, ou `/istqbfinder:installer`. Il prépare le venv,
  lance `telecharger --tous` ou `telecharger <codes>` (**istqb.org seulement**, domaines de
  `catalogue/istqb.json` contrôlés après redirection), puis `actualiser` et `diagnostic`.
  Les traductions françaises n'en font pas partie : le README et la fin de la commande
  renvoient vers `qa importer --prive <fichier>`.

### 6.4 Contrôles

- `tests/test_export_plugin.py` vérifie plusieurs points :
  - export dans un dossier temporaire, sans PDF, sans fichier de `bibliotheque/sources/`
    (empreintes et noms), sans `bibliotheque/`, `connaissances/`, `tests/` ni `.claude/` ;
  - fichiers requis, code complet, manifeste, marketplace, README et NOTICE ;
  - skills sans écriture pré-approuvée, et skill `installer` réservé à l'utilisateur ;
  - remplacement d'un export précédent, avec `.git/` gardé, et refus d'un dossier étranger ;
  - `verifier()` attrape un PDF glissé et un syllabus renommé ;
  - calcul du dossier de données (chargé en place, cache GitHub, `CLAUDE_PLUGIN_DATA`,
    `QAK_RACINE`), verrou libéré à la mort du processus, et refus d'un Python 3.9 ;
  - `claude plugin validate --strict` sur l'export, si la CLI est présente ;
  - **premier usage réel**, hors réseau ignoré : export, `bin/qa installer CTFL` avec un
    vrai téléchargement depuis istqb.org, index, recherche, puis serveur MCP lancé comme
    par Claude Code. Rien ne doit être écrit dans le dossier du plugin. istqb.org
    injoignable → ignoré avec la raison ; mauvaise réponse → échec. Le test ne tourne
    qu'avec `QAK_ESSAI_PREMIER_USAGE=1`.
- Job CI `plugin-export` (Linux, Python 3.10, version minimale) : export,
  `claude plugin validate --strict` sur l'export, puis ces tests avec
  `QAK_ESSAI_PREMIER_USAGE=1`.

### 6.5 Essai réel (2026-10-26, Claude Code 2.1.310, Linux)

- `python scripts/exporter_plugin.py <dossier>` : 43 fichiers, aucun PDF.
  `claude plugin validate --strict` : « Validation passed ».
- `claude plugin marketplace add <dossier>`, puis `claude plugin install istqbfinder@istqbfinder` :
  installé, version `1.0.0+<commit>`, « Read from: <dossier> » (chargé en place).
- `bin/qa installer CTFL CTAL-TM`, en 28 s :
  - venv créé dans `~/.claude/plugins/data/istqbfinder-istqbfinder/venv` ;
  - `CTAL-TM importe CTAL-TM-3.0-en — 87 pages`, `CTFL importe CTFL-4.0.1-en — 78 pages`,
    téléchargés depuis istqb.org ;
  - `Diagnostic : OK` (2 documents, 370 passages) ;
  - aucun `__pycache__`, PDF ni `.db` dans le dossier du plugin.
- `claude mcp list` : `plugin:istqbfinder:istqbfinder … bin/qa mcp - ✔ Connected`.
- `claude -p … --model haiku --max-budget-usd 0.50`, depuis un dossier vide, avec les seuls
  outils `mcp__plugin_istqbfinder_istqbfinder__*`, 0,008 $ :
  - appels `chercher` (en français puis en anglais), `section CTFL-4.0.1-en 5.2`, puis
    `confiance` ;
  - réponse sourcée, `Citer : [CTFL v4.0.1 EN, §5.2, p. 51]` recopié depuis la sortie de
    `section`, et « Confiance : 77/100 ».
- Un premier essai sur `CTAL-TM` a donné `chercher` puis `lire`, avec
  `Citer : [CTAL-TM v3.0 EN, §1.3.3, p. 30]` (0,006 $).
- `claude plugin uninstall` a bien supprimé `…/data/istqbfinder-istqbfinder/` (§ 6.6).
- Outil Bash (haiku, 0,004 $) : `qa emplacements` et `qa inventaire` donnent le même
  dossier de données que le serveur MCP, avec les 2 documents.
- Installation copiée dans le cache, comme depuis GitHub (marketplace de test à source
  `url` `file://…`) :
  - le plugin est copié dans `plugins/cache/<marketplace>/istqbfinder/1.0.0-<commit>/` ;
  - le lanceur retrouve `istqbfinder-<marketplace>`, le dossier que Claude Code a créé ;
  - premier `claude mcp list` en échec, venv en préparation, prête en 59 s ;
  - second `claude mcp list` : ✔ Connected.

### 6.6 Limites

- **Pas encore publié** : le dépôt `Opaland/ISTQBFinder-plugin` n'existe pas. Son
  installation depuis GitHub n'a été essayée que par la marketplace de test à source `url`
  (§ 6.5).
- **Première session** : le serveur MCP peut être en échec le temps que le venv se prépare.
  Il faut le reconnecter dans `/mcp`, ou attendre 15 minutes en `claude -p`.
- **`--plugin-dir`** : Claude Code donne au plugin l'identifiant `istqbfinder@inline`. Le
  serveur MCP utilise alors `…/data/istqbfinder-inline`, et l'outil Bash
  `…/data/istqbfinder-istqbfinder`. Définir `QAK_RACINE` pour les réunir.
- **Désinstallation** : la base d'idées du dossier de données part avec le plugin, sauf
  `--keep-data` ou `QAK_RACINE` placé ailleurs. Le README du plugin le dit.
- **Windows et macOS** : le lanceur et le serveur MCP sont vérifiés en CI (#203). Le premier
  usage réel n'a été essayé que sous Linux.
- Le venv demande un accès à PyPI. Sous Debian ou Ubuntu, il faut aussi `python3-venv` ; le
  lanceur le dit.

## 7. Publication et mises à jour (par l'utilisateur)

### 7.1 Première publication

1. Sur GitHub, créer le dépôt **public** `Opaland/ISTQBFinder-plugin`, vide : sans README,
   sans licence, sans `.gitignore`.
2. Depuis un clone à jour de ce dépôt (`main`, CI verte) :

   ```bash
   git clone https://github.com/Opaland/ISTQBFinder-plugin.git ../ISTQBFinder-plugin
   python scripts/exporter_plugin.py ../ISTQBFinder-plugin    # « aucun PDF », code 0
   claude plugin validate --strict ../ISTQBFinder-plugin      # « Validation passed »
   cd ../ISTQBFinder-plugin
   git status                                                 # aucun .pdf
   git add -A
   git commit -m "Plugin ISTQBFinder <version> (export du commit <commit court>)"
   git push origin main
   ```

3. Essai depuis un autre poste, ou après `claude plugin uninstall` de la version locale :

   ```bash
   claude plugin marketplace add Opaland/ISTQBFinder-plugin
   claude plugin install istqbfinder@istqbfinder
   ```

   Puis, dans Claude Code, `/istqbfinder:installer CTFL`, `/mcp` (serveur connecté) et une
   question à `/istqbfinder:qa-knowledge`.
4. Facultatif : le README de ce dépôt-ci peut renvoyer vers le dépôt du plugin.

### 7.2 À chaque version

1. Fusionner dans `main` ici les changements voulus (skills, agents, `qak/`, catalogue).
2. Réexporter dans le clone du dépôt du plugin, puis committer et pousser :

   ```bash
   cd ../ISTQBFinder-plugin && git pull
   cd -
   python scripts/exporter_plugin.py ../ISTQBFinder-plugin
   claude plugin validate --strict ../ISTQBFinder-plugin
   cd ../ISTQBFinder-plugin && git add -A && git commit -m "Plugin ISTQBFinder <version>" && git push
   ```

   L'export remplace tout sauf `.git/`, donc un fichier retiré à la source disparaît aussi.
   La version par défaut, `1.0.0+<commit court>`, change à chaque commit source : Claude
   Code voit donc une mise à jour. Pour une version lisible, passer
   `--version 1.1.0`, toujours croissante.
3. Côté utilisateurs : `claude plugin marketplace update istqbfinder`, puis
   `claude plugin update istqbfinder@istqbfinder`. Le venv se complète seul si les
   `requirements*.txt` ont changé, et les données du dossier de données sont gardées.
4. Une **nouvelle version d'un syllabus** sur istqb.org demande seulement de mettre
   `catalogue/istqb.json` à jour ici, puis de publier. Chez l'utilisateur,
   `/istqbfinder:bibliotheque versions` la propose au téléchargement.

## Documentation consultée (2026-10-26)

- [Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference.md)
- [Plugin loading reference](https://code.claude.com/docs/en/plugins/loading.md)
- [MCP dans Claude Code](https://code.claude.com/docs/en/mcp) (serveurs fournis par un plugin)
- [Permissions](https://code.claude.com/docs/en/permissions) (règles `mcp__…__*`, `allowed-tools`)
- [Plugins components](https://code.claude.com/docs/en/plugins/components.md) (« Reference plugin paths and store data », `${CLAUDE_PLUGIN_DATA}`)
- [Plugin commands reference](https://code.claude.com/docs/en/plugins/cli-reference.md) (`plugin uninstall --keep-data`)
- [Hooks](https://code.claude.com/docs/en/hooks) (formes exec et shell, Windows sans Git Bash) ; [variables d'environnement](https://code.claude.com/docs/en/env-vars) (`MCP_TIMEOUT`, `CLAUDE_CONFIG_DIR`)
- `claude plugin --help`, `claude plugin validate --help` (Claude Code 2.1.310)
