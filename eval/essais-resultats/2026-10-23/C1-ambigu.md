# C1-ambigu — skill

**Question** : Comment on gère les risques ?

**Tours** : 6 · **coût** : 0.272 $ · **confiance annoncée** : 79 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 3/3

## Réponse

## Gérer les risques en test : le processus ISTQB

**Hypothèse :** vous parlez des risques *qualité* gérés par les tests (test basé sur les risques), pas de la gestion de risques projet au sens large. Je n'ai pas votre contexte (cycle de vie, taille d'équipe, réglementation).

La base d'idées capitalisées ne contient rien sur le sujet. Les réponses viennent donc des syllabus locaux, que j'ai lus.

### Le processus (CTAL-TM v3.0 FR)
- **Principe.** Le test basé sur les risques consiste à identifier, évaluer, suivre et atténuer les risques pour piloter les tests. Plus le niveau de risque est élevé, plus les tests commencent tôt et plus l'effort est intense [CTAL-TM v3.0 FR, §1.3, p. 29].
- **Deux grandes activités.** L'analyse des risques (identification puis évaluation) et le contrôle des risques (suivi et atténuation). Elles suivent un ordre logique mais peuvent se chevaucher [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **Identification.** Le Test Manager recueille les risques auprès des parties prenantes. Les techniques citées sont les entretiens d'experts, les évaluations indépendantes, les rétrospectives, les ateliers sur les risques, le brainstorming, les checklists et l'expérience passée. La liste des participants doit être convenue avec le chef de projet [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30].
- **Évaluation.** On catégorise chaque risque (produit ou projet, caractéristique de qualité touchée), puis on estime sa probabilité et son impact. Les facteurs de probabilité incluent la complexité, la maturité de l'organisation, la pression sur les délais et le taux de changement. Les facteurs d'impact incluent la fréquence d'usage, la criticité, la réputation, les pertes financières et la sûreté [CTAL-TM v3.0 FR, §1.3.3, pp. 30-31].
- **Niveau de risque.** Il combine probabilité et impact. En général l'évaluation est qualitative, sur une échelle ordinale, avec une matrice de risque. Un produit probabilité × montant n'est justifié que si les données sont étendues et statistiquement valables [CTAL-TM v3.0 FR, §1.3.3, p. 31].
- **Atténuation et suivi.** L'atténuation est répartie sur plusieurs activités de test :
  - Planification : concentrer les tests sur les bons domaines avec les bonnes techniques.
  - Analyse : le niveau de risque guide les conditions de test à couvrir.
  - Exécution : la priorisation par les risques fixe l'ordre des tests.

  Le suivi des tests inclut celui des risques : nouveaux risques et mise à jour du registre [CTAL-TM v3.0 FR, §1.3.1, p. 29].

### Le point de vue du Test Analyst (CTAL-TA v4.0 FR)
Les risques évoluent dans le temps, donc le pilotage est régulier : en général une fois par itération en cycle itératif. L'analyste met à jour le référentiel des risques. Il agit aussi sur l'atténuation par les revues, les techniques et niveaux de couverture adaptés, les types de test et la régression [CTAL-TA v4.0 FR, §2.2, p. 28].

### Où creuser ensuite
Je n'ai pas lu ces sections, donc je ne les cite pas :
- `section CTAL-TM-3.0-fr 1.3.4` : atténuation par des tests appropriés.
- `section CTAL-TM-3.0-fr 1.3.5` : techniques de test basé sur les risques.
- `section CTAL-TM-3.0-fr 1.3.6` : métriques de succès et difficultés.
- CTAL-TTA v4.0, §1.2.2 : évaluation des risques côté technique.
- CTFL v4.0, §5.2 : gestion des risques de base (anglais seulement).

### Par quoi je commencerais
1. **Atelier de risques** avec les parties prenantes, pour produire un registre avec une matrice probabilité × impact qualitative. Impact fort, effort faible.
2. **Relier le niveau de risque à la priorité d'exécution et à la profondeur de test.** Impact fort, effort moyen.
3. **Revue du registre à chaque itération ou jalon**, avec des métriques de succès (à lire en §1.3.6). Impact moyen, effort faible.

### Questions à choix
1. Quel est votre cycle de vie ?
   1. Agile / itératif
   2. Cascade ou en V
   3. Hybride
2. Que voulez-vous approfondir ?
   1. Mener l'atelier de risques
   2. Relier les risques à la priorisation des tests
   3. Les métriques de suivi

### Confiance : 79/100 (élevée)
- Base : 82 × 0,6 = 49.
- Trois passages lus : +20.
- Deux syllabus courants concordants (CTAL-TM et CTAL-TA) : +10.
- Total : 79.

Je peux capitaliser une idée de type « atelier de risques → registre → priorisation » si vous le souhaitez.

## Commandes exécutées

- `Skill {"skill": "qa-knowledge", "args": "Comment on gère les risques ?"}`
- `python qa.py idee chercher risque gestion des risques 2>&1 | head -60; echo ======; python qa.py chercher "risk management gestion des risques" 2>&1 | head -80`
- `python qa.py section CTAL-TM-3.0-fr 1.3 --max-caracteres 6000 2>&1; echo =====; python qa.py section CTAL-TA-4.0-fr 2.2 --max-caracteres 2500 2>&1`
- `python qa.py section CTAL-TM-3.0-fr 1.3.3 --max-caracteres 4000 2>&1; python qa.py confiance --base 82 --lus 3 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 0 --non-couvert 0 2>&`
