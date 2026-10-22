# T1-couverture — thomas

**Question** : Quelles techniques ISTQB permettent d'améliorer la couverture des tests ?

**Tours** : 6 · **coût** : 0.161 $ · **confiance annoncée** : 90 · **citations** : 8/9 lues · **Web** : 0

## Réponse

Les syllabus répondent à deux niveaux. D'abord, des techniques de conception qui produisent des tests systématiques. Ensuite, des mesures de couverture qui montrent ce qui reste non testé. L'idée clé est de combiner les deux. La base d'idées capitalisées ne contient rien sur ce sujet.

**Pistes par syllabus**

- **CTFL v4.0.1 (EN) – §4.1 Aperçu des techniques**
  - Les techniques servent à définir les conditions de test et à identifier les *coverage items*, avec un jeu de tests « relativement petit mais suffisant ». Elles se classent en boîte noire, boîte blanche et basées sur l'expérience. [CTFL v4.0.1 EN, §4.1, p. 39]
  - Les techniques basées sur l'expérience peuvent détecter des défauts que les deux autres familles manquent. Elles les complètent. [CTFL v4.0.1 EN, §4.1, p. 39]
  - *À creuser : §4.2 (partitions d'équivalence, valeurs limites, tables de décision, transitions d'état) et §4.4 (error guessing, exploratoire, checklists).* Je n'ai lu que le sommaire du chapitre 4 (p. 38), pas ces sections.

- **CTFL v4.0.1 (EN) – §4.3 Boîte blanche**
  - La couverture des branches inclut celle des instructions, l'inverse est faux. [CTFL v4.0.1 EN, §4.3.2, p. 43]
  - Des tests purement boîte noire ne donnent pas de mesure de la couverture du code. Les mesures boîte blanche indiquent quels tests ajouter. [CTFL v4.0.1 EN, §4.3.3, p. 43]
  - Limite : la boîte blanche ne détecte pas les omissions, c'est-à-dire une exigence non implémentée. [CTFL v4.0.1 EN, §4.3.3, p. 43]

- **CTAL-TTA v4.0 (EN) – §2.8 Choisir une technique boîte blanche**
  - Séquence conseillée : appliquer la boîte noire d'abord, mesurer la couverture, puis ne recourir à la boîte blanche que si le niveau requis n'est pas atteint. [CTAL-TTA v4.0 EN, §2.8, p. 18]
  - N'exiger un niveau de couverture qu'à 100 % : en visant 80 %, on laisse souvent non testé le code le plus complexe et le plus défaillant. [CTAL-TTA v4.0 EN, §2.8, p. 18]
  - Hiérarchie de subsomption : multiple condition ⊃ MC/DC ⊃ décision/branche ⊃ instruction. Il suffit d'exiger un seul critère. [CTAL-TTA v4.0 EN, §2.8, p. 18]
  - ISO 29119-4 permet d'écarter les éléments de couverture infaisables, ce qui rend le 100 % atteignable. [CTAL-TTA v4.0 EN, §2.8, p. 18]
  - Le passage lu sur l'API (§2.7, p. 18) mentionne des critères de sortie comme couvrir toutes les opérations, tous les paramètres, les séquences d'opérations et tous les codes de statut.

- **CTAL-TA v4.0 (EN) – §3.5 Techniques et automatisation de la conception**
  - Combiner les techniques : valeurs limites sur les gardes d'une transition d'état, scénarios avec couverture de décision, scénarios avec couverture aller-retour (*round-trip*). [CTAL-TA v4.0 EN, §3.5.1, p. 41]
  - L'automatisation de la conception (model-based) permet des critères plus riches, comme le combinatoire, l'aléatoire ou la couverture N-switch. Elle réduit le risque de code non testé. [CTAL-TA v4.0 EN, §3.5.2, p. 41]
  - Risque associé : les conditions absentes du modèle sont oubliées. [CTAL-TA v4.0 EN, §3.5.2, p. 42]

- **CT-MBT v1.1 (EN) – §5.1.1–5.1.2**
  - Le MBT cite une meilleure couverture de test et de meilleures traces (traçabilité) parmi ses bénéfices. [CT-MBT v1.1 EN, §5.1.1, p. 38]
  - Il permet aussi de sélectionner le jeu de tests le mieux adapté à l'objectif via des stratégies de génération. [CT-MBT v1.1 EN, §5.1.1, p. 38]

- **CTAL-TM v3.0 (FR) – §1.2.6 Management par type de test**
  - Côté pilotage, le TM doit analyser que la boîte noire couvre tous les scénarios d'usage et toutes les exigences métier. Pour la boîte blanche, il doit utiliser des outils de couverture de code pour repérer les lacunes et y orienter les ressources. [CTAL-TM v3.0 FR, §1.2.6, p. 26]

- **CT-AI v2.0 (EN) – §3.4.3 (cas particulier)**
  - Pour les réseaux de neurones, la couverture se mesure par neurones (neuron coverage, kMNC, NBC). Elle ne garantit pas la généralisation. Le syllabus recommande d'y ajouter des tests adversariaux et métamorphiques. [CT-AI v2.0 EN, §3.4.3, p. 37]

**Ce que j'en retiens** (interprétation)
- Le levier le plus économique consiste à enchaîner les techniques boîte noire, à mesurer, puis à compléter ciblé en boîte blanche (CTAL-TTA).
- Les omissions d'exigences échappent à la boîte blanche. Elles se traitent par la traçabilité exigences ↔ tests et par la boîte noire (CTAL-TM, CTFL).
- La couverture n'est qu'une des mesures possibles. Le CTAL-AT parle aussi de couverture des exigences et des risques (§3.1, p. 24), mais je n'ai lu que l'extrait de recherche.

**Où creuser ensuite**
- `section CTFL-4.0.1-en 4.2` : les quatre techniques boîte noire et leurs *coverage items*.
- `section CTAL-TA-4.0-en 3` : les techniques avancées, dont le combinatoire.
- `section CTAL-TTA-4.0-en 2` : MC/DC, multiple condition, API testing.
- `section CTAL-TM-3.0-fr 1.2` : les métriques de couverture côté pilotage.

**Confiance : 90/100 (élevée).** La confiance documentaire de `chercher` est de 100/100 et plusieurs syllabus courants concordent, ce qui ajoute 5 points. J'en retire 15 parce que certaines pistes (§4.2, §4.4, CTAL-AT) ne reposent que sur des titres ou des extraits, et que la synthèse « ce que j'en retiens » est de l'interprétation.

**À capitaliser ?** (rien n'est enregistré sans ton accord)
1. **Boucle d'amélioration de la couverture** : boîte noire, puis mesure, puis boîte blanche ciblée, avec un seul critère exigé à 100 % (CTAL-TTA §2.8).
2. **Angle mort de la couverture de code** : elle ne détecte pas les omissions d'exigences, d'où une couverture double code et exigences (CTFL §4.3.3 et CTAL-TM §1.2.6).

## Commandes exécutées

- `Skill {"skill": "qa-knowledge"}`
- `python qa.py idee chercher couverture des tests coverage 2>&1 | head -40; echo ----; python qa.py chercher "test coverage techniques" 2>&1 | head -60; echo ----; python qa.py chercher "couverture des `
- `cat .claude/skills/qa-knowledge/reference/strategie.md`
- `python qa.py lire 4797 --contexte 1; echo =====; python qa.py lire 4811 --contexte 1; echo =====; python qa.py lire 2135 --contexte 1; echo =====; python qa.py lire 2948 --contexte 1; echo =====; pyth`
