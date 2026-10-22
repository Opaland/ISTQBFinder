# T2-rbt-agile — thomas

**Question** : Recherche des idées pour intégrer le risk-based testing dans une équipe produit agile.

**Tours** : 5 · **coût** : 0.149 $ · **confiance annoncée** : 82 · **citations** : 3/3 lues · **Web** : 0

## Réponse

Les syllabus ISTQB couvrent bien ce sujet, et c'est le CTAL-AT v2.0 (2026) qui répond le plus directement à ta question. La base d'idées est vide sur ce thème. Je n'ai lu que les passages cités ci-dessous.

**Pistes par syllabus**

- **CTAL-AT v2.0 (EN, 2026-04-17), §3.1.1 Test planning in Agile**
  - En planification d'itération, le testeur peut animer des sessions de *risk-storming* avec le métier et les développeurs. Elles servent à identifier les risques, prioriser les activités de test, définir les conditions de test et affiner les critères d'acceptation [CTAL-AT v2.0, §3.1.1, pp. 24-25].
  - En planification de release, on évalue les risques qualité sur tout le périmètre et on en déduit les objectifs, niveaux, types et techniques de test. Le testeur fait souvent le modérateur d'ateliers collaboratifs (mind-mapping, risk-storming) [pp. 24-25].
  - Les quadrants de test aident à choisir types et niveaux de test pour l'itération [p. 25].
  - La Definition of Done doit préciser comment les résultats de test et la couverture contribuent à la DoD de chaque item [p. 25].

- **CTFL-AT v2014 (EN), §3.2.1 Assessing quality risks**
  - *Source ancienne (2014), à recouper avec le CTAL-AT v2.0.* Elle donne un processus en 6 étapes pour l'itération [CTFL-AT 2014, §3.2.1, p. 32] :
    1. Réunir l'équipe, testeur inclus.
    2. Lister les items du backlog d'itération.
    3. Identifier les risques par item.
    4. Les évaluer (impact × probabilité).
    5. Proportionner l'effort de test au niveau de risque.
    6. Choisir les techniques de test.
  - Les tâches à risque élevé démarrent plus tôt et reçoivent plus de test [p. 32].
  - Le syllabus prévoit un réajustement périodique de l'analyse (nouveaux risques, réévaluation, efficacité des mitigations) [p. 32].
  - On peut aussi traiter un risque avant l'exécution, par exemple en relisant à fond les user stories [p. 32].

- **CTFL v4.0.1 (EN), §5.1.2 Contribution du testeur à la planification**
  - En release planning, le testeur participe aux analyses de risques projet et qualité.
  - En iteration planning, il participe à l'analyse détaillée des risques par user story, évalue la testabilité et estime l'effort de test [CTFL v4.0.1, §5.1.2, pp. 48-49].

- **CTAL-TA v4.0 (EN, 2025), §2.1 Risk analysis**
  - Le risque évolue : le suivi se fait à la fréquence choisie par l'équipe, probablement une fois par itération. Le Test Analyst met à jour le registre des risques et les actions de mitigation [CTAL-TA v4.0, §2.1, p. 25].
  - Facteurs d'évaluation proposés : fréquence d'usage, criticité métier, dommages financiers ou de réputation, qualité de la base de test, contraintes légales ou sécurité [p. 25].
  - Il faut découper l'objet de test en items, car le risque n'est pas réparti uniformément. Il faut aussi choisir les mitigations les plus précoces possibles (*shift left*) [p. 25].

- **CTAL-TM v3.0 (FR), §1.3.6 Métriques de succès et difficultés**
  - Ce sont des questions à poser en rétrospective [CTAL-TM v3.0 FR, §1.3.6, p. 34] :
    - Les bonnes parties prenantes ont-elles participé à l'analyse ?
    - Les défauts critiques ont-ils été trouvés tôt ?
    - Les tests ignorés étaient-ils moins risqués que ceux exécutés ?
    - Sait-on rendre compte des résultats en termes de risque ?
  - Pièges listés, avec leurs remèdes :
    - Niveau de risque difficile à estimer : s'appuyer sur l'historique.
    - Approche qui s'essouffle sous la pression du court terme : suivre et rapporter les risques.
    - Mêmes risques à chaque projet (« déjà vu ») : faire participer les bonnes personnes.
    - Risques importants non identifiés : impliquer des personnes expérimentées.
    - Parties prenantes qui changent : refaire l'analyse en continu.

| Moment | Activité | Qui | Source |
|---|---|---|---|
| Release planning | Risques à gros grain, stratégie de release | Métier + équipe + testeur | CTAL-AT v2.0 ; CTFL v4.0.1 §5.1.2 |
| Iteration planning | Risques par story, effort de test, techniques | Équipe entière | CTAL-AT v2.0 ; CTFL-AT 2014 |
| Pendant l'itération | Mise à jour du registre, réévaluation | Test Analyst / équipe | CTAL-TA v4.0 §2.1 |
| Rétrospective | Mesurer l'efficacité du RBT | Équipe | CTAL-TM v3.0 §1.3.6 |

**Ce que j'en retiens** (interprétation de ma part)
- Une démarche légère est possible : un risk-storming de 30 minutes par planification, puis un niveau de risque noté sur chaque story du board. Ce niveau pilote l'ordre des tâches et la profondeur de test.
- On peut intégrer le risque aux rituels existants : refinement, DoD et rétrospective. Cela évite d'ajouter un processus à côté.
- Ton rôle de Test Manager serait de fournir le cadre (facteurs d'évaluation, échelle, registre partagé) et de laisser l'équipe produit faire l'analyse.

**Où creuser ensuite**
- CTAL-TM v3.0 §1.3 en entier (`section CTAL-TM 1.3`), notamment les techniques de RBT. Je ne l'ai pas lu, je ne cite donc rien dessus.
- CTAL-AT v2.0, la suite de §3.1 (stratégie de test projet, §3.1.2).
- CTFL v4.0.1 §5.2 (risques produit et projet), référencé par le CTAL-TA.

**Confiance : 82/100** (bonne). La confiance documentaire est de 100/100 et j'ai lu 5 passages de 5 syllabus. J'applique −15 parce que la procédure détaillée en 6 étapes vient du syllabus de 2014. J'applique −10 parce que la synthèse « ce que j'en retiens » est mon raisonnement. Je compte +5 pour les syllabus courants qui concordent, et je n'ai pas fait de recherche Web.

**À capitaliser ?** (rien n'est enregistré sans ton accord)
1. **Pattern « risk-storming en planification d'itération »** : niveau de risque par story qui pilote l'ordre et l'effort de test, avec réévaluation à chaque itération (CTAL-AT v2.0, CTFL-AT 2014, CTAL-TA v4.0).
2. **Indicateurs de validation du RBT en rétrospective** : les questions de CTAL-TM §1.3.6 transformées en 3-4 métriques d'équipe.

Veux-tu que j'enregistre l'une de ces idées, ou que je lise CTAL-TM §1.3 en entier d'abord ?

## Commandes exécutées

- `Skill {"skill": "qa-knowledge"}`
- `python qa.py idee chercher risk-based testing agile; python qa.py chercher "risk-based testing agile" ; python qa.py chercher "risk-based testing iteration planning"; python qa.py chercher "analyse de`
- `python qa.py lire 2822 --contexte 1; python qa.py lire 4826 --contexte 1; python qa.py lire 1519 --contexte 1; python qa.py lire 4562 --contexte 1; python qa.py lire 1762 --contexte 1`
