# M6-api — thomas

**Question** : Comment mettre en place les tests d'une API REST utilisée par plusieurs équipes : tests de contrat, test d'intégration et performance ?

**Tours** : 14 · **coût** : 0.193 $ · **confiance annoncée** : 81 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 0 · **critères** : 7/7

## Réponse

Je termine la vérification des sources et je rédige le rapport.

## Sources retenues

Lus et cités: CT-QDO v1.0 EN (§3.2.2), CTAL-TAE v2.0 EN (§5.1.3), CTAL-TTA v4.0 EN (§2.7), CT-TAS v1.0 FR (§3.1.1), CT-PT 2018 EN (§3.2, §4.1.2, §2.1.2, §4.2.6).
- La base d'idées n'a rien donné: 3 requêtes, aucune idée capitalisée.
- Il n'y a pas de syllabus API dédié.
- Les tests de contrat ne sont couverts qu'en anglais (CT-QDO, CTAL-TAE). CT-TAS en parle en français, mais seulement dans une définition.
- Aucun outil n'est nommé dans ta question, donc je n'ai pas fait de recherche Web.

Les syllabus décrivent les tests de contrat comme un test d'intégration complémentaire des autres tests d'API. La performance se traite à part, avec ses propres critères d'acceptation.

**Hypothèse de contexte:** une API REST interne exposée à plusieurs équipes consommatrices, en microservices, avec CI/CD, sans contrainte réglementaire.

## Méthode pas à pas

1. **Cartographier les consommateurs et les dépendances.** QA Lead, au démarrage. Livrable: liste des équipes consommatrices, documentation de l'API (paramètres, en-têtes, types de requête/réponse) et relations entre les API. [CTAL-TAE v2.0 EN, §5.1.3, p. 36]
2. **Répartir les tests par niveau.** QA Lead avec les équipes. Livrable: une pyramide cible. Le niveau service se découpe en tests d'intégration de composants (avec doubles de test), tests de contrat (entre services) et tests d'API (données réelles, services réels). Dessine l'état actuel et l'état ciblé. [CT-TAS v1.0 FR, §3.1.1, p. 25]
3. **Définir les contrats.** Fournisseur et consommateurs, ensemble. Livrable: contrat versionné décrivant les formats de requête, les champs de réponse, les codes de statut et les types de données. [CT-QDO v1.0 EN, §3.2.2, p. 40-41]
   - Choisis un mode. En mode piloté par le consommateur, chaque consommateur fixe ce qu'il attend du fournisseur. En mode piloté par le fournisseur, c'est le fournisseur qui publie le contrat. [CTAL-TAE v2.0 EN, §5.1.3, p. 36]
   - Avec plusieurs équipes consommatrices, le mode consommateur semble plus naturel (interprétation).
4. **Vérifier les contrats en CI et les gouverner.** Chaque équipe, à chaque build. Livrable: contrats stockés en gestion de versions, tests lancés dans le pipeline pour détecter les ruptures avant déploiement. Le syllabus prévient que les changements de contrat demandent une coordination entre équipes et un investissement en outillage et en standards communs. [CT-QDO v1.0 EN, §3.2.2, p. 41]
5. **Concevoir les tests d'API et d'intégration.** TTA ou développeurs, par sprint. Livrable: une suite de tests d'API. [CTAL-TTA v4.0 EN, §2.7, p. 17-18]
   - Couverture minimale: des appels avec des valeurs réalistes et des valeurs inattendues.
   - Critères d'entrée possibles: toutes les opérations, tous les paramètres, des séquences d'opérations.
   - Critères de sortie possibles: tous les codes de statut corrects et erronés, des réponses avec toutes les propriétés.
   - Les tests négatifs sont souvent essentiels. Teste aussi la reprise et les nouvelles tentatives (transactions perdues, problèmes de timing).
   - Le contrat ne remplace pas ces tests: il en est un complément. [CT-QDO v1.0 EN, §3.2.2, p. 41]
6. **Fixer les critères de performance avant d'écrire les scripts.** Ingénieur performance, avec les métiers. Livrable: un plan de test avec des critères d'acceptation reliés aux objectifs, aux SLA et à une baseline mesurée. Le temps de réponse est une préoccupation utilisateur, le débit une préoccupation métier, l'utilisation des ressources une préoccupation système. [CT-PT 2018 EN, §4.1.2, p. 34]
   - Les métriques possibles incluent le débit des transactions clés, les taux de violation de SLA, la concurrence et les erreurs. [CT-PT 2018 EN, §2.1.2, p. 19]
7. **Scripter la charge au niveau protocole.** Ingénieur performance. Livrable: des scripts avec initialisation, corps et nettoyage.
   - Les chronomètres encadrent une unité de travail logique. À ce niveau, on ne mesure que le temps serveur et réseau.
   - Ajoute des vérifications du résultat, car la gestion d'erreur par défaut des outils est minimale (souvent le seul code HTTP). [CT-PT 2018 EN, §4.2.6, p. 45-46]
   - L'API est aussi une source de charge imprévue, par exemple en ouvrant à des clients nouveaux un système ancien. [CT-PT 2018 EN, §3.2, p. 27]

## Exemple de mise en œuvre (fictif, interprétation)

« Une API Commandes est consommée par trois équipes: web, mobile et facturation.
- Chaque consommateur publie ses attentes dans un dépôt de contrats versionné (étapes 3-4).
- Le fournisseur rejoue ces contrats à chaque pull request. Les ruptures bloquent la fusion.
- Une suite d'API nocturne couvre les codes d'erreur et les séquences create → read → cancel (étape 5).
- Avant chaque release majeure, un test de charge vise le débit et le temps de réponse de référence convenus avec le métier, comparés à la baseline (étapes 6-7). »

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| API (ton cas) | Le contrat sert de pivot entre équipes | CT-QDO §3.2.2, CTAL-TAE §5.1.3, CTAL-TTA §2.7 |
| Santé / réglementé | Pas de syllabus santé, donc pas de norme IEC 62304 dans la bibliothèque. Une recherche Web serait nécessaire. | — |
| Web | Pas de syllabus dédié. Les risques de performance par architecture se transposent. | CT-PT §3.2 |
| Embarqué | Peu pertinent pour une API REST. | CT-PT §3.2 |
| Mobile | Les applications mobiles dépendent de services distants, source possible de goulot de performance. | CT-PT §3.2, CT-MAT |

## Par quoi je commencerais

1. Cartographier les consommateurs et choisir un seul contrat pilote. Impact fort, effort faible.
2. Brancher la vérification des contrats dans la CI. Impact fort, effort moyen.
3. Définir les SLA et la baseline de performance, avant tout outil de charge. Impact moyen, effort faible.

## Où creuser ensuite

- `section CT-QDO-1.0-en 3.1.1`: gestion de versions et contrats (renvoi du §3.2.2, non lu).
- `section CT-PT-2018-en 4.1`: approche de charge et plan de test.
- `section CT-TAS-1.0-fr 3.1`: distribution des tests et pyramide.
- `section CTAL-TAE-2.0-en 5.1`: stratégie d'automatisation d'API.

## Confiance

**Confiance: 81/100 (élevée)**. Calcul: base 85 × 0,6 = 51, plus 7 passages lus (+20), plus 4 syllabus concordants (+20), moins 10 pour le raisonnement sans source. Les deux étapes marquées « interprétation » sont le choix du mode consommateur et l'exemple.

## À capitaliser ?

Pas de doublon (`idee doublons`: aucune idée similaire; thème suggéré: `api`).

```json
{
  "titre": "Séquencer tests de contrat, d'API et de performance pour une API partagée entre équipes",
  "resume": "Le contrat versionné sert de pivot entre équipes et se vérifie en CI. Il complète les tests d'API, qui couvrent les cas négatifs et les séquences. La performance se pilote à part, avec SLA et baseline.",
  "principe": "Définir le contrat, le versionner, le faire vérifier en CI par fournisseur et consommateurs. Compléter par des tests d'API (valeurs inattendues, codes d'erreur). Fixer des critères d'acceptation de performance avant de scripter la charge.",
  "theme": "api",
  "references": [
    {"doc": "CT-QDO-1.0-en", "page": 41, "extrait": "Contract tests do not cover all functional aspects of API testing, and they supplement other test types."},
    {"doc": "CT-PT-2018-en", "page": 34, "extrait": "response time is a user concern, throughput is a business concern, and resource utilization is a system concern."}
  ]
}
```

L'`extrait` reprend les passages lus. Les champs doivent être confrontés à `python qa.py idee modele` avant `idee ajouter`.

## Questions à choix

1. **Quel est ton contexte?**
   1. Microservices en agile avec CI/CD
   2. Système plus ancien avec cycle séquentiel
   3. Secteur réglementé (santé, finance)
2. **Quelle suite?**
   1. Approfondir les tests de contrat (consommateur contre fournisseur)
   2. Approfondir la performance d'API (SLA, baseline)
   3. Capitaliser cette idée

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher "contrat API" ; python qa.py idee chercher "performance API" ; python qa.py idee chercher "intégration API REST"`
- `python qa.py chercher "contract testing API" ; python qa.py chercher "API testing REST" ; python qa.py chercher "tests d'intégration API" ; python qa.py chercher "performance testing API load"`
- `python qa.py section CT-QDO-1.0-en 3.2.2 --max-caracteres 7000`
- `python qa.py section CTAL-TAE-2.0-en 5.1.3 --max-caracteres 5000`
- `python qa.py section CTAL-TTA-4.0-en 2.7 --max-caracteres 6000`
- `python qa.py lire 3477 --contexte 1 --max-caracteres 5000; python qa.py lire 850 --contexte 0 --max-caracteres 3000; python qa.py lire 886 --contexte 0 --max-caracteres 3000`
- `python qa.py lire 3477 --contexte 1; python qa.py lire 850; python qa.py lire 886`
- `python qa.py section CT-PT-2018-en 4.2.6 --max-caracteres 3500`
- `python qa.py chercher "performance test objectives service level agreements throughput response time" --doc CT-PT | head -30; python qa.py chercher "Pact consumer-driven contract" ; python qa.py cherc`
- `python qa.py lire 865; python qa.py lire 833`
- `python qa.py confiance --help | head -20; python qa.py idee doublons --titre "Mise en place tests API REST multi-équipes : contrat, intégration, performance" --resume "Séquencer tests de contrat versi`
- `python qa.py confiance --base 85 --lus 7 --concordants 4 --raisonnement 1`
