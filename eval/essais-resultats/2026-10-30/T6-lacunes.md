# T6-lacunes — thomas

**Question** : Identifie les thèmes QA sur lesquels notre base de connaissances est encore pauvre.

**Tours** : 4 · **coût** : 0.083 $ · **confiance annoncée** : 85 · **verdict** : réussi · **citations** : 0/0 lues · **Web** : 0 · **fidélité** (juge LLM, indicatif) : None sur 0 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : `python qa.py couverture` et `idee lister` (base d'idées), plus `inventaire` (42 fichiers, syllabus FR/EN). Je n'ai lu aucun passage de syllabus et je n'ai pas fait de recherche Web. Ce rapport mesure la couverture de la base, pas le contenu des syllabus, donc il n'y a pas de citation ISTQB.

## Constat

**La base d'idées est vide.** `idee lister` renvoie « Aucune idée », et les 39 thèmes de la taxonomie sont à 0 idée (état « vide »). Tous les thèmes sont donc « pauvres ». Seul le volume de syllabus disponible permet de les ordonner.

Hypothèse de contexte : tu veux savoir où capitaliser en premier. Je n'ai pas de contexte projet (agile ou séquentiel, domaine, réglementation).

## Thèmes par volume de passages dans les syllabus

Plus le volume est élevé, plus il y a de matière à capitaliser.

| Priorité | Thème (code) | Passages | Idées |
|---|---|---|---|
| Très riche en passages | Exigences et critères d'acceptation (`exigences`) | 1901 | 0 |
| | Outils, méthodes et organisation (`organisation`) | 1747 | 0 |
| | Test en contexte agile et à l'échelle (`agile`) | 1133 | 0 |
| | Métriques et reporting (`metriques`) | 1162 | 0 |
| | Analyse et conception des tests (`conception`) | 1119 | 0 |
| | Estimation et planification (`estimation`) | 1099 | 0 |
| | Automatisation des tests (`automatisation`) | 1019 | 0 |
| | Niveaux et types de test (`niveaux-types`) | 1003 | 0 |
| Matière moyenne | Test management (`test-management`) | 779 | 0 |
| | Utilisabilité et accessibilité (`utilisabilite`) | 718 | 0 |
| | Domaines métier (`domaines-metier`) | 617 | 0 |
| | Environnements et données de test (`environnements`) | 601 | 0 |
| | Compétences et animation d'équipe (`competences`) | 591 | 0 |
| | CI/CD (`cicd`) | 583 | 0 |
| | Shift-right et test en production (`shift-right`) | 500 | 0 |
| Peu de matière | Shift-left et shift-right (parent) (`shift`) | 82 | 0 |
| | Priorisation des tests (`priorisation`) | 82 | 0 |
| | Stratégie et ROI de l'automatisation (`strategie-automatisation`) | 110 | 0 |
| | L'IA au service du test (`ia-pour-tester`) | 111 | 0 |

La base ne contient aucune idée, donc ces chiffres ne mesurent pas ce qui manque. Ils mesurent seulement l'effort de capitalisation possible.

## Limites de couverture des syllabus

Ce sont des points déjà connus de la bibliothèque. Je ne les ai pas revérifiés avec `chercher`.
- **Santé / dispositif médical** : pas de syllabus dédié (IEC 62304 absent). Le thème `reglementee` (301 passages) s'appuie sur des sources indirectes.
- **Web et API** : pas de syllabus dédié (l'API compte 157 passages).
- **Documents anciens ou en retrait** : CTFL-AT 2014, CTAL-ATT 1.1 et CTEL 2011.
- **Syllabus sans traduction française** : plusieurs spécialités ne sont qu'en anglais (CT-AI, CT-GenAI, CT-QDO, CT-FT, CT-SEC, etc.). Sauf demande contraire, mes citations resteront en anglais.

## Par quoi je commencerais

1. **`metriques`, `estimation` ou `rbt`** : impact fort, effort faible. Ce sont des sujets de Test Manager, bien couverts par CTAL-TM v3.0 en FR et EN.
2. **`exigences` ou `agile`** : impact fort, effort moyen. Le volume est grand, il faudra donc filtrer.
3. **`ia-pour-tester` ou `shift-left`** : impact moyen, effort faible. Peu de passages, donc une capitalisation rapide.

## Où creuser ensuite

Je n'ai lu aucun passage, donc je ne cite aucune section. Pistes à lire : `python qa.py chercher --theme metriques`, `--theme rbt` et `--theme agile`.

**Confiance : 85/100** (bonne). L'inventaire et la couverture sont des sorties directes de l'outil. Je n'ai pas calculé le score avec `qa.py confiance`. Le reste de la réponse n'est qu'un classement par volume de passages, sans lecture de syllabus.

**Questions à choix**

1. Quel est ton contexte principal ?
   1. Agile / Scrum
   2. Séquentiel ou réglementé
   3. Autre ou mixte

2. Quelle suite veux-tu ?
   1. Explorer un thème précis (par exemple `metriques` ou `rbt`) et en tirer 3 idées à capitaliser
   2. Lancer une campagne par ordre de priorité sur les 3 premiers thèmes
   3. Vérifier d'abord les lacunes de couverture (santé, web, API), avec `/ajouter-syllabus <code>` si besoin

## À capitaliser ?

Rien à proposer. Je n'ai lu aucun passage, et il ne faut pas enregistrer d'idée sans source lue.

## Commandes exécutées

- `python qa.py inventaire; python qa.py themes; python qa.py couverture --help | head -20`
- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py couverture; python qa.py idee lister 2>&1 | tail -60`
