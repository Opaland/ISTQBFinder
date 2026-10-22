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

## Règles de développement

- **Un problème = une issue** GitHub (constat, scénario reproductible, impact attendu),
  qu'il vienne d'une revue, d'un test ou de l'usage.
- **Un correctif = une PR** : une branche partie de `main` à jour, un seul sujet, et
  `Closes #n` dans la description. Jamais de commit direct sur `main`.
- Une PR n'est fusionnée que si la CI est verte ; la fusion ferme l'issue.
- Avant de pousser : `python -m pytest tests/ -q -rs` vert, et `python qa.py evaluer
  --jeu controle` si le moteur de recherche est touché (chiffres dans la PR).

## Règles métier

- Ne jamais citer une page, une section ou un passage non lu via `lire`/`section`/`page`.
- Une référence ISTQB n'est enregistrée que vérifiée par l'outil (page, extrait) ;
  ne jamais contourner ces contrôles.
- Téléchargement depuis istqb.org uniquement (`catalogue/istqb.json`).
- Tout changement d'extraction, de découpage ou de détection incrémente
  `VERSION_EXTRACTEUR` (qak/extraction.py).
- Moteur de recherche : mesurer `evaluer --jeu controle` avant et après ; ajouter une
  question qui échoue au jeu de contrôle AVANT de modifier le moteur (pas de sur-réglage).
- Tests : pas de client HTTP bouchonné ; `tests/test_sources_reelles.py` appelle vraiment
  istqb.org (injoignable → ignoré avec la raison ; mauvaise réponse → échec). Le garde-fou
  `autouse` de `tests/conftest.py` isole chaque test dans un dossier temporaire.
- Base d'idées : `connaissances/connaissances.jsonl` est la source versionnée ; ne
  capitaliser qu'avec l'accord de l'utilisateur ; proposer un commit après une session.
- Les PDF de `bibliotheque/sources/` sont © ISTQB (copie autorisée avec citation) : ne
  pas les modifier ; ils ne relèvent pas de la licence MIT.
