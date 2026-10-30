# T8-tmmi-tpi — thomas

**Question** : Quelle différence entre TMMi et TPI Next, et lequel choisir pour une première évaluation de nos pratiques de test ?

**Tours** : 11 · **coût** : 0.196 $ · **confiance annoncée** : 44 · **verdict** : réussi · **citations** : 3/3 lues · **Web** : 1 · **critères** : 2/2 · **fidélité** (juge LLM, indicatif) : 0.69 sur 2 lignes citées, 0 contradiction(s)

## Réponse

Sources retenues : j'ai lu CTEL-ITP v2011 EN §3.3.3 (p. 27) et CTAL-TM v3.0 EN §1.5.2 (pp. 39-40). Je n'ai pas lu la traduction FR de CTEL-ITP ni les chapitres d'évaluation de ce syllabus. La base d'idées ne contient rien sur le sujet. Pour l'état actuel de TPI Next, j'ai fait une recherche Web, parce que CTEL-ITP date de 2011 et que le statut du modèle a pu changer depuis.

TMMi est un modèle **par étapes** (5 niveaux de maturité). TPI Next est un modèle **continu** (16 domaines clés, chacun noté séparément). Pour une première évaluation, je commencerais par TPI Next, ou par un TMMi limité au niveau 2, selon ce que vous cherchez (voir la recommandation plus bas).

Hypothèse de contexte : organisation sans évaluation de maturité préalable, sans exigence de certification, cycle de vie et domaine inconnus.

**Pistes par syllabus**
- **CTEL-ITP 2011 — §3.3.3 Comparing TPI Next to TMMi**
  - Type : TPI Next est un modèle continu, TMMi un modèle par étapes. [CTEL-ITP 2011 EN, §3.3.3, p. 27]
  - Méthode de test : TPI Next s'appuie sur les pratiques génériques de TMap Next. TMMi est indépendant de toute méthode. [CTEL-ITP 2011 EN, §3.3.3, p. 27]
  - Lien avec l'amélioration des processus logiciels : TMMi est très corrélé à CMMI. TPI Next n'a pas de relation formelle avec un modèle précis, mais une correspondance reste possible. [CTEL-ITP 2011 EN, §3.3.3, p. 27]
  - Focus : TPI Next donne une vue détaillée par domaine clé et une vue d'ensemble du processus de test. TMMi se concentre sur peu de zones de processus par niveau. Il couvre aussi les revues de testabilité, le contrôle qualité, la prévention des défauts et le programme de mesure. [CTEL-ITP 2011 EN, §3.3.3, p. 27]
  - Approche : TPI Next est rigoureux, orienté métier et ingénierie de test. TMMi insiste fortement sur l'engagement du management. [CTEL-ITP 2011 EN, §3.3.3, p. 27]
- **CTAL-TM v3.0 — §1.5.2 Amélioration basée sur un modèle**
  - TMMi compte 5 niveaux de maturité. Chaque niveau, sauf le 1, comporte des zones de processus et des objectifs d'amélioration, avec pratiques, sous-pratiques et exemples. Une directive existe pour son usage en agile. [CTAL-TM v3.0 EN, §1.5.2, p. 39]
  - TPI Next compte 16 domaines clés (stratégie de test, métriques, outils, environnement…) avec 4 niveaux de maturité chacun. Les résultats sont résumés dans une matrice de maturité. [CTAL-TM v3.0 EN, §1.5.2, pp. 39-40]
  - L'évaluation peut se limiter au niveau projet (planification, conception de tests). On laisse alors de côté les zones organisationnelles (politique de test, organisation de test) ou on les adapte au contexte. [CTAL-TM v3.0 EN, §1.5.2, p. 39]

**Comparaison pour une première évaluation** (la dernière colonne est mon interprétation)

| Critère | TMMi | TPI Next | Ce que ça change pour vous |
|---|---|---|---|
| Structure | 5 niveaux, on progresse par étapes | 16 domaines, chacun noté séparément | TPI Next permet d'améliorer là où ça fait mal, sans attendre un niveau global |
| Résultat | Un niveau de maturité de l'organisation | Une matrice de maturité par domaine | TMMi donne une étiquette lisible par la direction, TPI Next un diagnostic plus fin |
| Dépendance | Indépendant de la méthode de test | Vocabulaire et pratiques issus de TMap | Si vous n'utilisez pas TMap, TMMi est plus neutre |
| Engagement | Fort accent sur le management | Approche orientée métier | TMMi suppose un sponsor |
| Certification et support (Web) | Évaluation formelle par la TMMi Foundation | Pas de certification formelle ; statut du support incertain | Voir ci-dessous |

Web, sur l'état actuel : un support de conférence de 2024 (Erik van Veenendaal) indique « No further support » pour TPI Next, contre un développement continu pour TMMi, qui offre une certification ([Test Process Improvement, JSTQB Japan 2024](https://jstqb.jp/prinfo/conference2024/pdf/Test%20Process%20Improvement.pdf)). Sogeti propose pourtant toujours une auto-évaluation TPI Next ([Sogeti](https://www.sogeti.ie/link/b3a7f4f6233b44eb8e7937ec3f1b5d17.aspx)). Je n'ai trouvé aucune annonce officielle qui retire TPI Next, et le support de 2024 est une source secondaire. Vérifiez auprès de Sogeti avant de vous engager sur ce modèle.

**Ce que j'en retiens** (interprétation)
- Pour une première évaluation sans ambition de certification, TPI Next convient bien : l'évaluation est modulable par domaine et le diagnostic est détaillé. Son avenir et son lien avec TMap sont deux réserves.
- Si vous visez une reconnaissance externe ou un cadre durable, ou si votre organisation connaît déjà CMMI, TMMi est le meilleur choix.
- Dans les deux cas, vous pouvez limiter la première évaluation au niveau projet. [CTAL-TM v3.0 EN, §1.5.2, p. 39]

**Par quoi je commencerais**
1. Cadrer l'objectif : diagnostic interne ou reconnaissance externe. Impact fort, effort faible.
2. Faire une auto-évaluation légère, limitée au projet et aux domaines qui vous préoccupent, avec l'un des deux modèles. Impact fort, effort moyen.
3. Décider ensuite d'une évaluation formelle TMMi. Impact moyen, effort fort.

Indicateurs de validation à suivre après l'évaluation : taux de défauts échappés, délai de détection des défauts, couverture des risques par les tests.

**Où creuser ensuite**
- `section CTEL-ITP-2011-en 3.3` : le tableau complet, et peut-être des critères de choix plus fins. Je n'ai lu que §3.3.3, et le texte affiché s'arrête à « Strong focus on management commitment », donc des lignes ont pu m'échapper.
- Le syllabus d'évaluation du même document, à lire sur le chapitre 3 (objectifs LO 3.3.7 à 3.3.9, dont l'évaluation informelle avec TPI Next).
- CTAL-TM v3.0 FR §1.5.2, pour la version française.

**Confiance : 44/100** (moyenne). Calcul : base 73 × 0,6 = 44 ; 2 passages lus +20 ; Web −10 ; raisonnement sans source −10 → 44. La comparaison s'appuie sur un syllabus de 2011, et le statut de TPI Next vient d'une source secondaire.

**Questions à choix**
1. Quel est votre objectif principal ?
   1. Diagnostic interne rapide
   2. Reconnaissance externe ou certification
   3. Alignement avec CMMI ou un cadre existant
2. Quel est votre cycle de vie dominant ?
   1. Agile / itératif
   2. Séquentiel
   3. Mixte
3. Que voulez-vous faire ensuite ?
   1. Approfondir CTEL-ITP §3.3
   2. Comparer avec l'amélioration analytique (CTAL-TM §1.5)
   3. Capitaliser cette comparaison

**À capitaliser ?** Une proposition, en clair, car je n'ai pas lancé `idee modele` : « Choisir TMMi ou TPI Next, un critère décisif est modèle par étapes (TMMi) ou continu (TPI Next), puis l'objectif de certification et le support du modèle. » Source : [CTEL-ITP 2011 EN, §3.3.3, p. 27]. Je n'ai pas vérifié les doublons non plus : la vérification a échoué sur le thème, et le thème `maturite` existe. Je prépare le JSON si vous êtes d'accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher TMMi TPI Next amélioration processus de test`
- `python qa.py chercher TMMi TPI Next test process improvement model`
- `python qa.py chercher modèle d'amélioration continu vs par étapes évaluation processus de test`
- `python qa.py section CTEL-ITP-2011-en 3.3.3 --max-caracteres 8000`
- `python qa.py section CTAL-TM-3.0-en 1.5.2 --max-caracteres 9000`
- `python qa.py page CTEL-ITP-2011-en 28 --max-caracteres 5000`
- `WebSearch {"query": "TPI Next status Sogeti Capgemini retired TMMi Foundation assessment formal 2025", "mode": "standard"}`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Choisir TMMi ou TPI Next pour une première évaluation" --resume "Comparaison modèle par étapes vs continu" --principe "TMM`
- `python qa.py confiance --base 73 --lus 2 --concordants 1 --ancien 1 --web 1 --raisonnement 1; python qa.py themes | grep -i -E "process|amélio|improv"`
