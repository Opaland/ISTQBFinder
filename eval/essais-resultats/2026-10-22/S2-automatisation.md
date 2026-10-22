# S2-automatisation — sylvie

**Question** : On veut automatiser 100 % de nos tests de régression avec Playwright, les lancer à chaque commit et supprimer les tests manuels. Est-ce aligné avec les recommandations ISTQB ? Niveau de maturité ?

**Tours** : 7 · **coût** : 0.131 $ · **confiance annoncée** : 80 · **verdict** : réussi · **citations** : 7/7 lues · **Web** : 0

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

**Synthèse.** La démarche est en partie alignée. Automatiser la régression et l'intégrer au pipeline CI/CD est recommandé. En revanche, « 100 % automatisé », « tout à chaque commit » et « suppression des tests manuels » vont plus loin que ce que décrivent les syllabus lus. Je relève un écart net (supprimer les tests manuels) et deux pratiques partiellement alignées. Aucune pratique n'est décrite comme déjà en place : le niveau est plafonné à 1.

**Pratiques reformulées** (uniquement celles que tu décris) :
- P1 : automatiser 100 % de la régression avec Playwright. Intention.
- P2 : lancer ces tests à chaque commit. Intention.
- P3 : supprimer les tests manuels. Intention.

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Automatiser la régression | Intention | Partiellement aligné | La régression doit être « aussi complètement automatisée que possible » et intégrée à la conception du pipeline. Aucun passage lu ne fixe 100 % comme objectif. L'automatisation a aussi des risques : attentes irréalistes, coûts de maintenance mal estimés, outil utilisé là où le manuel conviendrait mieux, confiance excessive dans l'outil. Le choix de Playwright n'est pas évalué ici : ces passages ne traitent pas de la sélection d'outil. | [CT-QDO v1.0 EN, §3.2.1, p. 39] ; [CTFL v4.0.1 EN, §6.2, pp. 59-60] |
| P2 Exécution à chaque commit | Intention | Partiellement aligné | Une régression incrémentale lance **un sous-ensemble** de tests à chaque commit, choisi selon l'impact et la probabilité de risque ainsi que la localisation et les dépendances du changement. Toute la suite n'est pas relancée à chaque fois : cela consommerait des ressources inutilement. Plusieurs suites, avec des fréquences et des moments différents (avant ou après fusion, de nuit), sont courantes. La suite complète tourne avant la mise en production. | [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CT-QDO v1.0 EN, §3.2.1, p. 39] ; [CTAL-TAE v2.0 EN, §5.1.1, p. 35] |
| P3 Supprimer les tests manuels | Intention | **Écart** | Même avec un haut niveau d'automatisation, le test manuel reste nécessaire, notamment du point de vue de l'utilisateur. Certains aspects de qualité (ex. l'utilisabilité) sont difficiles à évaluer automatiquement. Le test exploratoire complète l'automatisation. Un risque cité est de s'en remettre trop à l'outil et d'ignorer l'esprit critique humain. | [CTFL v4.0.1 EN, §2.1.4, p. 27] ; [CT-QDO v1.0 EN, §2.1.2, p. 24] ; [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CTFL v4.0.1 EN, §6.2, p. 60] |

**Ce qui manque**
- **Sélection fondée sur les risques.** Aucune sélection des tests à automatiser ou à lancer n'est décrite. Le syllabus mentionne une sélection par risque, par analyse d'impact ou par tags et filtres. Il précise aussi que cette approche aide à décider où l'automatisation est inutile et où l'humain apporte plus de valeur [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CT-QDO v1.0 EN, §3.2.1, p. 39].
- **Stratification des suites.** Les suites (smoke, régression ciblée, régression complète) ne sont pas définies. Le syllabus les distingue selon leur finalité, avec des pipelines et des environnements différents [CTAL-TAE v2.0 EN, §5.1.2, p. 35]. Le smoke test peut servir de barrière qualité [CTAL-AT v2.0 EN, §1.4, p. 17].
- **Rôle du test manuel et exploratoire.** Ce rôle n'est pas défini, alors que le syllabus prévoit explicitement une complémentarité avec l'automatisation [CTAL-AT v2.0 EN, §1.3, p. 17].
- **Analyse des risques de l'automatisation.** Il n'y a ni estimation de l'effort de maintenance des scripts ni plan d'atténuation [CTFL v4.0.1 EN, §6.2, p. 60].
- **Gestion de configuration du testware.** Elle couvre la configuration des environnements, les données de test et les suites. Elle n'est pas mentionnée [CTAL-TAE v2.0 EN, §5.1.2, p. 35].
- **Environnements de test parallèles.** Ils ne sont pas mentionnés. Ils servent à raccourcir les temps d'exécution [CT-QDO v1.0 EN, §3.2.1, p. 39].

**Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné**
- Aucune pratique n'est « en place », donc le plafond est 1. Je n'ai aucune preuve d'une stratégie écrite, d'un pipeline existant ou d'indicateurs.
- Visé : 2. Pour y arriver, il faudrait une stratégie d'automatisation écrite, des suites planifiées, un suivi des résultats et un environnement de test. Ces critères viennent de la grille du dépôt.
- **Pour passer au niveau 2** :
  - Garder le test manuel et exploratoire ciblé sur ce que l'automatisation évalue mal.
  - Définir des suites par risque et par fréquence.
  - Écrire la stratégie.
  - Suivre les exécutions et la maintenance.
- Les niveaux 3 à 5 sont une adaptation du dépôt, non issue des syllabus lus.

**Confiance : 80/100.** Les passages cités sont lus : CTFL v4.0.1, CT-QDO, CTAL-AT v2.0 et CTAL-TAE v2.0. Ils convergent sur les trois pratiques. La confiance n'est pas plus haute pour deux raisons : la démarche est brève, et je n'ai pas lu les sections de CTAL-TAE sur la stratégie d'automatisation ni sur la maintenance.

**Limites**
- Aucun syllabus de la bibliothèque ne couvre Playwright ni un outil particulier.
- Si ton domaine est réglementé, aucun syllabus lu ne couvre ce cadre. Les exigences correspondantes sont non vérifiables ici. Le syllabus mentionne seulement le risque de choisir un outil non conforme [CTFL v4.0.1 EN, §6.2, p. 60].
- La conformité ISO/IEC/IEEE 29119 est non vérifiable : cette norme n'est pas dans la bibliothèque.
- Si tu veux que je précise ou affines, deux questions utiles pour la suite.

**Questions à choix**
1. Ton contexte est-il réglementé (santé, finance, ferroviaire) ?
   - Non
   - Oui, je précise le domaine
   - Je ne sais pas
2. Quelle suite veux-tu ?
   - Une liste de contrôle d'automatisation de la régression au format JSON, sans l'enregistrer
   - Une recherche de Thomas sur la stratégie d'automatisation (CTAL-TAE)
   - Aucune

**Traçabilité**
- Date de l'avis : 2026-10-22.
- Documents lus, tous publiés par l'ISTQB :
  - CTFL-4.0.1-en (v4.0.1, 2024-09-15) : pp. 27, 59, 60.
  - CTAL-AT-2.0-en (v2.0, 2026-04-17) : p. 17, §1.3 et §1.4.
  - CT-QDO-1.0-en (v1.0, 2026-04-17) : pp. 24, 39.
  - CTAL-TAE-2.0-en (v2.0, 2024-05-03) : p. 35, §5.1.1 et §5.1.2.
- Requêtes `chercher` lancées :
  - `"test automation regression suite benefits risks manual testing"`
  - `"automatisation des tests régression intégration continue"`
  - `"test automation not everything can be automated manual testing still needed suitability"`

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/referentiel/grille-maturite`
- `python qa.py chercher "test automation regression suite benefits risks manual testing" 2>&1 | head -80`
- `python qa.py chercher "automatisation des tests régression intégration continue" 2>&1 | head -80`
- `python qa.py page CTFL-4.0.1-en 59; python qa.py page CTAL-AT-2.0-en 17; python qa.py page CT-QDO-1.0-en 39; python qa.py page CTAL-TAE-2.0-en 35`
- `python qa.py page CTFL-4.0.1-en 60; python qa.py chercher "test automation not everything can be automated manual testing still needed suitability" 2>&1 | head -40`
- `python qa.py page CTFL-4.0.1-en 27; python qa.py page CT-QDO-1.0-en 24`
