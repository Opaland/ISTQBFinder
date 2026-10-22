# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 8 · **coût** : 0.181 $ · **confiance annoncée** : 68 · **verdict** : réussi · **citations** : 12/12 lues · **Web** : 0 · **critères** : 5/5

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est en partie alignée. La traçabilité et les tests système sont compatibles avec l'ISTQB mais incomplets. L'analyse de risques faite une seule fois est un écart. Les trois pratiques sont des intentions, donc le niveau atteint est plafonné à 1.

## Pratiques décrites

- **P1** : matrice de traçabilité exigences → tests, tenue dans un tableur. *Intention.*
- **P2** : analyse de risques faite une seule fois, en début de projet. *Intention.*
- **P3** : tests système manuels avant chaque release. *Intention.*

## Verdicts

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Matrice exigences → tests (tableur) | Intention | Partiellement aligné | La traçabilité relie les éléments de la base de test, le testware (conditions de test, risques, cas de test), les résultats de test et les défauts. Elle permet de vérifier la couverture des exigences par les cas de test. Les résultats de test reliés aux risques servent à évaluer le risque résiduel. Elle sert aussi à analyser l'impact des changements et à faciliter les audits. Ta matrice ne couvre que exigences → tests. Les résultats, les défauts et les risques n'y figurent pas. Le syllabus ne dit rien sur l'outil (tableur ou autre). | [CTFL v4.0.1 EN, §1.4.4, pp. 20-21] |
| P2 Analyse de risques unique en début de projet | Intention | Écart (sur le « une seule fois ») ; l'analyse précoce est alignée | Idéalement, l'analyse des risques produit commence tôt dans le cycle de vie, ce que ta démarche respecte. Mais la gestion des risques comprend aussi le contrôle des risques, c'est-à-dire l'atténuation et le suivi. Le suivi vérifie que les actions d'atténuation sont efficaces et fait apparaître de nouveaux risques. Le pilotage des tests doit inclure le suivi des risques, l'analyse de tout nouveau risque qualité et l'ajustement du registre des risques. Une analyse figée contredit cette boucle. | [CTFL v4.0.1 EN, §5.2.3, p. 52 ; §5.2.4, p. 53] ; [CTAL-TM v3.0 FR, §1.3.1, p. 29] |
| P3 Tests système manuels avant chaque release | Intention | Partiellement aligné | Rien ne contredit le fait de tester manuellement au niveau système. Mais le syllabus attend que l'effort de test soit proportionné au niveau de risque. Les tests à risque élevé commencent tôt, avec des techniques plus rigoureuses. Chaque élément à tester est testé le plus tôt possible. Le niveau de risque influence aussi l'étendue des tests de régression. Ta démarche ne dit pas comment les tests système sont choisis ni priorisés selon les risques. Elle ne dit pas non plus si des tests ont lieu avant le niveau système. Les résultats peuvent être rapportés en risque résiduel pour appuyer la décision de livraison. | [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33] |

## Ce qui manque

- **Parties prenantes** : une identification des risques avec l'échantillon le plus large possible de parties prenantes, dont la liste est convenue avec le chef de projet [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30].
- **Évaluation des risques** : une catégorisation puis une évaluation probabilité × impact, avec une matrice de risque si l'approche est qualitative [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31 ; CTFL v4.0.1 EN, §5.2.3, p. 53].
- **Atténuation** : les résultats de l'analyse doivent déterminer le périmètre, les niveaux et types de test, les techniques, la couverture et l'effort [CTFL v4.0.1 EN, §5.2.3, p. 53].
- **Suivi des risques** : un suivi pendant le projet, avec registre des risques mis à jour [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **Priorisation** : une priorisation de l'exécution fondée sur les risques, en profondeur d'abord ou en largeur d'abord, avec une recommandation fondée sur le risque restant si le temps manque [CTAL-TM v3.0 FR, §1.3.4, p. 33].
- **Technique d'analyse** : le syllabus indique que les systèmes critiques pour la sécurité utilisent très souvent des techniques « lourdes » (formelles, documentées), par exemple l'analyse des dangers ou l'AMDE. Ta démarche ne précise pas laquelle tu retiens [CTAL-TM v3.0 FR, §1.3.5, p. 33].
- **Suivi et rapports** : des métriques de suivi (couverture des exigences, risque résiduel) et des rapports d'avancement et de fin de test [CTFL v4.0.1 EN, §5.3.1-5.3.2, p. 54].
- **Cadre normatif** : le syllabus de gestion des tests demande de respecter les normes de sûreté qui prescrivent des techniques et une couverture selon le niveau d'intégrité. Il cite la norme IEC 61508 en exemple [CTAL-TM v3.0 FR, §1.3.4, p. 32]. Ta démarche ne mentionne aucune exigence de ce type.

## Niveau atteint : 1 — Initial · niveau visé : 2 (Discipliné)

- **Niveau 1** : aucune des trois pratiques n'est déclarée en place. Selon la grille du dépôt, seules les pratiques en place comptent.
- **Niveau 2 visé, mais pas encore atteignable** : il demande une politique et une stratégie de test écrites, une planification et un pilotage du test, une conception et une exécution des tests, et un environnement de test (grille du dépôt). Seules la conception et l'exécution sont esquissées. Aucun pilotage, aucune stratégie ni aucun environnement n'est évoqué. Ces critères sont donc « non démontrés ».
- **Pour passer au niveau 2** :
  1. Écrire la stratégie de test fondée sur les risques.
  2. Rendre l'analyse de risques itérative, avec registre et suivi.
  3. Étendre la matrice aux risques, aux résultats et aux défauts.
  4. Piloter l'avancement avec des rapports.
  5. Documenter l'environnement de test.
- **Niveaux 3 à 5** : leurs critères sont une adaptation du dépôt, pas une lecture du syllabus.

## Confiance : 68/100

- **Pour** : les passages clés ont été lus en entier (CTFL §1.4.4 et §5.2, CTAL-TM §1.3.1 à 1.3.5).
- **Contre** :
  - La description est courte, donc plusieurs critères du niveau 2 sont « non démontrés ».
  - Le contexte réglementaire n'est pas couvert (voir Limites).

## Limites

- **Réglementation** : aucun syllabus de la bibliothèque ne couvre le cadre réglementaire d'un dispositif médical (exigences de cycle de vie logiciel, gestion des risques, documentation). Je n'ai pas lu de texte à ce sujet. Les exigences de traçabilité, de gestion des risques et de documentation propres à ton domaine sont donc **non vérifiables** ici. Elles peuvent être plus strictes que les pratiques ISTQB.
- **ISO** : l'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable.
- **Recherche élargie** : Thomas peut chercher plus largement, y compris sur le Web, si tu veux explorer le cadre réglementaire.

## Questions à choix

**1. Ces pratiques sont-elles déjà appliquées ?**
1. Oui, avec des preuves : matrice existante, registre des risques, rapports de tests.
2. Non, tout est encore prévu.
3. Certaines le sont (précise lesquelles).

**2. Quelle suite veux-tu ?**
1. Une liste de contrôle de risques à valider (modèle JSON, sans enregistrement).
2. Une recherche élargie sur le cadre réglementaire (Thomas).
3. Un nouvel avis après ta réponse à la question 1.

## Traçabilité

- **Date de l'avis** : 2026-10-22.
- **Documents lus** :
  - `CTAL-TM-3.0-fr`, v3.0, publié le 2024-03-28 : §1.3.1 à 1.3.5, pp. 29-34.
  - `CTFL-4.0.1-en`, v4.0.1, publié le 2024-09-15 : §1.4.4, pp. 20-21 ; §5.2, pp. 51-53 ; page 54 (§5.3).
- **Requêtes `chercher`** :
  1. `"risk-based testing identification évaluation atténuation"`
  2. `"traceability requirements test cases coverage"`
  3. `"regression testing before release manual system test execution"`
  4. `"medical device regulatory safety-critical"`
  5. `"test types regression testing change-related confirmation"` (avec `--langue en`)
- **Lu en page entière** : `grille-maturite.md`. Les extraits de `chercher` seuls n'ont pas été cités.

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-144/referentiel/grille-maturi`
- `python qa.py chercher "risk-based testing identification évaluation atténuation" 2>&1 | head -60`
- `python qa.py chercher "traceability requirements test cases coverage" 2>&1 | head -50`
- `python qa.py section CTAL-TM-3.0-fr 1.3.1 ; python qa.py section CTAL-TM-3.0-fr 1.3.2; python qa.py section CTAL-TM-3.0-fr 1.3.3`
- `python qa.py section CTFL-4.0.1-en 1.4.4; python qa.py section CTFL-4.0.1-en 5.2`
- `python qa.py chercher "regression testing before release manual system test execution" 2>&1 | head -30; python qa.py chercher "medical device regulatory safety-critical" 2>&1 | head -30`
- `python qa.py section CTAL-TM-3.0-fr 1.3.4; python qa.py section CTAL-TM-3.0-fr 1.3.5; python qa.py page CTFL-4.0.1-en 54; python qa.py chercher "test types regression testing change-related confirmati`
