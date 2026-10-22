# T1-couverture — thomas

**Question** : Quelles techniques ISTQB permettent d'améliorer la couverture des tests ?

**Tours** : 9 · **coût** : 0.164 $ · **confiance annoncée** : 88 · **verdict** : réussi · **citations** : 6/6 lues · **Web** : 0

## Réponse

Je rédige le rapport final : les passages sont lus et le doublon est vérifié.

**Sources retenues**
- CTFL v4.0.1 EN : §4.1, §4.2.4, §4.3, §4.3.1.
- CTAL-TTA v4.0 EN : §2.8.
- CTAL-TA v4.0 FR : §3.2.2.
- CT-AI v2.0 EN : §3.4.3.
- Base d'idées : aucune idée capitalisée sur ce sujet.
- Web : non utilisé, car aucun outil n'est nommé dans ta question.

Hypothèse de contexte : tu poses la question en général, sans domaine ni cycle de vie précisés. Les syllabus répondent surtout par la notion de **coverage item** (élément de couverture). Chaque technique définit ce qu'elle compte et mesure un pourcentage d'éléments exercés.

**Pistes par syllabus**

- **CTFL v4.0.1 — §4.1 Vue d'ensemble des techniques**
  - Les techniques aident à définir les conditions de test, à identifier les *coverage items* et les données de test. Trois familles : boîte noire, boîte blanche, basées sur l'expérience. [CTFL-4.0.1 EN, §4.1, p. 39]
  - Les techniques basées sur l'expérience sont complémentaires des deux autres : elles peuvent trouver des défauts que celles-ci manquent. [CTFL-4.0.1 EN, §4.1, p. 39]
- **CTFL v4.0.1 — §4.2 Boîte noire** (les objectifs d'apprentissage sont listés au début du chapitre 4)
  - Quatre techniques sont à appliquer (niveau K3) : partitions d'équivalence, valeurs limites, tables de décision, transitions d'état. [CTFL-4.0.1 EN, §4, p. 38]
  - Pour les transitions d'état, trois critères sont ordonnés du plus faible au plus fort :
    - *all states* ;
    - *valid transitions* (0-switch), le plus utilisé ;
    - *all transitions* (valides et invalides), à viser au minimum pour le logiciel critique. [CTFL-4.0.1 EN, §4.2.4, p. 42]
- **CTFL v4.0.1 — §4.3 Boîte blanche**
  - Couverture des instructions (*statement*) : instructions exécutées ÷ total. Elle ne garantit ni les défauts dépendants des données ni toute la logique de décision. [CTFL-4.0.1 EN, §4.3.1, p. 42]
  - Le syllabus indique qu'il existe des techniques plus rigoureuses pour les environnements critiques, et des couvertures non liées au code (ex. neurones). [CTFL-4.0.1 EN, §4.3, p. 42] — *à creuser : §4.3.2 couverture des branches*
- **CTAL-TTA v4.0 — §2.8 Choisir une technique boîte blanche**
  - Appliquer d'abord la boîte noire, mesurer la couverture, puis ne recourir à la boîte blanche que pour les écarts. [CTAL-TTA-4.0 EN, §2.8, p. 18]
  - Spécifier un niveau de couverture à 100 % sur un seul critère. Un niveau inférieur laisse souvent non testées les parties les plus complexes. [CTAL-TTA-4.0 EN, §2.8, p. 18]
  - Hiérarchie de subsomption : la couverture des branches/décisions inclut celle des instructions, MC/DC inclut décisions et branches, la condition multiple inclut MC/DC. [CTAL-TTA-4.0 EN, §2.8, p. 18]
  - Moduler le niveau requis selon le risque de chaque partie du système. Pour les API, le niveau augmente avec le risque. [CTAL-TTA-4.0 EN, §2.8, p. 18]
- **CTAL-TA v4.0 — §3.2.2 Transitions d'état (avancé)**
  - Couverture **N-switch** (séquences de N+1 transitions) : 0-switch et 1-switch sont courants. Le 2-switch est réservé aux risques élevés, car le nombre de séquences croît de façon exponentielle. [CTAL-TA-4.0 FR, §3.2.2, p. 35]
  - Couverture **aller-retour** (*round-trip*) sur les boucles, jugée très efficace pour détecter les défauts. [CTAL-TA-4.0 FR, §3.2.2, p. 35]
- **CT-AI v2.0 — §3.4.3 Couverture des réseaux de neurones**
  - Mesures spécifiques : *neuron coverage*, kMNC, NBC. Elles révèlent les zones non testées, mais ne garantissent pas la généralisation du modèle. Il faut les compléter par des tests adversariaux et métamorphiques. [CT-AI-2.0 EN, §3.4.3, p. 37]

| Famille | Élément de couverture | Limite | Source |
|---|---|---|---|
| Boîte noire | partitions, limites, règles, transitions | indépendante de l'implémentation | CTFL §4.1–4.2 |
| Boîte blanche | instructions, branches, MC/DC | dépend de la conception, à mesurer en complément | CTFL §4.3, TTA §2.8 |
| Expérience | défauts probables, checklists | dépend des compétences du testeur | CTFL §4.1 |
| IA | neurones, sections de sortie | ne garantit pas la généralisation | CT-AI §3.4.3 |

**Ce que j'en retiens** (interprétation)
- Améliorer la couverture, c'est d'abord choisir un critère mesurable pour chaque niveau de risque, puis combler les écarts.
- Les syllabus ne s'accordent pas sur un seul niveau de couverture. Ils préconisent de le moduler par risque.

**Par quoi je commencerais**
1. Mesurer la couverture d'instructions ou de branches sur les tests existants. Impact fort, effort faible.
2. Compléter les tests par valeurs limites et tables de décision sur les règles métier. Impact fort, effort moyen.
3. Passer des transitions valides à *all transitions* ou 1-switch, seulement pour les zones à risque élevé. Impact moyen, effort moyen.

**Où creuser ensuite** : `section CTFL-4.0.1-en 4.3.2`, `section CTAL-TTA-4.0-en 2.5` (MC/DC, si ce numéro existe : vérifie le plan), `section CTAL-TA-4.0-fr 3.2`, thème `couverture`.

**Confiance : 88/100** (élevée). `base 80 × 0,6 = 48 ; 8 passages lus +20 ; syllabus concordants +20 → 88`. Limite : je n'ai pas lu les sections sur les branches ni sur MC/DC, ni les techniques d'expérience en détail.

**Questions à choix**
1. Quel est ton contexte ?
   1. Agile, livraisons fréquentes.
   2. Séquentiel ou réglementé (criticité élevée).
   3. Systèmes d'IA.
2. Quelle suite veux-tu ?
   1. Approfondir la boîte blanche (branches, MC/DC).
   2. Comparer les critères de couverture par niveau de risque.
   3. Capitaliser l'idée ci-dessous.

**À capitaliser ?** (doublons vérifiés : aucune idée similaire)
```json
{
  "titre": "Mesurer la couverture : boîte noire d'abord, puis boîte blanche pour combler",
  "resume": "Appliquer les techniques boîte noire, mesurer la couverture structurelle, et n'ajouter des tests boîte blanche que pour combler les écarts.",
  "principe": "Exiger 100 % sur un seul critère de couverture ; moduler le critère selon le risque de chaque partie du système.",
  "theme": "couverture",
  "references": [
    {
      "document": "CTAL-TTA-4.0-en",
      "page": 18,
      "extrait": "However black-box test techniques are normally applied first, coverage is then measured, and the white-box test technique only used if the required white-box coverage level has not been achieved."
    }
  ]
}
```
Les champs exacts viennent de `python qa.py idee modele`, que je n'ai pas lancé. La conversation principale devra les vérifier avant `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher couverture des tests techniques; python qa.py chercher "test coverage techniques"; python qa.py chercher "couverture techniques de test boîte noire"; python qa.py chercher "`
- `python qa.py lire 4812 --contexte 1 --max-caracteres 3500; python qa.py lire 4823 --contexte 1 --max-caracteres 3500; python qa.py lire 2137 --contexte 1 --max-caracteres 3500; python qa.py lire 1976 `
- `for i in 4812 4823 2137 1976 2958; do echo "=== $i"; python qa.py lire $i --contexte 1; done`
- `python qa.py lire 4812 --contexte 1; python qa.py lire 4823 --contexte 1; python qa.py lire 2137 --contexte 1; python qa.py lire 1976 --contexte 1; python qa.py lire 2958 --contexte 1`
- `python qa.py idee doublons --titre "Mesurer la couverture : boîte noire d'abord, puis boîte blanche pour combler" --resume "Appliquer les techniques boîte noire, mesurer la couverture structurelle, n'`
- `python qa.py themes | head -40; python qa.py confiance --base 80 --lus 8 --concordants 3`
- `python qa.py idee doublons --titre "Mesurer la couverture : boîte noire d'abord, puis boîte blanche pour combler" --resume "Appliquer les techniques boîte noire, mesurer la couverture structurelle, n'`
