# S2-automatisation — sylvie

**Question** : On veut automatiser 100 % de nos tests de régression avec Playwright, les lancer à chaque commit et supprimer les tests manuels. Est-ce aligné avec les recommandations ISTQB ? Niveau de maturité ?

**Tours** : 7 · **coût** : 0.149 $ · **confiance annoncée** : 72 · **verdict** : ÉCHEC · **citations** : 11/12 lues · **Web** : 0

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est **partiellement alignée**. Automatiser massivement la régression dans le pipeline CI/CD est bien recommandé. En revanche, « 100 % » et « supprimer les tests manuels » vont plus loin que ce que décrivent les syllabus, et la suppression des tests manuels est un **écart**.

## Pratiques décrites

Toutes sont des intentions : tu n'as cité aucune preuve de mise en place (pipeline, suite existante, indicateurs).

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1. Automatiser 100 % de la régression | Intention | Partiellement aligné | La régression doit être « aussi automatisée que possible » et intégrée à la conception du pipeline. Elle s'appuie sur les niveaux de risque, pas sur un objectif de 100 %. Parmi les risques de l'automatisation : attentes irréalistes, estimations de maintenance inexactes, recours à l'outil quand le manuel serait plus adapté. | [CT-QDO v1.0 EN, §3.2 p. 38 ; §3.2.1 p. 39] ; [CTFL v4.0.1 EN, §6.2, pp. 59-60] |
| P2. Lancer la suite à chaque commit | Intention | Partiellement aligné | Un **sous-ensemble** de tests de régression est déclenché à chaque commit, choisi selon l'impact, la probabilité de risque, l'emplacement et les dépendances du changement. Lancer tous les tests à chaque exécution est jugé mauvais pour la viabilité économique et la durabilité. On crée plusieurs suites (avant fusion, après fusion, de nuit), avec tags et filtres. La suite complète s'exécute avant la mise en production. | [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CT-QDO v1.0 EN, §3.2.1, p. 39] |
| P3. Supprimer les tests manuels | Intention | **Écart** | L'exploration est la « contrepartie de l'automatisation » : le retour vient des personnes, pas des outils. Les résultats exploratoires sont enregistrés dans le pipeline avec les résultats automatisés. La régression exploratoire complète l'automatisation, et l'approche par les risques aide à décider où l'automatisation est inutile. Un excès de confiance dans l'outil ignore le besoin d'esprit critique humain. | [CT-QDO v1.0 EN, §3.3.2, pp. 42-43] ; [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CTFL v4.0.1 EN, §6.2, p. 60] |
| Choix de Playwright | Intention | Hors ISTQB | Les syllabus lus sont indépendants des outils. Ils demandent seulement d'analyser les risques liés à l'outil : dépendance au fournisseur, projet open source abandonné, incompatibilité avec la plateforme, exigences réglementaires. | [CTFL v4.0.1 EN, §6.2, p. 60] |

## Ce qui manque

- **Sélection des tests par les risques ou l'impact** : aucun critère n'est décrit pour choisir quoi lancer à chaque commit. Les syllabus citent l'analyse d'impact outillée, la sélection par risques, l'historique et la traçabilité [CTAL-TA v4.0 EN, §2.2, pp. 26-27].
- **Revue régulière du périmètre de régression** : à chaque cycle, avec ajustement de la suite [CTAL-TA v4.0 EN, §2.2, p. 26].
- **Plusieurs suites et une suite complète avant livraison** : une suite rapide par commit, d'autres avant fusion ou la nuit [CT-QDO v1.0 EN, §3.2.1, p. 39].
- **Place de l'exploratoire, du collaboratif et du manuel** : à planifier, notamment pour l'utilisabilité et l'acceptation. Les cycles de livraison courts demandent beaucoup d'automatisation (quadrants 1 et 4), mais la stratégie reste un équilibre entre quadrants [CTAL-AT v2.0 EN, §1.4, pp. 17-18 ; §3.1.2, p. 26].
- **Traçabilité légère** entre exigences ou user stories et tests, pour savoir quoi relancer [CTAL-AT v2.0 EN, §1.4, p. 18].
- **Analyse des risques de l'automatisation** : coût de maintenance, attentes irréalistes, tests instables. Les syllabus lus ne détaillent pas le traitement des faux positifs, hormis la ré-exécution manuelle d'un test automatisé en échec [CTAL-TA v4.0 EN, §1.2.4, p. 17, vu en extrait seulement].
- **Environnements** de test suffisants, en parallèle, pour tenir les temps d'exécution [CT-QDO v1.0 EN, §3.2.1, p. 39].

## Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné

- **Pourquoi le niveau 1** : aucune pratique n'est en place, donc le niveau est plafonné à 1 (grille du dépôt).
- **Pourquoi le niveau 2 est visé** : la démarche décrit une exécution automatisée, mais pas de stratégie écrite, de sélection fondée sur les risques ni de supervision. Ces éléments relèvent du niveau 2 (grille du dépôt).
- **Pour passer au niveau 2** :
  1. Rédiger une stratégie de régression : quoi automatiser, quoi garder en manuel ou exploratoire, et pourquoi.
  2. Définir des suites et des critères de sélection (risque ou impact).
  3. Mettre en place le pipeline et son suivi (résultats, tests instables, maintenance), avec les environnements nécessaires.
- **Niveaux 3 à 5** : leurs critères sont une adaptation du dépôt, pas un modèle TMMi.

## Questions à choix

1. Quel est le contexte du produit ?
   1. Application web classique, sans contrainte réglementaire
   2. Domaine réglementé (santé, finance, transport)
   3. Je préfère ne pas préciser
2. Que recouvre « tests manuels » dans ton projet ?
   1. Surtout de l'exécution manuelle de scénarios de régression
   2. Un mélange d'exécution de scénarios, d'exploratoire et d'acceptation
   3. Autre
3. Quelle suite veux-tu ?
   1. Évaluer une stratégie de régression à plusieurs suites (commit, fusion, nuit, avant livraison)
   2. Chercher des critères de sélection des tests dans les syllabus
   3. Rien de plus

## Confiance : 72/100

- **Pour** : les passages clés (CT-QDO §3.2.1, CTAL-AT §1.4, CTFL §6.2, CTAL-TA §2.2) ont été lus en entier, et ce sont des versions courantes.
- **Contre** : la démarche est peu détaillée, et aucun syllabus ne traite de Playwright ni du contexte réglementaire. Le sujet est le plus explicite dans des syllabus récents (CT-QDO, CTAL-AT 2.0). Je n'ai lu aucun passage du CTAL-TAE.

## Limites

- Aucun syllabus de la bibliothèque ne couvre Playwright, ni un cadre réglementaire éventuel de ton domaine. Ce qui en dépend est « Non vérifiable ».
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque : aucune conformité ISO n'est vérifiable ici.
- Pour une recherche plus large (retours d'expérience, tests instables, outils), Thomas peut chercher sur le Web.

## Traçabilité

- **Date de l'avis** : 2026-10-23.
- **Documents lus** :

| Document | Version (publication) | Sections et pages lues |
|---|---|---|
| CTFL-4.0.1-en | v4.0.1 (2024-09-15) | §6.2, pp. 59-60 |
| CTAL-AT-2.0-en | v2.0 (2026-04-17) | §1.4, pp. 17-18 ; §3.1.2, p. 26 (page affichée) |
| CT-QDO-1.0-en | v1.0 (2026-04-17) | §3.2, pp. 38-39 ; §3.2.1, p. 39 ; §3.2.3 p. 41 (lu, non cité) ; §3.3.2, pp. 42-43 |
| CTAL-TA-4.0-en | v4.0 (2025-05-02) | §2.2, pp. 26-27 |

- **Requêtes `chercher`** :
  - « test automation regression suite benefits risks manual testing »
  - « automatisation des tests régression intégration continue avantages risques »
  - « exploratory testing manual testing experience-based cannot be automated »
- **Référence non lue** : CTAL-TA §1.2.4 p. 17 (cité « en extrait seulement ») n'est vu que comme extrait de recherche. Je ne m'appuie pas dessus pour un verdict.
- **Grille de maturité** : citée comme « grille du dépôt », sans page des documents TMMi.

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/referentiel/grille-maturi`
- `python qa.py chercher "test automation regression suite benefits risks manual testing" 2>&1 | head -80`
- `python qa.py chercher "automatisation des tests régression intégration continue avantages risques" 2>&1 | head -80`
- `python qa.py section CTFL-4.0.1-en 6.2; echo ======; python qa.py section CTAL-AT-2.0-en 1.4; echo ======; python qa.py section CT-QDO-1.0-en 3.2`
- `python qa.py section CTAL-TA-4.0-en 2.2; echo ======; python qa.py chercher "exploratory testing manual testing experience-based cannot be automated" 2>&1 | head -40`
- `python qa.py section CT-QDO-1.0-en 3.3.2; python qa.py page CTAL-AT-2.0-en 26`
