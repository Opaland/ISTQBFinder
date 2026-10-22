# Exemples de conversations

Les commandes et extraits ci-dessous proviennent d'exécutions réelles sur la bibliothèque
du dépôt (42 fichiers, octobre 2026). Les numéros de passage (`#13411`) changent à chaque
réindexation : ils servent à lire, jamais à citer. On cite document, version, section, page.

---

## 1. Question de mise en place (cas M) — sortie réelle de Thomas

> **Utilisateur** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

Sortie réelle de l'agent Thomas (`claude -p --agent thomas`, essai `M1-rbt-agile` du
2026-10-22, 7 tours, 0,17 $), résumée fidèlement ; réponse complète et commandes
exécutées : `eval/essais-resultats/2026-10-22/M1-rbt-agile.md`. Le harnais a vérifié que
les 11 citations renvoient à des pages lues pendant la conversation.

```text
$ python qa.py idee chercher risk-based agile          # rien de capitalisé
$ python qa.py chercher '"risk-based testing" agile'
$ python qa.py lire … --contexte 1                      # CTFL-AT §3.2.1, CTAL-AT §3.1.1, CTFL §5.1.2…
$ python qa.py section CTAL-TM-3.0-fr 1.3.6
```

> **Thomas** : **Sources retenues** : CTFL-AT 2014 EN §3.2.1 (ancien), CTFL v4.0.1 EN
> §5.1.2, CTAL-AT v2.0 EN §3.1.1, CTAL-TA v4.0 FR §2.1.1 et §2.2, CTAL-TM v3.0 FR §1.3.6 ;
> pas de Web. L'ISTQB ne décrit pas une méthode unique : il greffe le RBT sur la
> planification de release et d'itération, avec une réévaluation continue.
> **Hypothèse de contexte** : équipe Scrum, application web, pas de contrainte
> réglementaire forte.
>
> **Méthode pas à pas**
> 1. Cadrer le niveau de risque : risques produit vs projet, probabilité × impact
>    [CTFL-AT 2014 EN, §3.2.1, p. 31].
> 2. Planification de release : le métier donne la vue d'ensemble, toute l'équipe
>    identifie et évalue [CTFL-AT 2014 EN, §3.2.1, p. 32 ; CTFL v4.0.1 EN, §5.1.2, p. 48].
> 3. Planification d'itération : analyse détaillée par user story, sessions de
>    *risk-storming* animées par le testeur [CTAL-AT v2.0 EN, §3.1.1, p. 24-25] ; les six
>    étapes du CTFL-AT (réunir l'équipe, lister le backlog, identifier, évaluer,
>    proportionner l'effort, choisir les techniques) [CTFL-AT 2014 EN, §3.2.1, p. 32].
> 4. Prioriser : risque élevé = démarrage plus tôt et plus d'effort de test [idem].
> 5. Atténuer avant l'exécution : revue des stories à risque, *shift-left*
>    [CTAL-TA v4.0 FR, §2.1.1, p. 27].
> 6. Réévaluer à chaque itération [CTAL-TA v4.0 FR, §2.2, p. 28].
> 7. Mesurer en rétrospective (parties prenantes impliquées ? défauts graves trouvés
>    tôt ? tests ignorés moins risqués ?) [CTAL-TM v3.0 FR, §1.3.6, p. 34].
>
> **Exemple de mise en œuvre (fictif — interprétation)** : équipe Scrum de 6 personnes,
> appli web livrée toutes les 2 semaines : 20 min de risk-storming au planning, chaque
> story notée faible / moyen / élevé ; le paiement (élevé) testé en premier avec revue de
> la story ; à la rétro, on vérifie si les bugs sont apparus là où on les attendait.
>
> **Adaptation par domaine** — santé / réglementé : traçabilité renforcée, couverture par
> niveau d'intégrité, *aucun syllabus santé ni IEC 62304* (Web nécessaire pour la norme) ;
> web : pas de syllabus dédié, CT-PT §3.2 ; embarqué : CT-AuT et CTEL-TM §8.3.3, en
> anglais ; mobile : CT-MAT (2019) ; API : pas de syllabus dédié, tests de contrat dans
> CT-QDO §3.2.2. « Je n'ai lu aucune des sections de ce tableau : ce sont des repères à
> vérifier, pas des citations. »
>
> **Par quoi je commencerais** : risk-storming de 15-20 min au planning (impact fort,
> effort faible) ; lier niveau de risque, ordre des tâches et effort (fort / faible) ;
> questions du CTAL-TM §1.3.6 en rétro (moyen / faible).
> **Confiance : 80/100 (élevée)** — source la plus détaillée ancienne (2014), exemple et
> ordre des étapes en partie interprétés.
> **Questions à choix** : 1. contexte (Scrum/Kanban web · agile à l'échelle · secteur
> réglementé) ; 2. suite (approfondir CTAL-AT §3.1 · comparer avec le cycle séquentiel ·
> `/ajouter-syllabus` pour un domaine non couvert). Suit une proposition à capitaliser en
> JSON (« Risk-storming à la planification d'itération »), non enregistrée.

Avant le correctif de #91, la même question classée « connaissance » donnait des pistes
par syllabus sans méthode ni exemple
(`eval/essais-resultats/2026-10-22/M1-rbt-agile-avant-correctif.md`).

---

## 2. Recherche approfondie avec Web justifié (cas B)

> **Utilisateur** : Comment réduire le coût de maintenance de nos tests Playwright ?

```text
$ python qa.py chercher maintenabilité solution automatisation --doc CTAL-TAE
[1] CTAL-TAE-2.0-en … p. 32 · §4.3 Test Automation Solution Maintainability
$ python qa.py section CTAL-TAE-2.0-fr 4.3
$ python qa.py section CTAL-TAE-2.0-fr 3.1.3      # superposition (couches) du TAF
$ python qa.py section CTAL-TAE-2.0-fr 3.1.5      # principes et canevas de conception
$ python qa.py chercher playwright
⚠ Aucun passage trouvé dans la bibliothèque locale : reformuler (termes anglais des syllabus),
  élargir les filtres, ou justifier une recherche Web.
```

> **Assistant** : Les syllabus donnent les principes : maintenabilité de la solution
> d'automatisation [ISTQB CTAL-TAE v2.0 FR, §4.3, p. 35], superposition du framework en
> couches (scripts de test, logique métier, bibliothèques principales)
> [ISTQB CTAL-TAE v2.0 FR, §3.1.3, p. 26 ; EN p. 24], canevas de conception dont le modèle
> d'objet de page [ISTQB CTAL-TAE v2.0 FR, §3.1.5, p. 31]. Ils ne parlent pas de Playwright : **recherche Web
> nécessaire** pour les pratiques propres à l'outil (sélecteurs, auto-wait, fixtures).
>
> *(WebSearch / WebFetch sur la documentation officielle Playwright)*
>
> **Diagnostic** · **Options** (1. sélecteurs orientés utilisateur — Web : doc Playwright ;
> 2. couches du TAF — ISTQB CTAL-TAE §3.1.3 ; Page Object — §3.1.5 ; 3. quarantaine et suivi des tests
> instables — Web ; …) · **Recommandation** · **Mise en œuvre** · **Indicateurs** (taux de
> tests instables, temps de correction après changement d'UI) · **Sources et limites**
> (ISTQB = principes génériques ; Web = documentation d'outil, consultée le …).
>
> À capitaliser ? 2 idées : « Sélecteurs orientés utilisateur » (`maintenance-automatisation`,
> source Web) et « Architecture en couches des tests E2E » (source ISTQB + Web).

---

## 3. Capitalisation contrôlée (cas C)

> **Utilisateur** : Oui, enregistre l'idée sur la matrice probabilité × impact.

```text
$ python qa.py section CTAL-TM-3.0-fr 1.3.3        # relu avant de citer
$ python qa.py theme proposer "prioriser les tests selon probabilité et impact des risques"
  rbt   Test management › Risk-Based Testing
$ python qa.py idee doublons --titre "Prioriser les tests par matrice probabilité × impact" --resume "…" --theme rbt
Aucune idée similaire.
$ python qa.py idee ajouter <<'JSON'
<le même JSON>
JSON
Idée créée : QA-0001
```

avec le JSON (passé sur l'entrée standard, sans fichier temporaire) :

```json
{"titre": "Matrice probabilité × impact pour prioriser les tests",
 "resume": "Évaluer chaque risque qualité selon sa probabilité et son impact, puis en dériver l'effort et l'ordre de test.",
 "probleme": "Effort de test réparti uniformément alors que les risques produit sont inégaux.",
 "principe": "Lister les risques qualité, noter probabilité et impact, calculer le niveau de risque, allouer profondeur et ordre de test.",
 "theme_principal": "rbt", "themes_secondaires": ["priorisation"], "maturite": "documentee",
 "provenance": "Recherche du 2026-10-21 : intégrer le RBT en agile",
 "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "30", "section": "1.3.3",
                 "extrait": "pour chaque élément de risque, de la probabilité du risque et de l'impact du risque"}]}
```

Ce que l'outil refuse (essais réels) :

```text
référence vers la page 300            → Erreur : Page 300 inexistante dans CTAL-TM-3.0-fr (95 pages).
extrait reformulé (ordre changé)      → Erreur : L'extrait cité n'apparaît pas mot pour mot aux pages 30 de CTAL-TM-3.0-fr : recopier une suite continue du passage lu…
même idée reformulée                   → REFUSÉ — Doublon probable : compléter l'idée existante (`idee modifier`)…
                                          DOUBLON PROBABLE QA-0001 « Matrice probabilité × impact… » (similarité 0.69)
statut validée sans motif              → Erreur : Le statut « validee » exige un motif (--motif)…
expérimentée sans retour d'expérience  → Erreur : « expérimentée » exige au moins un retour d'expérience
```

---

## 4. Retrouver et faire évoluer (cas C/D)

> **Utilisateur** : Retrouve les idées que nous avons déjà capitalisées sur le shift-left.

```text
$ python qa.py idee chercher shift-left
$ python qa.py idee lister --theme shift          # inclut shift-left et shift-right
```

> **Utilisateur** : On l'a testée sur la release 3.2, ça a marché.

```text
$ python qa.py idee retour QA-0001 --contexte "Release 3.2, équipe paiement" \
      --resultat "2 défauts critiques trouvés avant la recette" --enseignement "atelier d'1 h suffisant"
$ python qa.py idee statut QA-0001 experimentee --motif "appliquée sur la release 3.2"
QA-0001 : a_explorer → experimentee
```

---

## 5. Exploration d'un thème et lacunes (cas D)

> **Utilisateur** : Identifie les thèmes QA sur lesquels notre base est encore pauvre.

```text
$ python qa.py couverture
thème                                    idées passages  état
Test management                              0      773  vide
  Risk-Based Testing                         1      367  pauvre
…
Thèmes pauvres en idées mais documentés dans les syllabus (pistes d'exploration) : …
```

> **Assistant** : propose 2-3 thèmes à explorer en priorité (beaucoup de matière ISTQB,
> aucune idée capitalisée), et pour chacun lance `chercher --theme <code>` pour en extraire
> les pistes les plus exploitables, regroupées par sous-thème.

---

## 6. Comparaison ISTQB / Web (cas B)

> **Utilisateur** : Compare les techniques de priorisation de l'ISTQB avec les retours d'expérience récents.

1. `chercher priorisation des cas de test` → CTFL v4.0.1 §5.1.5 (*Test Case Prioritization*),
   CTAL-TM §1.3.5 (*Techniques pour le test basé sur les risques*) ; lecture des sections.
2. Lacune identifiée : pas de données terrain récentes → Web justifié (retours
   d'expérience sur la sélection de tests de régression en CI).
3. Tableau comparatif : technique · source (ISTQB §/p. ou URL + date) · conditions ·
   limites ; les éléments Web ne sont jamais présentés comme ISTQB.
4. Proposition de capitalisation : une comparaison (`priorisation`) liée aux idées
   existantes par `idee lier … --type complementaire|contradictoire`.

---

## 7. Extraits réels de Thomas et de Sylvie (essais du 2026-10-22)

Extraits **raccourcis mais non retouchés** des essais de bout en bout
(`python scripts/essais_agents.py`, rapport : [essais-reponses.md](essais-reponses.md)).
Les réponses complètes, avec les commandes exécutées, sont dans
`eval/essais-resultats/2026-10-22/`. Ces essais sont antérieurs aux corrections
qu'ils ont motivées : les défauts sont signalés sous chaque extrait.

### Thomas — comparaison (T5, 4 tours, 3/3 citations lues)

> **Utilisateur** : Compare les techniques de priorisation des tests décrites par l'ISTQB.

> **Thomas** : Il y a deux niveaux dans les syllabus. Le Foundation donne trois
> **stratégies de priorisation des cas de test**. L'Advanced Test Management détaille la
> plus utilisée, la priorisation par les risques […]
>
> **Pistes par syllabus**
> - **CTFL v4.0.1 (EN) — §5.1.5 Test Case Prioritization**
>   - Trois stratégies : par les risques, par la couverture, par les exigences [CTFL v4.0.1 EN, §5.1.5, p. 50].
>   - […]
> - **CTAL-TM v3.0 (EN) — §1.3.4 Quality Risk Mitigation Through Appropriate Testing**
>   - Deux ordonnancements. En *depth-first*, on exécute par niveau de risque décroissant.
>     En *breadth-first*, on affecte au moins un test par risque en priorité maximale, puis
>     on trie le reste par niveau de risque [CTAL-TM v3.0 EN, §1.3.4, p. 31].
>   - […]
>
> | Approche | Principe | Quand l'utiliser | Source |
> |---|---|---|---|
> | Par les risques | Les tests qui couvrent les risques majeurs passent en premier | Quand il existe une analyse de risque | CTFL §5.1.5 |
> | Risque breadth-first | Au moins un test par risque d'abord | Quand les parties prenantes veulent une vue globale de la qualité au plus tôt | CTAL-TM §1.3.4 |
> | […] | | | |
>
> **Confiance : 90/100** (élevée) — […] J'ai retiré 10 points parce que je n'ai lu ni le
> CTAL-TA ni le CTAL-TTA […]

Défauts relevés depuis : ajustement « −10 non lus » absent de la grille (#18), pas de
contexte projet ni de « Par quoi je commencerais » (#31), « Dis-moi si tu veux que je
capitalise » impossible pour un sous-agent (#23).

### Sylvie — vérification d'une démarche (S1, 9 tours, 9/10 citations lues)

> **Utilisateur** : […] un atelier en début de release avec le PO pour lister les
> fonctionnalités risquées, on teste ces fonctionnalités en premier et plus en profondeur,
> et on ne fait que du smoke test sur le reste. Est-ce que je suis aligné ISTQB ? Quel est
> le niveau de maturité de ma démarche ?

> **Sylvie** : Ta démarche va dans le bon sens, mais elle est incomplète. Elle couvre
> l'identification des risques et la priorisation. L'évaluation structurée, l'atténuation
> proportionnée au niveau de risque et le suivi ne sont pas décrits. Je la place au
> niveau 1 de maturité.
>
> | Pratique | Verdict | Ce que dit l'ISTQB | Source |
> |---|---|---|---|
> | P1 – Atelier avec le PO | **Partiellement conforme** | Les ateliers sur les risques sont une technique reconnue d'identification. Il faut impliquer « l'échantillon le plus large possible de parties prenantes » […] Le PO seul ne suffit donc pas. | CTAL-TM 3.0 fr, §1.3.2, p. 29-30 |
> | P1 – « Lister » les fonctionnalités risquées | **Partiellement conforme** | Après l'identification vient l'évaluation […] Une simple liste ne donne pas de niveau de risque. | CTAL-TM 3.0 fr, §1.3.3, p. 30-31 ; CTFL 4.0.1 en, §5.2.3, p. 52-53 |
> | […] | | | |
>
> **Ce qui manque** : évaluation probabilité × impact […] ; suivi des risques pendant la
> release […] ; rapport en termes de risque résiduel […]
>
> **Niveau de maturité : 1 — Initial** […] **Pour passer au niveau 2** : 1. Évaluer chaque
> risque (probabilité × impact) avec un barème partagé. 2. Relier chaque niveau de risque
> à une profondeur de test précise. […]
>
> **Confiance : 82/100** […]

Défauts relevés depuis : verdicts « Conforme » (vocabulaire de conformité) et absence de
distinction intention / en place (#30), confiance non reproductible avec la grille (#18),
« dis-le-moi et je réviserai » impossible pour un sous-agent (#23).
