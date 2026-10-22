# C1-ambigu — skill

**Question** : Comment on gère les risques ?

**Tours** : 6 · **coût** : 0.147 $ · **confiance annoncée** : 76 · **verdict** : ÉCHEC · **citations** : 3/3 lues · **Web** : 0 · **critères** : 2/3 (manquent : questions_choix)

## Réponse

## La gestion des risques en test (ISTQB)

**Hypothèse :** vous parlez des risques qualité et produit, côté Test Manager (test basé sur les risques), pas des risques projet au sens large. Dites-moi si vous visiez autre chose.

**Base d'idées :** aucune idée capitalisée sur le sujet pour l'instant.

### Ce que disent les syllabus (passages lus)

- **Le processus** [CTAL-TM v3.0 FR, §1.3.1, p. 29]. Le test basé sur les risques suit le processus générique de gestion du risque, en deux temps :
  - l'**analyse des risques**, qui comprend l'identification et l'évaluation ;
  - le **contrôle des risques**, qui consiste à suivre et à atténuer.
  
  Ces activités sont séquentielles mais peuvent se chevaucher.
- **Les tests sont un moyen d'atténuation.** Un défaut trouvé est un risque traité avant la release. Une absence de défaut indique un risque plus faible que prévu [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- **L'atténuation se répartit sur tout le processus de test** [CTAL-TM v3.0 FR, §1.3.1, p. 29] :
  - planification : concentrer les tests sur les bons domaines avec les bonnes techniques ;
  - analyse : le niveau de risque guide les conditions de test à couvrir ;
  - exécution : la hiérarchisation par les risques fixe l'ordre des tests.
- **Identification** [CTAL-TM v3.0 FR, §1.3.2, pp. 29-30]. Le Test Manager recueille les risques auprès des parties prenantes avec ces techniques :
  - entretiens avec des experts ;
  - évaluations indépendantes ;
  - rétrospectives ;
  - ateliers sur les risques ;
  - brainstorming ;
  - checklists ;
  - expérience passée.

  Deux points d'attention :
  - la liste des participants doit être convenue avec le chef de projet, car oublier une partie prenante clé est « très problématique » ;
  - le risque n'est pas réparti uniformément : une zone client et une zone d'administration n'ont pas les mêmes risques d'utilisabilité.
- **Contrôle et suivi** [CTAL-TM v3.0 FR, §1.3.1, p. 29]. Le suivi des tests inclut celui des risques : nouveaux risques et ajustement du registre des risques.
- **Rôle de l'analyste de test** [CTAL-TA v4.0 FR, §2.2, p. 28]. Les risques et leurs niveaux évoluent. Le pilotage est donc régulier, une fois par itération en cycle itératif. L'analyste met à jour le référentiel de risques et ajuste les actions d'atténuation. Il le fait par les revues, les techniques et niveaux de couverture adaptés, les types de tests adaptés et la régression.

### Où creuser ensuite (non lu, donc non cité)
- **CTAL-TM §1.3.5** : techniques formelles (PRAM, PRISMA) citées dans l'extrait de recherche.
- **CTAL-TTA §1.2.2** : évaluation des risques côté technique.
- **CTAL-TA §3.5.1** : choix des techniques de test pour atténuer les risques produit.
- **CT-ATLaS §5.1.5** : risques organisationnels en contexte agile à grande échelle (tableau de risques partagé).
- **CT-TAS §4.2.3** : risques de déploiement de l'automatisation.

### Par quoi je commencerais
1. **Atelier de risques** avec les parties prenantes, pour obtenir un registre initial (impact élevé, effort faible).
2. **Relier les niveaux de risque** à la priorisation des conditions et de l'exécution des tests.
3. **Revoir le registre à chaque itération** ou jalon (effort faible, bénéfice durable).

### Questions à choix
- Votre cycle de vie : 1. agile/itératif · 2. cascade/V · 3. mixte ?
- Angle à approfondir : 1. techniques d'évaluation (PRAM/PRISMA) · 2. lien risques → stratégie de test · 3. risques projet et organisationnels ?

**Confiance : 76/100 (élevée)**
- Base : 94 × 0,6 = 56
- Passages lus (3) : +20
- Syllabus concordants (2) : +10
- Interprétation (hypothèse de cadrage) : −10

Je peux capitaliser une idée sur ce sujet, par exemple « atelier de risques puis revue à chaque itération », si vous le souhaitez.

## Commandes exécutées

- `Skill {"skill": "qa-knowledge", "args": "Comment on gère les risques ?"}`
- `python qa.py idee chercher risque risk-based 2>&1 | head -40; echo ======; python qa.py chercher "risk-based testing gestion des risques" 2>&1 | head -60`
- `python qa.py section CTAL-TM-3.0-fr 1.3.1 --max-caracteres 3500 2>&1; echo =====; python qa.py section CTAL-TA-4.0-fr 2.2 --max-caracteres 2500 2>&1`
- `python qa.py section CTAL-TM-3.0-fr 1.3.2 --max-caracteres 3500 2>&1; python qa.py confiance --base 94 --lus 3 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0 2>&`
