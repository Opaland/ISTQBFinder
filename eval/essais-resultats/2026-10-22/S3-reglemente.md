# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 8 · **coût** : 0.161 $ · **confiance annoncée** : 72 · **verdict** : réussi · **citations** : 14/14 lues · **Web** : 0 · **critères** : 5/5

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est partiellement alignée. L'analyse de risques faite une seule fois est un écart net avec le syllabus. La matrice de traçabilité et les tests système manuels sont conformes à l'esprit, mais incomplets. Les trois pratiques sont des intentions, donc le niveau atteint est plafonné à 1.

## Pratiques reformulées (toutes en intention, aucune preuve de mise en œuvre fournie)

- **P1** : matrice de traçabilité exigences → tests, tenue dans un tableur (intention).
- **P2** : analyse de risques réalisée une seule fois, en début de projet (intention).
- **P3** : tests système manuels avant chaque release (intention).

## Verdicts

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Matrice exigences → tests | Intention | Partiellement aligné | La traçabilité est établie et maintenue tout au long du processus de test. Elle relie les éléments de la base de test, le testware (conditions de test, risques, cas de test), les résultats et les défauts. Elle sert à évaluer la couverture, l'impact des changements et le risque résiduel, et elle facilite les audits. Ta matrice ne couvre que le lien exigences → tests. Les liens vers les résultats, les défauts et les risques ne sont pas mentionnés. Le choix d'un tableur n'est pas traité par les syllabus lus, donc je ne le juge pas. | [CTFL v4.0.1 EN, §1.4.4, pp. 20-21] ; matrice utilisée pour l'impact des changements d'exigences sur les tests de régression : [CTAL-TA v4.0 FR, §2.2.1, p. 29] |
| P2 Analyse de risques unique | Intention | **Écart** | Le syllabus dit que l'analyse des risques est « une activité continue et itérative qui ne doit pas être réalisée une seule fois au début du projet ». Le suivi des tests doit inclure le suivi des risques, l'analyse des nouveaux risques et l'ajustement du registre. Le contrôle des risques comprend l'atténuation et le suivi. Les résultats de l'analyse doivent piloter la périmètre, les techniques, la couverture, l'effort et la priorisation des tests. On ne sait pas si ton analyse fait participer plusieurs parties prenantes ni si elle évalue probabilité et impact. | [CTAL-TM v3.0 FR, §1.3.6, p. 34] ; [CTAL-TM v3.0 FR, §1.3.1, p. 29] ; [CTFL v4.0.1 EN, §5.2.3-5.2.4, pp. 52-53] |
| P3 Tests système manuels avant chaque release | Intention | Partiellement aligné | Le test système est un niveau décrit : il porte sur le comportement global du système, fonctionnel et non fonctionnel, et peut être réalisé par une équipe indépendante. Les syllabus lus sur ce point ne contiennent aucune règle qui interdise l'exécution manuelle. Il manque le lien avec les risques. Les tests devraient être priorisés selon le niveau de risque, et le niveau de risque influe sur l'étendue de la régression et sur l'indépendance des tests. Le sujet « une seule campagne avant release » n'est pas traité comme tel : le syllabus mentionne seulement la sélection des tests de régression (impact, historique, couverture). | [CTFL v4.0.1 EN, §2.2.1, p. 29] ; [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33] ; [CTAL-TA v4.0 FR, §2.2.1, p. 29] |
| Exigences réglementaires du dispositif médical | Non décrites | **Non vérifiable** | Le syllabus cite seulement, à titre d'exemple, que des normes de sûreté (ex. IEC 61508) prescrivent des techniques de test et une couverture selon le niveau d'intégrité, et que le Test Manager doit s'assurer qu'elles sont respectées. | [CTAL-TM v3.0 FR, §1.3.4, p. 32] |

## Ce qui manque

- **Parties prenantes et évaluation des risques** : identification des risques avec les parties prenantes, puis évaluation probabilité × impact, par exemple dans une matrice de risque [CTAL-TM v3.0 FR, §1.3.2-1.3.3, pp. 29-31]. Pour un dispositif médical, les facteurs d'impact incluent les besoins en matière de sûreté et la responsabilité juridique [CTAL-TM v3.0 FR, §1.3.3, p. 31].
- **Mise à jour des risques** : suivi et réévaluation des risques pendant le projet, avec registre des risques ajusté [CTAL-TM v3.0 FR, §1.3.1, p. 29 ; §1.3.6, p. 34].
- **Atténuation par les tests** : traduction des risques en choix de techniques, de profondeur et d'ordre d'exécution (profondeur d'abord ou largeur d'abord) [CTAL-TM v3.0 FR, §1.3.4, pp. 32-33].
- **Reporting par les risques** : rapports d'avancement en termes de risque résiduel, pour appuyer la décision de livraison [CTAL-TM v3.0 FR, §1.3.4, p. 32].
- **Traçabilité élargie** : liens vers les résultats de test, les défauts et les risques [CTFL v4.0.1 EN, §1.4.4, pp. 20-21].
- **Stratégie de test écrite** : aucune politique ni stratégie de test, planification, supervision, contrôle ni environnement de test n'est mentionné. La grille du dépôt rattache ces éléments au niveau 2.

## Niveau atteint : 1 — Initial · niveau visé : 2 (Discipliné)

- **Pourquoi le niveau 1** : toutes les pratiques sont des intentions, et la grille du dépôt plafonne alors le niveau à 1.
- **Pourquoi le niveau 2 n'est pas encore le niveau visé complet** : même une fois les pratiques en place, l'analyse de risques unique empêcherait d'atteindre le niveau 2. Les critères de supervision et de contrôle pendant le projet ne seraient pas satisfaits. La stratégie, la planification et l'environnement de test ne sont pas démontrés.
- **Pour passer au niveau 2** :
  1. mettre les pratiques en place et en garder une preuve (matrice, registre des risques, rapports de campagne) ;
  2. rédiger une stratégie de test ;
  3. faire de l'analyse de risques une activité itérative qui pilote les tests ;
  4. suivre les tests et les risques pendant le projet.
- **Niveaux 3 à 5** : leurs critères sont une adaptation du dépôt, pas du TMMi ni de l'ISTQB. Ils ne s'appliquent pas encore ici.

## Questions à choix

1. Quel cadre réglementaire s'applique à ton dispositif ?
   - a) Marquage CE / règlement européen
   - b) FDA (États-Unis)
   - c) Je ne sais pas / autre
2. Quelles pratiques sont déjà en place ?
   - a) Aucune, tout est prévu
   - b) La matrice existe déjà
   - c) Une analyse de risques existe déjà
3. Quelle suite veux-tu ?
   - a) Une liste de contrôle RBT détaillée
   - b) Un plan pour passer au niveau 2
   - c) Une recherche Web sur le cadre réglementaire (Thomas)

## Confiance : 72/100

- **Ce qui l'appuie** : les passages clés ont été lus en entier (CTAL-TM §1.3.1-1.3.4 et 1.3.6, CTFL §1.4.4, 2.2.1 et 5.2, CTAL-TA §2.2.1). Les versions sont courantes.
- **Ce qui la limite** : la description est brève, les preuves de mise en œuvre sont absentes, et le cadre réglementaire est inconnu.

## Limites

- Aucun syllabus de la bibliothèque ne couvre le cadre réglementaire d'un dispositif médical (ex. IEC 62304, ISO 14971, MDR, FDA). Les exigences de preuve, de validation ou de traçabilité qui en découlent sont **non vérifiables** ici. La recherche sur ce sujet n'a renvoyé que des passages sur l'IA, la sécurité et la finance.
- La série ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque : toute conformité ISO est non vérifiable.
- §1.3.5 (techniques légères et lourdes de RBT) est lu seulement en partie. Je ne la cite que pour dire que les systèmes critiques utilisent souvent des techniques lourdes, et je ne m'appuie pas sur elle pour un verdict.
- L'avis porte sur une démarche décrite, pas sur des preuves de terrain.

## Traçabilité

- **Date de l'avis** : 2026-10-22.
- **Documents lus** :
  - `CTAL-TM-3.0-fr`, v3.0 (2024-03-28) : §1.3 à 1.3.4 (pp. 29-33), §1.3.5 partielle (p. 33), §1.3.6 (p. 34).
  - `CTFL-4.0.1-en`, v4.0.1 (2024-09-15) : §1.4.4 (pp. 20-21), §2.2.1 (pp. 28-29), §5.2 à 5.2.4 (pp. 51-53).
  - `CTAL-TA-4.0-fr`, v4.0 (2025-05-01) : §2.2.1 (p. 29).
- **Requêtes `chercher`** :
  - `"risk-based testing" identification évaluation atténuation`
  - `traçabilité exigences tests couverture`
  - `test d'intégration système manuel régression release exécution des tests`
  - `medical device regulatory software testing`
- **Grille** : `referentiel/grille-maturite.md` (grille du dépôt, citée sans page).

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/referentiel/grille-maturite`
- `python qa.py chercher "risk-based testing" identification évaluation atténuation 2>&1 | head -60`
- `python qa.py chercher "traçabilité exigences tests couverture" 2>&1 | head -60`
- `python qa.py section CTAL-TM-3.0-fr 1.3 2>&1; python qa.py section CTFL-4.0.1-en 1.4.4 2>&1`
- `python qa.py chercher "test d'intégration système manuel régression release exécution des tests" 2>&1; python qa.py chercher "medical device regulatory software testing" 2>&1`
- `python qa.py section CTFL-4.0.1-en 5.2 2>&1; python qa.py section CTFL-4.0.1-en 2.2.1 2>&1`
- `python qa.py page CTAL-TA-4.0-fr 29 2>&1; python qa.py section CTAL-TM-3.0-fr 1.3.6 2>&1`
