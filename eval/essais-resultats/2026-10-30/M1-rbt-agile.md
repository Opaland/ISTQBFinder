# M1-rbt-agile — thomas

**Question** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

**Tours** : 8 · **coût** : 0.222 $ · **confiance annoncée** : 81 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 12/12 · **fidélité** (juge LLM, indicatif) : 0.59 sur 3 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : CTAL-AT v2.0 EN §3.1.1 (2026) ; CTFL v4.0.1 EN §5.1.2 ; CTAL-TM v3.0 FR §1.3.6 ; CTFL-AT 2014 EN §3.2.1, **syllabus en retrait** (successeur : CTAL-AT). La base d'idées ne contient rien sur le sujet. Vu seulement en extrait, donc non cité : CTAL-TA v4.0 §2 et §2.2, CTAL-TTA v4.0 §1.2. Je n'ai pas lu de section dédiée au test basé sur les risques dans CTAL-AT v2.0. Je n'ai pas fait de recherche Web : la question ne nomme aucun outil.

L'ISTQB ne décrit pas un « RBT agile » à part. Il greffe l'analyse de risque sur les deux rituels de planification, release et itération, puis la réévalue en continu. La description la plus détaillée est dans le CTFL-AT 2014, ancien mais explicite. Le CTAL-AT v2.0 la confirme avec le « risk-storming ».

**Hypothèse de contexte** : équipe Scrum d'environ 6 personnes, application web, pas de contrainte réglementaire forte.

**Méthode pas à pas**
1. **Planification de release : cartographier les risques qualité à gros grain.** Les représentants métier donnent une vue d'ensemble des risques et toute l'équipe aide à les identifier et à les évaluer [CTFL-AT 2014 EN, §3.2.1, p. 32]. Le livrable est un niveau de risque par fonctionnalité de la release. Le testeur évalue les risques sur tout le périmètre et définit niveaux, types, approches et techniques de test pour les atténuer [CTAL-AT v2.0 EN, §3.1.1, p. 25]. Le testeur participe aussi aux analyses de risques projet et qualité [CTFL v4.0.1 EN, §5.1.2, p. 48].
2. **Planification d'itération : analyse détaillée des user stories.** Le testeur peut animer des séances de risk-storming avec le métier et les développeurs [CTAL-AT v2.0 EN, §3.1.1, p. 24]. Il prend part à l'analyse détaillée des risques des stories [CTFL v4.0.1 EN, §5.1.2, p. 48].
3. **Appliquer la boucle en 6 étapes du CTFL-AT** [CTFL-AT 2014 EN, §3.2.1, p. 32] :
   - réunir l'équipe, testeurs compris ;
   - lister les éléments du backlog ;
   - identifier les risques par élément, sur toutes les caractéristiques qualité ;
   - évaluer chaque risque (catégorie, impact × probabilité) ;
   - proportionner l'effort de test au niveau de risque ;
   - choisir la technique de test qui atténue chaque risque.
4. **Piloter l'ordre et l'effort.** Les tâches à risque élevé démarrent plus tôt et reçoivent plus de tests, celles à risque faible plus tard et moins de tests [CTFL-AT 2014 EN, §3.2.1, p. 32]. Le livrable est un task board annoté par niveau de risque.
5. **Atténuer avant l'exécution.** Si l'identification révèle des problèmes dans les stories, relire les stories en profondeur compte comme une atténuation [CTFL-AT 2014 EN, §3.2.1, p. 32].
6. **Réévaluer périodiquement.** Il s'agit d'identifier de nouveaux risques, de réévaluer les niveaux existants et de mesurer l'efficacité des atténuations [CTFL-AT 2014 EN, §3.2.1, p. 32]. L'analyse est continue et itérative, pas un acte unique de début de projet [CTAL-TM v3.0 FR, §1.3.6, p. 34].
7. **Mesurer en rétrospective.** Questions à se poser :
   - les bonnes parties prenantes ont-elles participé ?
   - les défauts de priorité élevée sont-ils apparus tôt ?
   - les tests ignorés étaient-ils moins risqués que ceux exécutés ?
   - sait-on expliquer les résultats en termes de risque ? [CTAL-TM v3.0 FR, §1.3.6, p. 34]

   Ce passage liste aussi des pièges : évaluation difficile, complaisance, risques majeurs non identifiés.

**Exemple de mise en œuvre** (fictif, interprétation)
Sprint de 2 semaines. Le premier jour, 45 minutes de risk-storming (PO, dev, testeur) sur les 8 stories (étapes 2-3). Chaque story reçoit un niveau haut, moyen ou bas, affiché sur le board (étape 4). Les stories « haut » sont testées dès les premiers jours, avec une revue de la story avant codage (étape 5). À la rétrospective, on regarde si les bugs échappés viennent de stories classées « bas » (étapes 6-7).

**Adaptation par domaine**
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Pas de syllabus santé dans la bibliothèque (IEC 62304 absente). Risque tracé et formalisé. | à lire : CTAL-AT v2.0 §3.1.2 ; Web justifié pour la norme |
| Web | Pas de syllabus dédié. Principes transposés tels quels. | à lire : CT-PT §3.2 pour les risques de performance |
| Embarqué | Risques matériel/logiciel, couverture liée au niveau d'intégrité. | à lire : CTAL-TTA v4.0 §2.8.2, CT-AuT |
| Mobile | Risques propres aux appareils et réseaux. | à lire : CT-MAT 2019 §1.8 |
| API | Risques de contrat et d'intégration. | à lire : CTAL-TTA v4.0 §2.7, CT-QDO §3.2.2 |

**Par quoi je commencerais**
1. Séance de risk-storming à chaque planification d'itération : impact fort, effort faible.
2. Niveau de risque visible sur le board qui pilote l'ordre des tests : impact fort, effort faible.
3. Réévaluation en rétrospective avec les métriques de CTAL-TM §1.3.6 : impact moyen, effort moyen.

**Où creuser ensuite**
- `section CTAL-AT-2.0-en 3.1` en entier (planification, Definition of Done).
- `section CTAL-TM-3.0-fr 1.3` (techniques et déroulé du RBT).
- `section CTAL-TA-4.0-en 2` (tâches du Test Analyst dans le RBT, réévaluation par itération).
- `section CTFL-4.0.1-en 5.2` (analyse et contrôle des risques).

**Confiance : 81/100 (élevée)** : base 85 × 0,6 = 51 ; 5 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10. La description pas à pas vient d'un syllabus de 2014 en retrait, que le CTAL-AT v2.0 confirme dans ses grandes lignes.

**Questions à choix**
1. Quel est ton contexte ?
   1. Scrum ou Kanban, application web, sans contrainte réglementaire
   2. Domaine réglementé (santé, finance, automobile)
   3. Mobile, embarqué ou API
2. Que veux-tu faire ensuite ?
   1. Approfondir : lire CTAL-AT §3.1 et CTAL-TM §1.3 en entier
   2. Comparer le RBT agile et le RBT séquentiel (CTAL-TM contre CTFL-AT)
   3. Capitaliser l'idée ci-dessous (`/ajouter-syllabus <code>` si tu veux importer un autre syllabus)

**À capitaliser ?** `idee doublons` : aucune idée similaire.
```json
{
 "titre": "Risk-storming à chaque planification d'itération pour piloter l'effort de test",
 "resume": "Analyse de risque qualité légère, répétée à chaque planification de release et d'itération, qui fixe l'ordre et l'effort des tests, puis réévaluée périodiquement.",
 "probleme": "Une équipe agile ne peut pas tout tester à chaque itération et doit prioriser les tests.",
 "principe": "Séance collective (métier, dev, testeur) : identifier les risques par story, évaluer impact et probabilité, proportionner l'effort et choisir les techniques, afficher le niveau sur le board, réévaluer en rétrospective.",
 "theme_principal": "rbt",
 "themes_secondaires": ["agile", "priorisation"],
 "domaine_application": "Équipes agile/Scrum à itérations courtes",
 "prerequis": "Présence du métier et des développeurs en planification ; échelle de risque simple partagée.",
 "benefices": "Effort de test aligné sur le risque, détection précoce des problèmes de stories, langage commun avec le métier.",
 "limites": "Évaluation du risque subjective ; complaisance si les mêmes risques reviennent ; description détaillée tirée d'un syllabus 2014 en retrait.",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ? »",
 "references": [
  {"type": "istqb", "doc_id": "CTFL-AT-2014-en", "pages": "32", "section": "3.2.1", "extrait": "the whole team identifies and assesses the quality risks"},
  {"type": "istqb", "doc_id": "CTAL-AT-2.0-en", "pages": "24", "section": "3.1.1", "extrait": "facilitating risk-storming sessions with business representatives and developers"}
 ]
}
```
Je n'ai rien enregistré. La conversation principale lancera `idee ajouter` si tu es d'accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher risk-based testing agile risque; python qa.py chercher "risk-based testing agile" ; python qa.py chercher "risk analysis iteration planning agile"; python qa.py chercher "te`
- `python qa.py section CTAL-AT-2.0-en 3.1.1 --max-caracteres 6000; echo =======; python qa.py section CTFL-AT-2014-en 3.2.1 --max-caracteres 6000; echo =======; python qa.py chercher "quality risk analy`
- `python qa.py lire 4837 --contexte 1 --max-caracteres 4000; echo =======; python qa.py lire 4572 --contexte 1 --max-caracteres 4000`
- `python qa.py idee doublons --titre "Analyse des risques qualité à chaque planification d'itération (agile)" --resume "Risk-storming en planification d'itération/release, niveau de risque = effort de t`
- `python qa.py themes | head -40; python qa.py confiance --base 85 --lus 5 --concordants 3 --raisonnement 1`
- `python qa.py idee doublons --titre "Analyse des risques qualité à chaque planification d'itération (agile)" --resume "Risk-storming en planification d'itération et de release, niveau de risque = effor`
