# T5-priorisation — thomas

**Question** : Compare les techniques de priorisation des tests décrites par l'ISTQB.

**Tours** : 4 · **coût** : 0.114 $ · **confiance annoncée** : 90 · **citations** : 3/3 lues · **Web** : 0

## Réponse

Il y a deux niveaux dans les syllabus. Le Foundation donne trois **stratégies de priorisation des cas de test**. L'Advanced Test Management détaille la plus utilisée, la priorisation par les risques, avec deux variantes d'ordonnancement et des techniques d'analyse de risque. Les deux syllabus sont complémentaires et je n'ai pas trouvé de contradiction entre eux.

**Pistes par syllabus**
- **CTFL v4.0.1 (EN) — §5.1.5 Test Case Prioritization**
  - Trois stratégies : par les risques, par la couverture, par les exigences [CTFL v4.0.1 EN, §5.1.5, p. 50].
  - La couverture a une variante, la couverture additionnelle. Le premier test est celui qui couvre le plus. Chaque test suivant est celui qui ajoute le plus de couverture [p. 50].
  - Deux contraintes s'appliquent à toutes les stratégies. Si un test prioritaire dépend d'un test moins prioritaire, ce dernier passe d'abord. La disponibilité des ressources compte aussi : outils, environnements, personnes [p. 50].
- **CTAL-TM v3.0 (EN) — §1.3.4 Quality Risk Mitigation Through Appropriate Testing**
  - Deux ordonnancements. En *depth-first*, on exécute par niveau de risque décroissant. En *breadth-first*, on affecte au moins un test par risque en priorité maximale, puis on trie le reste par niveau de risque [CTAL-TM v3.0 EN, §1.3.4, p. 31].
  - En pratique, on commence souvent en depth-first, puis on bascule en breadth-first quand le temps manque [p. 31].
  - Si le temps est épuisé, l'approche par les risques permet de recommander à la direction soit d'étendre les tests, soit d'accepter le risque résiduel [p. 31].
- **CTAL-TM v3.0 (EN) — §1.3.5 Techniques for Risk-Based Testing**
  - Les techniques *heavyweight* sont formelles et adaptées aux systèmes critiques : hazard analysis, cost of exposure, FMEA, fault tree analysis [CTAL-TM v3.0 EN, §1.3.5, p. 32].
  - Les techniques *lightweight* réduisent le risque à impact × probabilité sur une échelle ordinale : PRAM, PRISMA, SST [p. 32].

**Comparaison**

| Approche | Principe | Quand l'utiliser | Source |
|---|---|---|---|
| Par les risques | Les tests qui couvrent les risques majeurs passent en premier | Quand il existe une analyse de risque | CTFL §5.1.5 |
| Par la couverture (et additionnelle) | Les tests qui couvrent le plus passent en premier | Quand la couverture est mesurable, par exemple en code | CTFL §5.1.5 |
| Par les exigences | On suit la priorité des exigences définie par les parties prenantes | Quand la traçabilité exigences ↔ tests existe | CTFL §5.1.5 |
| Risque depth-first | Ordre strictement décroissant de risque | Quand il faut réduire les plus gros risques au plus tôt | CTAL-TM §1.3.4 |
| Risque breadth-first | Au moins un test par risque d'abord | Quand les parties prenantes veulent une vue globale de la qualité au plus tôt | CTAL-TM §1.3.4 |

**Ce que j'en retiens** (interprétation)
- Les trois stratégies du CTFL ne s'excluent pas. Les critères de choix du syllabus sont la disponibilité des données (risques, couverture, traçabilité), les dépendances entre tests et les ressources.
- Le CTAL-TM décrit le cas particulier du risque. Il ajoute le séquencement (depth/breadth) et le lien avec la décision de fin de test.
- La priorisation du *plan d'amélioration* du CTEL-ITP (§6.4.1) porte sur un autre sujet. Je ne l'ai pas lue, donc je n'en dis rien de plus.

**Où creuser ensuite**
- `section CTAL-TM-3.0-en 1.3` : l'identification et l'évaluation des risques, avant la priorisation.
- `section CTAL-TA-4.0-en 2` : le rôle du Test Analyst dans le RBT, que je n'ai pas lu.
- `section CTFL-4.0.1-en 5.2.3` : la section sur l'analyse de risque, vers laquelle renvoie le §5.1.5.
- `section CT-GenAI-1.1-en 2.2.2` : un exercice de priorisation assistée par GenAI. Il apparaît dans les résultats mais je ne l'ai pas lu.

**Confiance : 90/100** (élevée)
- La confiance documentaire est de 100/100 et j'ai lu intégralement deux syllabus pertinents, CTFL et CTAL-TM.
- J'ai retiré 10 points parce que je n'ai lu ni le CTAL-TA ni le CTAL-TTA, qui concordent probablement. Je n'ai pas cherché la priorisation des tests de régression en particulier.

**À capitaliser ?**
1. Les trois stratégies de priorisation du CTFL (risque, couverture, exigences), avec leurs contraintes de dépendances et de ressources.
2. L'idée depth-first puis breadth-first quand le temps manque, avec la recommandation « étendre ou accepter le risque résiduel ».

Je n'ai rien enregistré. Dis-moi si tu veux que je capitalise l'une de ces idées ou les deux.

## Commandes exécutées

- `cat .claude/skills/qa-knowledge/reference/strategie.md | head -80; python qa.py idee chercher priorisation des tests`
- `python qa.py chercher test case prioritization; python qa.py chercher priorisation des cas de test; python qa.py chercher risk-based prioritization risk level`
- `python qa.py section CTFL-4.0.1-en 5.1.5; python qa.py lire 4361 --contexte 1; python qa.py section CTAL-TM-3.0-en 1.3.5`
