# T3-playwright — thomas

**Question** : Comment réduire le coût de maintenance de nos tests Playwright ?

**Tours** : 12 · **coût** : 0.158 $ · **confiance annoncée** : 68 · **verdict** : réussi · **citations** : 7/7 lues · **Web** : 1

## Réponse

# Réduire le coût de maintenance de vos tests Playwright

## Sources retenues
- **CTAL-TAE v2.0 EN** (2024-05-03) : §3.1.5, §4.3.1 et §8.1.2, lus. La version FR existe (§4.3, §8.1.2) mais je n'ai cité que l'EN.
- **CT-TAS v1.0 EN** (2024-05-03) : §1.1.2, §1.1.3 et §5.1.1, lus.
- **Base d'idées** : rien de capitalisé sur le sujet.
- **Playwright** : `chercher playwright` ne trouve aucun passage, ce qui est normal puisque l'ISTQB ne cite pas d'outil. J'ai donc lu la documentation officielle.

**Hypothèse de contexte** : application web, équipe qui exécute les tests en CI, Playwright déjà en place avec une suite qui vieillit. Je n'ai pas votre langage, la taille de la suite ni son taux de tests instables.

## Pistes par syllabus

**CTAL-TAE v2.0 — §4.3.1 Maintenabilité de la solution d'automatisation**
- Appliquer les principes du *clean code* : nommage commun, structure de projet logique, pas de valeurs codées en dur, méthodes courtes, journalisation. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
- Sortir les données des scripts (*data-driven*) et utiliser des constantes. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
- Ajouter des analyseurs statiques et une stratégie de branches convenue. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]

**CTAL-TAE v2.0 — §3.1.5 Design patterns**
- *Page object model* : quand l'application change, on ne corrige le locator qu'à un seul endroit. [CTAL-TAE v2.0 EN, §3.1.5, p. 28]
- *Flow model* : une façade supplémentaire au-dessus des page objects réunit les actions utilisateur réutilisables. [CTAL-TAE v2.0 EN, §3.1.5, p. 28]

**CTAL-TAE v2.0 — §8.1.2 Améliorer une solution déployée**
- Consolider les étapes qui se recoupent dans une bibliothèque de fonctions paramétrées. [CTAL-TAE v2.0 EN, §8.1.2, p. 49]
- Réviser les mécanismes d'attente. Les attentes fixes sont décrites comme une cause racine fréquente de défauts d'automatisation. L'attente dynamique est préférable, avec un délai maximal. [CTAL-TAE v2.0 EN, §8.1.2, p. 49]
- Mettre en place un processus de reprise sur échec, pour que la suite continue avec le test suivant. [CTAL-TAE v2.0 EN, §8.1.2, p. 49]
- Adopter des méthodes de vérification standard. [CTAL-TAE v2.0 EN, §8.1.2, p. 50]
- Appliquer la nouvelle technique de script aux tests qui coûtent le plus cher à maintenir, pas à toute la suite. [CTAL-TAE v2.0 EN, §8.1.2, p. 49]

**CT-TAS v1.0 — §1.1.2 et §5.1.1 (angle stratégique)**
- Facteurs de succès : dépannage facile, tests à jour, tests retirés quand il le faut, gestion efficace des exceptions. [CT-TAS v1.0 EN, §1.1.2, p. 17]
- ROI : le temps moyen de maintenance d'un script et le pourcentage de scripts en échec figurent dans l'investissement. [CT-TAS v1.0 EN, §5.1.1, p. 38]
- Appliquer la pyramide des tests réduit le temps d'exécution et améliore le ROI. [CT-TAS v1.0 EN, §5.1.1, p. 39]

**Web : documentation officielle Playwright** (consultée le 2026-10-23, [playwright.dev/docs/best-practices](https://playwright.dev/docs/best-practices))
- Préférer des locators orientés utilisateur comme `getByRole` aux sélecteurs CSS ou XPath, qui cassent quand le DOM change.
- Utiliser les assertions *web-first*, qui réessaient jusqu'à ce que la condition soit vraie. L'auto-attente remplace les attentes fixes.
- Garder chaque test indépendant. Réutiliser l'état connecté avec un projet de setup pour ne se connecter qu'une fois.
- Simuler les tiers avec `page.route` et tester le comportement visible, pas l'implémentation.
- En CI, utiliser le trace viewer avec `on-first-retry`, et ajouter le sharding et le mode parallèle.
- La page ne couvre pas les page objects ni les fixtures en détail.

## Ce que j'en retiens (interprétation)
- L'ISTQB donne les principes de conception : abstraction des locators, données externalisées, attentes dynamiques. Playwright fournit déjà une partie de la réponse de façon native (auto-attente, locators par rôle).
- Corrigez d'abord ce qui casse le plus souvent, avant toute refonte : l'ISTQB recommande de cibler les tests les plus coûteux à maintenir.
- Sans mesure, vous ne saurez pas si le coût baisse. L'ISTQB place le temps de maintenance dans le calcul du ROI, mais je n'ai pas lu d'indicateur prêt à l'emploi sur la maintenance elle-même.

## Par quoi je commencerais
| Piste | Impact | Effort |
|---|---|---|
| Supprimer les `waitForTimeout` au profit des assertions web-first et de l'auto-attente | Fort | Faible |
| Migrer les sélecteurs CSS/XPath vers `getByRole` ou `getByTestId`, en commençant par les tests qui cassent le plus | Fort | Moyen |
| Centraliser locators et actions (page objects ou flow model) et sortir les données des scripts | Fort | Moyen à fort |
| Mesurer le temps de maintenance et le taux d'échec par script, puis retirer les tests obsolètes | Moyen | Faible |

## Où creuser ensuite
- `section CTAL-TAE-2.0-en 3.1` : architecture, approches de script et patterns.
- `page CTAL-TAE-2.0-en 50-51` : suite de §8.1.2, avec TAA, TAF, setup/teardown et documentation. Je ne l'ai pas lue.
- `section CT-TAS-1.0-en 5.2` : métriques d'automatisation.

**Confiance : 68/100 (moyenne)** — base 96 × 0,6 = 58 ; 6 passages lus +20 ; 2 syllabus concordants +10 ; Web −10 ; raisonnement sans source −10. La bibliothèque ne contient rien de spécifique à Playwright : cette partie vient du Web et d'une seule page de la documentation officielle.

## Questions à choix
**1. Quel est votre symptôme principal ?**
1. Tests instables (échecs aléatoires)
2. Tests cassés à chaque évolution de l'interface
3. Suite trop lente ou trop volumineuse

**2. Quelle suite voulez-vous ?**
1. Approfondir la conception (page objects, flow model, fixtures)
2. Définir des indicateurs de maintenance (CT-TAS §5.2)
3. Capitaliser les idées ci-dessous

## À capitaliser ?
Aucun doublon trouvé (`idee doublons`). Les références ci-dessous viennent de passages lus. Le thème `maintenance-automatisation` existe.

```json
{
  "titre": "Réduire la maintenance d'une suite Playwright par la conception",
  "resume": "Abstraire les locators, remplacer les attentes fixes par des attentes dynamiques, externaliser les données et cibler d'abord les tests les plus coûteux.",
  "principe": "La maintenabilité d'une suite automatisée vient de principes de conception (page object, flow model, data-driven, attentes dynamiques). On les applique en priorité aux tests qui coûtent le plus cher à maintenir.",
  "theme": "maintenance-automatisation",
  "references": [
    {"doc": "CTAL-TAE-2.0-en", "page": 28, "extrait": "Whenever the SUT’s structure changes, the TAE will have to make updates in only one place, the locator inside a page model, instead of updating the locators in each test case."},
    {"doc": "CTAL-TAE-2.0-en", "page": 49, "extrait": "Hard coded waits (i.e., wait a certain number of milliseconds) which can be a root cause for many test automation defects given the unpredictability of software response times."},
    {"doc": "CTAL-TAE-2.0-en", "page": 32, "extrait": "It can be avoided by using data -driven testing, so the test data comes from a common source that can be maintained more easily."}
  ]
}
```

Je n'ai pas vérifié les noms de champs avec `idee modele`. La conversation principale devra le faire avant `idee ajouter`. Il faudra aussi vérifier que l'extrait de la p. 32 correspond mot pour mot à la page : l'espace dans « data -driven » vient de l'extraction.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher maintenance automatisation tests 2>&1 | head -40; python qa.py idee chercher Playwright 2>&1 | head -20`
- `for q in "test automation maintenance" "maintenabilité automatisation des tests" "page object locators fragile" "flaky tests" "test automation architecture layers" "test automation solution design"; d`
- `python qa.py chercher "test automation maintenance" 2>&1 | head -40`
- `python qa.py chercher "playwright" 2>&1 | head -15; python qa.py chercher "maintenabilité automatisation des tests" 2>&1 | head -30`
- `python qa.py section CTAL-TAE-2.0-en 4.3 --max-caracteres 9000`
- `python qa.py section CTAL-TAE-2.0-en 8.1.2 --max-caracteres 6000; python qa.py section CT-TAS-1.0-en 5.1 --max-caracteres 5000`
- `WebFetch {"url": "https://playwright.dev/docs/best-practices", "prompt": "List the best practices that reduce flakiness and maint`
- `python qa.py section CTAL-TAE-2.0-en 3.1.5 --max-caracteres 4500; python qa.py lire 3602 --contexte 1 --max-caracteres 3500`
- `python qa.py idee doublons --titre "Réduire le coût de maintenance des tests Playwright" --resume "Locators robustes, attentes dynamiques, patterns, KPI de maintenance" --principe "Réduire la maintena`
- `python qa.py confiance --base 96 --lus 6 --concordants 2 --web 1 --raisonnement 1 2>&1; python qa.py themes 2>&1 | grep -i -E "maintenance|automatis" | head`
