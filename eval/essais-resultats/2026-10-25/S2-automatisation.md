# S2-automatisation — sylvie

**Question** : On veut automatiser 100 % de nos tests de régression avec Playwright, les lancer à chaque commit et supprimer les tests manuels. Est-ce aligné avec les recommandations ISTQB ? Niveau de maturité ?

**Tours** : 8 · **coût** : 0.164 $ · **confiance annoncée** : 74 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0

## Réponse

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

Ta démarche est **partiellement alignée**. Automatiser la régression et la lancer dans la chaîne CI/CD va dans le sens de l'ISTQB. Les syllabus lus contredisent en revanche l'objectif « 100 % » et la suppression des tests manuels. Rien n'est encore en place, donc le niveau est plafonné à 1.

## Pratiques décrites

- **P1** : automatiser 100 % de la régression avec Playwright. *Intention.*
- **P2** : lancer les tests à chaque commit. *Intention.*
- **P3** : supprimer les tests manuels. *Intention.*

| Pratique | Statut | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Automatiser la régression | intention | Aligné sur le principe, Partiellement aligné sur le « 100 % » | La régression doit être « aussi complètement automatisée que possible » et faire partie de la conception du pipeline. L'automatisation fait gagner du temps sur le travail manuel répétitif, comme les tests de régression. Elle a aussi des risques : attentes irréalistes, estimations de maintenance inexactes, outil utilisé là où le manuel conviendrait mieux, confiance excessive dans l'outil. Le choix de Playwright n'est pas évalué : aucun syllabus lu ne traite de cet outil. | [CT-QDO v1.0 EN, §3.2.1, p. 39] ; [CTFL v4.0.1 EN, §6.2, pp. 59-60] |
| P2 Lancement à chaque commit | intention | Partiellement aligné | L'approche « incrémentale » déclenche automatiquement, à chaque commit, un sous-ensemble de tests choisi selon l'impact et la probabilité de risque. Le syllabus DevOps déconseille de tout lancer à chaque exécution du pipeline : cela consomme du temps, du coût et de l'énergie. Il décrit plusieurs suites, lancées avant le merge, après le merge ou la nuit, sélectionnées par les risques, les tags ou les filtres. La suite complète tourne avant la mise en production. | [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CT-QDO v1.0 EN, §3.2.1, p. 39] |
| P3 Supprimer les tests manuels | intention | **Écart** | Même avec un haut niveau d'automatisation, le test manuel reste nécessaire, surtout du point de vue de l'utilisateur. En DevOps, des tests manuels subsistent, notamment exploratoires, parce que certains aspects (comme l'utilisabilité) sont difficiles à évaluer automatiquement. Le test exploratoire complète l'automatisation. Un risque cité est de « se reposer trop sur l'outil », en ignorant le besoin de pensée critique humaine. Le Test Analyst ré-exécute à la main les tests automatisés en échec pour écarter un faux positif. | [CTFL v4.0.1 EN, §2.1.4, p. 27] ; [CT-QDO v1.0 EN, §2.1.2, p. 24] ; [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CTFL v4.0.1 EN, §6.2, p. 60] ; [CTAL-TA v4.0 EN, §1.2.4, p. 17] |

## Ce qui manque

- **Priorisation par les risques.** Il faut décider quoi automatiser et quoi laisser en manuel. L'approche de régression basée sur les risques sert justement à décider « où l'automatisation est inutile » [CTAL-AT v2.0 EN, §1.4, p. 17]. Le syllabus DevOps parle aussi de décider ce qui ne doit pas être automatisé et pourquoi [CT-QDO v1.0 EN, §3.2, p. 39].
- **Stratification des suites.** Il faut un sous-ensemble par commit, une suite plus large la nuit et la suite complète avant livraison [CT-QDO v1.0 EN, §3.2.1, p. 39].
- **Test exploratoire et manuel conservé.** Il faut prévoir une place pour l'exploratoire et pour le test du point de vue utilisateur [CT-QDO v1.0 EN, §2.1.2, p. 24] [CTAL-AT v2.0 EN, §1.4, p. 17].
- **Analyse des risques de l'automatisation.** Il faut estimer l'effort de maintenance des scripts et les attentes réalistes, et vérifier que l'outil convient (plateforme, contraintes réglementaires) [CTFL v4.0.1 EN, §6.2, p. 60].
- **Gestion de configuration du testware.** Elle couvre la configuration d'environnement, les données et les suites de tests, avec des suites distinctes smoke et régression [CTAL-TAE v2.0 EN, §5.1.2, p. 35].
- **Traçabilité.** Elle relie les exigences ou user stories aux tests, pour cibler les tests à rejouer [CTAL-AT v2.0 EN, §1.4, p. 18].

## Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné

- **Justification** : les trois pratiques sont des intentions, et la grille plafonne alors le niveau à 1. La visée relève plutôt du niveau 2 (stratégie écrite, planification, supervision, environnement de test), mais elle n'est pas documentée.
- **Pour passer au niveau 2** :
  - rédiger une stratégie de régression fondée sur les risques ;
  - définir les suites par déclencheur ;
  - mettre en place l'environnement et le suivi (taux d'échec, instabilité, durée) ;
  - conserver une part de test manuel ou exploratoire ciblée.
- **Niveaux 3 à 5** : les critères sont une adaptation du dépôt (standardisation, indicateurs, amélioration continue), pas un contenu de syllabus.

## Confiance : 74/100

- J'ai lu les passages de CT-QDO, CTFL, CTAL-AT, CTAL-TA et CTAL-TAE cités.
- Je ne connais ni le contexte, ni la criticité du produit, ni la durée de la suite de tests.
- Le CTAL-AT v2.0 et le CT-QDO v1.0 ont été publiés en 2026-04 ; je ne sais pas s'ils sont déjà utilisés dans votre organisation.

## Limites

- Aucun syllabus de la bibliothèque ne couvre Playwright en particulier.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable.
- Si votre produit relève d'un cadre réglementaire (santé, finance, ferroviaire), aucun syllabus de la bibliothèque ne le couvre. Les exigences correspondantes sont non vérifiables ici.

## Questions à choix

**Quel est le contexte du produit ?**
1. Application web grand public, non réglementée
2. Domaine réglementé (santé, finance, transport…)
3. Outil interne

**Quelle suite voulez-vous affiner ?**
1. Une stratégie de régression par niveaux de risque
2. La part de test manuel ou exploratoire à garder
3. Une liste de contrôle de l'automatisation en CI/CD

## Où creuser ensuite

- à lire : CTAL-TAE v2.0 §5.1.1 et §5.1.2 en entier (stratégie d'automatisation, pipelines)
- à lire : CT-QDO v1.0 §2.2.6 et §3.1.6 (conception du pipeline, environnements)
- à lire : CTAL-AT v2.0 EN §3.1.2 (stratégie de test de projet et degré d'automatisation)

## Traçabilité

- **Date de l'avis** : 2026-10-25
- **Documents lus** :
  - CTFL-4.0.1-en, v4.0.1 (2024-09-15) : pp. 27, 59, 60
  - CT-QDO-1.0-en, v1.0 (2026-04-17) : pp. 24, 39
  - CTAL-AT-2.0-en, v2.0 (2026-04-17) : §1.4, pp. 17-18
  - CTAL-TA-4.0-en, v4.0 (2025-05-02) : p. 17
  - CTAL-TAE-2.0-en, v2.0 (2024-05-03) : p. 35
  - Grille `referentiel/grille-maturite.md`
- **Requêtes `chercher`** :
  - « test automation regression 100% automation manual testing benefits risks »
  - « continuous integration regression testing automation pipeline »
  - « exploratory testing experience-based complement automated tests »
  - « test automation not everything can be automated manual testing still needed »

**Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-K178/referentiel/grille-matur`
- `python qa.py chercher "test automation regression 100% automation manual testing benefits risks" 2>&1 | head -80`
- `python qa.py chercher "continuous integration regression testing automation pipeline" 2>&1 | head -60`
- `python qa.py page CTFL-4.0.1-en 59; python qa.py page CT-QDO-1.0-en 39; python qa.py section CTAL-AT-2.0-en 1.4 --max-caracteres 5000; python qa.py page CTAL-TA-4.0-en 17`
- `python qa.py page CTAL-TAE-2.0-en 35; python qa.py chercher "exploratory testing experience-based complement automated tests" 2>&1 | head -30`
- `python qa.py page CTFL-4.0.1-en 60; python qa.py chercher "test automation not everything can be automated manual testing still needed" 2>&1 | head -25`
- `python qa.py page CTFL-4.0.1-en 27; python qa.py page CT-QDO-1.0-en 24`
