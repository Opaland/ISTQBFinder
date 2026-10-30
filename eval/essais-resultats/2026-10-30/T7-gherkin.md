# T7-gherkin — thomas

**Question** : Je veux rédiger mes critères d'acceptation en Gherkin, j'ai besoin d'aide.

**Tours** : 10 · **coût** : 0.205 $ · **confiance annoncée** : 90 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 5/5 · **fidélité** (juge LLM, indicatif) : 0.85 sur 5 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : base d'idées (aucune idée sur Gherkin ni BDD) ; syllabus lus : CT-AcT 2019 EN §2.2.2, CTFL v4.0.1 EN §4.5.2, CTAL-ATT v1.1 EN §2.1.2 (en retrait, remplacé par CTAL-AT), CTAL-AT v2.0 EN §4.1.3. Web non consulté : Gherkin est couvert localement. Je finalise le rapport.

Les syllabus décrivent Gherkin comme un format de rédaction (Given/When/Then), pas comme une méthode complète. Ils donnent surtout des règles de forme et une technique en amont, l'Example Mapping.

Hypothèse de contexte : équipe agile qui écrit des user stories, domaine web ou générique. Je n'ai pas d'autre information.

**Pistes par syllabus**
- **CTFL v4.0.1 — §4.5.2 Critères d'acceptation**
  - Il existe deux formats courants : orienté scénario (Given/When/Then) ou orienté règles (liste à puces, tableau entrées/sorties). Gherkin n'est donc pas obligatoire. [CTFL v4.0.1 EN, §4.5.2, p. 46]
  - Les critères doivent décrire les scénarios positifs et négatifs, et servir de base à la planification et à l'estimation. [CTFL v4.0.1 EN, §4.5.2, p. 46]
- **CT-AcT 2019 — §2.2.2 Langage Gherkin**
  - Le motif est Given (situation), When (action sur le système), Then (résultat attendu). Les cas ne citent pas d'éléments d'interface, mais des actions de l'utilisateur sur le système. [CT-AcT 2019 EN, §2.2.2, p. 17]
  - Le format se parse automatiquement, ce qui permet de générer des scripts automatisés par mots-clés. [CT-AcT 2019 EN, §2.2.2, p. 17]
- **CTAL-ATT v1.1 — §2.1.2 BDD** (en retrait, mais c'est le plus détaillé sur la rédaction)
  - Extraire les scénarios des critères d'acceptation, des exemples et des cas d'usage. Un scénario décrit un seul comportement. [CTAL-ATT v1.1 EN, §2.1.2, p. 14]
  - Consignes de rédaction : scénarios atomiques et isolés, exécutables dans n'importe quel ordre. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
  - Les When décrivent des actions sémantiques (« confirme la commande », pas « clique sur Confirmer »). Les Then décrivent des observations précises, jamais un « succès » ou une « erreur » générique. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
  - Autres points de la même page : repérer les étapes répétées, les données aléatoires ou de synthèse, et les mocks nécessaires. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- **CTAL-AT v2.0 — §4.1.3 Example Mapping**
  - Avant d'écrire du Gherkin, faire un atelier avec des cartes : story, règles, exemples, questions. Les exemples deviennent les scénarios. [CTAL-AT v2.0 EN, §4.1.3, p. 33]
  - Trop de cartes « question » indique qu'il reste beaucoup à clarifier. Beaucoup de règles, ou une règle avec beaucoup d'exemples, indique une story à découper. [CTAL-AT v2.0 EN, §4.1.3, p. 33]

**Ce que j'en retiens** (interprétation)
- Écris d'abord les règles et les exemples (Example Mapping), puis traduis chaque exemple en un scénario Gherkin court.
- Garde Gherkin pour les comportements. Pour des règles de calcul ou des tableaux de valeurs, le format « règles » du CTFL est souvent plus lisible.

**Par quoi je commencerais**
1. Impact fort, effort faible : appliquer les 5 règles de rédaction (atomique, sémantique, Then précis, pas d'interface, un comportement par scénario) à tes 2-3 prochaines stories.
2. Impact fort, effort moyen : faire un Example Mapping de 25 minutes pendant l'affinage.
3. Impact moyen, effort moyen : relire tes scénarios avec le métier, puis les brancher sur l'automatisation.

**Où creuser ensuite**
- À lire : `section CT-AcT-2019-en 2.2` (les tests d'acceptation en pratique).
- À lire : `section CTAL-AT-2.0-en 4.1` (l'affinage, dont le découpage des stories).

**Confiance : 90/100** (élevée). Calcul : base 100 × 0,6 = 60 ; 4 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10. Réserve : les consignes de rédaction détaillées viennent d'un syllabus ancien (2019, en retrait). Je n'ai pas vérifié ce que CTAL-AT v2.0 dit de la rédaction de scénarios.

**Questions à choix**
1. Quel est ton contexte ?
   1. Équipe agile (Scrum/Kanban), stories en affinage
   2. Projet réglementé ou cycle séquentiel
   3. Autre (précise)
2. Quelle suite veux-tu ?
   1. Un modèle de scénario Gherkin commenté, à partir d'une de tes stories
   2. Une comparaison Gherkin / format orienté règles
   3. Lire en entier Example Mapping et CT-AcT §2.2

**À capitaliser ?**
Aucun doublon trouvé (`idee doublons`). Thèmes suggérés par l'outil : `exigences`, `niveaux-types`. Je n'ai pas lancé `idee ajouter`.
```json
{
 "titre": "Rédiger des critères d'acceptation en Gherkin : règles de forme",
 "resume": "Écrire des scénarios Given/When/Then atomiques, sémantiques et à résultats observables, après un atelier d'Example Mapping.",
 "probleme": "Critères d'acceptation ambigus, liés à l'interface, difficiles à automatiser et à relire par le métier.",
 "principe": "Partir des règles et exemples (Example Mapping), puis écrire un scénario par comportement : Given = état, When = action sémantique de l'utilisateur, Then = observation précise. Garder le format orienté règles pour les calculs ou tableaux de valeurs.",
 "theme_principal": "exigences",
 "themes_secondaires": ["niveaux-types"],
 "domaine_application": "Équipes agiles qui écrivent des user stories",
 "prerequis": "Présence du métier à l'affinage ; langage commun (ubiquitous language)",
 "benefices": "Critères compréhensibles par tous, base d'automatisation, ambiguïtés repérées avant le code",
 "limites": "Les consignes détaillées viennent de CTAL-ATT 2019 (en retrait). Gherkin est lourd pour les règles de calcul.",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « Je veux rédiger mes critères d'acceptation en Gherkin »",
 "references": [
  {"type": "istqb", "doc_id": "CTFL-4.0.1-en", "pages": "46", "section": "4.5.2", "extrait": "Scenario-oriented (e.g., Given/When/Then format used in BDD"},
  {"type": "istqb", "doc_id": "CT-AcT-2019-en", "pages": "17", "section": "2.2.2", "extrait": "Test cases written in Gherkin do not refer to"},
  {"type": "istqb", "doc_id": "CTAL-ATT-1.1-en", "pages": "15", "section": "2.1.2", "extrait": "The Then steps should describe specific observations or states"}
 ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher Gherkin acceptance criteria; python qa.py idee chercher BDD Given When Then`
- `python qa.py chercher Gherkin Given When Then; python qa.py chercher behavior-driven development acceptance criteria; python qa.py chercher critères d'acceptation scénarios`
- `python qa.py chercher Gherkin Given When Then; python qa.py chercher behavior-driven development acceptance criteria; python qa.py chercher "critères d'acceptation" scénarios`
- `python qa.py section CT-AcT-2019-en 2.2.2 --max-caracteres 6000; python qa.py section CTFL-4.0.1-en 4.5.2 --max-caracteres 5000; python qa.py section CTAL-ATT-1.1-en 2.1.2 --max-caracteres 7000`
- `python qa.py section CTAL-AT-2.0-en 4.1.3 --max-caracteres 5000`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Écrire des critères d'acceptation en Gherkin" --resume "Bonnes pratiques de rédaction Given/When/Then" --principe "Scénari`
- `python qa.py confiance --base 100 --lus 4 --concordants 3 --raisonnement 1; python qa.py themes | head -30`
- `python qa.py idee modele`
