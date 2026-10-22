# M6-api — thomas

**Question** : Comment mettre en place les tests d'une API REST utilisée par plusieurs équipes : tests de contrat, test d'intégration et performance ?

**Tours** : 19 · **coût** : 0.216 $ · **confiance annoncée** : 80 · **citations** : 11/11 lues · **Web** : 0 · **critères** : 7/7

## Réponse

La vérification des doublons n'a pas pu s'exécuter, car l'environnement a bloqué la commande. Je le signale dans la section « À capitaliser ? ».

# Tests d'une API REST partagée par plusieurs équipes : contrat, intégration, performance

**Sources retenues**
- CT-QDO v1.0 EN (2026), §3.2.2 : tests d'API et tests de contrat. C'est la source la plus directe.
- CTAL-TAE v2.0 EN, §5.1.3 : dépendances de l'automatisation d'API et approches de contrat.
- CT-TAS v1.0 EN/FR, §3.1.1 : place des tests de contrat, d'intégration et d'API dans la distribution des tests.
- CTAL-TTA v4.0 EN, §2.7 : test d'API, couverture REST, types de défauts.
- CT-PT 2018 EN, §3.2 et §4.1.2 : risques de performance et plan de test de performance.
- CTAL-TM v3.0 FR, §1.4.2 : alignement entre équipes.
- Base d'idées : rien sur ce sujet.
- Les tests de contrat n'existent qu'en anglais (CT-QDO, CTAL-TAE). Il n'y a pas de syllabus API dédié.
- Je n'ai pas fait de recherche Web : la question ne nomme aucun outil.

**Hypothèse de contexte** : API REST de type microservices, cycle agile avec CI/CD, plusieurs équipes consommatrices, pas de contrainte réglementaire. Je n'ai pas cette information, d'où les questions de cadrage en fin de rapport.

## Méthode pas à pas

1. **Cartographier la répartition des tests entre niveaux.** Le niveau « service » se découpe en trois types :
   - les tests d'intégration de composants, avec des doubles de test (mocks, stubs) ;
   - les tests de contrat ;
   - les tests d'API fonctionnels, avec de vraies données et de vraies connexions.

   Il faut dessiner l'état actuel et l'état cible. [CT-TAS v1.0 EN, §3.1.1, p. 23]
   *Qui / livrable* : QA Lead avec les tech leads, une cartographie « qui teste quoi, à quel niveau » (interprétation pour le format).
2. **Aligner les équipes et prioriser selon le risque.** Dans un système de systèmes, le test doit être aligné avec les autres équipes. Le test basé sur les risques sert à hiérarchiser les tests d'intégration. [CTAL-TM v3.0 FR, §1.4.2, p. 37]
   *Livrable* : liste des consommateurs et des parcours critiques, avec leur niveau de risque (interprétation).
3. **Définir et versionner le contrat.** Le contrat décrit les formats de requête, les champs de réponse, les codes de statut et les types de données. Il est versionné sous gestion de configuration, parce que plusieurs équipes y touchent. [CT-QDO v1.0 EN, §3.2.2, p. 40-41]
   *Qui* : fournisseur et consommateurs, ensemble.
4. **Choisir le sens du contrat.**
   - Approche pilotée par le consommateur : chaque consommateur exprime ses attentes.
   - Approche pilotée par le fournisseur : le fournisseur publie le contrat.

   [CTAL-TAE v2.0 EN, §5.1.3, p. 36]
   Pour une API partagée, l'approche consommateur donne au fournisseur la liste de ce qu'il peut casser. C'est mon raisonnement, pas une recommandation des syllabus (interprétation).
5. **Écrire les tests d'API et d'intégration.**
   - Le minimum : des appels avec des valeurs réalistes et des valeurs inattendues. [CTAL-TTA v4.0 EN, §2.7, p. 18]
   - Les critères de couverture REST se divisent en entrées (opérations, paramètres, séquences d'opérations) et sorties (codes de statut corrects et erronés, propriétés des ressources). [CTAL-TTA v4.0 EN, §2.7, p. 17-18]
   - Les défauts attendus sont les problèmes d'interface, de données, de timing, les transactions perdues ou dupliquées, et les exceptions mal gérées. [CTAL-TTA v4.0 EN, §2.7, p. 18]
   - Les tests négatifs sont souvent déterminants, tout comme les tests de reprise et de nouvelle tentative. [CTAL-TTA v4.0 EN, §2.7, p. 17]
6. **Brancher dans le pipeline CI/CD.** Les tests de contrat s'exécutent à chaque changement, pour détecter les ruptures avant le déploiement. [CT-QDO v1.0 EN, §3.2.2, p. 41] Les tests d'API plus lourds se placent plus loin dans le pipeline (interprétation).
7. **Planifier la performance.** Rédiger un plan de test de performance (PTP) avec :
   - des objectifs par type de partie prenante ;
   - des critères d'acceptation reliés aux SLA et à une valeur de référence (*baseline*) ;
   - des données de test.

   Le temps de réponse est une préoccupation de l'utilisateur, le débit une préoccupation métier, l'usage des ressources une préoccupation du système. [CT-PT 2018 EN, §4.1.2, p. 33-34]
   Une API ouverte à plusieurs consommateurs peut subir des charges imprévues. Le syllabus le décrit pour les mainframes exposés par API. [CT-PT 2018 EN, §3.2, p. 27]

## Exemple de mise en œuvre (fictif, interprétation)

« Cinq équipes consomment une API de commandes ; l'équipe fournisseur livre toutes les 2 semaines. Je ferais :
- Atelier de 2 h pour lister les consommateurs et les endpoints critiques (étapes 1 et 2).
- Contrats versionnés dans un dépôt partagé, avec un propriétaire par contrat (étape 3).
- Chaque consommateur publie ses attentes (étape 4). Le fournisseur les vérifie à chaque merge (étape 6).
- Suite d'API nocturne : cas négatifs, codes d'erreur, idempotence des retries (étape 5).
- Test de charge avant chaque release majeure. Il couvre les 3 endpoints les plus appelés, avec une baseline et un seuil de temps de réponse négocié avec les consommateurs (étape 7). »

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Traçabilité renforcée des contrats et des résultats. Aucun syllabus santé dans la bibliothèque (IEC 62304 absente) ; le Web serait nécessaire pour la norme. | CTAL-TTA v4.0 §2.8.2 (non lu) |
| Web | Cas du présent exemple. Aucun syllabus web dédié, principes transposés. | CT-PT §3.2 |
| Embarqué | Contraintes temps réel et charge différente. | CT-PT §3.2 (non lu en détail) |
| Mobile | Réseau variable et dépendance à des services distants. | CT-PT 2018 §3.2, p. 26 |
| API | Cas central de la question. | CT-QDO §3.2.2, CTAL-TAE §5.1.3 |

## Par quoi je commencerais

1. **Contrats versionnés avec vérification CI** : impact fort, effort moyen. C'est ce qui protège le plus les équipes entre elles.
2. **Suite d'API avec cas négatifs et couverture des statuts** : impact fort, effort moyen.
3. **Plan de performance léger** (baseline, 2-3 endpoints, SLA) : impact moyen, effort faible à moyen. À commencer avant que la charge augmente.

## Où creuser ensuite

- `section CT-QDO-1.0-en 3.2.2` : la suite sur les compromis des tests de contrat, et §4.1 sur l'outillage.
- `section CTAL-TAE-2.0-en 5.1` : la suite de l'infrastructure d'API.
- `section CT-PT-2018-en 4.2` : conception et exécution des tests de performance.
- `section CT-TAS-1.0-en 3.1` : distribution et optimisation du *shift left*.

## Confiance : 80/100 (élevée)

- La confiance documentaire est de 100/100 sur les recherches d'API. Pour la performance, elle est de 69 : seul CT-PT couvre bien le sujet, et il date de 2018.
- J'ai lu au moins quatre passages de syllabus différents.
- L'ordre des étapes et l'exemple relèvent de mon raisonnement (−10).
- Aucune notion n'est restée sans passage lu.

## À capitaliser ?

Je propose une seule idée. Je n'ai pas pu vérifier les doublons : la commande `idee doublons` a été bloquée par l'environnement. La conversation principale devra la relancer avant `idee ajouter`.

```json
{
 "titre": "Contrats d'API versionnés et vérifiés en CI pour une API partagée par plusieurs équipes",
 "resume": "Pour une API REST consommée par plusieurs équipes, formaliser le contrat consommateur/fournisseur, le versionner et le vérifier dans chaque pipeline CI/CD.",
 "probleme": "Les changements d'une API partagée cassent des consommateurs découverts tard, en intégration ou en production.",
 "principe": "Définir le contrat, écrire des tests de contrat côté consommateur et fournisseur, les exécuter en CI/CD, versionner les contrats sous gestion de configuration.",
 "theme_principal": "api",
 "themes_secondaires": ["cicd", "shift-left"],
 "domaine_application": "API REST / microservices consommés par plusieurs équipes",
 "prerequis": "Standards partagés et outillage de tests de contrat",
 "benefices": "Retour rapide et isolé, détection des ruptures avant déploiement",
 "limites": "Ne couvre pas tous les aspects fonctionnels ; coordination entre équipes requise",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-22 : mise en place des tests d'une API REST multi-équipes",
 "references": [
  {"type": "istqb", "doc_id": "CT-QDO-1.0-en", "pages": "41", "section": "3.2.2", "extrait": "contracts should be versioned and stored in version control"}
 ]
}
```

## Questions à choix

1. Quel est ton contexte ?
   1. Microservices en agile avec CI/CD.
   2. Plateforme d'API plus classique, avec des releases espacées.
   3. Domaine réglementé (santé, finance).
2. Par où continuer ?
   1. Approfondir la performance (conception des scénarios et profils de charge).
   2. Comparer contrat piloté par le consommateur et par le fournisseur.
   3. Capitaliser l'idée proposée.
3. Un outil précis est-il envisagé ? Si oui, je ferai une recherche Web sur sa documentation officielle.
   1. Oui, un outil de tests de contrat.
   2. Oui, un outil de charge.
   3. Non.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher "contrat API" ; python qa.py idee chercher "API REST intégration"; python qa.py idee chercher "performance API"`
- `for q in "contract testing API" "test de contrat" "API testing" "integration testing approach" "tests d'intégration API" "performance testing API" "test de performance" "service virtualization" "consu`
- `python qa.py chercher "contract testing API" 2>&1 | head -40`
- `python qa.py chercher "API testing integration" 2>&1 | head -40`
- `python qa.py chercher "performance testing load API" 2>&1 | head -40`
- `python qa.py chercher "service virtualization test doubles" 2>&1 | head -40`
- `python qa.py section CT-QDO-1.0-en 3.2.2 2>&1 | head -80`
- `python qa.py section CTAL-TAE-2.0-en 5.1.3 2>&1 | head -60`
- `python qa.py section CTAL-TTA-4.0-en 2.7 2>&1 | head -50`
- `python qa.py lire 7575 --contexte 1 2>&1 | head -40; python qa.py lire 10338 --contexte 1 2>&1 | head -30`
- `python qa.py chercher "performance test objectives metrics load profile" --doc CT-PT 2>&1 | head -30`
- `python qa.py chercher "integration testing strategy big bang incremental interfaces between teams" 2>&1 | head -30`
- `python qa.py lire 8859 --contexte 1 2>&1 | head -40`
- `python qa.py lire 7590 --contexte 1 2>&1 | head -50; python qa.py lire 11304 --contexte 1 2>&1 | head -30`
- `python qa.py idee modele 2>&1 | head -50`
- `python qa.py themes 2>&1 | head -60`
- `python qa.py idee doublons <<'JSON'
{
 "titre": "Contrats d'API versionnés et vérifiés en CI pour une API partagée par plusieurs équipes",
 "resume": "Pour une API REST consommée par plusieurs équipes`
