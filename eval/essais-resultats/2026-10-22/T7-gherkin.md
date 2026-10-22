# T7-gherkin — thomas

**Question** : Je veux rédiger mes critères d'acceptation en Gherkin, j'ai besoin d'aide.

**Tours** : 11 · **coût** : 0.161 $ · **confiance annoncée** : 90 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 0 · **critères** : 4/4

## Réponse

**Sources retenues**
- CT-AcT v2019 EN, §1.2.3, §2.1 et §2.2.2. Il existe aussi une version FR, mais je n'ai lu que l'EN.
- CTAL-ATT v1.1 EN, §2.1.2 et §2.1.3, publié en 2019. Ce syllabus est en retrait, son successeur est CTAL-AT.
- CTAL-AT v2.0 EN, §4.1.3, publié en 2026.
- CTFL v4.0.1 EN, §4.5.3.
- La base d'idées ne contient rien sur ce sujet.
- Je n'ai pas consulté le Web. Gherkin est couvert par les syllabus, et l'ISTQB donne les principes, pas la syntaxe complète de l'outil.

Les syllabus voient Gherkin comme un format pour écrire des critères d'acceptation sous forme de tests. Ils donnent surtout des règles de rédaction : précis, déclaratifs, atomiques.

Hypothèse de contexte : équipe agile qui travaille avec des user stories, sans contrainte réglementaire particulière.

**Pistes par syllabus**
- **CT-AcT v2019 — §2.1 Writing Acceptance Criteria**
  - Un bon critère est précis, mesurable et concis. Le testeur doit pouvoir dire si l'objet testé le respecte. [CT-AcT v2019 EN, §2.1, p. 16]
  - Il dit « quoi » et non « comment » : pas de détail de solution technique. [CT-AcT v2019 EN, §2.1, p. 16]
  - Il couvre aussi les exigences non fonctionnelles, pas seulement le fonctionnel. [CT-AcT v2019 EN, §2.1, p. 16]
  - Les critères se relisent comme les user stories (revue, séance de planification). [CT-AcT v2019 EN, §2.1, p. 16]
  - La rédaction se fait à deux : analyste métier et testeur. [CT-AcT v2019 EN, §2.1, p. 15]
- **CT-AcT v2019 — §2.2.2 Gherkin**
  - Le motif est Given (situation), When (action sur le système), Then (résultat attendu). [CT-AcT v2019 EN, §2.2.2, pp. 16-17]
  - Les scénarios Gherkin ne citent pas d'éléments d'interface mais des actions de l'utilisateur sur le système. [CT-AcT v2019 EN, §2.2.2, p. 17]
  - Le format peut être analysé automatiquement, ce qui permet de générer des scripts en mode keyword-driven. [CT-AcT v2019 EN, §2.2.2, p. 17]
  - *À creuser : §1.2.3, la différence entre BDD (Gherkin) et ATDD (formes textuelles ou graphiques variées).* [CT-AcT v2019 EN, §1.2.3, p. 14]
- **CTAL-ATT v1.1 — §2.1.2 BDD (le plus concret, mais en retrait)**
  - Pour extraire des scénarios d'une story, on écrit un ou plusieurs scénarios par critère. On cherche aussi les cas conditionnels, les données et les pas répétés. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
  - Il faut identifier les étapes qui demandent des mocks ou des stubs. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
  - Les scénarios sont atomiques et isolés, exécutables dans n'importe quel ordre. Le When peut être limité à une étape. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
  - Le When décrit une action sémantique (« l'utilisateur confirme la commande »), pas un clic. Le Then décrit des observations précises, pas un « succès » ou une « erreur » génériques. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- **CTAL-AT v2.0 — §4.1.3 Example Mapping**
  - Avant d'écrire du Gherkin, on trie en cartes : story, règles métier, exemples, questions. Les exemples deviennent les scénarios. Trop de cartes « question » ou « règle » signalent une story trop grosse à découper. [CTAL-AT v2.0 EN, §4.1.3, p. 33]
  - L'atelier clarifie les critères d'acceptation qui alimentent l'ATDD et le BDD, et il révèle les manques avant le codage. [CTAL-AT v2.0 EN, §4.1.3, p. 34]
- **CTFL v4.0.1 — §4.5.3 ATDD**
  - L'atelier de spécification commence par les cas positifs, puis les cas négatifs, puis les caractéristiques non fonctionnelles. [CTFL v4.0.1 EN, §4.5.3, p. 46]
  - Les cas couvrent toute la story sans la dépasser, et deux cas ne décrivent jamais la même caractéristique. [CTFL v4.0.1 EN, §4.5.3, p. 46]

**Ce que j'en retiens** (interprétation)
- Un critère d'acceptation est une règle ou un exemple métier. Un scénario Gherkin en est la version exécutable. Les deux se rédigent donc dans cet ordre.
- Les consignes « atomique, déclaratif, sans interface » sont dans l'ISTQB. Il ne couvre pas les `Background`, les `Scenario Outline` ni les tags, qui relèvent de la documentation de Cucumber.
- Les deux sources sur les cas négatifs et non fonctionnels sont le CTFL et CT-AcT. Elles évitent de ne rédiger que le cas nominal.

**Par quoi je commencerais**
1. Un atelier Example Mapping de 25 minutes sur une story. Impact fort, effort faible.
2. Une checklist de revue de scénario tirée de CTAL-ATT §2.1.2 : un comportement, un utilisateur, un Given qui pose l'état, un When sémantique, un Then observable. Impact fort, effort faible.
3. Pour chaque critère, au moins un scénario négatif et un critère non fonctionnel (CTFL §4.5.3, CT-AcT §2.1). Impact moyen, effort moyen.

**Où creuser ensuite**
- `section CT-AcT-2019-en 2` pour le chapitre complet.
- `section CTAL-ATT-1.1-en 2.1.2` pour la liste de rédaction.
- `section CTAL-AT-2.0-en 4.1` pour le raffinement et le découpage des stories.

**Confiance : 90/100** (élevée). Calcul : base 100 × 0,6 = 60 ; 5 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10 → 90. Le seul syllabus détaillé sur la rédaction est CTAL-ATT, déjà en retrait, mais CT-AcT le confirme.

**Questions à choix**
1. Que veux-tu faire en premier ?
   1. Un exemple de story avec critères puis scénarios, que je rédige à titre d'illustration.
   2. Une checklist de revue de scénarios Gherkin.
   3. La comparaison ATDD / BDD / Example Mapping.
2. Quel est ton contexte ?
   1. Web / API.
   2. Mobile ou embarqué.
   3. Santé ou réglementé.

**À capitaliser ?**

Pas de doublon trouvé (`idee doublons`). Rien n'est enregistré sans ton accord.

```json
{
  "titre": "Rédiger des scénarios Gherkin atomiques et déclaratifs à partir des critères d'acceptation",
  "resume": "Chaque critère d'acceptation donne un ou plusieurs scénarios Given/When/Then, atomiques, isolés et formulés en actions sémantiques, avec des Then observables.",
  "probleme": "Des critères d'acceptation vagues ou liés à l'interface, impossibles à mesurer ou fragiles à automatiser.",
  "principe": "Un comportement par scénario ; Given pose l'état, When décrit une action sémantique, Then décrit une observation précise ; scénarios indépendants ; critères précis, mesurables, sans détail de solution.",
  "theme_principal": "exigences",
  "themes_secondaires": ["niveaux-types"],
  "domaine_application": "Équipes agiles qui pratiquent ATDD ou BDD sur des user stories",
  "prerequis": "Collaboration entre analyste métier, testeur et développeur ; story raffinée",
  "benefices": "Critères partagés et compréhensibles, base d'automatisation en keyword-driven, documentation vivante",
  "limites": "Syntaxe avancée de Gherkin (Outline, Background, tags) non couverte par l'ISTQB ; le CTAL-ATT qui détaille les consignes est en retrait.",
  "maturite": "documentee",
  "statut": "a_evaluer",
  "provenance": "Recherche du 2026-10-22 : « rédiger mes critères d'acceptation en Gherkin »",
  "references": [
    {
      "type": "istqb",
      "doc_id": "CT-AcT-2019-en",
      "pages": "16-17",
      "section": "2.2.2",
      "extrait": "Test cases written in Gherkin do not refer to user interface elements"
    },
    {
      "type": "istqb",
      "doc_id": "CTAL-ATT-1.1-en",
      "pages": "15",
      "section": "2.1.2",
      "extrait": "The scenarios should be isolated and atomic"
    }
  ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-q/.claude/skills/qa-knowledge`
- `python qa.py idee chercher Gherkin critères d'acceptation; python qa.py idee chercher acceptance criteria BDD`
- `python qa.py chercher Gherkin; python qa.py chercher "Given/When/Then"; python qa.py chercher "critères d'acceptation"; python qa.py chercher "behavior-driven development"`
- `python qa.py idee chercher "Gherkin critères acceptation"; python qa.py idee chercher "acceptance criteria BDD"`
- `python qa.py section CT-AcT-2019-en 2.2.2 --max-caracteres 6000`
- `python qa.py lire 5546 --contexte 1 --max-caracteres 5000; python qa.py lire 1546 --contexte 1 --max-caracteres 4000`
- `python qa.py lire 1649 --contexte 1; python qa.py lire 1546 --contexte 1; python qa.py lire 4838 --contexte 1`
- `python qa.py section CT-AcT-2019-en 2.1 --max-caracteres 5000; python qa.py lire 32 --contexte 1`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Rédiger des scénarios Gherkin atomiques et déclaratifs" --resume "Écrire les critères d'acceptation en Given/When/Then, un`
- `python qa.py confiance --base 100 --lus 5 --concordants 3 --raisonnement 1; python qa.py idee modele; python qa.py idee doublons --titre "Rédiger des scénarios Gherkin atomiques et déclaratifs" --resu`
