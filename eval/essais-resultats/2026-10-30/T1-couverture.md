# T1-couverture — thomas

**Question** : Quelles techniques ISTQB permettent d'améliorer la couverture des tests ?

**Tours** : 9 · **coût** : 0.307 $ · **confiance annoncée** : 88 · **verdict** : réussi · **citations** : 8/8 lues · **Web** : 0 · **fidélité** (juge LLM, indicatif) : 1.0 sur 8 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : base d'idées (aucune idée capitalisée sur le sujet), puis CTFL v4.0.1 EN (§4.2, §4.3), CTAL-TA v4.0 EN (§3.1.2), CTAL-TTA v4.0 EN (§2.4, §2.8) et CT-AI v2.0 EN (§3.4.3), tous lus. Le Web n'a pas été utilisé, car les syllabus suffisent. Je n'ai lu que les versions EN, plus complètes ; les versions FR existent pour CTAL-TA et CTAL-TTA.

Dans les syllabus, chaque technique définit ses propres « éléments de couverture » (coverage items), avec une formule de mesure. Améliorer la couverture revient donc à choisir la technique, à mesurer, puis à combler les trous.

Hypothèse de contexte : application classique, sans contrainte réglementaire particulière, sans équipe ni cycle précisés.

**Pistes par syllabus**

- **CTFL v4.0.1 — §4.2 Techniques boîte noire**
  - Partitions d'équivalence : l'élément de couverture est la partition, y compris les partitions invalides. « Each Choice » couvre chaque partition au moins une fois, sans tenir compte des combinaisons. [CTFL v4.0.1 EN, §4.2.1, p. 40]
  - Valeurs limites (BVA) : la version à 3 valeurs détecte des défauts que celle à 2 valeurs rate. Exemple du syllabus : `x ≤ 10` implémenté en `x = 10` n'est détecté que par x = 9. [CTFL v4.0.1 EN, §4.2.2, p. 40]
  - Tables de décision : la couverture se mesure en colonnes réalisables. La technique révèle aussi les trous et contradictions des exigences. Quand les règles explosent, on utilise une table minimisée ou une approche par les risques. [CTFL v4.0.1 EN, §4.2.3, p. 41]
  - Transitions d'états : trois critères, du plus faible au plus fort : tous les états, transitions valides (0-switch), toutes les transitions. Ce dernier est recommandé au minimum pour le logiciel critique. [CTFL v4.0.1 EN, §4.2.4, p. 42]
- **CTFL v4.0.1 — §4.3 Techniques boîte blanche**
  - Couverture des instructions et des branches. La branche subsume l'instruction. [CTFL v4.0.1 EN, §4.3.2, p. 43]
  - Faire seulement de la boîte noire ne donne aucune mesure de la couverture réelle du code. La mesure boîte blanche indique où ajouter des tests. [CTFL v4.0.1 EN, §4.3.3, p. 43]
- **CTAL-TA v4.0 — §3.1.2 Test combinatoire**
  - Couverture par paires (pairwise) et « base choice ». Appliquer d'abord les partitions d'équivalence pour réduire le nombre de valeurs. [CTAL-TA v4.0 EN, §3.1.2, p. 31]
  - Le syllabus cite une étude limitée selon laquelle environ 97 % des défaillances viennent d'une ou deux conditions en interaction. [CTAL-TA v4.0 EN, §3.1.2, p. 31]
- **CTAL-TTA v4.0 — §2.4 et §2.8 (avancé, boîte blanche)**
  - MC/DC : chaque condition atomique doit influer seule sur la décision, avec en général N+1 exécutions. Le court-circuit du compilateur peut empêcher de l'atteindre. [CTAL-TTA v4.0 EN, §2.4, p. 15-16]
  - Stratégie : boîte noire d'abord, couverture mesurée, boîte blanche seulement si le niveau requis n'est pas atteint. Il est conseillé de n'exiger que 100 %, sur un seul critère. Hiérarchie de subsomption : multiple condition ⊃ MC/DC ⊃ décision/branche ⊃ instruction. Le niveau varie selon le risque de chaque partie du système. [CTAL-TTA v4.0 EN, §2.8, p. 18]
- **CT-AI v2.0 — §3.4.3 Couverture des réseaux de neurones**
  - Couverture de neurones, kMNC, NBC. Utile pour repérer les zones non exercées, mais insuffisante seule : il faut y ajouter des tests adversariaux et métamorphiques. [CT-AI v2.0 EN, §3.4.3, p. 37]

| Besoin | Technique | Critère de couverture | Source |
|---|---|---|---|
| Entrées / sorties simples | EP, BVA | partitions, valeurs limites | CTFL §4.2.1-4.2.2 |
| Règles métier | Table de décision | colonnes réalisables | CTFL §4.2.3 |
| Comportement à états | Transitions d'états | états, transitions valides, toutes transitions | CTFL §4.2.4 |
| Paramètres et configurations | Pairwise, base choice | paires de valeurs | CTAL-TA §3.1.2 |
| Code | Instruction, branche, MC/DC | instructions, branches, conditions | CTFL §4.3 ; CTAL-TTA §2.4 |

**Ce que j'en retiens** (interprétation)
- La couverture se mesure toujours par rapport à un modèle : partitions, table, diagramme d'états ou graphe de flot. Si le modèle est faux ou incomplet, les 100 % ne valent rien.
- Le syllabus suggère un enchaînement : techniques boîte noire, mesure de couverture du code, puis tests ciblés sur les zones non couvertes.

**Par quoi je commencerais**
1. Mesurer la couverture de branches de la suite actuelle (impact fort, effort faible).
2. Passer le BVA de 2 à 3 valeurs et ajouter les partitions invalides (impact moyen, effort faible).
3. Modéliser les règles métier en tables de décision et les parcours à états en tables d'états (impact fort, effort moyen).

**Où creuser ensuite** : à lire : CTAL-TTA v4.0 EN §2.8.1 et §2.8.2 (niveaux de couverture selon l'intégrité), CTFL v4.0.1 EN §4.4 (techniques fondées sur l'expérience), CTAL-TA v4.0 EN §3.1 (autres techniques d'analyse).

**Confiance : 88/100** (élevée) — base 80 × 0,6 = 48 ; 8 passages lus +20 ; 3 syllabus concordants +20 → 88.

**Questions à choix**

Quel est ton contexte principal ?
1. Application métier (web ou API), sans réglementation
2. Système critique ou réglementé
3. Autre (IA, mobile, embarqué…)

Que veux-tu faire ensuite ?
1. Approfondir une technique (laquelle ?)
2. Un plan « mise en place » pour mesurer et améliorer la couverture
3. Comparer avec les techniques fondées sur l'expérience

**À capitaliser ?** (doublons vérifiés : aucune idée similaire)

```json
{
 "titre": "Choisir la technique de test à partir de l'élément de couverture visé",
 "resume": "Chaque technique ISTQB définit ses éléments de couverture et sa mesure. On applique d'abord la boîte noire, on mesure la couverture du code, puis on comble avec la boîte blanche.",
 "probleme": "Suite de tests dont la couverture est inconnue ou jugée insuffisante.",
 "principe": "Boîte noire d'abord, mesure de la couverture, boîte blanche ciblée sur les zones non couvertes. Seuil de 100 % sur un critère unique, modulé selon le risque de chaque partie du système.",
 "theme_principal": "couverture",
 "themes_secondaires": ["boite-noire", "boite-blanche"],
 "domaine_application": "Tout produit logiciel ; rigueur croissante pour les systèmes critiques",
 "prerequis": "Modèle du test object (partitions, table de décision, diagramme d'états) et outil de mesure de couverture du code",
 "benefices": "Objectiver la couverture et cibler l'effort de test supplémentaire",
 "limites": "100 % de couverture ne garantit pas l'absence de défauts (défauts dépendants des données, omissions)",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « Quelles techniques ISTQB permettent d'améliorer la couverture des tests ? »",
 "references": [
  {"type": "istqb", "doc_id": "CTAL-TTA-4.0-en", "pages": "18", "section": "2.8", "extrait": "black-box test techniques are normally applied first, coverage is then measured"},
  {"type": "istqb", "doc_id": "CTFL-4.0.1-en", "pages": "43", "section": "4.3.3", "extrait": "Performing only black-box testing does not provide a measure of actual code coverage"}
 ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher couverture des tests techniques; python qa.py chercher couverture des tests techniques; python qa.py chercher test coverage techniques`
- `python qa.py section CTFL-4.0.1-en 4.2 --max-caracteres 6000; echo ======; python qa.py section CTFL-4.0.1-en 4.3 --max-caracteres 5000`
- `python qa.py section CTAL-TTA-4.0-en 2.8 --max-caracteres 5000; echo ======; python qa.py section CT-AI-2.0-en 3.4.3 --max-caracteres 3500`
- `python qa.py section CTFL-4.0.1-en 4.2.3 --max-caracteres 3500; echo =====; python qa.py section CTFL-4.0.1-en 4.2.4 --max-caracteres 3500; echo =====; python qa.py section CTAL-TTA-4.0-en 2.4 --max-c`
- `python qa.py section CTAL-TA-4.0-en 3.1.2 --max-caracteres 3500; echo ====; python qa.py confiance --base 80 --lus 6 --help | head -30`
- `python qa.py confiance --base 80 --lus 8 --concordants 3; python qa.py idee doublons --titre "Choisir une technique de test selon le critère de couverture" --resume "Chaque technique ISTQB définit ses`
- `python qa.py idee doublons --titre "Choisir une technique de test selon le critère de couverture" --resume "Chaque technique ISTQB définit ses éléments de couverture ; mesurer la couverture puis compl`
