<!-- Fichier généré par scripts/generer_integrations.py : ne pas modifier, relancer le script. -->

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
claude plugin install istqbfinder@istqbfinder-local
```

Licence : MIT (code et documentation), comme le dépôt ; les syllabus n'en relèvent pas.
