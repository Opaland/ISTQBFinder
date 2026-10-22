# S2-automatisation — sylvie

**Question** : On veut automatiser 100 % de nos tests de régression avec Playwright, les lancer à chaque commit et supprimer les tests manuels. Est-ce aligné avec les recommandations ISTQB ? Niveau de maturité ?

**Tours** : 7 · **coût** : 0.164 $ · **confiance annoncée** : 72 · **citations** : 6/6 lues · **Web** : 0

## Réponse

Votre démarche est alignée sur le principe (automatiser la régression, l'exécuter en continu). Elle présente en revanche un écart net sur « 100 % » et sur « supprimer les tests manuels », et plusieurs étapes décrites par l'ISTQB n'y figurent pas.

## Pratiques reformulées
- **P1** : automatiser 100 % des tests de régression.
- **P2** : utiliser Playwright comme outil.
- **P3** : lancer la régression à chaque commit.
- **P4** : supprimer les tests manuels.

## Verdicts

| Pratique | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|
| P1 : automatiser la régression | Partiellement conforme | La régression est « l'opportunité la plus simple » pour passer à l'automatisation. Il faut d'abord vérifier que le test manuel fonctionne, puis démontrer l'équivalence du test automatisé avant de remplacer l'ancien. Automatiser 100 % des tests manuels n'équivaut pas à couvrir 100 % de ce qui est automatisable. Le « 100 % » comme objectif n'est pas recommandé. | [CT-TAS v1.0 FR, §6.1.1, pp. 49-50] |
| P1 (suite) : choix de ce qu'on automatise | Écart sur le « 100 % » | L'approche de régression basée sur les risques aide à décider « où l'automatisation est inutile et où l'investigation humaine apporte plus de valeur ». Parmi les risques de l'automatisation figurent l'usage d'un outil « quand le test manuel est plus approprié » et l'excès de confiance dans l'outil, qui ignore l'esprit critique humain. | [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CTFL v4.0.1 EN, §6.2, p. 60] |
| P2 : Playwright | Hors ISTQB | Les syllabus que j'ai lus ne traitent pas d'un outil en particulier. Le CTFL demande d'analyser et d'atténuer les risques liés à l'outil : estimation de l'effort de maintenance, compatibilité avec la plateforme, dépendance au fournisseur ou à l'open source. | [CTFL v4.0.1 EN, §6.2, pp. 59-60] |
| P3 : à chaque commit | Partiellement conforme | Le syllabus décrit la régression incrémentale : un sous-ensemble de tests est déclenché à chaque commit. Il est choisi selon l'impact et la probabilité de risque, la localisation et les dépendances du changement. Rien dans les passages lus ne dit de lancer toute la suite à chaque commit. Les suites longues peuvent tourner la nuit. Les tests système se placent plutôt dans le pipeline de déploiement. | [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CTAL-TAE v2.0 FR, §5.1.1, pp. 38-39] |
| P4 : supprimer les tests manuels | Écart (si cela inclut l'exploratoire) ; conforme seulement pour l'exécution manuelle de la régression, une fois l'équivalence démontrée | Une fois les tests automatisés jugés équivalents, l'effort manuel peut aller vers les tests exploratoires et la conception de nouveaux cas. Les approches « exploratory regression » et « collaborative regression » complètent l'automatisation. La seconde est utile quand l'automatisation n'est pas encore mature. | [CT-TAS v1.0 FR, §6.1.1, p. 49] ; [CTAL-AT v2.0 EN, §1.4, pp. 17-18] |

## Ce qui manque
- **Sélection et revue du périmètre de régression** à chaque cycle, par analyse d'impact, risques, historique, couverture, traçabilité ou profils opérationnels. L'ISTQB note que l'exécution complète est parfois impossible, y compris pour les tests automatisés de longue durée. [CTAL-TA v4.0 FR, §2.2.1, pp. 28-29]
- **Traçabilité** entre stories, exigences et tests, pour savoir quoi rejouer et repérer les trous de couverture. [CTAL-AT v2.0 EN, §1.4, p. 18]
- **Plan de transition manuel → automatisé** :
  - coûts de double exécution pendant la transition ;
  - chevauchement fonctionnel (par exemple le login factorisé en composant) ;
  - données de test partagées ;
  - interdépendance des tests ;
  - préconditions d'exécution.

  [CT-TAS v1.0 FR, §6.1.1, pp. 49-50]
- **Analyse des risques de l'outil et de l'automatisation** : attentes irréalistes, maintenance sous-estimée, compétences. [CTFL v4.0.1 EN, §6.2, p. 60] ; [CTEL-TM 2011 EN, §2.3.7, p. 16]
- **Conditions de succès de la stratégie** : tests maintenables, compétences de l'équipe, outils disponibles, périmètre produit changeant. [CTEL-TM 2011 EN, §2.3.7, p. 16]
- **Amélioration continue de la sélection** : analyser l'efficacité des techniques après chaque cycle, garder les efficaces et remplacer les autres. [CTAL-TA v4.0 FR, §2.2.1, p. 29]
- **Mesure** : rien n'est dit sur les indicateurs de succès (fiabilité de la suite, taux de tests instables, défauts échappés).

## Niveau de maturité : 1 — Initial
La démarche est une intention. Je ne vois ni étapes définies, ni rôles, ni planification, ni suivi. Aucun critère du niveau 2 n'est démontré, et un critère non mentionné compte comme non démontré. Ce n'est pas une évaluation TMMi officielle.

**Pour passer au niveau 2 (Géré), au niveau d'un projet :**
- remplacer « 100 % » par un périmètre priorisé selon les risques ;
- planifier la transition avec exécution manuelle et automatisée en parallèle, puis valider l'équivalence ;
- définir les suites déclenchées par commit, par nuit et par déploiement ;
- garder l'exploratoire et la régression collaborative ;
- assigner des rôles et un suivi (revue du périmètre à chaque cycle).

Les niveaux 3 à 5 demandent une stratégie d'automatisation commune à l'organisation, des métriques définies à l'avance, puis une amélioration continue fondée sur ces mesures.

## Confiance : 72/100
- La recherche sur la régression et l'automatisation est bien couverte : 4 syllabus contiennent toutes les notions, et j'ai lu les sections citées.
- Je n'ai pas fait de recherche spécifique sur CI/CD « à chaque commit » en dehors du CTAL-AT et du CTAL-TAE.
- Je n'ai pas lu les sections plus générales de CT-TAS sur la stratégie, ni la gestion des tests instables.
- Votre message est bref : j'ai supposé que « supprimer les tests manuels » inclut l'exploratoire. Si vous visez seulement l'exécution manuelle de la régression, P4 devient conforme sous condition.

**Limites :**
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable.
- Playwright n'est pas évaluable avec les syllabus. Thomas pourrait chercher sur le Web si vous voulez comparer les outils.
- CTAL-AT v2.0 est un syllabus avancé en anglais seulement, et j'ai traduit les passages cités.

## À capitaliser ?
Une idée durable ressort : une liste de contrôle « passage du manuel à l'automatisation de la régression ». Elle comprendrait les prérequis (test exécutable, équivalence), les risques de l'outil, le périmètre par risque, la place de l'exploratoire et les déclencheurs en pipeline. Je ne l'ai pas enregistrée. Voulez-vous que je prépare la fiche et vérifie les doublons ?

## Commandes exécutées

- `Skill {"skill": "qa-knowledge"}`
- `Read {"file_path": "/home/user/istqbfinder/referentiel/grille-maturite.md"}`
- `python qa.py chercher "test automation regression suite benefits risks" && python qa.py chercher "automatisation des tests régression 100 % tests manuels"`
- `python qa.py section CTFL-4.0.1-en 6.2; echo ======; python qa.py section CT-TAS-1.0-fr 6.1.1; echo ======; python qa.py section CTEL-TM-2011-en 2.3.7`
- `python qa.py section CTAL-AT-2.0-en 1.4; echo ======; python qa.py section CTAL-TAE-2.0-fr 5.1.1; echo ======; python qa.py section CTAL-TA-4.0-fr 2.2.1`
