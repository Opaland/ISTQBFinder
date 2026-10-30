# S4-recette — sylvie

**Question** : Notre démarche : revues de code obligatoires, tests unitaires à 80 % de couverture, campagne de recette manuelle de 2 semaines avant chaque mise en production, défauts suivis dans Jira sans analyse des causes. Est-ce aligné ISTQB ? Quel niveau de maturité ?

**Tours** : 13 · **coût** : 0.303 $ · **confiance annoncée** : 70 · **verdict** : réussi · **citations** : 17/17 lues · **Web** : 0 · **critères** : 6/6 · **fidélité** (juge LLM, indicatif) : 0.53 sur 6 lignes citées, 0 contradiction(s)

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

Ta démarche est en partie alignée : les revues et la mesure de couverture sont dans l'esprit ISTQB. Il y a un écart net sur le suivi des défauts « sans analyse des causes », et plusieurs éléments attendus ne sont pas démontrés.

Tu décris quatre pratiques. Je les ai toutes marquées « en place », parce que tu les présentes comme appliquées. Aucune preuve précise n'est citée (outil de revue, rapport de couverture, plan de recette, tickets Jira), donc la colonne « preuve » reste à confirmer.

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1. Revues de code obligatoires | en place (preuve : non précisée) | Partiellement aligné | Les revues réussissent avec des objectifs clairs, des critères de sortie mesurables, un type de revue adapté, des retours aux auteurs et un lien avec l'amélioration des processus. Le processus type comprend planification, revue individuelle, analyse et suivi des défauts. Tu ne précises ni type de revue, ni critères, ni retour d'information. | [CTFL v4.0.1 EN, §3.2.5, p. 37] ; [CTFL v4.0.1 EN, §3.2.2, p. 35] |
| P2. Tests unitaires à 80 % de couverture | en place (preuve : non précisée) | Partiellement aligné | La couverture est un pourcentage d'éléments exercés, et un « niveau acceptable » est visé. Mais 100 % de couverture des instructions ne détecte pas tous les défauts (ex. dépendants des données), ni toute la logique de décision. Le syllabus ne fixe aucun seuil. Ta démarche n'indique ni le type de couverture (instructions ou branches), ni la justification des 80 %, ni les critères de sortie définis par niveau de test. | [CTFL v4.0.1 EN, §4.3.1, p. 42] ; [CTFL v4.0.1 EN, §4.3.2, p. 43] ; [CTFL v4.0.1 EN, §5.1.3, p. 49] |
| P3. Campagne de recette manuelle de 2 semaines avant chaque mise en production | en place (preuve : non précisée) | Partiellement aligné | La recette (acceptation) valide l'aptitude au déploiement, idéalement par les utilisateurs visés. Des critères d'entrée et de sortie sont à définir pour chaque niveau de test. Rien dans ta description sur qui exécute la recette, ni sur ses critères d'entrée et de sortie. Rien non plus sur la priorisation selon les risques ou la régression. | [CTFL v4.0.1 EN, §2.2.1, p. 29] ; [CTFL v4.0.1 EN, §5.1.3, p. 49] |
| P4. Défauts suivis dans Jira, sans analyse des causes | en place (preuve : Jira) | Écart sur l'exploitation ; suivi lui-même partiellement aligné | Un processus de gestion des défauts avec workflow de la découverte à la clôture est « essentiel ». Les rapports de défaut doivent aussi « fournir des idées d'amélioration du processus ». Les informations de cause racine et de phase d'introduction servent à réduire le nombre total de défauts. Sans ces données, les améliorations sont « difficiles à mettre en œuvre ». | [CTFL v4.0.1 EN, §5.5, p. 56] ; [CTAL-TM v3.0 FR, §2.3.6, p. 64] ; [CTAL-TM v3.0 FR, §2.3.6, p. 65] |

Tracer les défauts dans un outil est conforme à l'esprit de [CTFL v4.0.1 EN, §5.5, p. 56]. C'est l'absence d'analyse des causes qui s'écarte de ce que décrit [CTAL-TM v3.0 FR, §2.3.6, p. 64]. Ce que le syllabus appelle « analyse des causes racines » est décrit en [CTAL-TM v3.0 FR, §1.5.3, p. 42] : regrouper des défauts, puis chercher les causes (diagramme d'Ishikawa par exemple).

## Ce qui manque
- **Analyse des causes** : phase d'introduction, cause racine, regroupements de défauts, avec des actions d'amélioration. [CTAL-TM v3.0 FR, §2.3.6, p. 64] ; [CTAL-TM v3.0 FR, §1.5.3, p. 42]
- **Critères d'entrée et de sortie** définis par niveau de test (unitaire, recette), avec des mesures de complétude comme la couverture, les défauts non résolus ou la densité de défauts. [CTFL v4.0.1 EN, §5.1.3, p. 49]
- **Objectifs et critères mesurables pour les revues**, choix du type de revue, retour d'information aux auteurs, revues rattachées à l'amélioration des processus. [CTFL v4.0.1 EN, §3.2.5, p. 37]
- **Justification de l'objectif de couverture** (type de couverture, seuil de 80 %). [CTFL v4.0.1 EN, §4.3.1, p. 42]
- **Politique ou stratégie de test écrite, planification, suivi et contrôle** : non mentionnés dans ta description, donc non démontrés (grille du dépôt).

## Niveau atteint : 1 — Initial (niveau visé : 2 — Discipliné)
**Justification.** Les pratiques sont réelles, mais je n'ai aucune preuve d'une politique ou stratégie de test écrite. Rien non plus sur la planification et le suivi, ni sur l'environnement de test. La grille du dépôt rattache ces éléments au niveau 2. Un critère non mentionné compte comme « non démontré ». Le niveau 2 est donc visé, pas atteint.

**Pour passer au niveau 2** :
- Documenter une stratégie de test qui relie revues, tests unitaires, recette et gestion des défauts.
- Définir des critères d'entrée et de sortie par niveau.
- Planifier et suivre la campagne de recette pendant le projet.
- Exploiter les données de défauts, au moins par la phase d'introduction et la cause racine.

Les niveaux 3 à 5 (processus commun, indicateurs de pilotage, amélioration continue) sont une adaptation du dépôt, pas une notation TMMi. L'analyse des causes relèverait du niveau 5 dans cette adaptation, et [CTAL-TM v3.0 FR, §1.5.3, p. 41] la rattache à l'amélioration analytique du processus de test.

## Confiance : 70/100 (moyenne)
Calcul : base 84 × 0,6 = 50 ; 21 passages lus +20 ; 2 syllabus courants concordants +10 ; raisonnement sans source −10 → 70.

La couverture documentaire est élevée et les passages lus concordent. L'attribution du niveau repose en partie sur mon raisonnement : les preuves de terrain ne sont pas fournies.

## Limites
- Je n'ai lu aucun passage sur la planification ou la stratégie de test, ni sur la supervision et le contrôle. Le niveau 2 s'appuie donc sur la grille du dépôt, pas sur un passage de syllabus lu.
- Aucun syllabus de la bibliothèque ne couvre le seuil de 80 % de couverture ni la durée de 2 semaines de recette : le syllabus ne prescrit aucune valeur.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque : toute conformité ISO est non vérifiable. Je n'ai pas non plus évalué un éventuel cadre réglementaire propre à ton domaine.
- Les syllabus ne disent pas que 80 % soit « bon » ou « mauvais ». Je constate seulement qu'une justification manque.

## Questions à choix
**Quelle suite veux-tu ?**
1. Détailler un plan d'analyse des causes (modèle de classification des défauts dans Jira).
2. Lire la planification et la stratégie de test pour affiner le niveau 2.
3. Évaluer la recette de 2 semaines sous l'angle des risques et de la régression.

**Ton domaine est-il réglementé ?**
1. Non
2. Oui (précise lequel)
3. Je ne sais pas

## Où creuser ensuite
- À lire : CTAL-TM v3.0 FR §1.2 et §1.3 (stratégie de test, test basé sur les risques).
- À lire : CTAL-TM v3.0 FR §2.1.2 (pilotage, contrôle et clôture).
- À lire : CTAL-TA v4.0 EN §5.3.2 (classification des défauts pour l'analyse des causes racines), vu seulement en extrait.
- À lire : CTEL-ITP 2011 EN §3.3.2 (niveaux TMMi).

## Traçabilité
- **Date de l'avis** : 2026-10-30.
- **Documents lus** :
  - CTAL-TM-3.0-fr, v3.0, publié le 2024-03-28 : §2.3.6 (pp. 64-65), §1.5.3 (pp. 41-42).
  - CTFL-4.0.1-en, v4.0.1, publié le 2024-09-15 : §5.1.3 (p. 49), §3.2 à 3.2.5 (pp. 35-37), §4.3 à 4.3.3 (pp. 42-43), §5.5 (pp. 56-57), §2.2.1 (pp. 28-29).
  - Référentiel : `referentiel/grille-maturite.md`.
- **Requêtes `chercher`** :
  - « analyse des causes racines défauts amélioration du processus de test »
  - « revue de code revues techniques statiques »
  - « couverture des tests unitaires critères de sortie »

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/referentiel/grille-m`
- `python qa.py chercher "analyse des causes racines défauts amélioration du processus de test"`
- `python qa.py chercher "revue de code revues techniques statiques"`
- `python qa.py chercher "couverture des tests unitaires critères de sortie"`
- `python qa.py section CTAL-TM-3.0-fr 2.3.6`
- `python qa.py section CTAL-TM-3.0-fr 1.5.3`
- `python qa.py section CTFL-4.0.1-en 5.1.3`
- `python qa.py section CTFL-4.0.1-en 3.2`
- `python qa.py section CTFL-4.0.1-en 4.3`
- `python qa.py section CTFL-4.0.1-en 5.5`
- `python qa.py section CTFL-4.0.1-en 2.2.1`
- `python qa.py confiance --autorite 0 --base 84 --lus 21 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0`
