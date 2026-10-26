# ISTQBFinder — plugin Claude Code

Assistant de connaissances QA pour Test Manager et QA Lead, utilisable dans Claude Code
depuis **n'importe quel projet**. Il cherche dans les syllabus ISTQB® et cite la page et la
section. Il tient une base d'idées QA, et il fournit deux agents, Thomas (chercheur) et Sylvie
(auditrice), ainsi qu'un serveur MCP local en lecture seule.

> Ce dépôt est **généré** depuis [Opaland/ISTQBFinder](https://github.com/Opaland/ISTQBFinder)
> par `scripts/exporter_plugin.py`, au commit `{commit}`, version `{version}`. Ne pas le
> modifier à la main : corriger la source, puis réexporter.

Il ne contient **aucun syllabus** : les documents se téléchargent au premier usage, depuis
istqb.org uniquement (voir `NOTICE.md`).

## Prérequis

- Claude Code.
- Python 3.10 ou plus dans le `PATH` : `python3` ou `python` sous Linux et macOS, `python`
  ou `py` sous Windows. Sous Debian ou Ubuntu, il faut aussi le paquet `python3-venv`.
- Accès réseau à PyPI (pour le venv) et à istqb.org (pour les syllabus).

## Installation

```bash
claude plugin marketplace add Opaland/ISTQBFinder-plugin
claude plugin install istqbfinder@istqbfinder
```

## Premier usage

Dans Claude Code, lancer `/istqbfinder:installer`, ou `/istqbfinder:installer CTFL CTAL-TM`
pour ne prendre que certains syllabus. Depuis un terminal, on peut aussi lancer
`<dossier du plugin>/bin/qa installer` (`qa emplacements` affiche ce dossier).

La commande fait quatre choses :

1. Elle crée un venv (pypdf, SDK MCP) dans le dossier de données du plugin, en une minute
   environ.
2. Elle télécharge les syllabus **anglais** depuis istqb.org, et seulement depuis les
   domaines de `catalogue/istqb.json`. Les prendre tous demande quelques minutes.
3. Elle les indexe.
4. Elle lance le diagnostic.

À la toute première session, le serveur MCP trouve le venv absent. Il lance alors sa
préparation dans un processus détaché (journal `preparation.log` du dossier de données) et
l'attend 20 secondes. Claude Code n'attend un serveur que 30 secondes (`MCP_TIMEOUT`), et
l'installation de pip dure souvent plus longtemps. Si `/mcp` montre le serveur en échec,
le reconnecter dans `/mcp` une minute plus tard, ou après `/istqbfinder:installer`. En mode
`claude -p`, Claude Code ne retente pas un serveur de plugin en échec avant 15 minutes.

## Utilisation

- `/istqbfinder:qa-knowledge <question>` : réponse sourcée (syllabus lus, base d'idées), avec
  un score de confiance.
- `@agent-istqbfinder:thomas <question>` ouvre des pistes sourcées ;
  `@agent-istqbfinder:sylvie <démarche>` aligne une démarche sur l'ISTQB et en évalue la
  maturité.
- `/istqbfinder:bibliotheque` (état, manquants, nouvelles versions) et
  `/istqbfinder:ajouter-syllabus`.
- Les outils MCP en lecture seule `chercher`, `lire`, `section`, `page`, `plan`,
  `idee_chercher`, `idee_voir`, `confiance` et `passages_lus`.
- `qa <commande>` (lanceur dans `bin/`) : toute la CLI, `qa --help`.

## Où vont les données

Rien n'est écrit dans le dossier d'installation du plugin. Tout va dans le **dossier de
données du plugin** (`${CLAUDE_PLUGIN_DATA}`, soit
`~/.claude/plugins/data/istqbfinder-istqbfinder/`). `qa emplacements` l'affiche.

- `venv/` : l'environnement Python.
- `donnees/bibliotheque/` : les PDF téléchargés et l'index.
- `donnees/connaissances/` : la base d'idées et le journal.

Claude Code garde ce dossier quand le plugin est mis à jour. Il **le supprime à la
désinstallation**, sauf avec `claude plugin uninstall istqbfinder@istqbfinder --keep-data`.

Pour mettre les données ailleurs, définir `QAK_RACINE` dans le bloc `env` de
`~/.claude/settings.json`, avec un chemin absolu. Le serveur MCP et l'outil Bash le
voient tous les deux. On peut ainsi garder la base hors du dossier que la désinstallation
supprime, ou pointer vers un clone d'ISTQBFinder pour profiter de ses traductions et de sa
base d'idées.

## Traductions françaises

Elles **ne sont pas téléchargées**, car seul istqb.org est autorisé. Deux façons de les
avoir :

- **Les déposer à la main**, si vous disposez des PDF (CFTL, par exemple) :
  `qa importer --prive <fichier.pdf>` (métadonnées détectées, à corriger avec
  `--code`, `--version` ou `--langue fr` si besoin), ou `/istqbfinder:ajouter-syllabus`.
  Les documents vont dans `donnees/bibliotheque/prive/`.
- **Utiliser un clone d'ISTQBFinder** comme dossier de données (`QAK_RACINE`, voir plus
  haut), avec les droits décrits dans son `NOTICE.md`.

## Base d'idées

Il y a **une base par installation** : celle du dossier de données
(`donnees/connaissances/connaissances.jsonl`). Elle est vide au départ, et rien n'est
partagé avec d'autres utilisateurs ni avec le dépôt source. Les consignes « proposer un
commit » des skills ne s'appliquent pas, puisque ce dossier n'est pas un dépôt Git. Pour la
sauvegarder ou la partager, il y a deux possibilités :

- copier `connaissances.jsonl` ;
- faire de `QAK_RACINE` un dépôt Git à soi.

## Permissions conseillées

Un plugin ne peut pas livrer de règles de permission. Pour que Thomas et Sylvie lisent sans
demander à chaque fois, ajouter dans `~/.claude/settings.json` (lecture seule) :

```json
{"permissions": {"allow": ["mcp__plugin_istqbfinder_istqbfinder__*",
                            "Bash(qa chercher:*)", "Bash(qa lire:*)", "Bash(qa section:*)",
                            "Bash(qa page:*)", "Bash(qa plan:*)", "Bash(qa idee chercher:*)",
                            "Bash(qa idee voir:*)", "Bash(qa confiance:*)"]}}
```

Ne mettez jamais de règle `allow` pour `qa installer`, `qa telecharger`, `qa importer` ou
`qa idee ajouter` : ces commandes écrivent, et elles restent soumises à votre accord.

## Mise à jour

```bash
claude plugin marketplace update istqbfinder
claude plugin update istqbfinder@istqbfinder
```

Le venv est complété tout seul si les dépendances ont changé. Les données sont conservées.

## Systèmes

Le plugin fonctionne sous Linux, macOS et Windows. Le serveur MCP est déclaré une seule
fois : `${CLAUDE_PLUGIN_ROOT}/bin/qa`. Sous Windows, Claude Code le résout vers
`bin/qa.cmd`, avec ou sans Git Bash.

## Licence

Le code et la documentation sont sous licence MIT (`LICENSE`). Les syllabus téléchargés ne
relèvent pas de cette licence : voir `NOTICE.md`.
