# Essais de bout en bout des agents (Thomas, Sylvie)

Questions posées en conditions réelles (`claude -p --agent …`) par `scripts/essais_agents.py`
sur `eval/essais.json`. Réponses complètes et commandes exécutées :
`eval/essais-resultats/<date>/<id>.md`. Le harnais vérifie automatiquement que chaque
citation « §x, p. N » (ou « pp. N-M ») correspond à une page **lue** pendant la
conversation ; une référence que l'agent déclare lui-même non lue (ou lue en partie) dans
« Confiance », « Limites », « Traçabilité » ou « Sources retenues » n'est pas une citation.
Les essais tournent avec les permissions réelles du dépôt (règles `allow` de
`.claude/settings.json`, aucune écriture pré-approuvée) sur une copie temporaire des
données (`QAK_RACINE`). Le jugement de fond ci-dessous est humain.

Les tableaux d'une campagne qui désigne ses fichiers (« Fichiers : `eval/…/<date>/` »)
reprennent les en-têtes de ces fichiers ; `tests/test_essais.py` vérifie l'accord (#178).
Les tableaux plus anciens sont historiques : leurs fichiers ont pu être régénérés depuis.

## Campagne du 2026-10-22 (main après #17)

| Essai | Agent | Tours | Coût | Confiance annoncée | Citations lues | Web | Verdict |
|---|---|---|---|---|---|---|---|
| T1 couverture des tests | Thomas | 6 | 0,16 $ | 90 | 8/9 | 0 | Bon : pistes CTFL §4.2-4.4, TTA §2.8, CT-AI §3.4.3 ; 1 citation non lue (CTAL-AT §3.1) |
| T2 RBT en équipe agile | Thomas | 5 | 0,15 $ | 82 | 3/3 | 0 | Bon |
| T3 maintenance Playwright | Thomas | 6 | 0,14 $ | **95** | 4/4 | **0** | Principes ISTQB justes et lus, liens Playwright signalés comme interprétation ; **mais** Web non fait alors que justifié, confiance gonflée → #49, #18 |
| T4 processus de qualification | Thomas | 5 | 0,13 $ | 70 | 4/5 | 0 | Bon : hypothèse de lecture explicitée, IDEAL, TMMi/TPI, rétrospectives ; 1 citation non lue |
| T5 priorisation des tests | Thomas | 4 | 0,11 $ | 90 | 3/3 | 0 | Très bon : tableau comparatif CTFL §5.1.5 / CTAL-TM §1.3.4-1.3.5 |
| T6 thèmes pauvres de la base | Thomas | 5 | 0,08 $ | 80 | — | 0 | Juste : constate que la base d'idées est vide, propose les thèmes riches en syllabus |
| S1 démarche RBT (cas d'usage) | Sylvie | 9 | 0,17 $ | 82 | 9/10 | 0 | Très utile : 4 pratiques, verdicts sourcés (CTAL-TM §1.3.2-1.3.6, CTFL §5.2.3-5.2.4), 8 manques, niveau 1 justifié, chemin vers le niveau 2 ; défauts : vocabulaire « Conforme », confiance non reproductible, section lue partiellement → #30, #18, #22 |
| S2 100 % automatisé Playwright | Sylvie | 7 | 0,16 $ | 72 | 6/6 | 0 | Bon : écart sur « 100 % » et « supprimer le manuel », Playwright « Hors ISTQB » |

**Synthèse** : 8 réponses utiles, au format demandé (pistes par syllabus, tableaux, « où
creuser », « à capitaliser » sans enregistrement), coût moyen ≈ 0,14 $. 37 citations sur
40 correspondent à une page lue ; les 3 autres renvoient à des passages vus seulement en
extrait de recherche (règle « lire avant de citer » imparfaitement suivie). Aucune
recherche Web, y compris quand elle était justifiée (T3). Les scores de confiance ne sont
pas reproductibles. Défauts suivis dans les issues #18, #22, #30, #49.

## Campagne du 2026-10-22 (bis) : mise en place par domaine et mode conversationnel (#90, #91, #92)

> Chiffres du premier passage. Les fichiers de `2026-10-22/` ont été régénérés depuis : chiffres à jour dans la campagne du 2026-10-23 (#178).

Nouveaux essais `M*` (mise en place par domaine), `S3` (audit en domaine réglementé) et
`C1` (question volontairement ambiguë, skill seul en `claude -p`). Chaque essai porte des
`criteres` contrôlés par `controler()` dans `scripts/essais_agents.py` : méthode en ≥ 4
étapes, chaque étape sourcée (« § ») ou marquée interprétation, exemple fictif, domaines
du tableau, questions de cadrage / à choix, hypothèses explicites, couverture absente
signalée, mentions attendues, confiance.

| Essai | Agent | Tours | Coût | Confiance | Citations lues | Web | Critères | Verdict |
|---|---|---|---|---|---|---|---|---|
| M1 RBT en agile (sans domaine) | Thomas | 7 | 0,17 $ | 80 | 11/11 | 0 | 11/11 | Bon : 7 étapes sourcées (CTFL-AT §3.2.1, CTFL §5.1.2, CTAL-AT §3.1.1, CTAL-TA §2.1.1-2.2, CTAL-TM §1.3.6), exemple Scrum fictif, tableau des 5 domaines (repères signalés « non lus »), questions à choix. Remplace l'exemple 1 de `exemples-conversations.md` |
| M2 dispositif médical | Thomas | 6 | 0,16 $ | 55 | 9/9 | 1 | 7/7 | Bon et honnête : traçabilité (CTFL §1.4.4, CT-FT §3.3) + RBT (CTAL-TM §1.3) ; dit qu'aucun syllabus ne couvre IEC 62304 / ISO 14971, Web (sources secondaires) signalé et confiance abaissée |
| M3 web e-commerce | Thomas | 11 | 0,20 $ | 66 | 5/5 | 1 | 6/6 | Bon : CT-TAS §1.1, §3.1.1, §4.1, CTAL-AT §1.4, §3.1.2 ; « pas de syllabus web dédié, principes transposés » ; Web marginal et signalé |
| M4 embarqué / intégration matériel | Thomas | 10 | 0,18 $ | 68 | 5/5 | 0 | 7/7 | Bon : CT-AuT (niveaux ISO 26262 / ASPICE, XiL/HiL), CTEL-TM 2011 §8.3.3 (labo d'intégration, prototypes), CTAL-TTA §4.1 ; aucun syllabus industriel |
| M5 mobile iOS / Android | Thomas | 14 | 0,20 $ | 68 | 12/13 | 0 | 6/6 | Très bon : CT-MAT 2019 dédié (§1.1, §1.6, §1.8, §4-5) ; 1 citation non lue (CTAL-TAE §4.2.1 EN) |
| M6 API REST multi-équipes | Thomas | 19 | 0,22 $ | 80 | 11/11 | 0 | 7/7 | Bon : contrat versionné en CI (CT-QDO §3.2.2), alignement des équipes (CTAL-TM §1.4.2), performance (CT-PT §3.2) ; choix consommateur/fournisseur marqué interprétation |
| S3 audit, dispositif médical | Sylvie | 6 | 0,15 $ | 72 | 6/7 | 0 | 5/5 | Utile : analyse de risques unique = **Écart** (CTAL-TA §2.1, CTAL-TM §1.3.1), traçabilité incomplète, niveau 1 ; normes du domaine « non vérifiables ici » ; questions à choix ; 1 citation non lue (CTFL §2.2.3) |
| C1 « Comment on gère les risques ? » | skill | 4 | 0,12 $ | 82 | 1/1 | 0 | 3/3 | Conforme à #92 en `-p` : « **Hypothèse :** risques produit/qualité » en tête, ne bloque pas, « Questions à choix » (criticité a/b/c, besoin a-d) en fin |

**Avant correctif** (premier passage, conservé en `*-avant-correctif.md`) : M1 (6/11) et M4
(4/7) étaient traités comme des questions de connaissance (pistes, pas de méthode ni
d'exemple) parce que « comment l'ISTQB propose-t-il d'intégrer… » et « comment organiser… »
n'étaient pas reconnus comme des questions de mise en place ; C1 (1/3) posait des
questions ouvertes sans hypothèse ni options. Corrigé dans cette PR (détection élargie
dans `strategie.md`, `SKILL.md`, `thomas.md` ; hypothèse en tête et questions de cadrage
**à choix**), puis relancé.

**Citations non lues (#127)** : M5 (CTAL-TAE §4.2.1 EN) et S3 (CTFL §2.2.3) citaient une
page vue seulement en extrait de recherche. Correctif : « contrôle avant d'envoyer »
(chaque référence doit avoir son `lire`/`section`/`page`, sinon lue ou retirée) dans le
skill, Thomas et Sylvie ; `essais_agents.py` marque désormais l'essai **en échec** (code
retour 1) dès qu'une citation n'a pas été lue. Relance : M5 10/10 citations lues (0,20 $),
S3 5/5 (0,16 $), tous critères satisfaits ; les fichiers M5 et S3 sont ceux de la relance.

### Couverture de la bibliothèque par domaine

| Domaine | Couvert par | Non couvert (dit par l'assistant) |
|---|---|---|
| Santé / réglementé | principes : CTAL-TM v3.0 §1.3, CTFL v4.0.1 §1.4.4, CTAL-TTA v4.0 §2.8.2 (niveaux d'intégrité), CTEL-TM 2011 §8.3.4, CT-FT (conformité, finance) | **aucun syllabus santé / dispositif médical** ; IEC 62304, ISO 14971 absents → Web ou import du texte des normes |
| Web | CT-TAS v1.0, CTAL-AT v2.0, CT-PT 2018 §3.2, CT-MAT §2.2.4 (web apps) | **aucun syllabus web dédié** : principes transposés |
| Embarqué / intégré | CT-AuT v2.1.1 (automobile, EN), CTEL-TM 2011 §8.3.3 (EN, ancien), CTAL-TTA §4.1 | rien d'industriel, ferroviaire ou aéronautique (DO-178C seulement cité) ; anglais seulement |
| Mobile | CT-MAT 2019 (FR + EN), dédié | version 2019 : aucun outil actuel |
| API | CTAL-TTA v4.0 §2.7, CT-QDO v1.0 §3.2.2 (contrat, EN seulement), CTAL-TAE v2.0 §5.1.3, CT-PT | **aucun syllabus API dédié** |

Ces manques ne figurent pas dans `manquants` : ce n'est pas un syllabus ISTQB absent
(les 26 codes du catalogue sont présents en anglais), mais un domaine que l'ISTQB ne
couvre pas. Pour aller plus loin : importer un document non ISTQB (`/ajouter-syllabus`
avec le fichier, cité comme « non ISTQB ») ou recherche Web justifiée.

**Coût** : 11 essais (8 + 3 relances) ≈ 2,06 $, soit ≈ 0,19 $ par essai.
Relancer : `python scripts/essais_agents.py M S3-reglemente C1-ambigu` (préfixe accepté).

## Campagne du 2026-10-22 (ter) : citations déclarées non lues, sorties tronquées (#139, #140, #142)

La relance sur `main` (a9ddcd7) donnait 3 échecs sur 16 :
- **S1-rbt** : un faux positif du harnais (#139). Les références que Sylvie déclare elle-même « non lue » ou « non citée » dans « Confiance » ou « Traçabilité » étaient comptées comme des citations.
- **S3-reglemente** : de vraies citations non lues. `section CTAL-TM-3.0-fr 1.3 | head -150` coupe la sortie avant §1.3.3 (p. 30-31), et le critère `non_couvert` manque.
- **M3-web** : « CTAL-TAS §1.1.1, p. 16 » au lieu de CT-TAS-1.0-en, une section jamais affichée.

Correctifs :
- `verifier_citations()` ignore les phrases de bilan qui déclarent une référence non lue (#139).
- Les citations « pp. N-M » sont contrôlées et ne fusionnent plus avec la référence voisine (#142). Avant, elles échappaient au contrôle.
- Dans le skill, Thomas et Sylvie (#140) :
  - jamais de `| head` sur `lire`, `section` ou `page` (`--max-caracteres` ou la sous-section précise) ;
  - ne citer que les pages affichées, avec le sigle exact du document, et chaque référence nomme son document ;
  - Sylvie ne reprend pas avec leur page les références de la grille de maturité, qu'elle n'a pas lues, et dit ce qu'aucun syllabus ne couvre.

Relances ciblées : M3 vert dès le premier passage (7/7 citations lues). S1 et S3 sont restés rouges pendant deux passages : une page CTEL-ITP §3.3.2 recopiée de la grille, une référence `[§1.3.4, p. 32]` sans document, puis la fusion « pp. » de #142. Après les consignes complétées, ils sont verts (10/10 et 11/11).

Campagne complète qui suit (fichiers de ce dossier) :

| Essai | Agent | Tours | Coût | Confiance | Citations lues | Web | Critères | Verdict |
|---|---|---|---|---|---|---|---|---|
| T1-couverture | Thomas | 9 | 0,16 $ | 88 | 6/6 | 0 | — | réussi |
| T2-rbt-agile | Thomas | 13 | 0,26 $ | 81 | 16/16 | 0 | — | réussi |
| T3-playwright | Thomas | 11 | 0,14 $ | 75 | 6/6 | 1 | — | réussi |
| T4-qualification | Thomas | 10 | 0,16 $ | 75 | 10/10 | 0 | — | réussi |
| T5-priorisation | Thomas | 6 | 0,12 $ | 83 | 3/3 | 0 | — | réussi |
| T6-lacunes | Thomas | 4 | 0,08 $ | 70 | — | 0 | — | réussi |
| S1-rbt | Sylvie | 6 | 0,12 $ | 78 | 6/6 | 0 | — | réussi (avant : ÉCHEC, faux positif) |
| S2-automatisation | Sylvie | 7 | 0,13 $ | 80 | 7/7 | 0 | — | réussi |
| M1-rbt-agile | Thomas | 11 | 0,18 $ | 66 | 7/7 | 0 | 11/11 | réussi |
| M2-sante | Thomas | 11 | 0,19 $ | 73 | 12/12 | 1 | 7/7 | réussi |
| M3-web | Thomas | 9 | 0,14 $ | 83 | 5/5 | 0 | 6/6 | réussi (avant : 12/13, sigle faux) |
| M4-embarque | Thomas | 11 | 0,17 $ | 66 | 8/8 | 0 | 7/7 | réussi |
| M5-mobile | Thomas | 13 | 0,20 $ | 80 | 12/12 | 0 | 6/6 | réussi |
| M6-api | Thomas | 14 | 0,19 $ | 81 | 9/9 | 0 | 7/7 | réussi |
| S3-reglemente | Sylvie | 8 | 0,16 $ | 72 | 14/14 | 0 | 5/5 | réussi (avant : 5/7, `non_couvert` manquant) |
| C1-ambigu | skill | 6 | 0,15 $ | 76 | 3/3 | 0 | 2/3 | **ÉCHEC** : options des questions à choix écrites en ligne → #144 |

**Synthèse** : 15 essais sur 16 réussis. 124 citations sur 124 correspondent à une page lue (`pp.` compris). Les commandes `lire`/`section`/`page` tronquées par `| head` passent de 17 sur 88 à 3 sur 122, toutes dans T3 (`lire … | head`, aucune citation hors page affichée). Le seul échec, C1, est un défaut de format sans lien avec les citations (#144).

**Coût** : campagne complète 2,57 $, plus 7 relances ciblées 1,09 $, soit 3,66 $.

## Questions à choix : une option par ligne (#144)

La consigne (`reference/conversation.md`) impose désormais une question par puce et ses
options numérotées une par ligne. L'exemple du §1 et le gabarit « mise en place » de
`strategie.md`, qui titrait « Questions de cadrage », sont alignés. Relance des trois essais
qui exigent `questions_choix` :

| Essai | Avant | Après |
|---|---|---|
| C1-ambigu | ÉCHEC 2/3 (options en ligne) | réussi 3/3, 4/4 citations lues (0,27 $) |
| S3-reglemente | réussi 5/5 | réussi 5/5, 12/12 citations lues (0,18 $) |
| M1-rbt-agile | réussi 11/11 | 1er passage : ÉCHEC 10/11 (titre « Questions de cadrage », repris du gabarit) ; après correction du gabarit : réussi 11/11, 5/5 citations lues (0,17 $) |

Coût : 0,82 $. Avec #144, les 16 essais de la campagne sont verts.

## Questions réelles de l'utilisateur : shift left et Gherkin

Deux questions posées telles quelles par l'utilisateur deviennent des essais versionnés :

| Essai | Question | Tours | Coût | Confiance | Citations lues | Critères | Constat |
|---|---|---|---|---|---|---|---|
| M7-shift-left | « Je veux mettre en place une démarche shift left testing, comment faire ? Qu'est-ce que cela impose ? » | 8 | 0,14 $ | 90 | 9/9 | 7/7 | Ce que ça impose (CTFL §2.1.5 : coût initial, adhésion, ne pas négliger les tests tardifs), méthode en 7 étapes sourcées (CTFL, CTAL-AT v2.0, CT-TAS), exemple fictif, adaptation par domaine, questions à choix |
| T7-gherkin | « Je veux rédiger mes critères d'acceptation en Gherkin, j'ai besoin d'aide. » | 11 | 0,16 $ | 90 | 9/9 | 4/4 | Formats de CTFL §4.5.2, règles d'écriture (CT-AcT §2.2.2, CTAL-ATT §2.1.2 signalé en retrait), Example Mapping (CTAL-AT §4.1.3), exemple Gherkin en français, propose de réécrire un critère de l'utilisateur |

Premier passage de M7 en échec : une citation écrite « CTAL-TAS » au lieu de CT-TAS (6/7). La relance est verte ; le défaut récurrent est suivi dans #172.

## Campagne complète du 2026-10-23 (main a93d3fb, avant diffusion)

Tous les essais sur `main` après le lot « avant diffusion » (#156, #158, #159, #161, #163,
#165, #166, #174). Fichiers : `eval/essais-resultats/2026-10-23/`. Ces chiffres remplacent ceux
des tableaux du 2026-10-22, dont les fichiers ont été régénérés depuis (#178).

| Essai | Agent | Tours | Coût | Confiance | Citations lues | Web | Critères | Verdict |
|---|---|---|---|---|---|---|---|---|
| T1-couverture | thomas | 9 | 0,168 $ | 88 | 8/8 | 0 | — | réussi |
| T2-rbt-agile | thomas | 8 | 0,148 $ | 81 | 6/6 | 0 | — | réussi |
| T3-playwright | thomas | 12 | 0,158 $ | 68 | 7/7 | 1 | — | réussi |
| T4-qualification | thomas | 13 | 0,168 $ | 96 | 12/12 | 0 | — | réussi |
| T5-priorisation | thomas | 7 | 0,111 $ | 83 | 3/3 | 0 | — | réussi |
| T6-lacunes | thomas | 4 | 0,079 $ | 70 | 0/0 | 0 | — | réussi |
| S1-rbt | sylvie | 10 | 0,189 $ | 70 | 10/10 | 0 | — | réussi |
| S2-automatisation | sylvie | 7 | 0,149 $ | 72 | 11/12 | 0 | — | **ÉCHEC** : citation non lue : CTAL-TA §1.2.4, p. 17 |
| M1-rbt-agile | thomas | 12 | 0,174 $ | 81 | 6/6 | 0 | 11/11 | réussi |
| M2-sante | thomas | 9 | 0,196 $ | 73 | 11/11 | 1 | 7/7 | réussi |
| M3-web | thomas | 10 | 0,138 $ | 83 | 8/8 | 0 | 6/6 | réussi |
| M4-embarque | thomas | 9 | 0,172 $ | 67 | 6/6 | 0 | 7/7 | réussi |
| M5-mobile | thomas | 14 | 0,279 $ | 69 | 13/14 | 3 | 6/6 | **ÉCHEC** : citation non lue : CTAL-TAE §4.2.1, lu en partie (le reste est à la p. 35 |
| M6-api | thomas | 12 | 0,183 $ | 79 | 10/10 | 0 | 7/7 | réussi |
| S3-reglemente | sylvie | 6 | 0,138 $ | 62 | 9/9 | 0 | 5/5 | réussi |
| C1-ambigu | skill | 6 | 0,272 $ | 79 | 5/5 | 0 | 3/3 | réussi |
| M7-shift-left | thomas | 11 | 0,167 $ | 90 | 10/10 | 0 | 7/7 | réussi |
| T7-gherkin | thomas | 12 | 0,162 $ | 80 | 9/9 | 1 | 4/4 | réussi |

**Synthèse** : 16 essais sur 18 réussis, 144 citations sur 146 lues, coût 3,05 $.
Les deux échecs sont mineurs. M5 est un faux positif du contrôle : une lecture partielle déclarée
dans « Sources retenues » est comptée comme une citation (#181). S2 contient une vraie entorse :
une référence « vue en extrait seulement » est citée entre crochets malgré la règle (#182).

## Relance ciblée du 2026-10-25 (main d73630d : #157, #172, #181, #182)

Relance des essais touchés par le lot : M5 et S2 (échecs du 2026-10-23), M3, M7 et S3
(sigle reconstruit, #172). Fichiers : `eval/essais-resultats/2026-10-25/`. Premiers
passages, aucune relance nécessaire.

| Essai | Agent | Tours | Coût | Confiance | Citations lues | Web | Critères | Verdict |
|---|---|---|---|---|---|---|---|---|
| S2-automatisation | sylvie | 8 | 0,164 $ | 74 | 10/10 | 0 | — | réussi (23/10 : ÉCHEC, 11/12) |
| M3-web | thomas | 9 | 0,191 $ | 83 | 7/7 | 0 | 6/6 | réussi (23/10 : réussi, 8/8) |
| M5-mobile | thomas | 8 | 0,164 $ | 72 | 8/8 | 0 | 6/6 | réussi (23/10 : ÉCHEC, 13/14) |
| S3-reglemente | sylvie | 4 | 0,133 $ | 62 | 11/11 | 0 | 5/5 | réussi (23/10 : réussi, 9/9) |
| M7-shift-left | thomas | 8 | 0,162 $ | 90 | 9/9 | 0 | 7/7 | réussi (23/10 : réussi, 10/10) |

**Synthèse** : 5 essais sur 5 réussis, 45 citations sur 45 lues (avant : 3 sur 5, 49/53).
Aucun sigle reconstruit (« CTAL-TAS » : 0 occurrence) ; 69 des 77 références entre crochets
sont la copie exacte d'une ligne `Citer :` affichée (les autres regroupent des pages, `pp. N-M`). Aucune référence vue en extrait
entre crochets : S2 renvoie à « Où creuser ensuite ». Les essais ont tourné sans
écriture pré-approuvée, sur une copie des données ; les permissions réelles suffisent
(aucune commande de lecture refusée). Coût : 0,81 $.

## Relancer

```bash
python qa.py actualiser                       # index à jour
python scripts/essais_agents.py               # tous les essais (16, ≈ 2,60 $, ≈ 30 min)
python scripts/essais_agents.py S1-rbt        # un seul
python scripts/essais_agents.py M             # par préfixe : tous les essais M…
python scripts/essais_agents.py --fidelite S3-reglemente   # + juge LLM de fidélité, indicatif (#152)
```
