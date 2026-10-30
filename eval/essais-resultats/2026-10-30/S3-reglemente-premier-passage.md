# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 11 · **coût** : 0.272 $ · **confiance annoncée** : 60 · **verdict** : réussi · **citations** : 14/14 lues · **Web** : 0 · **critères** : 9/9 · **fidélité** (juge LLM, indicatif) : 0.8 sur 4 lignes citées, 0 contradiction(s)

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

**Synthèse** : la démarche a un point solide, la traçabilité, et un écart net, l'analyse de risques faite une seule fois. Les tests système manuels ne contredisent pas l'ISTQB, mais l'absence de lien avec les risques et la régression pèse sur l'avis. Les trois pratiques sont des **intentions** (« je prévois »). Le niveau atteint est donc plafonné à 1.

**Pratiques reformulées** (uniquement celles que tu décris)
- P1 : matrice de traçabilité exigences → tests, tenue dans un tableur.
- P2 : analyse de risques réalisée une seule fois, en début de projet.
- P3 : tests système manuels avant chaque release.

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Matrice exigences → tests (tableur) | Intention | Partiellement aligné | La traçabilité doit être établie et maintenue tout au long du processus de test. Elle relie base de test, testware (conditions, **risques**, cas de test), résultats et anomalies. Exigences → cas de test vérifie la couverture. Résultats → risques permet d'évaluer le risque résiduel. Elle sert aussi à mesurer l'impact des changements et à faciliter les audits. Le syllabus ne dit rien sur l'outil : le tableur n'est ni bon ni mauvais en soi. Ta matrice s'arrête aux exigences : les liens vers les risques, les résultats et les anomalies ne sont pas mentionnés. | [CTFL v4.0.1 EN, §1.4.4, p. 20] ; [CTFL v4.0.1 EN, §1.4.4, p. 21] |
| P2 Analyse de risques unique, en début de projet | Intention | **Écart** (sur le « une seule fois ») | L'analyse des risques (identification + évaluation) est suivie du contrôle des risques (atténuation + suivi). Le suivi sert à vérifier l'efficacité des mesures et à repérer les risques émergents. Le suivi des tests doit inclure le suivi des risques : analyser les nouveaux risques qualité et ajuster le registre des risques. Commencer tôt est cohérent (« idéalement tôt dans le cycle »), mais une analyse figée ne couvre pas le suivi. | [CTFL v4.0.1 EN, §5.2, p. 51] ; [CTFL v4.0.1 EN, §5.2.4, p. 53] ; [CTAL-TM v3.0 EN, §1.3.1, p. 28] |
| P3 Tests système manuels avant chaque release | Intention | Partiellement aligné | Les types de test (fonctionnel, non fonctionnel dont la sécurité, boîte noire) s'appliquent à tous les niveaux. Après une modification, il faut des tests de confirmation et de régression, précédés d'une analyse d'impact. Les suites de régression sont « de bonnes candidates à l'automatisation ». Le syllabus ne dit pas que le manuel est interdit. En revanche, des tests uniquement avant release, sans lien avec les risques, trouvent les défauts tard. L'étendue de la régression et la rigueur doivent suivre le niveau de risque. | [CTFL v4.0.1 EN, §2.2.2, p. 30] ; [CTFL v4.0.1 EN, §2.2.3, p. 31] ; [CTAL-TM v3.0 EN, §1.3.4, p. 31] |

**Ce qui manque**
- **Évaluation des risques : probabilité × impact, ou matrice de risques.** Sans elle, rien ne justifie la profondeur de test. [CTFL v4.0.1 EN, §5.2.3, p. 53]
- **Identification avec des parties prenantes variées** (ateliers, entretiens). [CTAL-TM v3.0 EN, §1.3.1, p. 28] ; [CTFL v4.0.1 EN, §5.2.3, p. 52]
- **Atténuation par les tests** : choix des techniques, de la couverture, des types de test, de l'indépendance et du niveau d'expérience des testeurs. [CTFL v4.0.1 EN, §5.2.4, p. 53]
- **Suivi des risques pendant le projet** : réévaluation, nouveaux risques, registre mis à jour. [CTAL-TM v3.0 EN, §1.3.1, p. 28]
- **Priorisation de l'exécution selon le risque** (en profondeur ou en largeur), et compte rendu en risque résiduel pour décider de la release. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- **Analyse d'impact et stratégie de régression** : confirmation, régression, et réflexion sur l'automatisation. [CTFL v4.0.1 EN, §2.2.3, p. 31]
- **Niveaux de test** autres que le système : aucun test n'est mentionné avant la phase système. Le syllabus recommande de tester tôt les risques élevés. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- **Stratégie de test écrite, planification, supervision et contrôle, environnement de test** : rien n'est décrit. Ce sont les domaines du niveau 2 de la grille du dépôt.
- **Dispositif médical** : aucune exigence réglementaire n'est mentionnée dans ta démarche. Voir les limites.

**Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné**
- **Justification** : aucune pratique n'est « en place » avec une preuve citée. La grille du dépôt plafonne alors le niveau à 1.
- **Niveau visé** : en l'état, le plan ne remplit pas les critères du niveau 2 (grille du dépôt). L'analyse de risques n'est pas suivie, la stratégie n'est pas écrite, et la supervision et l'environnement de test ne sont pas décrits.
- **Pour atteindre le niveau 2** : appliquer les pratiques et produire des preuves : stratégie de test écrite, registre des risques révisé, matrice reliée aux risques et aux résultats, rapports de test en risque résiduel.
- **Pour le niveau 3 et au-delà** : les critères des niveaux 3 à 5 sont une adaptation du dépôt (grille du dépôt), pas une lecture du syllabus.

**Confiance : 60/100 (moyenne)**
Calcul : base 71 × 0,6 = 43 ; 16 passages lus +20 ; 2 syllabus concordants +10 ; raisonnement −10 → 63, plafonné à 60 car une notion de la question n'est pas couverte (cadre réglementaire).
Raisons : les passages de CTFL et de CTAL-TM concordent. Mon jugement sur le tableur et sur le manuel relève en partie du raisonnement.

**Limites**
- **Aucun syllabus de la bibliothèque ne couvre le cadre réglementaire d'un dispositif médical** (IEC 62304, ISO 14971, MDR/FDA, etc.). Tout ce qui en dépend est « Non vérifiable » ici : le niveau de rigueur exigé, l'analyse de risques réglementaire, la traçabilité et la documentation de validation. Un seul passage lu, sur les systèmes critiques, indique que des normes de sûreté peuvent imposer des techniques de test et une couverture selon le niveau d'intégrité, et que le Test Manager doit s'y conformer. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- Pour le même sujet, l'analyse de risques d'un dispositif médical est très probablement soumise à des exigences réglementaires bien plus strictes que « une fois en début de projet ». Je ne peux pas le confirmer avec cette bibliothèque.
- La série ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque : toute conformité ISO est non vérifiable.
- Je n'ai pas vu comment tu tiens la matrice (versionnement, revues). Je n'ai donc pas pu juger la maintenance de la traçabilité.

**Où creuser ensuite**
- à lire : CTAL-TM v3.0 EN §1.3.5 (techniques de test basé sur les risques, légères et lourdes ; passage entamé seulement, non cité)
- à lire : CTEL-ITP 2011 EN §2.5.4.4 (amélioration du processus de test et adoption de normes et réglementations)
- à lire : CTAL-TM v3.0 EN §1.3.2 et §1.3.3 (identification et évaluation des risques)
- Pour la partie réglementaire : une recherche plus large avec Thomas.

**Questions à choix**

Quel est le cadre réglementaire de ton dispositif ?
1. Marquage CE (règlement européen sur les dispositifs médicaux)
2. FDA (États-Unis)
3. Autre ou pas encore défini

Que veux-tu faire ensuite ?
1. Détailler la liste de contrôle d'un test basé sur les risques pour ton cas
2. Lire les techniques de test basé sur les risques (CTAL-TM §1.3.5)
3. Passer la main à Thomas pour une recherche sur le cadre réglementaire

**Piste à conserver (JSON, non enregistrée)**
```json
{"titre":"Liste de contrôle RBT sur un projet à risque élevé","contenu":"Identifier les risques avec des parties prenantes variées ; évaluer probabilité × impact ; atténuer par techniques, couverture et indépendance ; prioriser l'exécution ; suivre les risques et mettre à jour le registre ; rapporter en risque résiduel","sources":["CTFL v4.0.1 EN, §5.2.3, p. 53","CTAL-TM v3.0 EN, §1.3.1, p. 28"],"statut":"brouillon"}
```

**Traçabilité**
- **Date de l'avis** : 2026-10-30.
- **Documents lus**
  - CTFL-4.0.1-en, v4.0.1 (2024-09-15) : §1.4.4 (p. 20-21), §5.2 à §5.2.4 (p. 51-53), §2.2.2 (p. 29-30), §2.2.3 (p. 30-31).
  - CTAL-TM-3.0-en, v3.0 (2024-05-03) : §1.3.1 (p. 28), §1.3.4 (p. 30-31) ; page 31 lue. Le début de §1.3.5 a été affiché, sans être cité.
- **Requêtes `chercher`**
  - « risk-based testing identification évaluation atténuation revue des risques »
  - « traceability requirements test cases coverage »
  - « risk-based testing CTAL-TM gestion des risques revue périodique évaluation des risques »
  - « regulatory safety-critical medical device regulated domain »
  - « system testing regression testing automation test levels manual before release »
- **Grille** : `referentiel/grille-maturite.md`.

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/referentiel/grille-m`
- `python qa.py chercher "risk-based testing" identification évaluation atténuation revue des risques`
- `python qa.py chercher "traceability requirements test cases coverage"`
- `python qa.py section CTFL-4.0.1-en 1.4.4; python qa.py section CTFL-4.0.1-en 5.2`
- `python qa.py chercher "risk-based testing" CTAL-TM gestion des risques revue périodique évaluation des risques`
- `python qa.py chercher "regulatory safety-critical medical device regulated domain"`
- `python qa.py section CTAL-TM-3.0-en 1.3.1 --max-caracteres 3500; python qa.py section CTAL-TM-3.0-en 1.3.4 --max-caracteres 3500`
- `python qa.py chercher "system testing regression testing automation test levels manual before release"`
- `python qa.py page CTAL-TM-3.0-en 31; python qa.py section CTFL-4.0.1-en 2.2.2 --max-caracteres 3000; python qa.py section CTFL-4.0.1-en 2.2.3 --max-caracteres 2500`
- `python qa.py confiance --autorite 0 --base 71 --lus 16 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 1`
