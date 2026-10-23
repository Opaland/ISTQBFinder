# T1-couverture — thomas

**Question** : Quelles techniques ISTQB permettent d'améliorer la couverture des tests ?

**Tours** : 9 · **coût** : 0.168 $ · **confiance annoncée** : 88 · **verdict** : réussi · **citations** : 8/8 lues · **Web** : 0

## Réponse

Les syllabus ISTQB améliorent la couverture de deux façons. La première est de choisir une technique dont l'élément de couverture est explicite, puis de mesurer cette couverture. La seconde est d'ajouter des tests là où la couverture mesurée est trop faible. Les techniques sont réparties en trois niveaux de syllabus.

**Hypothèse de contexte :** la question ne précise ni le domaine ni le niveau de test. Je suppose un projet généraliste (web ou applicatif), sans contrainte de criticité.

## Sources retenues
- **Lus :**
  - CTFL v4.0.1 EN, §4.2 à §4.4.
  - CTAL-TA v4.0 EN, §3.1.2 et §3.3.1.
  - CTAL-TTA v4.0 EN, §2.4 et §2.8.
- **Base d'idées :** aucune idée capitalisée sur le sujet.
- **Non exploré :** CT-MBT (sélection de tests par modèle, résultat de recherche non lu) et CT-AI (couverture des réseaux de neurones, non lu).
- **Web :** non utilisé, aucun besoin identifiable.

## Pistes par syllabus

**CTFL v4.0.1 — Chapitre 4 (techniques de base)**
- **Partitions d'équivalence (EP).** L'élément de couverture est la partition. La couverture est le nombre de partitions exercées divisé par le nombre total, y compris les partitions invalides. [CTFL v4.0.1 EN, §4.2.1, p. 40]
  - Avec plusieurs jeux de partitions, le critère le plus simple est *Each Choice*. Il ne tient pas compte des combinaisons, d'où l'intérêt du test combinatoire (voir plus bas).
- **Analyse des valeurs limites (BVA).** Elle existe en version 2 valeurs et 3 valeurs. Les éléments de couverture sont les valeurs limites, et elles ne s'appliquent qu'à des partitions ordonnées. [CTFL v4.0.1 EN, §4.2.2, p. 40] *À creuser : la version 3 valeurs, `page CTFL-4.0.1-en 40`.*
- **Tables de décision et transitions d'état.** Je ne les ai pas lues dans le CTFL. *À creuser : §4.2.3 et §4.2.4.*
- **Test d'instruction et de branche.** Le test de branche subsume le test d'instruction (100 % de branches implique 100 % d'instructions, pas l'inverse). Le syllabus signale que 100 % d'instructions ne garantit pas que toute la logique de décision est testée. [CTFL v4.0.1 EN, §4.3.1 à §4.3.2, p. 42-43]
- **Techniques fondées sur l'expérience.**
  - Le *error guessing* s'appuie sur une liste d'erreurs possibles (« fault attacks »), construite à partir de l'expérience et des données de défauts. [CTFL v4.0.1 EN, §4.4.1, p. 44]
  - Le test exploratoire en sessions (charte, débriefing) sert à créer des tests pour les zones non testées. Il convient aussi quand les spécifications sont faibles ou que le temps manque. [CTFL v4.0.1 EN, §4.4.2, p. 44]
  - *À creuser : le test sur checklist, §4.4.3.*

**CTAL-TA v4.0 — Chapitre 3 (techniques du Test Analyst)**
- **Test combinatoire.** Il vise les défaillances d'interaction. [CTAL-TA v4.0 EN, §3.1.2, p. 30-31]
  - Les critères de couverture sont *base choice* et *pairwise*. Le pairwise est jugé efficace : environ 97 % des défaillances viennent d'une ou deux conditions en interaction (étude limitée).
  - Le syllabus conseille d'appliquer d'abord l'EP pour réduire le nombre de valeurs.
- **Tables de décision.** La couverture est le nombre de colonnes exercées divisé par le nombre de colonnes réalisables. Si le risque est élevé, il vaut mieux ne pas minimiser la table. [CTAL-TA v4.0 EN, §3.3.1, p. 35-36]
- **Test métamorphique.** On génère des tests de suivi à partir d'un test source et d'une relation métamorphique. Il est utile quand l'oracle est difficile à définir. [CTAL-TA v4.0 EN, §3.3.2, p. 36]

**CTAL-TTA v4.0 — Chapitre 2 (boîte blanche approfondie)**
- **Hiérarchie de subsomption.** Branche/décision subsume instruction, MC/DC subsume décision, et condition multiple subsume MC/DC. [CTAL-TTA v4.0 EN, §2.8, p. 18]
- **MC/DC.** Chaque condition atomique doit influencer seule le résultat. Pour N conditions indépendantes, il faut en général N+1 exécutions. [CTAL-TTA v4.0 EN, §2.4, p. 15]
  - *À creuser : test de condition multiple (§2.5) et test de chemins de base (§2.6).*
- **Séquence conseillée.** Appliquer d'abord les techniques boîte noire, mesurer la couverture, puis n'utiliser la boîte blanche que si le niveau requis n'est pas atteint. Pour une mesure informelle, le test d'instruction suffit. [CTAL-TTA v4.0 EN, §2.8, p. 18]
- **Niveau requis.** Fixer l'exigence à 100 % sur un seul critère. À moins de 100 %, les zones non couvertes sont souvent les plus complexes et les plus sujettes aux erreurs. Les niveaux peuvent varier selon le risque de chaque partie du système. [CTAL-TTA v4.0 EN, §2.8, p. 18]
- **Éléments irréalisables.** La norme ISO 29119-4 permet de les exclure du calcul, ce qui rend 100 % atteignable. [CTAL-TTA v4.0 EN, §2.8, p. 18]

## Vue d'ensemble

| Besoin | Technique | Élément de couverture | Source |
|---|---|---|---|
| Données d'entrée | EP, BVA | partitions, valeurs limites | CTFL §4.2 |
| Règles métier | Table de décision | colonnes réalisables | CTAL-TA §3.3.1 |
| Interactions de paramètres | Pairwise, base choice | paires de valeurs | CTAL-TA §3.1.2 |
| Code | Instruction, branche, MC/DC | instructions, branches, conditions | CTFL §4.3, CTAL-TTA §2 |
| Zones non couvertes | Exploratoire, *error guessing* | selon la charte | CTFL §4.4 |
| Oracle difficile | Métamorphique | relations métamorphiques | CTAL-TA §3.3.2 |

## Ce que j'en retiens (interprétation)
- Chaque technique définit ses propres éléments de couverture. Améliorer la couverture, c'est donc choisir la technique qui correspond au risque, puis mesurer.
- Un seul pourcentage ne suffit pas. Il vaut mieux combiner un critère boîte noire (partitions, limites, colonnes de table) et un critère de code.

## Par quoi je commencerais
1. **Mesurer la couverture existante** avec le test d'instruction ou de branche, de façon informelle, puis cibler les zones faibles. Impact fort, effort faible [CTAL-TTA §2.8].
2. **Passer les entrées multiples en EP/BVA, puis en pairwise** quand les paramètres interagissent. Impact fort, effort moyen [CTFL §4.2, CTAL-TA §3.1.2].
3. **Ajouter des sessions exploratoires** sur les zones à faible couverture. Impact moyen, effort faible [CTFL §4.4.2].

## Où creuser ensuite
- `section CTFL-4.0.1-en 4.2.3` et `4.2.4` (tables de décision et transitions d'état).
- `section CTAL-TTA-4.0-en 2.5` et `2.6` (condition multiple, chemins de base).
- `section CTAL-TA-4.0-en 3.2` (transitions d'état, couverture N-switch, d'après les notes de version).

**Confiance : 88/100 (élevée).** Calcul : base 80 × 0,6 = 48 ; 6 passages lus +20 ; 3 syllabus concordants +20. Deux limites : je n'ai pas lu le détail des tables de décision et des transitions du CTFL, ni CT-MBT.

## Questions à choix
**Quel est ton contexte principal ?**
1. Web ou applicatif généraliste.
2. Système critique ou réglementé (je regarderais les niveaux d'intégrité, CTAL-TTA §2.8.2).
3. Agile avec peu de documentation.

**Quelle suite veux-tu ?**
1. Approfondir les techniques boîte noire (transitions d'état, N-switch).
2. Approfondir la boîte blanche (MC/DC, condition multiple).
3. Capitaliser la piste « mesurer d'abord, puis cibler » dans la base.

## À capitaliser ?
Une proposition. Le contrôle de doublons ne trouve aucune idée similaire (thèmes suggérés : boite-blanche, niveaux-types, mbt).

```json
{
  "titre": "Mesurer la couverture boîte noire, puis cibler la boîte blanche sur les zones faibles",
  "resume": "Appliquer d'abord les techniques boîte noire, mesurer la couverture de code, n'utiliser une technique boîte blanche que si le niveau requis n'est pas atteint.",
  "principe": "Une exigence de couverture se fixe à 100 % sur un seul critère, avec des niveaux différents selon le risque de chaque partie du système.",
  "theme": "boite-blanche",
  "references": [
    {
      "document": "CTAL-TTA-4.0-en",
      "page": 18,
      "extrait": "black-box test techniques are normally applied first, coverage is then measured, and the white-box test technique only used if the required white-box coverage level has not been achieved."
    }
  ]
}
```

Le champ `theme` est un choix de ma part parmi les thèmes suggérés. La structure exacte reste à vérifier avec `python qa.py idee modele` avant `idee ajouter`. Je n'ai rien enregistré.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher couverture des tests techniques; python qa.py chercher couverture des tests techniques; python qa.py chercher test coverage techniques`
- `python qa.py section CTFL-4.0.1-en 4.2 --max-caracteres 5000; python qa.py section CTFL-4.0.1-en 4.3 --max-caracteres 3500; python qa.py section CTFL-4.0.1-en 4.4 --max-caracteres 3500`
- `python qa.py lire 2137 --contexte 1 --max-caracteres 4000; python qa.py chercher "coverage" "pairwise" "combinatorial" "decision table"`
- `python qa.py section CTAL-TA-4.0-en 3.1.2 --max-caracteres 3500; python qa.py lire 1795 --contexte 1 --max-caracteres 3000; python qa.py plan CTAL-TTA-4.0-en --max-caracteres 3000`
- `python qa.py plan CTAL-TTA-4.0-en | grep -n "2\.\(3\|4\|5\|6\)" | head -20; python qa.py section CTAL-TTA-4.0-en 2.4 --max-caracteres 2500; python qa.py idee doublons --titre "Choisir la technique sel`
- `python qa.py confiance --help | head -20`
- `python qa.py confiance --base 80 --lus 6 --concordants 3`
