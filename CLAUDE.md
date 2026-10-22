# ISTQBFinder — guide pour Claude Code

Assistant de connaissances QA **conversationnel** pour un Test Manager / QA Lead :
syllabus ISTQB locaux (FR/EN), base d'idées QA capitalisées, Web seulement si justifié.
Français partout (messages, commits, commentaires). Pas de serveur ni d'interface.

- Point d'entrée : le skill `.claude/skills/qa-knowledge/` (méthode, citations,
  capitalisation) et la CLI `python qa.py <commande>` (garanties : vérifications,
  déduplication, journal). Lire `README.md` et `docs/architecture.md`.
- Premier lancement sur un clone : `python qa.py actualiser` (≈ 3 min) reconstruit l'index.

## Commandes

```bash
python -m pytest tests/ -q -rs        # obligatoire avant tout commit/push (~15 s)
python qa.py evaluer --jeu controle   # qualité de la recherche (avant/après toute modif du moteur)
python qa.py inventaire               # état de la bibliothèque
```

## Consignes communes (Claude, Copilot, Gemini)

Règles de réponse, de développement et métier : dans `AGENTS.md` (source unique, lue
aussi par GitHub Copilot), importé ici :

@AGENTS.md

Les fichiers d'intégration des autres assistants sont générés depuis `.claude/` :
après toute modification d'un agent ou d'un skill, `python scripts/generer_integrations.py`.
