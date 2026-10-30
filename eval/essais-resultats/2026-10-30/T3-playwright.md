# T3-playwright — thomas

**Question** : Comment réduire le coût de maintenance de nos tests Playwright ?

**Tours** : 13 · **coût** : 0.246 $ · **confiance annoncée** : 68 · **verdict** : réussi · **citations** : 7/7 lues · **Web** : 1 · **fidélité** (juge LLM, indicatif) : 0.94 sur 7 lignes citées, 1 contradiction(s) (CTAL-AT §5.3, p. 46-47 : *God Test Case*, données codées en dur, *Copy-Paste Duplication*, solution « un )

## Réponse

**Sources retenues** : base d'idées (rien de capitalisé sur le sujet). Syllabus lus : CTAL-TAE v2.0 EN (§3.1.5, §4.3.1, §8.1.1), CTAL-AT v2.0 EN (§5.3) et CT-FT v1.0 EN (§6.4). `chercher playwright` ne donne aucun passage, donc j'ai ajouté le Web (doc officielle Playwright). Je n'ai pas lu la version FR de CTAL-TAE §4.3.

Les syllabus ne parlent pas de Playwright, mais CTAL-TAE donne les principes d'architecture et de code pour réduire la maintenance. La doc Playwright dit comment les appliquer à l'outil.

**Hypothèse de contexte** : tests UI end-to-end écrits en TypeScript, avec Playwright Test, dans une équipe qui livre en continu. Je ne connais pas ton symptôme principal (tests instables, ou changements d'UI qui cassent tout).

**Pistes par syllabus**

- **CTAL-TAE v2.0 — §3.1.5 et §4.3 (maintenabilité)**
  - Le *page object model* concentre les locators à un seul endroit. Quand l'UI change, on modifie la classe de page et non chaque test. [CTAL-TAE v2.0 EN, §3.1.5, p. 28]
  - Le *flow model* ajoute une seconde façade, qui regroupe les actions utilisateur pour réutiliser les étapes dans plusieurs scripts. [CTAL-TAE v2.0 EN, §3.1.5, p. 28]
  - Les principes de *clean code* servent de règle d'or : nommage commun, structure de projet logique, pas de valeurs en dur, méthodes courtes, logs, testabilité. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
  - Contre les valeurs en dur : tests pilotés par les données et constantes. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
  - Hygiène de code : analyseurs statiques, formateurs de code, stratégie de branches convenue en gestion de versions. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
- **CTAL-TAE v2.0 — §8.1.1 (amélioration par les données)**
  - L'histogramme des résultats de test repère les tests fragiles, à refactorer ou à réécrire. [CTAL-TAE v2.0 EN, §8.1.1, p. 48]
  - Le *self-healing* par IA détecte un locator modifié et le corrige, en le signalant dans le rapport. Le syllabus ne le présente que comme une opportunité. [CTAL-TAE v2.0 EN, §8.1.1, p. 48]
- **CTAL-AT v2.0 — §5.3 (test smells)**
  - Le syllabus décrit les smells des tests *manuels*. Pour l'automatisé, il renvoie à Aljedaani et al., 2021, que je n'ai pas lu.
  - Plusieurs smells se transposent à ton code (interprétation) :
    - tests interdépendants, solution « indépendants, exécutables dans n'importe quel ordre » [CTAL-AT v2.0 EN, §5.3, p. 45] ;
    - *God Test Case*, données codées en dur, *Copy-Paste Duplication*, solution « un test paramétré » [CTAL-AT v2.0 EN, §5.3, p. 46-47] ;
    - absence de nettoyage (*teardown*) [CTAL-AT v2.0 EN, §5.3, p. 47].
- **CT-FT v1.0 — §6.4 (front web)**
  - La flakiness du GUI s'attaque avec des locators fiables, des attentes explicites, un setup/teardown idempotent, la gestion des données de test et l'isolation des environnements en CI/CD. [CT-FT v1.0 EN, §6.4, p. 46]

**Côté Playwright** (Web, hors ISTQB) [Web — Best Practices, playwright.dev/docs/best-practices, consulté le 2026-10-30]

| Principe ISTQB | Application Playwright |
|---|---|
| Locators fiables | Locators orientés utilisateur (`getByRole`) plutôt que CSS/XPath liés au DOM |
| Attentes explicites | Auto-waiting et assertions « web first » (`toBeVisible()`) qui réessaient |
| Tests indépendants | Chaque test a son propre contexte (stockage, cookies, données) ; projet de *setup* pour la connexion |
| Isoler les dépendances | `page.route` pour simuler les services tiers |
| Diagnostic | Trace viewer au premier retry ; ne pas mettre la trace sur `on` en permanence (coûteux) |
| Hygiène de code | TypeScript et règle ESLint `no-floating-promises` |

La doc ne traite pas des Page Object Models ni des fixtures personnalisées dans cette page. Pour ces deux points, je m'appuie sur le syllabus.

**Ce que j'en retiens** (interprétation)
- La maintenance coûte surtout quand les locators et les flux sont dupliqués dans les tests. C'est l'argument central du POM et du flow model.
- Il vaut mieux mesurer avant de refactorer : le taux d'échec par test indique où agir.
- Le self-healing est une option tardive. Corriger la cause (locators sémantiques, isolation) coûte moins cher et reste prévisible.

**Par quoi je commencerais**
1. **Impact fort, effort faible** : passer les locators en `getByRole` / `getByLabel` / `getByTestId`, et remplacer les attentes fixes par des assertions web-first.
2. **Impact fort, effort moyen** : isoler les tests (données propres, setup de connexion partagé, teardown) et mocker les tiers avec `page.route`.
3. **Impact moyen, effort moyen** : centraliser en POM ou flow model, en commençant par les 3 pages les plus modifiées.
4. **Impact moyen, effort faible** : classer les tests par taux d'échec dans la CI et traiter les plus fragiles en premier.

**Indicateurs de validation** (interprétation) : taux de tests instables, nombre de tests modifiés par changement d'UI, temps passé à corriger les tests chaque sprint.

**Où creuser ensuite**
- `section CTAL-TAE-2.0-en 3.1` (conception de la solution d'automatisation).
- `section CTAL-TAE-2.0-en 8.1` (amélioration continue).
- À lire : CT-TAS v1.0 §5.2 (métriques d'automatisation), vu seulement dans un extrait de recherche.

**Confiance : 68/100** (bonne). Le calcul à la main est : base 71 × 0,6 ≈ 43, plus 4 passages lus (+20), plus 3 syllabus concordants (+10), moins 5 parce que les smells ne visent que le manuel. Playwright est couvert par une page Web officielle consultée, donc le plafond de 60 ne joue pas. Je n'ai pas lancé `qa.py confiance` pour ce score.

**Questions à choix**
1. Quel est ton principal symptôme ?
   1. Tests instables (flaky)
   2. L'UI change et casse beaucoup de tests
   3. Suite lente ou difficile à lire
2. Quelle suite veux-tu ?
   1. Approfondir POM / flow model (CTAL-TAE §3.1)
   2. Comparer self-healing IA et locators stables
   3. Capitaliser ces pistes

**À capitaliser ?** (`idee doublons` : aucune idée similaire ; thème suggéré : maintenance-automatisation)

```json
{
  "titre": "Réduire la maintenance des tests UI automatisés : centraliser les locators et isoler les tests",
  "resume": "Le POM (et le flow model) concentre les locators en un point. Le clean code, les données externalisées et les tests indépendants limitent la dette. Mesurer les tests fragiles avant de refactorer.",
  "principe": "Centraliser les locators et les flux, externaliser les données, isoler les tests, puis cibler les tests fragiles par les données de la CI.",
  "theme": "maintenance-automatisation",
  "references": [
    {"doc": "CTAL-TAE-2.0-en", "section": "3.1.5", "page": 28, "extrait": "Whenever the SUT’s structure changes, the TAE will have to make updates in only one place, the locator inside a page model, instead of updating the locators in each test case."},
    {"doc": "CTAL-TAE-2.0-en", "section": "4.3.1", "page": 32, "extrait": "Hardcoding reduces development time, but it is not recommended to use as data can change frequently which can be time consuming to maintain."},
    {"doc": "CTAL-TAE-2.0-en", "section": "8.1.1", "page": 48, "extrait": "The test histogram also enables the TAEs to identify and select those test cases that are fragile and refactor them"}
  ]
}
```

Les champs de ce JSON sont écrits de mémoire du gabarit. Je n'ai pas lancé `idee modele`, donc la conversation principale doit le faire avant `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher maintenance tests automatisés Playwright`
- `python qa.py chercher maintenance test automation maintainability`
- `python qa.py chercher page object locators fragile automatisation de test`
- `python qa.py section CTAL-TAE-2.0-en 4.3 --max-caracteres 9000`
- `python qa.py section CTAL-TAE-2.0-en 3.1.5 --max-caracteres 7000`
- `python qa.py section CTAL-AT-2.0-en 5.3 --max-caracteres 6000`
- `python qa.py chercher playwright`
- `WebFetch {"url": "https://playwright.dev/docs/best-practices", "prompt": "Liste les bonnes pratiques Playwright qui réduisent la `
- `python qa.py section CT-FT-1.0-en 6.4 --max-caracteres 6000`
- `python qa.py section CTAL-TAE-2.0-en 8.1.1 --max-caracteres 6000`
- `python qa.py idee doublons --titre "Réduire la maintenance des tests UI automatisés" --resume "Page object, locators stables, indépendance des tests, données externalisées" --principe "Centraliser les`
