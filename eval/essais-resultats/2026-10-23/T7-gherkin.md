# T7-gherkin — thomas

**Question** : Je veux rédiger mes critères d'acceptation en Gherkin, j'ai besoin d'aide.

**Tours** : 12 · **coût** : 0.162 $ · **confiance annoncée** : 80 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 1 · **critères** : 4/4

## Réponse

## Sources retenues

- **CTFL v4.0.1 EN**, §4.5.2 « Acceptance Criteria » (pp. 45-46). Lu.
- **CT-AcT 2019 EN**, §2.2.2 « Using the Gherkin Language to Write Test Cases » (pp. 16-17). Lu. Le document existe aussi en FR.
- **CTAL-ATT v1.1 EN**, §2.1.2 BDD (p. 15). Lu. Ce syllabus est en retrait ISTQB, remplacé par CTAL-AT.
- **CTAL-AT v2.0 EN** (2026-04-17), §4.1.3 « Example Mapping » (pp. 33-34). Lu.
- **Web**: la référence Gherkin de Cucumber, consultée le 2026-10-23. Je l'ai prise parce que l'ISTQB ne détaille pas les mots-clés de l'outil (`Background`, `Scenario Outline`…).
- **Base d'idées**: aucune idée capitalisée sur le sujet.

**Hypothèse de contexte**: équipe agile qui écrit des user stories sur une application web, sans contrainte réglementaire particulière. Tu ne m'as donné ni le domaine ni un exemple de story.

## Pistes par syllabus

**CTFL v4.0.1 — §4.5.2 Critères d'acceptation**
- Les critères sont les conditions qu'une story doit remplir pour être acceptée. Ils servent aussi de conditions de test. [CTFL v4.0.1 EN, §4.5.2, p. 45]
- Ils servent à délimiter le périmètre, à obtenir un consensus, à décrire les scénarios positifs **et négatifs**, et à planifier et estimer. [CTFL v4.0.1 EN, §4.5.2, p. 46]
- Deux formats courants existent: orienté scénario (Given/When/Then) et orienté règle (liste à puces ou table entrées/sorties). Un format maison reste possible s'il est précis et sans ambiguïté. [CTFL v4.0.1 EN, §4.5.2, p. 46]
  - Gherkin n'est donc pas obligatoire. Les règles de calcul se prêtent mieux à une table.

**CT-AcT 2019 — §2.2.2 Gherkin**
- Un cas de test Gherkin est déclaratif et suit le schéma Given [situation], When [action], Then [résultat attendu]. [CT-AcT 2019 EN, §2.2.2, p. 16]
- Given met le système dans un état. When est l'action. Then décrit ce qui est observable. [CT-AcT 2019 EN, §2.2.2, p. 17]
- Un test Gherkin ne cite pas d'éléments d'interface, mais des actions de l'utilisateur sur le système. [CT-AcT 2019 EN, §2.2.2, p. 17]
- La structure peut être analysée automatiquement, ce qui permet de générer des scripts en keyword-driven. [CT-AcT 2019 EN, §2.2.2, p. 17]

**CTAL-ATT v1.1 — §2.1.2 BDD** (en retrait, mais c'est le plus concret)
- Pour extraire les scénarios d'une story, écris un scénario par critère. Certains critères en demandent plusieurs. Repère aussi les conditions des cas d'usage et des exemples, ainsi que les étapes qui se répètent. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- Les scénarios doivent être isolés et atomiques, exécutables dans n'importe quel ordre. Les Given placent le système dans l'état nécessaire. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- Les When décrivent des actions sémantiques («l'utilisateur confirme la commande») plutôt que techniques («clique sur le bouton Confirmer»). Fais l'exception si le bouton lui-même est testé. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- Les Then décrivent des observations ou des états précis. Ils ne doivent pas se limiter à «succès» ou «erreur». [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- Écris à la troisième personne, du point de vue d'un utilisateur précis. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]
- Décide si chaque When n'a qu'une étape (un test ne vérifie qu'une chose) ou si tu optimises la vitesse d'exécution. [CTAL-ATT v1.1 EN, §2.1.2, p. 15]

**CTAL-AT v2.0 — §4.1.3 Example Mapping**
- Avant de rédiger, organise un atelier avec des cartes: story (jaune), règles métier (bleu), exemples (vert), questions (rouge). [CTAL-AT v2.0 EN, §4.1.3, p. 33]
- Les exemples validés deviennent tes scénarios. Beaucoup de cartes rouges signifient que la story n'est pas prête. Beaucoup de règles, ou une règle avec beaucoup d'exemples, signifient qu'il faut découper la story. [CTAL-AT v2.0 EN, §4.1.3, p. 33]
- L'atelier clarifie les critères d'acceptation qui alimentent l'ATDD et le BDD. [CTAL-AT v2.0 EN, §4.1.3, p. 34]

**Web — syntaxe Gherkin** [Web — Gherkin reference, cucumber.io, consulté le 2026-10-23]
- `Feature` regroupe les scénarios. `Rule` (depuis Gherkin 6) regroupe les scénarios d'une règle métier.
- `Background` porte les étapes communes à plusieurs scénarios.
- `Scenario Outline` + `Examples` répète un scénario avec plusieurs jeux de valeurs.
- `And` et `But` remplacent des Given, When ou Then successifs, pour la lisibilité.

## Exemple (interprétation, fictif)

Story: «En tant que client, je veux appliquer un code promo pour réduire mon panier.»

```gherkin
Feature: Code promo

  Rule: Un code valide réduit le total du panier

    Scenario: Code valide appliqué à un panier éligible
      Given une cliente avec un panier de 100 € hors frais de port
      And le code "PRINTEMPS10" offre 10 % de réduction
      When elle applique le code "PRINTEMPS10"
      Then le total du panier affiche 90 €
      And la ligne "Réduction : -10 €" apparaît dans le récapitulatif

    Scenario: Code expiré refusé
      Given un code "ETE2025" expiré depuis la veille
      When la cliente applique le code "ETE2025"
      Then le message "Ce code a expiré" s'affiche
      And le total du panier reste inchangé
```

- Chaque scénario porte un seul comportement (atomicité, ATT p. 15).
- Les When sont sémantiques et les Then observables (ATT p. 15).
- Le scénario négatif vient du critère «positifs et négatifs» (CTFL p. 46).
- Les seuils (par exemple remise plafonnée) iraient mieux dans un `Scenario Outline` ou une table (CTFL p. 46 pour le format orienté règle).

## Par quoi je commencerais

| Piste | Impact | Effort |
|---|---|---|
| Écrire les Then avec des valeurs observables et des When sémantiques | fort | faible |
| Un scénario par critère, plus un scénario négatif par règle | fort | faible |
| Faire un Example Mapping avant de rédiger | fort | moyen |
| Utiliser `Scenario Outline` pour les règles à valeurs (seuils, formats) | moyen | faible |

## Où creuser ensuite

- `section CT-AcT-2019-en 2` (critères, tests d'acceptation, pratiques)
- `section CTFL-4.0.1-en 4.5.3` (ATDD)
- `section CTAL-AT-2.0-en 4.1` (raffinement, Example Mapping)
- `section CTAL-ATT-1.1-en 2.1.2` (la suite du passage cité, pour les cas limites)

## Confiance: 80/100 (élevée)

Calcul: base 100 × 0,6 = 60; 5 passages lus +20; 3 syllabus concordants +20; Web −10; raisonnement −10 (l'exemple est fictif).

Limites:
- Le plus détaillé des syllabus (CTAL-ATT) est en retrait.
- L'ISTQB ne traite pas la syntaxe fine de Gherkin (`Background`, `Outline`). Je l'ai prise sur le Web, donc elle n'est pas validée par l'ISTQB.

## Questions à choix

**Pour adapter l'aide, quel est ton point de départ ?**
1. J'ai des user stories à transformer en scénarios Gherkin (colle-en une).
2. J'ai déjà des critères en Gherkin à relire et à améliorer.
3. Je veux d'abord une méthode d'équipe (atelier, Definition of Ready).

**Quel est ton domaine ?** (les règles changent: seuils pour le réglementé, mobile et API)
1. Web / SaaS
2. Santé ou réglementé (la bibliothèque n'a pas de syllabus dédié)
3. API ou mobile

**Suite à donner ?**
1. Approfondir l'Example Mapping.
2. Comparer le format Gherkin et le format orienté règle.
3. Capitaliser les bonnes pratiques ci-dessous.

## À capitaliser ?

Aucun doublon trouvé. La commande a suggéré les thèmes `exigences` et `niveaux-types`. Je retiens `exigences`.

```json
{
  "titre": "Rédiger des critères d'acceptation Gherkin atomiques, sémantiques et observables",
  "resume": "Un scénario Given/When/Then par comportement, étapes sémantiques, Then avec observations précises, scénarios négatifs inclus, isolés et exécutables dans n'importe quel ordre.",
  "principe": "Partir des critères d'acceptation de la story (un scénario par critère, plus négatifs). Écrire les When comme des actions utilisateur sémantiques et les Then comme des états observables précis, jamais « succès » ou « erreur » génériques. Garder chaque scénario isolé.",
  "theme": "exigences",
  "references": [
    {
      "document": "CTAL-ATT-1.1-en",
      "page": 15,
      "extrait": "The Then steps should describe specific observations or states. They should not specify generic success or error states."
    },
    {
      "document": "CTFL-4.0.1-en",
      "page": 46,
      "extrait": "There are several ways to write acceptance criteria for a user story. The two most common formats are:"
    }
  ]
}
```

Les `extrait` sont copiés des passages lus. Les champs exacts sont à confirmer avec `python qa.py idee modele` avant `idee ajouter`. Rien n'est enregistré sans ton accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher Gherkin critères d'acceptation; python qa.py idee chercher acceptance criteria BDD`
- `python qa.py chercher Gherkin; python qa.py chercher "Given When Then"; python qa.py chercher "critères d'acceptation"; python qa.py chercher "behavior-driven development"`
- `python qa.py idee chercher "Gherkin criteres acceptation"; python qa.py idee chercher "acceptance criteria BDD"`
- `python qa.py section CT-AcT-2019-en 2.2.2 --max-caracteres 7000`
- `python qa.py section CTFL-4.0.1-en 4.5.2 --max-caracteres 5000`
- `python qa.py lire 1649 --contexte 1 --max-caracteres 6000`
- `python qa.py section CTAL-AT-2.0-en 4.1.3 --max-caracteres 6000`
- `WebFetch {"url": "https://cucumber.io/docs/gherkin/reference/", "prompt": "Liste les mots-clés Gherkin (Feature, Rule, Scenario, `
- `python qa.py idee doublons --titre "Critères d'acceptation en Gherkin : atomiques, sémantiques, observables" --resume "Rédiger des critères d'acceptation Given/When/Then atomiques, déclaratifs, avec T`
- `python qa.py confiance --base 100 --lus 5 --concordants 3 --web 1 --raisonnement 1`
