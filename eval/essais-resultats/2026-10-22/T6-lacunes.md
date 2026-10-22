# T6-lacunes — thomas

**Question** : Identifie les thèmes QA sur lesquels notre base de connaissances est encore pauvre.

**Tours** : 5 · **coût** : 0.082 $ · **confiance annoncée** : 80 · **citations** : 0/0 lues · **Web** : 0

## Réponse

Le constat est net : **la base d'idées est vide**. `connaissances/connaissances.jsonl` compte 0 ligne, et `couverture` affiche 0 idée sur les 40 thèmes, tous marqués « vide ».

Je ne peux donc pas dire quels thèmes sont plus pauvres que d'autres, puisqu'aucun n'a de contenu. Ce que `couverture` indique, c'est où les syllabus sont riches. Ce sont les thèmes où une première capitalisation rapporterait le plus.

**Thèmes les plus documentés dans les syllabus locaux (nombre de passages)**

| Priorité | Thème | Passages |
|---|---|---|
| 1 | Exigences et critères d'acceptation | 1889 |
| 2 | Outils, méthodes et organisation des équipes | 1736 |
| 3 | Métriques et reporting | 1160 |
| 4 | Test en contexte agile et à l'échelle | 1141 |
| 5 | Analyse et conception des tests | 1107 |
| 6 | Estimation et planification | 1096 |
| 7 | Automatisation des tests | 1005 |
| 8 | Tests fonctionnels | 904 |

**Thèmes avec peu de matière dans les syllabus**

Ces thèmes sont peu couverts par les syllabus, donc le Web ou le retour terrain y seront plus utiles.
- Priorisation des tests : 82 passages.
- Shift-left et shift-right (thème parent) : 82 passages.
- Stratégie et ROI de l'automatisation : 109 passages.
- L'IA au service du test : 110 passages.
- Techniques boîte blanche et couverture : 150 passages.
- Test d'API et de services : 159 passages.
- Maintenabilité des tests automatisés : 177 passages.

Ces nombres comptent des passages, pas la qualité de la couverture. Je n'ai lu aucun passage pour cette réponse, donc je ne cite aucune page ni section.

**Confiance : 80/100.** Les chiffres viennent directement de `couverture` et du fichier de la base. Ils ne disent rien de la pertinence réelle des passages.

**Où creuser ensuite**
- Choisir 2 ou 3 thèmes qui comptent pour ton équipe, par exemple Risk-Based Testing, Métriques et reporting, Tests exploratoires. Je lance alors des recherches sur ces thèmes, je lis les meilleurs passages et je te propose des idées à capitaliser.
- Faire un état des lieux de la bibliothèque. `inventaire` indique que 12 syllabus n'existent qu'en anglais. Je ne l'ai lu que jusqu'à la ligne CTAL-TTA, donc je ne sais pas encore s'il signale des documents absents.

**À capitaliser ?**
Rien à capitaliser pour l'instant, puisque je n'ai lu aucune source. Dis-moi par quel thème tu veux commencer.

## Commandes exécutées

- `Skill {"skill": "qa-knowledge"}`
- `python qa.py couverture 2>&1 | head -80; python qa.py idee --help 2>&1 | head -5`
- `python qa.py inventaire 2>&1 | head -15; wc -l connaissances/connaissances.jsonl`
