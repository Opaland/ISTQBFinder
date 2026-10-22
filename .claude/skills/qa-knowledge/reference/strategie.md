# Stratégie de recherche et formats de réponse

## Comprendre l'intention

| Demande | Cas | Ce qu'on fait |
|---|---|---|
| « Qu'est-ce que… », « Que dit l'ISTQB sur… » | A — simple | base + syllabus, lecture, réponse courte citée |
| « Recherche des idées pour… », « Compare… » | B — approfondie | A + lacunes/contradictions + Web ciblé + comparaison + recommandations |
| « Classe / enregistre cette idée » | C — capitalisation | doublons → thème → ajout tracé |
| « Idées sur le thème X », « Où notre base est-elle pauvre ? » | D — exploration | `idee lister --theme`, `chercher --theme`, `couverture`, regroupement par sous-thème |

## Formuler les requêtes locales

- Découper la question en 2-4 notions et lancer une requête par angle :
  `chercher "risk-based testing" agile`, puis `chercher priorisation risques --doc CTAL-TM`.
- Ajouter le terme ISTQB anglais quand il est connu : les syllabus EN sont plus complets
  (26 codes) que les traductions FR (14 codes). Les deux langues sont indexées et
  cherchées ensemble : ne pas utiliser `--langue` sauf demande explicite de texte français
  à citer mot pour mot (et préciser alors que la couverture FR est partielle).
- `--theme <code>` restreint aux passages qui évoquent le thème (mots-clés de la taxonomie).
- Un résultat « PARTIEL » ne couvre qu'une partie des notions : le lire avant de l'utiliser.
- Un passage dans `§ 0.x` ou une annexe (« Business Outcomes », « Release Notes ») est
  rarement la réponse : préférer le chapitre de fond.
- Si rien ne sort : reformuler (synonymes, terme anglais), élargir (`--toutes-versions`),
  puis seulement envisager le Web.
- Outil, technologie ou pratique nommés par la question et introuvables localement
  (`chercher playwright` → aucun passage) : les principes ISTQB ne suffisent pas, la
  recherche Web ciblée (documentation officielle) fait partie de la réponse.

## Lire et recouper

- `lire <id> --contexte 1` donne le passage et ses voisins ; `section <doc> 4.2` toute une
  section. Lire au moins les 2-3 meilleurs passages, de documents différents si possible.
- Noter la version et la date du syllabus ; si deux syllabus divergent (ex. CTFL vs
  CTAL-TM), le dire et expliquer (niveau, date, angle).

## Format de réponse : ouvrir des pistes, pas livrer un texte à recopier

But : donner à l'utilisateur ce qu'il aurait trouvé en parcourant **tous** les syllabus —
les idées, où elles sont, ce qu'elles valent — pour qu'il aille lire et décide. Pas de
dissertation complète ni de longue paraphrase : une piste = 1-2 lignes + sa source.

Gabarit (adapter, rester proportionné ; 150-400 mots pour une question courante) :

```
<1-2 phrases conversationnelles : ce que les syllabus disent en gros, et où>

**Pistes par syllabus**
- **CTAL-TM v3.0 — §1.3 Test basé sur les risques**
  - <idée en une ligne> [CTAL-TM v3.0 FR, §1.3.3, p. 30]
  - <autre idée> [… p. 31] — *à creuser : §1.3.5 Techniques pour le RBT*
- **CTFL v4.0.1 — §5.1.5 Priorisation des cas de test**
  - <idée> [CTFL v4.0.1 EN, §5.1.5, p. 50]

<tableau si comparaison ou choix : | Approche | Principe | Quand l'utiliser | Source |>

**Ce que j'en retiens** (interprétation) : 2-3 puces reliant les pistes au contexte.
**Où creuser ensuite** : 2-4 sections à lire en entier (`section <doc> <num>`).
**Confiance : NN/100** (libellé) — 1-2 raisons.
**À capitaliser ?** 0-3 propositions (rien n'est enregistré sans accord).
```

- Grouper par syllabus puis chapitre ; quand plusieurs syllabus disent la même chose,
  une seule puce avec les deux sources.
- Tableau dès qu'il y a ≥ 3 options à comparer ou des critères de choix.
- Amélioration de processus : faire précéder les pistes d'un diagnostic d'une phrase et
  terminer par 2-3 indicateurs de validation.
- Question simple : 2-5 phrases + source(s) + confiance, sans gabarit complet.

## Score de confiance (obligatoire)

La grille est dans SKILL.md (seul texte préchargé chez Thomas et Sylvie) et dans
`qak/confiance.py` ; `python qa.py confiance …` l'applique et affiche le calcul. Écrire
« Confiance : NN/100 (libellé) » suivi du calcul, par exemple :
`base 79 × 0,6 = 47 ; 3 passages lus +20 ; 2 syllabus concordants +10 ; Web −10 → 67`.
Aucun autre ajustement (« −5 syllabus non lu », point de départ choisi à l'œil…).
Plafond : si une notion de la question (ex. l'outil nommé) n'est couverte ni par un
passage lu ni par une source Web consultée (`--non-couvert 1`), le score
ne dépasse pas **60** — le dire.

## Marquage de la provenance

- `[ISTQB CTAL-TA v4.0 FR, §3.1.1, p. 31]` — passage lu.
- `[Web — titre, domaine, consulté le AAAA-MM-JJ]`.
- `[Base QA-0007, statut à évaluer]`.
- « Interprétation : … » / « Hypothèse : … » pour ce qui vient du raisonnement.

## Quand dire « je ne sais pas »

Aucune source locale ni Web fiable, sources contradictoires sans arbitrage possible,
extraction défaillante du document utile (voir `inventaire`) : le dire, indiquer ce qui
manque (document à importer, version, terme à préciser).
