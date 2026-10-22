# Stratégie de recherche et formats de réponse

## Comprendre l'intention

| Demande | Cas | Ce qu'on fait |
|---|---|---|
| « Qu'est-ce que… », « Que dit l'ISTQB sur… » | A — simple | base + syllabus, lecture, réponse courte citée |
| « Comment intégrer / mettre en place / déployer / organiser X », « comment l'ISTQB propose-t-il d'intégrer… », « par où commencer pour… » | M — mise en place | gabarit « mise en place » ci-dessous : méthode, exemple, domaines |
| « Recherche des idées pour… », « Compare… » | B — approfondie | A + lacunes/contradictions + Web ciblé + comparaison + recommandations |
| « Classe / enregistre cette idée » | C — capitalisation | doublons → thème → ajout tracé |
| « Idées sur le thème X », « Où notre base est-elle pauvre ? » | D — exploration | `idee lister --theme`, `chercher --theme`, `couverture`, regroupement par sous-thème |

Question ambiguë, trop large ou sans syllabus proche : clarifier d'abord par des
questions à choix, puis montrer le plan de recherche — voir [conversation.md](conversation.md).

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

**Contexte projet** : cycle de vie (agile, séquentiel), taille d'équipe, contraintes
réglementaires, échéance. S'il est donné, s'en servir pour choisir et classer les pistes.
Sinon, le dire (« Hypothèse de contexte : … ») et terminer par 1-2 questions de cadrage
dont la réponse changerait la recommandation. Un sous-agent ne pose pas la question : il
la rend dans son rapport, la conversation principale la pose.

Gabarit (adapter, rester proportionné ; 150-400 mots pour une question courante) :

```
<1-2 phrases conversationnelles : ce que les syllabus disent en gros, et où>
<« Contexte : … » s'il est donné, sinon « Hypothèse de contexte : … »>

**Pistes par syllabus**
- **CTAL-TM v3.0 — §1.3 Test basé sur les risques**
  - <idée en une ligne> [CTAL-TM v3.0 FR, §1.3.3, p. 30]
  - <autre idée> [… p. 31] — *à creuser : §1.3.5 Techniques pour le RBT*
- **CTFL v4.0.1 — §5.1.5 Priorisation des cas de test**
  - <idée> [CTFL v4.0.1 EN, §5.1.5, p. 50]

<tableau si comparaison ou choix : | Approche | Principe | Quand l'utiliser | Source |>

**Ce que j'en retiens** (interprétation) : 2-3 puces reliant les pistes au contexte.
**Par quoi je commencerais** : 2-3 pistes classées impact / effort (impact fort / moyen /
faible ; effort faible / moyen / fort) ; d'abord fort impact pour faible effort.
**Où creuser ensuite** : 2-4 sections à lire en entier (`section <doc> <num>`).
**Confiance : NN/100** (libellé) — 1-2 raisons.
**Questions à choix** (questions de cadrage si le contexte manque, puis suites) : 1-2
questions, 3 options numérotées au plus chacune (voir conversation.md).
**À capitaliser ?** 0-3 propositions (rien n'est enregistré sans accord).
```

- Grouper par syllabus puis chapitre ; quand plusieurs syllabus disent la même chose,
  une seule puce avec les deux sources.
- Tableau dès qu'il y a ≥ 3 options à comparer ou des critères de choix.
- Amélioration de processus : faire précéder les pistes d'un diagnostic d'une phrase et
  terminer par 2-3 indicateurs de validation.
- Question simple : 2-5 phrases + source(s) + confiance, sans gabarit complet.

## Format « mise en place » (comment intégrer / déployer X)

Une question de **connaissance** (« que dit l'ISTQB… », « quelles techniques… ») garde le
format de pistes ci-dessus. Une question qui demande **comment faire** est une question de
mise en place, même formulée « comment l'ISTQB propose-t-il d'intégrer… » : la réponse
est alors la démarche ISTQB, en étapes. Une question de **mise en place** attend une démarche
exploitable : des pistes seules ne répondent pas. Cible 400-700 mots ; le reste ne change
pas (lire avant de citer, confiance, « où creuser », « à capitaliser ? »).

```
<1-2 phrases : ce que proposent les syllabus et où>
<« Contexte : … » ou « Hypothèse de contexte : … »>

**Méthode pas à pas** (4 à 7 étapes ; pour chacune : qui, quand, quel livrable)
1. <étape> — <qui / quand / livrable> [CTFL-AT 2014 EN, §3.2.1, p. 32]
2. <étape> — … [source lue] ou « (interprétation) » si aucune source
…

**Exemple de mise en œuvre** (fictif — interprétation)
« Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines,
je ferais : … » — chaque pratique utilisée renvoie à l'étape (et donc à la source) ci-dessus.

**Adaptation par domaine**
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | … | … |
| Web | … | … |
| Systèmes embarqués / intégrés | … | … |
| Mobile | … | … |
| API | … | … |

**Par quoi je commencerais** : 2-3 pistes classées impact / effort.
**Où creuser ensuite** : 2-4 sections à lire en entier.
**Confiance : NN/100** (libellé) — 1-2 raisons.
**Questions de cadrage** (à choix) : 2-3 questions si le contexte manque (domaine,
réglementation, taille et rythme de l'équipe, outillage), options numérotées ; elles ne
bloquent pas la réponse.
**À capitaliser ?** 0-3 propositions.
```

- Une étape sans passage lu est marquée « (interprétation) » ; jamais de source plaquée.
- L'exemple est toujours présenté comme fictif ; il illustre la méthode, il ne la remplace pas.
- Domaine donné par l'utilisateur : développer sa ligne, résumer ou omettre les autres.
  Domaine absent : tableau complet, puis question de cadrage sur le domaine.
- Le tableau renvoie aux syllabus **réellement présents** (`inventaire`) ; lire la
  section avant de la citer. Repères dans la bibliothèque actuelle (à vérifier par
  `chercher`, pas à citer sans lecture) :

| Domaine | Syllabus utiles | Couverture |
|---|---|---|
| Santé / réglementé | CTEL-TM 2011 §8.3.4 (safety-critical), CTAL-TTA v4.0 §2.8.2 (couverture par niveau d'intégrité), CTAL-AT v2.0 §3.1.2, CT-FT §2 (conformité, finance) ; CT-AuT pour ISO 26262 | **Pas de syllabus santé / dispositif médical** (IEC 62304 absent) : le dire, Web justifié pour la norme |
| Web | CT-PT §3.2 (risques de performance par architecture), CT-MAT §2.2.4 (web apps), CTAL-TAE / CT-TAS (automatisation) | **Pas de syllabus web dédié** : principes transposés, le signaler |
| Embarqué / intégré | CTEL-TM 2011 §8.3.3 (matériel/logiciel), CT-AuT v2.1.1 (niveaux ASPICE / ISO 26262, HiL), CT-PT §3.2 (temps réel) | Couvert surtout par l'automobile ; anglais seulement |
| Mobile | CT-MAT 2019 (§1.6 stratégie, §1.8 risques, §2) | Dédié, FR + EN, version 2019 |
| API | CTAL-TTA v4.0 §2.7, CT-QDO v1.0 §3.2.2 (tests de contrat), CTAL-TAE v2.0 §5.1.3 | Pas de syllabus API dédié ; tests de contrat en anglais seulement (CT-QDO) |

## Score de confiance (obligatoire)

Partir de la **confiance documentaire** affichée par `chercher` (0-100 ; prendre celle
de la requête la plus pertinente), puis ajuster :

| Situation | Ajustement |
|---|---|
| Moins de 2 passages réellement lus (`lire`/`section`) | − 20 |
| Seul un syllabus ancien (≤ 2016) ou une version remplacée couvre le sujet | − 15 |
| Syllabus contradictoires non arbitrés | − 15 |
| Une partie de la réponse repose sur le Web | − 10 (et préciser laquelle) |
| Une partie repose sur ton raisonnement sans source | − 10 |
| ≥ 3 syllabus courants concordants, passages lus | + 5 |

Plafond : si une notion de la question (ex. l'outil nommé) n'est couverte ni par un
passage lu ni par une source Web consultée, le score ne dépasse pas **60** — le dire.

Borner entre 0 et 100. Libellés : ≥ 75 élevée · 50-74 moyenne · 25-49 faible ·
< 25 très faible (le dire franchement et proposer Web ou reformulation).
Écrire « Confiance : NN/100 (libellé) » suivi des raisons principales.

## Marquage de la provenance

- `[ISTQB CTAL-TA v4.0 FR, §3.1.1, p. 31]` — passage lu.
- `[Web — titre, domaine, consulté le AAAA-MM-JJ]`.
- `[Base QA-0007, statut à évaluer]`.
- « Interprétation : … » / « Hypothèse : … » pour ce qui vient du raisonnement.

## Quand dire « je ne sais pas »

Aucune source locale ni Web fiable, sources contradictoires sans arbitrage possible,
extraction défaillante du document utile (voir `inventaire`) : le dire, indiquer ce qui
manque (document à importer, version, terme à préciser).
