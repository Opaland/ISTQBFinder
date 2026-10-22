# T3-playwright — thomas

**Question** : Comment réduire le coût de maintenance de nos tests Playwright ?

**Tours** : 11 · **coût** : 0.144 $ · **confiance annoncée** : 75 · **verdict** : réussi · **citations** : 6/6 lues · **Web** : 1

## Réponse

**Sources retenues**
- **Base d'idées** : aucune idée capitalisée sur la maintenance, ni sur Playwright.
- **CTAL-TAE v2.0 EN** (2024-05-03), lu : §3.1.3, §3.1.4, §4.3.1.
- **CT-TAS v1.0 EN** (2024-05-03), lu : §5.1.1.
- **CTAL-AT v2.0 EN** (2026-04-17), lu : §5.3.
- **Web** : `chercher playwright` ne donne rien en local. J'ai donc lu la page officielle des bonnes pratiques [Web — Best Practices, playwright.dev/docs/best-practices, consulté le 2026-10-22]. Elle ne traite ni le Page Object Model ni les retries comme pratiques de maintenance.

Les syllabus donnent les principes de conception, et la doc Playwright donne la mise en œuvre. Ils se recoupent bien.

Hypothèse de contexte : application web, équipe agile, tests E2E écrits en TypeScript. Tu ne m'as pas donné ces éléments.

**Pistes par syllabus**
- **CTAL-TAE v2.0 — §3.1.4 Approches d'automatisation**
  - Le *capture/playback* est « hard to maintain, scale and evolve », et la capture dépend de la version du SUT (System Under Test, le système testé). Le *linear scripting* a le même défaut. [CTAL-TAE v2.0 EN, §3.1.4, p. 25-26]
  - Le *structured scripting* est « easy to maintain, scale, port, adapt and evolve », car la logique métier est séparée des scripts. [CTAL-TAE v2.0 EN, §3.1.4, p. 26]
  - Piste : si vos tests viennent de `codegen`, refactorez-les en briques réutilisables (parcours, composants).
- **CTAL-TAE v2.0 — §3.1.3 Couches du framework**
  - Les bibliothèques indépendantes du SUT (*core libraries*) sont séparées de celles qui en dépendent (*business logic*). Les premières se réutilisent d'un projet à l'autre. [CTAL-TAE v2.0 EN, §3.1.3, p. 25]
- **CTAL-TAE v2.0 — §4.3.1 Maintenabilité**
  - Principes *clean code* : nommage commun, structure logique, pas de valeurs en dur, méthodes courtes, logs, design patterns utiles. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
  - Données externalisées (*data-driven*) plutôt que codées en dur, constantes pour ce qui change peu. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
  - Analyseurs statiques, formateurs de code et stratégie de branches claire. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
  - *À creuser* : la suite de §4.3 (autres facteurs, mises à jour du SUT). Ma commande `section 4.3.2` a échoué, donc la suite n'est pas lue : voir `plan CTAL-TAE-2.0-en`.
- **CTAL-AT v2.0 — §5.3 Test smells**
  - Un *test smell* « suggests potential risks and increased maintenance costs ». Le syllabus ne décrit que les smells des tests manuels. [CTAL-AT v2.0 EN, §5.3, p. 45]
  - *Interdependent Tests* : rendre les tests autonomes et exécutables dans n'importe quel ordre. *Hidden Dependencies* : rendre les dépendances explicites. [CTAL-AT v2.0 EN, §5.3, p. 45]
  - *Oracle* : pas de logique de décision dans le test. [CTAL-AT v2.0 EN, §5.3, p. 45]
  - Ces principes se transposent aux tests automatisés (c'est une interprétation de ma part). Le syllabus renvoie à Aljedaani et al., 2021 pour les smells d'automatisation, une source que je n'ai pas lue.
- **CT-TAS v1.0 — §5.1.1 ROI**
  - Le « temps moyen de maintenance par script » et le « % de scripts en échec » font partie du calcul du ROI. [CT-TAS v1.0 EN, §5.1.1, p. 38]
  - Piste : mesurer ces deux valeurs chez vous pour cibler les tests les plus coûteux.

**Côté Playwright** (Web, doc officielle)
- Locators orientés utilisateur (`getByRole`) plutôt que CSS ou XPath, qui cassent quand le DOM change.
- Assertions *web-first* (`toBeVisible()`) qui attendent et réessayent, ce qui évite les `sleep`.
- Tests isolés (stockage, cookies et données propres à chaque test), connexion faite une seule fois dans un *setup project*.
- Appels tiers simulés avec `page.route`, et données maîtrisées sur un environnement de test stable.
- Trace viewer sur la CI pour diagnostiquer vite, et `tsc --noEmit` avec un linter sur la CI.

**Ce que j'en retiens** (interprétation)
- Le coût de maintenance vient surtout de l'**architecture** (scripts linéaires, valeurs en dur, tests dépendants), plus que de l'outil.
- Les bonnes pratiques de Playwright sont l'application concrète des principes de la TAE : locators stables pour la couche d'accès au SUT, setup project pour l'indépendance des tests.

**Par quoi je commencerais**
1. Remplacer les locators CSS/XPath fragiles par des locators par rôle, et les attentes fixes par des assertions web-first. Impact fort, effort faible à moyen.
2. Rendre les tests indépendants (données et état propres à chaque test, connexion en setup). Impact fort, effort moyen.
3. Structurer les tests (briques ou Page Objects, données externalisées) et mesurer le temps de maintenance par script. Impact fort, effort moyen à fort.

**Où creuser ensuite**
- `section CTAL-TAE-2.0-en 3.1.5` : design patterns, facades, inheritance.
- `section CTAL-TAE-2.0-en 4.3` : le reste de la section.
- `section CT-TAS-1.0-en 5.1` : ROI et mesures.

**Confiance : 75/100** (élevée). Calcul : base 91 × 0,6 = 55 ; 4 passages lus +20 ; 3 syllabus concordants +20 ; Web −10 ; raisonnement sans source −10.

**Questions à choix**
1. Quelle est la cause dominante de votre maintenance ?
   1. Tests instables (flaky)
   2. Tests cassés à chaque évolution de l'UI
   3. Code dupliqué et difficile à relire
2. Que veux-tu faire ensuite ?
   1. Approfondir TAE §3.1.5 et §4.3
   2. Comparer *structured scripting*, Page Object et BDD
   3. Chercher la gestion des tests instables (flaky) dans les syllabus

**À capitaliser ?** Un doublon vérifié : aucune idée similaire. Thèmes suggérés : `maintenance-automatisation`, `strategie-automatisation`. Je n'enregistre rien. Les extraits sont copiés des passages lus.

```json
{
  "titre": "Réduire la maintenance des tests E2E automatisés : structurer, externaliser les données, isoler",
  "resume": "Le coût de maintenance dépend de l'architecture : scripts structurés plutôt que capturés, données externalisées, tests indépendants. Se transpose à Playwright (locators par rôle, assertions web-first, setup project).",
  "principe": "Séparer la logique métier des scripts, éviter les valeurs en dur, rendre les tests autonomes, mesurer le temps de maintenance par script.",
  "theme": "maintenance-automatisation",
  "references": [
    {"document": "CTAL-TAE-2.0-en", "page": 26, "extrait": "Easy to maintain, scale, port, adapt and evolve"},
    {"document": "CTAL-TAE-2.0-en", "page": 32, "extrait": "Hardcoding is the process of embedding values in the software without the ability to change them directly."},
    {"document": "CTAL-AT-2.0-en", "page": 45, "extrait": "Make tests independent, self-contained, and executable in any order."}
  ]
}
```

Les champs sont ceux que je suppose pour `idee modele`, que je n'ai pas lancé : vérifie-les avant `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher maintenance automatisation tests 2>&1 | head -40; python qa.py idee chercher Playwright 2>&1 | head -20`
- `python qa.py chercher maintenance scripts de test automatisés 2>&1 | head -50; python qa.py chercher test automation maintainability 2>&1 | head -50`
- `python qa.py section CTAL-TAE-2.0-en 4.3 --max-caracteres 9000 2>&1; python qa.py chercher playwright 2>&1 | head -15`
- `python qa.py lire 4220 --contexte 1 --max-caracteres 5000 2>&1; python qa.py lire 1580 --contexte 1 --max-caracteres 4000 2>&1; python qa.py lire 3602 --contexte 1 --max-caracteres 3500 2>&1`
- `WebFetch {"url": "https://playwright.dev/docs/best-practices", "prompt": "List the best practices that reduce test maintenance (l`
- `python qa.py section CTAL-TAE-2.0-en 4.3.2 --max-caracteres 6000 2>&1; python qa.py lire 4220 --contexte 1 2>&1 | head -60`
- `python qa.py lire 1580 --contexte 1 2>&1 | head -50; python qa.py lire 3656 --contexte 1 2>&1 | head -40`
- `python qa.py confiance --help 2>&1 | head -20; python qa.py idee doublons --titre "Réduire la maintenance des tests E2E automatisés" --resume "Approche structurée, données externalisées, indépendance `
- `python qa.py confiance --base 91 --lus 4 --concordants 3 --web 1 --raisonnement 1 2>&1`
