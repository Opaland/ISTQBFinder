# Exemples de conversations

Chaque exemple est tiré d'une **sortie réelle versionnée**, citée sous son titre :

- réponses des agents : essais de bout en bout du 2026-10-22
  (`python scripts/essais_agents.py`, rapport : [essais-reponses.md](essais-reponses.md)),
  fichiers `eval/essais-resultats/2026-10-22/<essai>.md` ;
- commandes de capitalisation et de suivi (§3 à §5) : rejouées dans une racine temporaire
  par `python scripts/rejouer_exemples.py`, sortie brute dans
  `eval/sorties-cli/2026-10-22/exemples-cli.md`.

Les extraits sont **raccourcis mais non retouchés** : « […] » marque une coupure, rien
n'est reformulé. `tests/test_exemples.py` vérifie l'accord de chaque extrait avec le fichier
cité (chiffres, citations, commandes et sorties). Les numéros de passage (`#1762`) changent
à chaque réindexation : ils servent à lire, jamais à citer. On cite document, version,
section, page.

---

## 1. Question de mise en place (cas M) — Thomas

Source : `eval/essais-resultats/2026-10-22/M1-rbt-agile.md` (`claude -p --agent thomas`,
11 tours, 0,168 $, 5/5 citations lues : le harnais a vérifié que chaque citation renvoie à
une page lue pendant la conversation).

> **Utilisateur** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

Commandes exécutées par Thomas (extrait) :

```text
$ python qa.py idee chercher risk-based testing agile
$ python qa.py chercher risk-based testing agile
$ python qa.py chercher analyse des risques itération agile
$ python qa.py section CTFL-AT-2014-en 3.2.1 --max-caracteres 6000
$ python qa.py section CTAL-AT-2.0-en 3.1.1 --max-caracteres 7000
$ python qa.py confiance --base 85 --lus 6 --concordants 3 --raisonnement 1
```

> **Thomas** : **Sources retenues**
> - CTAL-AT v2.0 EN (2026-04-17), §3.1.1 : lu.
> - CTFL-AT 2014 EN, §3.2.1 : lu. Ce syllabus est en retrait, remplacé par CTAL-AT.
> - […]
> - Je n'ai pas fait de recherche Web, parce que ta question porte sur ce que propose l'ISTQB.
>
> L'ISTQB n'a pas de chapitre unique qui "intègre le RBT en agile". La démarche se reconstitue à partir de ces syllabus : on analyse les risques avec toute l'équipe lors des planifications de release et d'itération, on dimensionne l'effort de test selon le niveau de risque, puis on réévalue à chaque itération.
>
> Hypothèse de contexte : équipe Scrum ou équivalente, sans contrainte réglementaire forte. Je n'ai pas de contexte projet.
>
> **Méthode pas à pas**
> 1. **Planification de release : survol des risques qualité.**
>    - Les représentants métier donnent une vue d'ensemble des risques. Toute l'équipe, testeurs compris, aide à les identifier et à les évaluer. [CTFL-AT 2014 EN, §3.2.1, p. 32]
>    - […]
> 2. **Planification d'itération : séance de risk-storming.**
>    - Le testeur anime la séance avec les représentants métier et les développeurs, pour identifier les risques et prioriser les activités de test. [CTAL-AT v2.0 EN, §3.1.1, p. 24-25]
>    - […]
> 3. **Évaluer chaque risque.**
>    - […]
>    - Les facteurs d'évaluation sont la fréquence d'usage, la criticité métier, le dommage financier ou de réputation, la qualité de la base de test et les exigences légales ou de sécurité. [CTAL-TA v4.0 EN, §2.1, p. 25]
> 4. **Piloter l'ordre et l'effort sur le task board.** Les tâches à risque élevé démarrent plus tôt et reçoivent plus de tests, celles à risque faible démarrent plus tard avec moins de tests. [CTFL-AT 2014 EN, §3.2.1, p. 32]
> 5. […]
> 6. **Réévaluer à chaque itération.**
>    - Dans un cycle itératif, le suivi des risques se fait à une fréquence choisie par l'équipe, probablement une fois par itération. Le testeur met à jour le registre des risques. [CTAL-TA v4.0 EN, §2.1, p. 25]
>    - L'analyse des risques est continue et itérative, pas une activité de début de projet. [CTAL-TM v3.0 FR, §1.3.6, p. 34]
> 7. **Mesurer en rétrospective.**
>    - Questions à poser : les parties prenantes étaient-elles impliquées ? Les défauts critiques sont-ils sortis tôt ? Les tests ignorés étaient-ils moins risqués que ceux exécutés ? [CTAL-TM v3.0 FR, §1.3.6, p. 34]
>
> **Exemple de mise en œuvre** (fictif, interprétation)
> Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines :
> - […]
> - À chaque planification, 20 minutes de risk-storming sur les stories retenues (étape 2). Chaque story reçoit une note impact × probabilité de 1 à 3, écrite sur le ticket (étape 3).
> - […]
>
> **Adaptation par domaine**
>
> | Domaine | Ce qui change | Où lire |
> |---|---|---|
> | Santé / réglementé | Plus de traçabilité et de preuves d'audit : accent sur les quadrants 2 et 4. [CTAL-AT v2.0 EN, §3.1.2, p. 25] Pas de syllabus santé dans la bibliothèque (IEC 62304 absent) : Web nécessaire pour la norme. | CTAL-AT §3.1.2 |
> | Web | Aucun syllabus web dédié : les principes ci-dessus se transposent. | CTAL-AT §3.1 |
> | Embarqué | Non lu pour cette question. | CTEL-TM §8.3.3, CT-AuT |
> | […] | | |
>
> **Par quoi je commencerais**
> 1. Risk-storming de 20 minutes à la planification d'itération : impact fort, effort faible.
> 2. […]
>
> **Confiance : 81/100 (élevée)** — base 85 × 0,6 = 51 ; 6 passages lus +20 ; 3 syllabus courants concordants +20 ; raisonnement sans source −10 (l'exemple et la grille 1-3). […]
>
> **Questions à choix**
> 1. Quel est ton domaine ?
>    1. Web / SaaS
>    2. Réglementé (santé, finance)
>    3. Embarqué, mobile ou API
> 2. […]
>
> **À capitaliser ?**
> Aucun doublon trouvé (`idee doublons` : « Aucune idée similaire »).
> […]

Défaut relevé : la phrase sur le suivi des risques « une fois par itération » est, dans le
PDF, juste avant le titre « 2.1 Risk Analysis » (introduction du chapitre 2, p. 25) ; l'index
range ce passage sous §2.1, d'où la citation `§2.1`. La liste des facteurs d'évaluation est
bien au §2.1.

Avant le correctif de #91, la même question classée « connaissance » donnait des pistes
par syllabus sans méthode ni exemple
(`eval/essais-resultats/2026-10-22/M1-rbt-agile-avant-correctif.md`).

---

## 2. Recherche avec Web justifié (cas B) — Thomas

Source : `eval/essais-resultats/2026-10-22/T3-playwright.md` (11 tours, 0,144 $, 6/6
citations lues, 1 page Web).

> **Utilisateur** : Comment réduire le coût de maintenance de nos tests Playwright ?

```text
$ python qa.py idee chercher Playwright
$ python qa.py chercher test automation maintainability
$ python qa.py section CTAL-TAE-2.0-en 4.3 --max-caracteres 9000
$ python qa.py chercher playwright
```

> **Thomas** : **Sources retenues**
> - **Base d'idées** : aucune idée capitalisée sur la maintenance, ni sur Playwright.
> - **CTAL-TAE v2.0 EN** (2024-05-03), lu : §3.1.3, §3.1.4, §4.3.1.
> - […]
> - **Web** : `chercher playwright` ne donne rien en local. J'ai donc lu la page officielle des bonnes pratiques [Web — Best Practices, playwright.dev/docs/best-practices, consulté le 2026-10-22]. […]
>
> **Pistes par syllabus**
> - **CTAL-TAE v2.0 — §3.1.4 Approches d'automatisation**
>   - Le *structured scripting* est « easy to maintain, scale, port, adapt and evolve », car la logique métier est séparée des scripts. [CTAL-TAE v2.0 EN, §3.1.4, p. 26]
> - **CTAL-TAE v2.0 — §3.1.3 Couches du framework**
>   - Les bibliothèques indépendantes du SUT (*core libraries*) sont séparées de celles qui en dépendent (*business logic*). Les premières se réutilisent d'un projet à l'autre. [CTAL-TAE v2.0 EN, §3.1.3, p. 25]
> - **CTAL-TAE v2.0 — §4.3.1 Maintenabilité**
>   - Données externalisées (*data-driven*) plutôt que codées en dur, constantes pour ce qui change peu. [CTAL-TAE v2.0 EN, §4.3.1, p. 32]
>   - […]
>
> **Côté Playwright** (Web, doc officielle)
> - Locators orientés utilisateur (`getByRole`) plutôt que CSS ou XPath, qui cassent quand le DOM change.
> - Assertions *web-first* (`toBeVisible()`) qui attendent et réessayent, ce qui évite les `sleep`.
> - […]
>
> **Par quoi je commencerais**
> 1. Remplacer les locators CSS/XPath fragiles par des locators par rôle, et les attentes fixes par des assertions web-first. Impact fort, effort faible à moyen.
> 2. […]
>
> **Confiance : 75/100** (élevée). Calcul : base 91 × 0,6 = 55 ; 4 passages lus +20 ; 3 syllabus concordants +20 ; Web −10 ; raisonnement sans source −10.

---

## 3. Capitalisation contrôlée (cas C) — CLI

Source : `eval/sorties-cli/2026-10-22/exemples-cli.md` (racine temporaire, base vide au
départ).

> **Utilisateur** : Oui, enregistre l'idée sur la matrice probabilité × impact.

```text
$ python qa.py section CTAL-TM-3.0-fr 1.3.3
…
$ python qa.py theme proposer "prioriser les tests selon probabilité et impact des risques"
  rbt                        Test management › Risk-Based Testing  (score 0.447)
  priorisation               Test management › Priorisation des tests  (score 0.365)
…
$ python qa.py idee doublons --titre "Matrice probabilité × impact pour prioriser les tests" --resume "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test." --theme rbt
Aucune idée similaire.
$ python qa.py idee ajouter <<'JSON'
<le JSON ci-dessous>
JSON
Idée créée : QA-20261022-484e
```

avec le JSON (passé sur l'entrée standard, sans fichier temporaire) :

```json
{"titre": "Matrice probabilité × impact pour prioriser les tests",
 "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test.",
 "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.",
 "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de risque, allouer profondeur et ordre de test.",
 "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee",
 "provenance": "Exemple rejoué par scripts/rejouer_exemples.py",
 "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "30", "section": "1.3.3",
                 "extrait": "pour chaque élément de risque, de la probabilité du risque et de l'impact du risque"}]}
```

L'identifiant `QA-AAAAMMJJ-xxxx` (date de création + suffixe aléatoire) change à chaque
exécution. Ce que l'outil refuse (même source, une variante du JSON par ligne) :

```text
référence vers la page 300 :
Erreur : Page 300 inexistante dans CTAL-TM-3.0-fr (95 pages).
extrait reformulé (impact et probabilité permutés) :
Erreur : L'extrait cité n'apparaît pas mot pour mot aux pages 30 de CTAL-TM-3.0-fr : recopier une suite continue du passage lu (`lire` / `page`), sans reformuler ni couper au milieu.
même idée, titre reformulé :
REFUSÉ — Doublon probable : compléter l'idée existante (`idee modifier`) ou la lier (`idee lier`) plutôt que d'en créer une nouvelle.
  DOUBLON PROBABLE QA-20261022-484e « Matrice probabilité × impact pour prioriser les tests » (similarité 1.0, a_explorer)
$ python qa.py idee statut QA-20261022-484e validee
Erreur : Le statut « validee » exige un motif d'au moins 10 caractères (--motif) : sur quoi repose la décision ?
$ python qa.py idee statut QA-20261022-484e experimentee --motif "appliquée sur une release"
Erreur : « expérimentée » exige au moins un retour d'expérience (`idee retour`).
```

---

## 4. Retrouver et faire évoluer (cas C/D) — CLI

Source : `eval/sorties-cli/2026-10-22/exemples-cli.md` (suite du §3, même racine
temporaire).

> **Utilisateur** : Retrouve les idées que nous avons déjà capitalisées sur la priorisation par les risques.

```text
$ python qa.py idee chercher probabilité impact
QA-20261022-484e  [a_explorer/documentee] Matrice probabilité × impact pour prioriser les tests (rbt)
$ python qa.py idee lister --theme rbt
QA-20261022-484e  rbt                    a_explorer   documentee Matrice probabilité × impact pour prioriser les tests
```

> **Utilisateur** : On l'a testée sur une release, ça a marché.

Le contexte reste anonyme (dépôt public) : ni client, ni projet, ni personne, ni montant.

```text
$ python qa.py idee retour QA-20261022-484e --contexte "Release web, équipe produit de 6 personnes" --resultat "2 défauts critiques trouvés avant la recette" --enseignement "atelier d'1 h suffisant"
QA-20261022-484e : retour d'expérience enregistré (1 au total)
$ python qa.py idee statut QA-20261022-484e experimentee --motif "appliquée sur une release"
QA-20261022-484e : a_explorer → experimentee
```

---

## 5. Exploration d'un thème et lacunes (cas D) — CLI et Thomas

> **Utilisateur** : Identifie les thèmes QA sur lesquels notre base est encore pauvre.

Sortie de `couverture` après le §4 (source : `eval/sorties-cli/2026-10-22/exemples-cli.md`) :

```text
$ python qa.py couverture
thème                                    idées passages  état
Stratégie et gouvernance QA                  0      624  vide
Test management                              0      781  vide
  Risk-Based Testing                         1      373  pauvre
…
  Priorisation des tests                     1       82  pauvre
…
Thèmes pauvres en idées mais documentés dans les syllabus (pistes d'exploration) : exigences (1901 passages), organisation (1748 passages), metriques (1164 passages), agile (1132 passages), conception (1118 passages)
```

Réponse de Thomas sur la base vide du dépôt (source :
`eval/essais-resultats/2026-10-22/T6-lacunes.md`, 4 tours, 0,08 $, 0/0 citations lues) :

> **Thomas** : Ta base d'idées est vide : `idee lister` répond « Aucune idée » et les 40 thèmes de la taxonomie affichent 0 idée. Elle est donc pauvre partout. Ce qui varie, c'est la quantité de matière que les syllabus offrent déjà pour la remplir.
>
> **Thèmes à remplir en premier** (beaucoup de matière dans les syllabus, aucune idée capitalisée)
> - Exigences et critères d'acceptation : 1 901 passages.
> - […]
>
> **Thèmes pauvres en idées ET en syllabus** (angles morts probables)
> - Priorisation des tests : 82 passages.
> - Shift-left et shift-right (thème parent) : 83 passages.
> - […]
>
> **Par quoi je commencerais** (interprétation)
> 1. **Métriques et reporting**, ou **Risk-Based Testing** (373 passages) : impact fort pour un Test Manager, effort faible. CTAL-TM v3.0 existe en FR et en EN.
> 2. […]
>
> **Confiance : 70/100** (correcte). Les chiffres viennent directement de l'outil (inventaire, thèmes, liste vide). Je n'ai lu aucun passage, donc je n'ai pas vérifié la qualité du contenu derrière les nombres de passages. […]

---

## 6. Comparaison de techniques (cas B) — Thomas

Source : `eval/essais-resultats/2026-10-22/T5-priorisation.md` (6 tours, 0,119 $, 3/3
citations lues).

> **Utilisateur** : Compare les techniques de priorisation des tests décrites par l'ISTQB.

> **Thomas** : Les syllabus ISTQB décrivent trois stratégies de priorisation au niveau Foundation. Le niveau Advanced ajoute des variantes de parcours (depth-first et breadth-first) et la sélection des tests de régression. Je n'ai pas fait de recherche Web, la question portant sur l'ISTQB.
>
> […]
>
> **Pistes par syllabus**
> - **CTFL v4.0.1, §5.1.5 Test Case Prioritization**
>   - Trois stratégies : basée sur les risques, basée sur la couverture (avec la variante « couverture additionnelle ») et basée sur les exigences (priorités fixées par les parties prenantes). [CTFL-4.0.1 EN, §5.1.5, p. 50]
> - **CTAL-TM v3.0, §1.3.4 Réduction des risques qualité**
>   - La priorisation à l'implémentation suit les niveaux de risque. *Depth-first* : ordre strictement décroissant du risque couvert, pour traiter les risques majeurs au plus tôt. *Breadth-first* : au moins un test par risque en priorité haute, pour avoir une vue globale de la qualité le plus tôt possible. [CTAL-TM-3.0 EN, §1.3.4, p. 31]
> - […]
>
> | Technique | Principe | Quand l'utiliser | Source |
> |---|---|---|---|
> | Basée sur les risques | Les tests couvrant les risques les plus élevés passent d'abord | Temps limité, enjeux métier ou sécurité | CTFL §5.1.5 ; CTAL-TM §1.3.4 |
> | Depth-first / breadth-first | Descente par niveau de risque, ou un test par risque d'abord | Depth-first : risques majeurs à traiter tôt. Breadth-first : vue globale rapide | CTAL-TM §1.3.4 |
> | […] | | | |
>
> **Confiance : 83/100 (élevée)** — base 88 × 0,6 = 53 ; 3 passages lus +20 ; 2 syllabus concordants +10 → 83. La section TA §2.2.1 n'est lue qu'en partie.

---

## 7. Vérification d'une démarche — Sylvie

Source : `eval/essais-resultats/2026-10-22/S1-rbt.md` (6 tours, 0,117 $, 6/6 citations
lues).

> **Utilisateur** : J'ai vu qu'on pouvait mettre en place une stratégie de test basée sur les risques. Je pense faire ceci : un atelier en début de release avec le PO pour lister les fonctionnalités risquées, on teste ces fonctionnalités en premier et plus en profondeur, et on ne fait que du smoke test sur le reste. Est-ce que je suis aligné ISTQB ? Quel est le niveau de maturité de ma démarche ?

> **Sylvie** : **Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.**
>
> Ta démarche suit l'esprit du test basé sur les risques (RBT), mais elle est incomplète. Trois étapes sont à compléter : les parties prenantes de l'atelier, l'évaluation du niveau de risque, et le suivi des risques pendant la release. Le « smoke test seulement » sur le reste ne correspond pas à ce que décrit le syllabus. Rien n'est encore en place, donc le niveau est plafonné à 1.
>
> […]
>
> | Pratique | Statut | Verdict | Ce que dit l'ISTQB | Source |
> |---|---|---|---|---|
> | P2 Tester d'abord le risqué | Intention | Aligné | Pour les risques élevés, les tests « doivent commencer tôt ». À l'exécution, la priorisation suit les niveaux de risque, ce qui assure une couverture précoce des zones critiques. Une exécution « profondeur d'abord » convient quand il faut atténuer les risques les plus élevés au plus vite. | [CTAL-TM v3.0 FR, §1.3, p. 29] ; [§1.3.4, pp. 32-33] |
> | […] | | | | |
>
> ## Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné
>
> - **Pourquoi 1 :** toutes les pratiques sont des intentions. Seules les pratiques en place comptent (grille du dépôt).
> - […]
>
> ## Confiance : 78/100
>
> - J'ai lu §1.3 à §1.3.4 et §1.3.6 de CTAL-TM v3.0 FR, un syllabus courant et explicite sur le sujet.
> - […]

---

## 8. Mise en place du shift left (cas M) — Thomas

Source : `eval/essais-resultats/2026-10-22/M7-shift-left.md` (8 tours, 0,14 $, 9/9
citations lues).

> **Utilisateur** : Je veux mettre en place une démarche shift left testing, comment faire ? Qu'est-ce que cela impose ?

```text
$ python qa.py idee chercher shift left testing
$ python qa.py section CTFL-4.0.1-en 2.1.5 --max-caracteres 3500
$ python qa.py section CTAL-AT-2.0-en 4.1.3 --max-caracteres 2500
$ python qa.py section CT-TAS-1.0-en 3.1.3 --max-caracteres 5000
```

> **Thomas** : […]
>
> ## Ce que l'ISTQB entend par shift left
> Le shift left est le principe du « test précoce » (early testing). On teste plus tôt dans le cycle de vie (SDLC), sans négliger les tests plus tardifs. [CTFL v4.0.1 EN, §2.1.5, p. 27]
>
> ## Méthode pas à pas
> 1. **Obtenir l'adhésion des parties prenantes et accepter le surcoût initial.**
>    - […]
>    - Le shift left peut coûter de la formation, de l'effort et de l'argent au début, mais il est censé faire économiser ensuite. Les parties prenantes doivent y adhérer. [CTFL v4.0.1 EN, §2.1.5, p. 27]
> 2. **Améliorer la base de test (test basis) avant le code.**
>    - […]
>    - L'example mapping est une conversation structurée. Elle produit règles, exemples (qui deviennent des cas de test) et questions. Beaucoup de questions ou de règles signalent une story à découper. [CTAL-AT v2.0 EN, §4.1.3, p. 33]
> 3. […]
> 6. **Rééquilibrer l'automatisation vers le bas de la pyramide.**
>    - […]
>    - Les tests de contrat permettent de trouver plus tôt les causes racines. [CT-TAS v1.0 EN, §3.1.3, p. 25]
> 7. **Tester le non-fonctionnel dès le niveau composant, puis compléter par du shift right.**
>    - […]
>    - Le shift right déplace des tests après la livraison, avec observabilité, canary releases et dark launches. Il complète le shift left et ne le remplace pas. [CT-TAS v1.0 EN, §3.1.3, p. 25]
>
> ## Ce que le shift left impose
> - Accepter un surcoût au départ et obtenir l'adhésion des parties prenantes. [CTFL v4.0.1 EN, §2.1.5, p. 27]
> - Faire travailler ensemble testeurs, PO et développeurs dès l'affinage du backlog.
> - Mettre en place un pipeline CI avec analyse statique.
> - Garder les tests tardifs et y ajouter le shift right, sans les supprimer.
>
> ## Par quoi je commencerais
> 1. **Impact fort, effort faible** : revue des specs et example mapping en affinage (étape 2).
> 2. […]
>
> **Confiance : 90/100 (élevée)** : base 100, 6 passages lus, 3 syllabus concordants (+20), raisonnement sans source pour l'exemple et l'adaptation par domaine (−10). […]

---

## 9. Aide à la rédaction : critères d'acceptation en Gherkin — Thomas

Source : `eval/essais-resultats/2026-10-22/T7-gherkin.md` (11 tours, 0,161 $, 9/9
citations lues).

> **Utilisateur** : Je veux rédiger mes critères d'acceptation en Gherkin, j'ai besoin d'aide.

```text
$ python qa.py chercher Gherkin
$ python qa.py section CT-AcT-2019-en 2.2.2 --max-caracteres 6000
$ python qa.py section CT-AcT-2019-en 2.1 --max-caracteres 5000
$ python qa.py confiance --base 100 --lus 5 --concordants 3 --raisonnement 1
```

> **Thomas** : […]
>
> Les syllabus voient Gherkin comme un format pour écrire des critères d'acceptation sous forme de tests. Ils donnent surtout des règles de rédaction : précis, déclaratifs, atomiques.
>
> **Pistes par syllabus**
> - **CT-AcT v2019 — §2.1 Writing Acceptance Criteria**
>   - Un bon critère est précis, mesurable et concis. Le testeur doit pouvoir dire si l'objet testé le respecte. [CT-AcT v2019 EN, §2.1, p. 16]
>   - […]
> - **CT-AcT v2019 — §2.2.2 Gherkin**
>   - Le motif est Given (situation), When (action sur le système), Then (résultat attendu). [CT-AcT v2019 EN, §2.2.2, pp. 16-17]
>   - Les scénarios Gherkin ne citent pas d'éléments d'interface mais des actions de l'utilisateur sur le système. [CT-AcT v2019 EN, §2.2.2, p. 17]
>   - […]
> - **CTAL-ATT v1.1 — §2.1.2 BDD (le plus concret, mais en retrait)**
>   - […]
>   - Le When décrit une action sémantique (« l'utilisateur confirme la commande »), pas un clic. Le Then décrit des observations précises, pas un « succès » ou une « erreur » génériques. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
> - […]
>
> **Ce que j'en retiens** (interprétation)
> - […]
> - Les consignes « atomique, déclaratif, sans interface » sont dans l'ISTQB. Il ne couvre pas les `Background`, les `Scenario Outline` ni les tags, qui relèvent de la documentation de Cucumber.
>
> **Confiance : 90/100** (élevée). Calcul : base 100 × 0,6 = 60 ; 5 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10 → 90. […]
