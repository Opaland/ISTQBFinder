# T5-priorisation — thomas

**Question** : Compare les techniques de priorisation des tests décrites par l'ISTQB.

**Tours** : 6 · **coût** : 0.119 $ · **confiance annoncée** : 83 · **verdict** : réussi · **citations** : 3/3 lues · **Web** : 0

## Réponse

Les syllabus ISTQB décrivent trois stratégies de priorisation au niveau Foundation. Le niveau Advanced ajoute des variantes de parcours (depth-first et breadth-first) et la sélection des tests de régression. Je n'ai pas fait de recherche Web, la question portant sur l'ISTQB.

**Sources retenues**
- Lus : CTFL v4.0.1 EN §5.1.5, CTAL-TM v3.0 EN §1.3.4, CTAL-TA v4.0 FR §2.2.1 (début de la section seulement, p. 28).
- Base d'idées : aucune idée capitalisée sur ce sujet.
- Repérés mais non lus : CTAL-AT v2.0 §1.4, CT-TAS §3.3.1, CT-GenAI §2.2.2.

Hypothèse de contexte : aucun contexte projet n'est donné, donc la comparaison est générique.

**Pistes par syllabus**
- **CTFL v4.0.1, §5.1.5 Test Case Prioritization**
  - Trois stratégies : basée sur les risques, basée sur la couverture (avec la variante « couverture additionnelle ») et basée sur les exigences (priorités fixées par les parties prenantes). [CTFL-4.0.1 EN, §5.1.5, p. 50]
  - Limites communes : une dépendance entre tests peut imposer l'ordre (un test prioritaire qui dépend d'un test moins prioritaire passe après lui). La disponibilité des ressources compte aussi : outils, environnements, personnes. [CTFL-4.0.1 EN, §5.1.5, p. 50]
- **CTAL-TM v3.0, §1.3.4 Réduction des risques qualité**
  - La priorisation à l'implémentation suit les niveaux de risque. *Depth-first* : ordre strictement décroissant du risque couvert, pour traiter les risques majeurs au plus tôt. *Breadth-first* : au moins un test par risque en priorité haute, pour avoir une vue globale de la qualité le plus tôt possible. [CTAL-TM-3.0 EN, §1.3.4, p. 31]
  - En pratique, on commence souvent en depth-first puis on bascule en breadth-first quand le temps manque. Si le temps s'épuise, le risque résiduel permet de recommander de prolonger ou d'accepter le risque. [CTAL-TM-3.0 EN, §1.3.4, p. 31]
- **CTAL-TA v4.0, §2.2.1 Périmètre des tests de régression**
  - Pour l'automatisé, l'analyse d'impact (outillée via la gestion de configuration) est présentée comme la technique la plus fiable. [CTAL-TA-4.0 FR, §2.2.1, p. 28]
  - Pour le manuel, aucune technique n'est démontrée supérieure, et l'AT choisit selon la situation. La sélection basée sur les risques est la première technique citée. [CTAL-TA-4.0 FR, §2.2.1, p. 28] La suite de la liste est à lire p. 29.

| Technique | Principe | Quand l'utiliser | Source |
|---|---|---|---|
| Basée sur les risques | Les tests couvrant les risques les plus élevés passent d'abord | Temps limité, enjeux métier ou sécurité | CTFL §5.1.5 ; CTAL-TM §1.3.4 |
| Depth-first / breadth-first | Descente par niveau de risque, ou un test par risque d'abord | Depth-first : risques majeurs à traiter tôt. Breadth-first : vue globale rapide | CTAL-TM §1.3.4 |
| Basée sur la couverture | Plus forte couverture d'abord, ou plus forte couverture additionnelle | Tests unitaires ou structurels, sans analyse de risque | CTFL §5.1.5 |
| Basée sur les exigences | Priorité des exigences, définie par les parties prenantes | Traçabilité exigences-tests en place | CTFL §5.1.5 |
| Analyse d'impact (régression) | Tests liés aux éléments de configuration modifiés | Suites automatisées, avec outillage | CTAL-TA §2.2.1 |

**Ce que j'en retiens** (interprétation)
- Ces techniques ne s'excluent pas. Le CTFL les présente comme des critères d'ordonnancement, et le CTAL-TM décrit le passage de l'un à l'autre dans le temps.
- La couverture ne dit rien de la valeur métier. Elle sert de critère secondaire, par exemple pour départager des tests de même niveau de risque.
- Dans tous les cas, il faut vérifier les dépendances et les ressources avant de figer l'ordre.

**Par quoi je commencerais**
1. Priorisation par les risques avec bascule depth-first vers breadth-first : impact fort, effort moyen (il faut une analyse de risques).
2. Contrôle des dépendances et des ressources dans le plan d'exécution : impact moyen, effort faible.
3. Analyse d'impact pour la régression automatisée : impact fort, effort fort (outillage).

**Où creuser ensuite**
- `section CTAL-TM-3.0-en 1.3.3` pour l'analyse de risques qui alimente la priorisation.
- `page CTAL-TA-4.0-fr 29` pour la suite des techniques de sélection en régression.
- `section CTAL-AT-2.0-en 1.4` pour la régression en agile.
- `section CT-TAS-1.0-en 3.3.1` pour la priorisation des tests à automatiser.

**Confiance : 83/100 (élevée)** — base 88 × 0,6 = 53 ; 3 passages lus +20 ; 2 syllabus concordants +10 → 83. La section TA §2.2.1 n'est lue qu'en partie.

**Questions à choix**
1. Quel est ton contexte ?
   1. Agile / itératif
   2. Séquentiel
   3. Réglementé / sûreté
2. Quelle suite veux-tu ?
   1. Approfondir la régression (TA §2.2.1, AT §1.4)
   2. Approfondir la priorisation par les risques (TM §1.3)
   3. Capitaliser la comparaison

**À capitaliser ?**
Je ne propose aucune entrée pour l'instant. Si tu choisis l'option 3, je prépare le JSON après `idee doublons`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher priorisation des tests; python qa.py chercher "test prioritization" | head -60; python qa.py chercher "priorisation des tests" | head -60`
- `python qa.py section CTFL-4.0.1-en 5.1.5 --max-caracteres 4000; python qa.py section CTAL-TM-3.0-en 1.3.4 --max-caracteres 4500; python qa.py chercher "regression test selection prioritization" | head`
- `python qa.py section CTAL-TA-4.0-en 2.2.1 --max-caracteres 3500; python qa.py confiance --help | head -20`
- `python qa.py section CTAL-TA-4.0-fr 2.2.1 --max-caracteres 3500; python qa.py confiance --base 88 --lus 3 --concordants 2`
