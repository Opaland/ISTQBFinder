# T5-priorisation — thomas

**Question** : Compare les techniques de priorisation des tests décrites par l'ISTQB.

**Tours** : 7 · **coût** : 0.111 $ · **confiance annoncée** : 83 · **verdict** : réussi · **citations** : 3/3 lues · **Web** : 0

## Réponse

Les syllabus décrivent trois stratégies de priorisation des cas de test au niveau Foundation, et deux variantes de la priorisation par les risques au niveau Advanced. Les passages sont dans CTFL §5.1.5 et CTAL-TM §1.3.4.

**Sources retenues** : CTFL v4.0.1 EN, §5.1.5 ; CTAL-TM v3.0 EN, §1.3.4 et début de §1.3.5 ; CTAL-TA v4.0 EN, §2.2. La base d'idées n'a rien donné. Des passages sont aussi remontés dans CT-SEC 2016, CT-FT 1.0 et CT-GenAI 1.1, mais je ne les ai pas lus, donc je ne m'en sers pas.

**Hypothèse de contexte** : tu veux ordonner l'exécution de tests déjà conçus, sans projet précis.

**Pistes par syllabus**
- **CTFL v4.0.1 §5.1.5, priorisation des cas de test**
  - Priorisation par les risques : on exécute d'abord les tests qui couvrent les risques les plus importants. [CTFL v4.0.1 EN, §5.1.5, p. 50]
  - Priorisation par la couverture : on exécute d'abord les tests qui atteignent la couverture la plus haute (exemple cité : les instructions). La variante « couverture additionnelle » choisit à chaque pas le test qui ajoute le plus de couverture nouvelle. [CTFL v4.0.1 EN, §5.1.5, p. 50]
  - Priorisation par les exigences : on suit les priorités des exigences, définies par les parties prenantes et reliées aux tests par la traçabilité. [CTFL v4.0.1 EN, §5.1.5, p. 50]
  - Deux limites s'appliquent à toutes les stratégies : un test prioritaire qui dépend d'un test moins prioritaire oblige à exécuter ce dernier d'abord. L'ordre doit aussi tenir compte de la disponibilité des ressources (outils, environnements, personnes). [CTFL v4.0.1 EN, §5.1.5, p. 50]
- **CTAL-TM v3.0 §1.3.4, atténuation des risques qualité**
  - La priorisation à l'implémentation repose sur les niveaux de risque. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
  - Depth-first : ordre strictement décroissant du niveau de risque. C'est adapté quand il faut réduire les plus gros risques au plus tôt. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
  - Breadth-first : au moins un test par risque en priorité maximale, puis les autres par niveau de risque. C'est adapté quand les parties prenantes veulent une vue d'ensemble de la qualité tôt. En pratique, on démarre souvent en depth-first puis on passe en breadth-first quand le temps manque. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
  - Si le temps est épuisé, le risque résiduel fonde une recommandation justifiée à la direction : prolonger les tests ou accepter le risque restant. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
  - *À creuser : §1.3.5, techniques lourdes (systèmes critiques) ou légères.* Je n'ai lu que son début.
- **CTAL-TA v4.0 §2.2, contrôle des risques**
  - Pour la sélection des tests de régression, le Test Analyst peut s'appuyer sur les profils opérationnels. Il priorise alors les schémas d'usage critiques et fréquents. Il peut aussi utiliser l'analyse d'impact. [CTAL-TA v4.0 EN, §2.2, p. 27]
  - Il combine les techniques de sélection en équilibrant couverture et taille de la suite, puis les réévalue après chaque cycle. [CTAL-TA v4.0 EN, §2.2, p. 27]

| Approche | Principe | Quand l'utiliser | Source |
|---|---|---|---|
| Par les risques | Les tests des risques majeurs passent en premier. | Le temps est limité et l'analyse de risque existe. | CTFL §5.1.5, CTAL-TM §1.3.4 |
| Depth-first | Ordre strict de risque décroissant. | Il faut réduire les gros risques au plus tôt. | CTAL-TM §1.3.4 |
| Breadth-first | Un test par risque d'abord, puis le reste. | On veut une vue globale de la qualité tôt. | CTAL-TM §1.3.4 |
| Par la couverture | Les tests à couverture maximale d'abord, ou à couverture additionnelle. | Une mesure de couverture est disponible (exemple du syllabus : les instructions). | CTFL §5.1.5 |
| Par les exigences | Les priorités des parties prenantes, via la traçabilité. | Les exigences sont priorisées et tracées. | CTFL §5.1.5 |
| Profils opérationnels / analyse d'impact | Sélection et priorisation pour la régression. | Régression en cycles itératifs. | CTAL-TA §2.2 |

**Ce que j'en retiens** (interprétation)
- Ces approches ne s'excluent pas. Le syllabus Foundation les présente comme des stratégies courantes, et CTAL-TM décrit lui-même un passage d'un mode à l'autre en cours de projet.
- Seule la priorisation par les risques est détaillée au niveau Advanced. Les deux autres restent au niveau Foundation dans les passages que j'ai lus.
- Les dépendances entre tests et les ressources s'appliquent quelle que soit la stratégie choisie.

**Par quoi je commencerais**
1. Priorisation par les risques, avec depth-first puis bascule en breadth-first : impact fort, effort moyen (il faut une analyse de risque).
2. Priorisation par les exigences : impact moyen, effort faible si la traçabilité existe déjà.
3. Couverture additionnelle : impact moyen, effort moyen à fort (il faut un outil de mesure).

**Où creuser ensuite** : `section CTAL-TM-3.0-en 1.3.5` (techniques lourdes et légères), `section CTFL-4.0.1-en 5.2.3` (analyse de risque), `section CTAL-TA-4.0-en 2.2`.

**Confiance : 83/100 (élevée)** — base 88 × … ; 3 passages lus +20 ; 2 syllabus concordants +10 (calcul par `qa.py confiance`). Pas de Web, et les versions FR de CTFL et CTAL-TA n'ont pas été relues.

**Questions à choix**
1. Quel est ton contexte ?
   1. Agile, itérations courtes
   2. Séquentiel / réglementé
   3. Régression de produit existant
2. Quelle suite veux-tu ?
   1. Approfondir CTAL-TM §1.3.5
   2. Comparer avec la sélection de régression (CTAL-TA)
   3. Capitaliser l'idée ci-dessous

**À capitaliser ?** (1 proposition ; le code de thème est à choisir avec `python qa.py themes`, mon essai avec « risk-based-testing » a été refusé. Je n'ai donc pas pu faire le contrôle de doublons complet, seule la recherche d'idées, vide, a été faite.)
```json
{
  "titre": "Choisir une stratégie de priorisation des cas de test",
  "resume": "Trois stratégies Foundation (risques, couverture, exigences) et deux modes de la priorisation par les risques (depth-first, breadth-first).",
  "principe": "Choisir la stratégie selon le contexte, respecter les dépendances entre tests et les ressources disponibles, et basculer de depth-first à breadth-first quand le temps manque.",
  "theme": "<à choisir via qa.py themes>",
  "references": [
    {"document": "CTFL-4.0.1-en", "page": 50, "extrait": "Risk-based prioritization, where the order of test execution is based on the results of risk analysis"},
    {"document": "CTAL-TM-3.0-en", "page": 31, "extrait": "This approach is called depth-first and is appropriate when it is important to mitigate the highest level risks as early as possible."}
  ]
}
```
Rien n'est enregistré. La conversation principale lancera `idee ajouter` après ton accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher priorisation des tests risque`
- `python qa.py chercher priorisation des tests`
- `python qa.py chercher test case prioritization risk-based coverage-based additional`
- `python qa.py lire 4846 --contexte 1 --max-caracteres 5000; python qa.py lire 4375 --contexte 1 --max-caracteres 4000; python qa.py lire 1767 --max-caracteres 3000`
- `python qa.py confiance --base 88 --lus 3 --concordants 2 2>&1 | tail -5; python qa.py idee doublons --titre "Comparer les stratégies de priorisation des cas de test" --resume "Risque, couverture, exig`
