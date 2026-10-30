# S3-reglemente — sylvie

**Question** : Pour le logiciel de notre dispositif médical, je prévois : une matrice de traçabilité exigences → tests tenue dans un tableur, une analyse de risques faite une seule fois en début de projet, et des tests système manuels avant chaque release. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 11 · **coût** : 0.248 $ · **confiance annoncée** : 60 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0 · **critères** : 9/9 · **fidélité** (juge LLM, indicatif) : 0.9 sur 5 lignes citées, 0 contradiction(s)

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

Ta démarche est partiellement alignée. La traçabilité est dans l'esprit ISTQB, mais l'analyse de risques faite une seule fois est un écart net. Les tests système manuels avant release ne sont alignés qu'en partie. Les trois pratiques sont des intentions (« je prévois »), donc le niveau atteint est plafonné à 1.

**Pratiques décrites**
- P1 : matrice de traçabilité exigences → tests, dans un tableur. Intention.
- P2 : analyse de risques faite une seule fois, en début de projet. Intention.
- P3 : tests système manuels avant chaque release. Intention.

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Matrice de traçabilité (tableur) | Intention | Partiellement aligné | La traçabilité doit être établie et maintenue tout au long du processus de test. Elle relie la base de test, les testwares (conditions de test, risques, cas de test), les résultats et les défauts. Elle sert à évaluer la couverture et l'impact des changements, et à faciliter les audits. Ta matrice ne couvre que exigences → tests : il manque les liens vers les résultats, les défauts et les risques. Le syllabus ne dit rien sur l'outil, donc le tableur n'est pas un problème en soi. | [CTFL v4.0.1 EN, §1.4.4, p. 20] ; [CTFL v4.0.1 EN, §1.4.4, p. 21] |
| P2 Analyse de risques unique, en début de projet | Intention | Écart | L'analyse des risques (identification et évaluation) est suivie du contrôle des risques (suivi et atténuation). Le suivi des tests doit inclure le suivi des risques : analyse des nouveaux risques et ajustement du registre. Une analyse faite une seule fois contredit ce passage. | [CTAL-TM v3.0 FR, §1.3.1, p. 29] |
| P3 Tests système manuels avant chaque release | Intention | Partiellement aligné | L'effort de test doit être proportionnel au niveau de risque, avec des techniques plus rigoureuses pour les risques élevés. Les risques sont aussi atténués par le choix des niveaux et types de test, y compris les tests statiques. Un seul niveau de test, placé juste avant la release, ne le montre pas. Une analyse d'impact devrait déterminer l'étendue de la régression. Les suites de régression sont de bons candidats à l'automatisation, car elles sont exécutées à chaque release. Les tests manuels ne contredisent pas l'ISTQB. | [CTAL-TM v3.0 FR, §1.3.4, p. 32] ; [CTFL v4.0.1 EN, §2.2.3, p. 31] |

**Ce qui manque**
- **Identification des risques avec les parties prenantes**. Techniques citées : entretiens avec des experts, ateliers sur les risques, checklists, etc. La liste des participants doit être complète et convenue avec le chef de projet. [CTAL-TM v3.0 FR, §1.3.2, p. 29-30]
- **Évaluation probabilité × impact**. Les risques sont catégorisés par type et par caractéristiques de qualité. Probabilité et impact sont combinés en un niveau de risque, le plus souvent dans une matrice de risque qualitative. [CTAL-TM v3.0 FR, §1.3.3, p. 30-31]
- **Atténuation par les tests**. Le temps et l'effort sont proportionnels au niveau de risque. Les risques élevés sont testés plus tôt et plus rigoureusement, et la priorisation des tests suit le niveau de risque. [CTAL-TM v3.0 FR, §1.3.4, p. 32]
- **Suivi des risques pendant le projet**. Le registre est mis à jour avec les nouveaux risques. Les rapports d'avancement s'expriment en risque résiduel pour appuyer la décision de livraison. [CTAL-TM v3.0 FR, §1.3.1, p. 29 ; §1.3.4, p. 32]
- **Liens traçabilité ↔ risques et résultats**. La traçabilité des résultats vers les risques permet d'évaluer le risque résiduel. [CTFL v4.0.1 EN, §1.4.4, p. 21]
- **Analyse d'impact pour la régression** avant chaque release. [CTFL v4.0.1 EN, §2.2.3, p. 31]
- **Exigences réglementaires**. Le syllabus note que certaines normes de sûreté prescrivent techniques de test et couverture selon le niveau d'intégrité, et que le Test Manager doit s'assurer qu'elles sont respectées. Ton dispositif médical est donc concerné, mais la norme applicable n'est pas dans la bibliothèque (voir Limites). [CTAL-TM v3.0 FR, §1.3.4, p. 32]

**Niveau atteint : 1 — Initial · niveau visé : 2 (Discipliné)**
- Les trois pratiques sont des intentions. Aucune n'est « en place » avec une preuve citée, donc le plafond de 1 s'applique (grille du dépôt).
- Même réalisées, les trois pratiques ne suffiraient pas au niveau 2. La grille exige une stratégie de test écrite, la supervision et le contrôle pendant le projet, et l'environnement de test. Ces points ne sont pas mentionnés, donc non démontrés.
- Pour passer au niveau 2, il faut d'abord mettre en place les pratiques et en donner la preuve. Il faut ensuite :
  - rédiger la stratégie de test avec une approche fondée sur les risques ;
  - rendre l'analyse de risques itérative (registre vivant, suivi) ;
  - relier risques, tests, résultats et défauts ;
  - piloter l'avancement en risque résiduel.
- Les niveaux 3 à 5 sont une adaptation du dépôt, non issue des syllabus.

**Confiance : 60/100 (moyenne)**
Calcul : base 66 × 0,6 = 40 ; 15 passages lus +20 ; 2 syllabus concordants +10 ; raisonnement −10 → 60.
Le verdict repose sur deux syllabus courants lus (CTAL-TM v3.0 FR et CTFL v4.0.1 EN). Mon interprétation du niveau de maturité et des manques de P3 est du raisonnement, pas une source.

**Limites**
- Aucun syllabus de la bibliothèque ne couvre le cadre réglementaire d'un dispositif médical (par exemple le cycle de vie logiciel ou la gestion des risques propres aux dispositifs médicaux). La recherche sur ce sujet n'a donné que des mentions de normes dans d'autres domaines. Les exigences d'audit, de documentation et de gestion des risques réglementaires sont donc **non vérifiables** ici.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque. Toute conformité ISO est non vérifiable.
- Je n'ai pas lu les autres sections du chapitre, dont les métriques de succès du test basé sur les risques (§1.3.6 du CTAL-TM).

**Questions à choix**

Quel est ton cadre réglementaire principal ?
1. Réglementation européenne des dispositifs médicaux
2. Réglementation américaine (FDA)
3. Autre ou non encore déterminé

Que veux-tu faire ensuite ?
1. Affiner P2 : détailler une démarche de test basé sur les risques itérative
2. Auditer P3 : régression, niveaux de test et automatisation
3. Lancer une recherche plus large sur le cadre réglementaire (Thomas)

**Où creuser ensuite**
- À lire : CTAL-TM v3.0 FR §1.3.5 (techniques pour le test basé sur les risques) et §1.3.6 (métriques de succès et difficultés).
- À lire : CTAL-TA v4.0 FR §2 (tâches de l'Analyste de test dans le test basé sur les risques).
- À lire : CTEL-ITP 2011 EN §9.1 (exigences externes obligatoires, ex. FDA pour le médical).
- Si besoin d'une base normative réglementaire : un syllabus ou une norme à importer via `/ajouter-syllabus` ou `importer --prive`.

**Traçabilité**
- Date de l'avis : 2026-10-30.
- Documents lus :
  - `CTAL-TM-3.0-fr`, v3.0, publié le 2024-03-28 : §1.3 (intro, p. 29), §1.3.1 (p. 29), §1.3.2 (p. 29-30), §1.3.3 (p. 30-31), §1.3.4 (p. 32-33).
  - `CTFL-4.0.1-en`, v4.0.1, publié le 2024-09-15 : §1.4.4 (p. 20-21), §2.2.3 (p. 30-31).
- Requêtes `chercher` :
  1. `"risk-based testing" identification évaluation atténuation suivi des risques`
  2. `"traçabilité exigences tests couverture"`
  3. `"system testing manual regression release test levels"`
  4. `"medical device regulated safety-critical software regulatory FDA IEC 62304"`

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/referentiel/grille-m`
- `python qa.py chercher "risk-based testing" identification évaluation atténuation suivi des risques`
- `python qa.py chercher "traçabilité exigences tests couverture"`
- `python qa.py section CTAL-TM-3.0-fr 1.3 --max-caracteres 9000`
- `python qa.py section CTFL-4.0.1-en 1.4.4`
- `python qa.py chercher "system testing manual regression release test levels" `
- `python qa.py section CTAL-TM-3.0-fr 1.3.4 --max-caracteres 6000`
- `python qa.py section CTFL-4.0.1-en 2.2.3`
- `python qa.py chercher "medical device regulated safety-critical software regulatory FDA IEC 62304"`
- `python qa.py confiance --autorite 0 --base 66 --lus 15 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 1`
