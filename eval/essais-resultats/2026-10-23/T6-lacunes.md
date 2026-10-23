# T6-lacunes — thomas

**Question** : Identifie les thèmes QA sur lesquels notre base de connaissances est encore pauvre.

**Tours** : 4 · **coût** : 0.079 $ · **confiance annoncée** : 70 · **verdict** : réussi · **citations** : 0/0 lues · **Web** : 0

## Réponse

**Sources retenues** : `python qa.py couverture`, `themes`, `inventaire` et `idee lister`, tous en lecture seule. Aucun passage de syllabus n'a été lu, donc je ne cite aucune référence ISTQB. Le Web n'était pas nécessaire. Hypothèse : par « base de connaissances », tu parles de la base d'idées capitalisées. Pour l'état des syllabus, je donne la couverture par thème.

**Constat principal : la base d'idées est vide.** `idee lister` répond « Aucune idée ». Les 40 thèmes de la taxonomie sont à 0 idée, donc tous sont « pauvres ». La question utile est de savoir par où commencer, d'après le nombre de passages de syllabus disponibles.

**Où commencer : thèmes très documentés, 0 idée** (c'est la liste de priorités que renvoie `couverture`)

| Thème | Passages | Remarque |
|---|---|---|
| `exigences` (Exigences et critères d'acceptation) | 1901 | le plus gros réservoir |
| `organisation` (Outils, méthodes, équipes) | 1748 | dont `agile` (1132) et `competences` (590) |
| `metriques` (Métriques et reporting) | 1164 | |
| `estimation` | 1099 | |
| `conception` | 1118 | `boite-noire` 272, `exploratoire` 332 |
| `niveaux-types` | 1006 | |
| `automatisation` | 1019 | `strategie-automatisation` 110 et `maintenance-automatisation` 180 seulement |

**Thèmes avec peu de passages** : `priorisation` (82), `shift` (83), `strategie-automatisation` (110) et `ia-pour-tester` (111). Dans l'index, ils sont minces. Là, la base d'idées pourrait apporter plus que les syllabus, avec le Web et le retour terrain.

**Limites de couverture des syllabus** (d'après `inventaire`)
- **Santé / dispositif médical** : pas de syllabus dédié, donc le thème `reglementee` (301 passages) repose sur l'automobile et la finance.
- **Documents anciens ou retirés** : CTFL-AT 2014 et CTAL-ATT 1.1 sont en retrait par l'ISTQB. CTEL 2011, CT-PT 2018, CT-SEC 2016 et CT-UT 2018 sont anciens. `securite` et `performance` s'appuient donc sur des sources datées.
- **Français partiel** : 14 codes en FR contre 26 en EN. CTFL 4.0.1 n'existe qu'en anglais dans la bibliothèque.
- **Nouveautés absentes** : DevOps, shift-right et CI/CD reposent sur CT-QDO 1.0, en anglais seulement. L'API n'a pas de syllabus dédié.

**Par quoi je commencerais**

| Piste | Impact | Effort |
|---|---|---|
| Capitaliser 3-5 idées sur `agile` et `metriques`, thèmes très documentés et courants pour un QA Lead | fort | faible |
| Une idée par thème de la stratégie d'automatisation (`strategie-automatisation`, `maintenance-automatisation`, `api`) | fort | moyen |
| Compléter `reglementee` et `shift-right` avec une recherche Web ciblée | moyen | moyen |

**Où creuser ensuite** : lance `idee lister --theme <code>` puis `chercher --theme <code>` sur `agile`, `metriques` ou `exigences`. Pour combler un manque de syllabus, utilise `/ajouter-syllabus <code>`.

**Confiance : 70/100** (bonne). Les chiffres viennent directement de l'outil, mais je n'ai lu aucun passage. Le nombre de passages mesure le volume des syllabus, pas leur pertinence pour ton contexte.

**Questions à choix**

1. Sur quel thème veux-tu qu'on commence à capitaliser ?
   1. Agile et organisation des équipes
   2. Métriques et reporting
   3. Exigences et critères d'acceptation

2. Quelle suite veux-tu ?
   1. Approfondir un thème : je lis les passages et je te propose des idées
   2. Comparer deux thèmes
   3. Combler un manque de syllabus avec `/ajouter-syllabus <code>`

**À capitaliser ?** Rien pour l'instant. Aucun passage n'a été lu, donc je ne peux pas proposer de JSON avec un extrait vérifié. Choisis un thème et je prépare des propositions.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py inventaire; python qa.py themes; python qa.py couverture`
- `python qa.py idee lister 2>&1 | head -20`
