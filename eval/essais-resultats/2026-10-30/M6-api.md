# M6-api — thomas

**Question** : Comment mettre en place les tests d'une API REST utilisée par plusieurs équipes : tests de contrat, test d'intégration et performance ?

**Tours** : 14 · **coût** : 0.35 $ · **confiance annoncée** : 78 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0 · **critères** : 8/8 · **fidélité** (juge LLM, indicatif) : 0.95 sur 10 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : base d'idées (aucune idée capitalisée sur le sujet) ; CT-QDO v1.0 EN §3.2.2 ; CTAL-TAE v2.0 EN §5.1.3 ; CTAL-TTA v4.0 EN §2.7 ; CTAL-AT v2.0 EN §1.2 ; CT-TAS v1.0 EN §3.1.3 ; CT-PT 2018 EN §3.2 et §4.1.2. Ce que `chercher` n'a pas donné : aucun syllabus API dédié, et aucun passage sur un outil précis. Je n'ai pas cherché sur le Web, parce que ta question ne nomme aucun outil. Les passages utiles sont presque tous en anglais.

Les syllabus décrivent une démarche en trois couches. Les tests de contrat servent de filet entre équipes, les tests d'intégration restent au niveau interface, et la performance suit un plan de test dédié. Aucun syllabus ne réunit les trois, donc l'assemblage ci-dessous est le mien.

**Hypothèse de contexte** : API REST de type microservices, plusieurs équipes consommatrices, pipeline CI/CD, domaine web non réglementé.

## Méthode pas à pas

1. **Cartographier producteurs et consommateurs.**
   - Qui : QA Lead avec les équipes. Quand : au démarrage. Livrable : un graphe d'appels des API.
   - Il permet d'identifier les points sensibles [CT-TAS v1.0 EN, §3.1.3, p. 25].
   - Il faut aussi rassembler la documentation de l'API (paramètres, en-têtes, types de requêtes et de réponses). Elle sert de référence aux tests automatisés [CTAL-TAE v2.0 EN, §5.1.3, p. 36].
2. **Définir le contrat et le versionner.**
   - Qui : consommateurs et fournisseur, ensemble. Livrable : un contrat dans le dépôt de code.
   - Le contrat précise les formats de requête, les champs de réponse, les codes de statut et les types de données [CT-QDO v1.0 EN, §3.2.2, p. 40].
   - Quand plusieurs équipes sont concernées, on le versionne et on le stocke sous gestion de versions [CT-QDO v1.0 EN, §3.2.2, p. 41].
   - Choisis l'approche : dans le mode « consumer-driven », le consommateur fixe ses attentes ; en mode « provider-driven », le fournisseur publie le contrat [CTAL-TAE v2.0 EN, §5.1.3, p. 36].
   - Le mode consumer-driven est présenté comme particulièrement efficace en agile, quand les services évoluent indépendamment [CTAL-AT v2.0 EN, §1.2, p. 15].
3. **Brancher les tests de contrat dans la CI.**
   - Qui : chaque équipe, à chaque commit. Livrable : un pipeline qui bloque les changements cassants avant déploiement [CT-QDO v1.0 EN, §3.2.2, p. 41].
   - Le contrat complète les autres tests sans les remplacer. Un changement de contrat demande une coordination entre équipes [CT-QDO v1.0 EN, §3.2.2, p. 41].
4. **Tests d'API et d'intégration par le fournisseur.**
   - Qui : Technical Test Analyst ou développeurs. Livrable : une suite fonctionnelle.
   - Prévois des cas négatifs et de la gestion d'erreur. Teste les combinaisons de paramètres, les reprises et les nouvelles tentatives. Vise les codes de statut corrects et erronés et les sorties de toutes les propriétés [CTAL-TTA v4.0 EN, §2.7, p. 17-18].
   - Utilise des doubles de test (mocks, stubs) pour ne pas dépendre de services réels [CT-TAS v1.0 EN, §3.1.3, p. 25].
5. **Garder peu de tests de bout en bout.**
   - Qui : QA Lead. Livrable : quelques parcours critiques seulement.
   - L'intégration se fait de préférence au niveau interface. Le contrat est une alternative aux nombreux tests E2E, qu'il complète sans les remplacer [CTAL-AT v2.0 EN, §1.2, p. 15-16].
6. **Rédiger un plan de test de performance.**
   - Qui : testeur performance avec les responsables métier. Livrable : un plan de test de performance.
   - Il contient les objectifs, les critères d'acceptation (SLA, valeurs de référence), les données, l'environnement, les profils de charge, les métriques et les risques [CT-PT 2018 EN, §4.1.2, p. 33-37].
   - Il peut cibler un composant isolé, moins cher et possible dès que le composant existe [CT-PT 2018 EN, §4.1.2, p. 35].
   - Le plan doit aussi dire comment extrapoler les résultats d'un environnement réduit vers la production [CT-PT 2018 EN, §4.1.2, p. 35].
7. **Surveiller en continu après la mise en production.** (interprétation, appuyée sur le « shift right »)
   - L'observabilité permet de suivre la performance des API avec de vrais utilisateurs [CT-TAS v1.0 EN, §3.1.3, p. 25].

## Exemple de mise en œuvre (fictif, interprétation)

Trois équipes consomment une API « Commandes » gérée par une quatrième.
- Chaque consommateur écrit ses attentes de contrat. Le fournisseur les rejoue à chaque build (étapes 2-3).
- Le fournisseur ajoute une suite fonctionnelle avec cas négatifs, et des tests d'intégration contre des stubs (étape 4).
- Deux parcours E2E seulement tournent avant les mises en production (étape 5).
- Une fois par sprint, un test de charge rejoue un profil de trafic agrégé des trois consommateurs, avec un seuil p90 issu du SLA (étape 6).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | La bibliothèque ne couvre pas le dispositif médical. La traçabilité du contrat versionné aide, et le masquage des données pèse sur la perf. | Masquage : CT-PT §4.1.2 ; CTAL-TTA §2.8.2 (à lire) |
| Web | Principes transposés (pas de syllabus web dédié). | CT-PT §3.2 |
| Embarqué | Peu pertinent ici, sauf API sur objets connectés. | CT-PT §3.2 (à lire) |
| Mobile | L'API est un goulet de performance fréquent côté mobile. | CT-PT §3.2, p. 26 |
| API | Cœur de la réponse, voir les étapes ci-dessus. | CT-QDO §3.2.2, CTAL-TTA §2.7 |

## Par quoi je commencerais

1. **Contrats consumer-driven en CI** : impact fort, effort moyen. C'est ce qui protège les équipes entre elles.
2. **Plan de test de performance avec SLA et profil de charge** : impact fort, effort moyen. Sans critères d'acceptation, les chiffres ne décident rien.
3. **Tests fonctionnels négatifs de l'API** : impact moyen, effort faible.

## Où creuser ensuite

- `section CT-QDO-1.0-en 3.2` pour les tests automatisés en équipe DevOps.
- `section CT-PT-2018-en 4.2` pour les profils et les scripts de charge.
- `section CTAL-TAE-2.0-en 5.1` pour l'intégration à la CI/CD.
- À lire : CT-PT 2018 EN §3.3, que je n'ai pas lu.

**Confiance : 78/100** (élevée) — base 80 × 0,6 = 48 ; 8 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10 (étape 7 et l'exemple). L'absence d'outil précis et de syllabus API dédié limite le niveau de détail.

## Questions à choix

1. Quel est ton contexte principal ?
   1. Web non réglementé
   2. Réglementé (santé, finance)
   3. Mobile ou embarqué
2. Quelle suite veux-tu ?
   1. Approfondir la performance (profils de charge, CT-PT §4.2)
   2. Comparer contrat consumer-driven et provider-driven
   3. Capitaliser la méthode dans la base

## À capitaliser ?

Aucun doublon trouvé. Thèmes suggérés : api, test-management, exigences.

```json
{
 "titre": "Contrat consumer-driven versionné pour API multi-équipes",
 "resume": "Contrats partagés, versionnés et rejoués en CI pour sécuriser une API utilisée par plusieurs équipes, complétés par peu de tests E2E.",
 "probleme": "Une API REST consommée par plusieurs équipes casse les consommateurs à chaque changement, et les tests E2E sont lents et peu diagnostiques.",
 "principe": "Définir le contrat, laisser les consommateurs exprimer leurs attentes, le versionner, le rejouer en CI, et limiter les tests de bout en bout aux parcours critiques.",
 "theme_principal": "api",
 "themes_secondaires": ["test-management"],
 "domaine_application": "Microservices ou API partagée entre plusieurs équipes, pipeline CI/CD",
 "prerequis": "Pipeline CI/CD, outillage de contrat et standards partagés entre équipes",
 "benefices": "Retour rapide, diagnostic plus simple, moins de tests E2E",
 "limites": "Ne couvre pas tout le fonctionnel ; les changements de contrat exigent de la coordination.",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « tests d'une API REST multi-équipes »",
 "references": [
  {"type": "istqb", "doc_id": "CT-QDO-1.0-en", "pages": "41", "section": "3.2.2", "extrait": "contracts should be versioned and stored in version control"},
  {"type": "istqb", "doc_id": "CTAL-AT-2.0-en", "pages": "15", "section": "1.2", "extrait": "contract testing offers an alternative to extensive end"}
 ]
}
```

Je n'ai rien enregistré. La conversation principale lancera `idee ajouter` si tu es d'accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher API contrat intégration performance`
- `python qa.py chercher "API testing contract"; python qa.py chercher "tests d'intégration API REST"; python qa.py chercher "performance testing API load"`
- `python qa.py section CT-QDO-1.0-en 3.2.2 --max-caracteres 9000`
- `python qa.py section CTAL-TAE-2.0-en 5.1.3 --max-caracteres 7000`
- `python qa.py section CTAL-TTA-4.0-en 2.7 --max-caracteres 6000`
- `python qa.py section CT-PT-2018-en 3.2 --max-caracteres 7000`
- `python qa.py lire 1495 --contexte 1 --max-caracteres 5000`
- `python qa.py chercher "operational profile load profile performance test planning"; python qa.py chercher "performance testing continuous integration pipeline DevOps"; python qa.py chercher "service v`
- `python qa.py section CT-PT-2018-en 4.1.2 --max-caracteres 7000`
- `python qa.py section CT-TAS-1.0-en 3.1.3 --max-caracteres 5000`
- `python qa.py confiance --help | head -30; python qa.py idee modele | head -40; python qa.py idee doublons --titre "Tests d'une API REST multi-équipes : contrat, intégration, performance" --resume "Mis`
- `python qa.py confiance --base 80 --lus 8 --concordants 3 --raisonnement 1`
