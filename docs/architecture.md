# Architecture et choix techniques

## Vue d'ensemble

```
Conversation Claude Code
        │  (le skill .claude/skills/qa-knowledge/SKILL.md décrit QUAND et COMMENT)
        ▼
python qa.py <commande>          ← une seule CLI, sortie texte FR (ou --json)
        │
        ├── Bibliothèque ISTQB ─────────────────────────────────────────────
        │     catalogue/istqb.json        catalogue officiel (26 syllabus, URL istqb.org)   [versionné]
        │     bibliotheque/sources/       PDF / .txt / .md (≈ 33 Mo)                        [versionné]
        │     bibliotheque/manifeste.json métadonnées par empreinte SHA-256                 [versionné]
        │     bibliotheque/index.db       SQLite : documents, sections, passages + FTS5     [reconstructible]
        │
        ├── Base de connaissances ───────────────────────────────────────────
        │     connaissances/connaissances.jsonl  une idée par ligne (miroir lisible)        [versionné]
        │     connaissances/journal.jsonl        journal append-only des modifications      [versionné]
        │     connaissances/base.db              SQLite + FTS5, reconstruit depuis le JSONL [reconstructible]
        │
        └── Référentiels ────────────────────────────────────────────────────
              referentiel/taxonomie.json   41 thèmes hiérarchiques + mots-clés FR/EN       [versionné]
              referentiel/thesaurus.json   ~130 concepts, ~1000 termes FR↔EN              [versionné]
```

Modules (`qak/`) : `extraction` (PDF → pages, plan, passages) · `bibliotheque` (import,
métadonnées, doublons, versions, index) · `catalogue` (istqb.org) · `recherche` (FTS5 +
thésaurus + reclassement) · `connaissances` (idées, déduplication, références vérifiées) ·
`taxonomie` · `journal` · `evaluation` · `cli`.

Aucun serveur réseau, aucune interface graphique, aucune clé d'API. Dépendance unique : `pypdf`.

`serveur_mcp` (#153, optionnel, SDK `mcp` de `requirements-mcp.txt`) : `python qa.py mcp`
expose les commandes de lecture sur stdio à tout client MCP. Chaque outil appelle
`cli.main()` et renvoie sa sortie texte (aucune logique dupliquée) ; les passages affichés
par `lire` / `section` / `page` sont relevés (`cli.LECTURES`) et consultables par l'outil
`passages_lus`. Aucune écriture n'est exposée.

## Choix et compromis

| Sujet | Choix | Pourquoi / compromis |
|---|---|---|
| Point d'entrée | **Un skill** + une CLI | Le skill porte la méthode (ordre de recherche, citations, capitalisation) ; la CLI porte les garanties (vérifications, déduplication, journal). Pas de sous-agent : rien ne le justifie aujourd'hui, et il perdrait le contexte de la conversation. |
| Stockage | **SQLite** (stdlib) | Local, sans service, transactionnel, FTS5 intégré. |
| Recherche | **FTS5 BM25 + thésaurus FR/EN + reclassement par couverture** | Les syllabus sont un vocabulaire contrôlé : la recherche lexicale suffit si l'on traduit les concepts (FR → EN). Voir « Mesures ». |
| Fautes de frappe, mots coupés | **Correction ciblée + recollage à l'extraction** (#106) | Un mot de la question absent à la fois de l'index et du thésaurus est remplacé par le mot connu le plus proche (difflib ≥ 0,8 sur les mots du thésaurus, ≥ 0,85 sur le vocabulaire `fts5vocab` de l'index ; mot de 4 lettres : une seule édition, transposition comprise, vers un mot du thésaurus, sans ex æquo — « tets » → « tests », #166), avec avertissement ; un mot connu n'est jamais touché, donc aucune question bien orthographiée ne change. Les fragments « utilisabilit é » sont recollés dans les passages quand le mot réuni existe dans le document et qu'un fragment n'est pas un mot (3 136 → 662 coupures probables). Pas de table `trigram` : la correction suffit sur le jeu, et le repli n'aurait servi qu'aux requêtes sans résultat. |
| Recherche sémantique | **Évaluée (#107), non retenue** — prototype optionnel conservé (`qak/semantique.py`, `requirements-semantique.txt`, `actualiser --semantique`, `chercher/evaluer --semantique`), désactivé par défaut | Mesure ci-dessous : la fusion hybride BM25 + cosinus (RRF) gagne une question de contrôle mais en perd une de réglage, et ne résout aucune des questions formulées loin du vocabulaire ISTQB (jeu « éloigné ») ; coût : 1,4 Go de dépendances (torch CPU), modèle 470 Mo, 12 s de chargement par commande. |
| Versionnement de la base | **JSONL miroir** + SQLite de travail | Un `.db` binaire se fusionne mal dans Git. Le JSONL (une idée par ligne, trié) donne des diffs lisibles ; après un `git pull`, l'empreinte du JSONL change et la base est reconstruite automatiquement. |
| PDF sources | **Versionnés** (≈ 33 Mo) | Un clone suffit pour travailler hors ligne, et les traductions françaises fournies à la main ne se perdent pas. La notice publique n'autorise que des extraits : les PDF sont versionnés avec l'autorisation obtenue par le mainteneur auprès de l'ISTQB, du CFTL et de la TMMi Foundation (voir NOTICE.md) ; le manifeste cite la source. Le manifeste garde les métadonnées et retrouve chaque fichier par empreinte. |
| Pages | **Page physique du PDF** + page imprimée si différente | La page physique est non ambiguë (c'est celle qu'ouvre un lecteur PDF) ; la page imprimée (« Page 12 de 80 ») est conservée quand elle diffère. Un passage ne franchit jamais une page. |
| Sections | Signets PDF si numérotés, sinon **plus longue chaîne de titres à numérotation cohérente** | Les syllabus FR n'ont souvent pas de signets. La programmation dynamique écarte les listes numérotées du préambule ; les titres répétés par les objectifs d'apprentissage sont écartés au profit du vrai titre. Un signet non numéroté sous une section (« Mots-clés », « Introduction ») est un intertitre : sans numéro, visible dans `plan --tout` seulement, ses passages restent dans la section numérotée (#210). |
| Taxonomie | Fichier JSON, codes stables, statut `obsolete` + `remplace_par` | Un thème n'est jamais supprimé ; les idées gardent leur classement historique et les requêtes suivent le remplaçant. |
| Déduplication | Signature = concepts du thésaurus + racines, + thème principal commun et noms propres partagés | « Partitions d'équivalence » et « Equivalence partitioning » ont la même signature ; un nom propre absent du thésaurus partagé par les deux titres (Herzberg) pèse fortement, le thème principal commun un peu ; seuil 0,6 = doublon probable (bloquant), 0,35 = proche (signalé). |
| Références ISTQB | **Vérifiées à l'écriture** | Document présent, page existante, section présente sur les pages citées, extrait recopié mot pour mot (suite contiguë du texte normalisé, ≥ 6 mots significatifs, espaces parasites des PDF recollés) : une citation inventée, inversée ou en vrac est refusée par l'outil, pas seulement déconseillée par le skill. Limite : une citation exacte mais sortie de son contexte n'est pas détectable. |

## Mesures de la recherche (bibliothèque réelle : 42 fichiers, 26 codes EN + 14 FR)

`python qa.py evaluer --jeu reglage|controle|eloigne|examens` — rappel@5 = la réponse attendue
(code + section) figure dans les 5 premiers résultats. La CI exige `evaluer --jeu controle --min-rappel 0.80`
(code retour 2 sous le seuil, ou si aucune question n'a pu être évaluée).

| Version du moteur | Jeu de réglage (36 q.) | Jeu de contrôle (jamais utilisé pour régler ; taille entre parenthèses) |
|---|---|---|
| FTS5 + thésaurus, « ET strict puis OU » | 75 % | — |
| + reclassement par couverture, concepts scindés, lexique FR→EN | 94 % | — |
| + rétrogradation annexes / notes de version | 100 % (MRR 0,82) | 88 % (MRR 0,76) |
| contrôle élargi à 18 q. (issue #4 : « shift-left », maintenance de l'automatisation) — avant correctif | 100 % (MRR 0,81) | 83 % (MRR 0,69) |
| + priorité aux sections dont le titre nomme la notion, thésaurus « maintainability » | 100 % (MRR 0,91) | 89 % (16/18, MRR 0,81) |
| Lot du 2026-10-22, mesures avant → après de chaque PR, questions de l'issue ajoutées au contrôle AVANT la correction : | | |
| #42 sigles de 2 lettres et IDEAL seulement en MAJUSCULES | 100 % → 100 % | 86 % → 91 % (22 q.) |
| #43 erreur / défaut / défaillance / anomalie séparés, « différence » générique | 100 % → 100 % | 88 % → 92 % (24 q.) |
| #45 TPI, CTP, STEP, modèle de maturité générique | 100 % → 100 % | 88 % → 92 % (25 q.) |
| #26 « motivation » distinct de « compétences » | 100 % → 100 % | 83 % → 92 % (24 q.) |
| #25 §0.x d'introduction rétrogradés (fraîcheur mesurée, non retenue) | 100 % → 100 % | 84 % → 84 % (25 q.) |
| #47 « layering » ↔ « superposition / couches » | 100 % → 100 % | 88 % → 88 % (25 q.) |
| #106 fautes de frappe corrigées, mots coupés recollés à l'extraction | 100 % (0,91) → 100 % (0,92) | 72 % → 82 % (40 q.) |
| #165 titre de section identique à la question (signature puis mots), « partitionnement d'équivalence » au thésaurus | 100 % (0,92) → 100 % (0,94) | 79 % (34/43, 0,70) → 88 % (38/43, 0,79) |
| #166 faute de frappe sur un mot de 4 lettres (« tets ») | 100 % (0,94) → 100 % (0,94) | 84 % (38/45, 0,75) → 89 % (40/45, 0,78) |
| #177 extraction : introduction de chapitre rattachée au chapitre et non à sa 1re sous-section (17 titres replacés, éloigné 20 % → 20 %) | 100 % (0,94) → 100 % (0,94) | 89 % (40/45, 0,78) → 89 % (40/45, 0,78) |
| #180 pluriels en « -es » : même racine que le singulier (« exploratoires »), mots en « -ss » gardés (éloigné 20 % → 20 %) | 100 % (0,94) → 100 % (0,94) | 87 % (40/46, 0,76) → 89 % (41/46, 0,77) |
| #196 « -ie » et « -ies » → « -y » : « stratégie(s) » et « strategy/strategies » ont la même racine (aucune question du contrôle n'échouait sur ce point ; mêmes classements sur les trois jeux, éloigné 20 % → 20 %) | 100 % (0,94) → 100 % (0,94) | 89 % (41/46, 0,77) → 89 % (41/46, 0,77) |
| #210 extraction : intertitres de signets sans numéro propre (passages rattachés à la section numérotée), signet numéroté en double écarté (27 numéros en double → 0 ; mêmes classements sur les trois jeux, éloigné 20 % → 20 %) | 100 % (0,94) → 100 % (0,94) | 89 % (41/46, 0,77) → 89 % (41/46, 0,77) |
| #209 participes : masculin, féminin, singulier et pluriel ont la même racine (« défini/définie » → « definy », « intégré/intégrée » → « integr », « vérifié/vérifiée » → « verify ») ; question « approche d'équipe intégré » ajoutée au contrôle avant correctif (éloigné 20 % → 20 %) | 100 % (0,94) → 100 % (0,94) | 87 % (41/47, 0,75) → 89 % (42/47, 0,77) |
| #220 extraction : ligne du titre d'un signet cherchée sans espaces (« 2.1 Whole T eam Approach ») ; 22 titres du CTAL-AT v2.0 EN replacés sur leur vraie ligne, l'introduction ne passe plus sous la 1re sous-section (« coût de maintenance des tests automatisés » rang 3 → 4, toujours trouvée ; éloigné 20 % → 20 %) | 100 % (0,94) → 100 % (0,95) | 89 % (42/47, 0,77) → 89 % (42/47, 0,77) |
| **État actuel** (moteur lexical ; #59 : mêmes classements, ≈ 8 × plus rapide) | **100 % (MRR 0,95)** | **89 % (42/47, MRR 0,77)** |

Le 100 % du jeu de réglage est optimiste par construction ; le chiffre honnête est celui
du jeu de contrôle. Les questions ajoutées au contrôle l'ont été AVANT la correction qu'elles
motivent ; le contrôle est passé de 18 à 47 questions, en grande partie des questions
difficiles issues des revues (fautes de frappe, questions de Test Manager, formulations loin
du vocabulaire ISTQB) : sa baisse de 89 % à 82 % (avant #165) vient de ces ajouts, pas d'une régression
(chaque PR a été mesurée avant/après sur le même jeu). Les 5 échecs actuels :
- requêtes très courtes faites de mots omniprésents (« principes du test », « contenu d'un
  plan de test ») : avec le terme ISTQB anglais (« testing principles », « purpose and
  content of a test plan ») la bonne section sort en 1re ou 2e position — le skill demande
  d'ajouter le terme anglais quand il est connu ;
- « rapport d'avancement des tests parties prenantes », « comment estimer l'effort de
  test » : arbitrages laissés ouverts dans #25 ;
- « architecture en couches d'un framework d'automatisation » : §3.1.3 n'emploie pas
  « architecture » (#47).

#165 : à couverture et titre égaux, une section dont le titre a la même signature que la
question (concepts du thésaurus + racines : « Exploratory Testing » pour « tests
exploratoires ») passe devant celles qui nomment seulement le même concept (« Session-Based
Test Management (SBTM) »), puis, parmi elles, le titre écrit avec les seuls mots de la
question. Égalité stricte et non proximité : un critère de proximité (Jaccard) faisait
passer « motivation » du rang 1 au rang 5 (titres courts favorisés contre BM25).

Temps : une recherche ≈ 50 ms de calcul (0,2-0,45 s pour la commande complète) ; import initial ≈ 3 s par syllabus (≈ 2-3 min pour 42) ;
actualisation sans changement < 1 s.

### Jeu « examens » : questions des examens blancs officiels (#150, 2026-10-28)

`python qa.py evaluer --jeu examens` lit `eval/examens.json` (fichier à part, hors seuil de la
CI, jamais utilisé pour régler le moteur) : 135 questions, une par question des examens blancs
ISTQB CTFL v4.0 A v1.7 (40), CTAL-TM v3.0 A v1.3.3 (50) et CTAL-TA v4.0 v4.1 (45). Chaque
question est reformulée en requête courte en français (l'énoncé n'est pas recopié) ; la vérité
terrain est l'objectif d'apprentissage donné par le corrigé officiel, ramené à la section la
plus profonde du plan (FL-4.2.1 → CTFL §4.2.1, FL-1.3.1 → CTFL §1.3 ; numérotation des
objectifs vérifiée sur les syllabus : elle suit celle des sections). Les corrigés se
téléchargent sur istqb.org (pages des certifications) et ne sont pas versionnés. Une seule
réponse attendue par question : un autre syllabus qui traite le même sujet ne compte pas,
ce jeu est donc plus sévère que le contrôle.

Ligne de base (moteur lexical inchangé) :

| Jeu | Rappel@5 | MRR |
|---|---|---|
| Réglage (36 q.) | 100 % (36/36) | 0,95 |
| Contrôle (47 q.) | 89 % (42/47) | 0,77 |
| Éloigné (5 q.) | 20 % (1/5) | 0,20 |
| **Examens (135 q.)** | **47 % (64/135)** (rappel@10 : 59 %) | **0,37** |
| — dont CTFL v4.0 (40 q.) | 20 % (8/40) | 0,12 |
| — dont CTAL-TM v3.0 (50 q.) | 58 % (29/50) | 0,47 |
| — dont CTAL-TA v4.0 (45 q.) | 60 % (27/45) | 0,47 |

Lecture : le CTFL v4.0 n'existe qu'en anglais dans la bibliothèque, et une question posée en
français fait remonter les syllabus français qui traitent le même sujet (CTFL-AT, CTAL-TA,
CTAL-TM FR) ; les questions d'examen sont aussi des mises en situation (« le site est tombé
deux jours », « vanne ouverte à 9 bars ») loin du vocabulaire des titres. Ce jeu sert de
réservoir : une question qui en est tirée passe au contrôle (ou au jeu éloigné) AVANT tout
correctif qu'elle motive.

### Reformulation de la question par l'agent avant `chercher` (#151, 2026-10-28) : retenue

Le jeu éloigné est passé de 5 à **20 questions** : 15 questions du jeu « examens » formulées
en mots de métier ou en mise en situation, toutes en échec, ajoutées AVANT la consigne
(éloigné 20 % (1/5) → 5 % (1/20), moteur inchangé). Consigne ajoutée au skill qa-knowledge
(étape 2, « Reformuler avant de chercher ») : 2 ou 3 requêtes courtes en vocabulaire ISTQB,
au moins une en anglais et une en français, lancées en plus de la question. Le moteur n'est
pas modifié.

Mesure : `python scripts/mesure_reformulation.py --jeux eloigne controle reglage examens
--passages 3` donne la consigne (lue dans le skill) à `claude -p` (modèle par défaut de la
CLI, sans outil, lots de 20 questions), puis passe chaque requête par `chercher`. Indicateur
principal : fusion des listes (question + reformulations) par rang réciproque (RRF), 5
passages gardés, même budget que `evaluer` ; secondaire : « une requête suffit » (la section
attendue est dans les 5 premiers d'au moins une requête, l'agent lisant chaque liste).
3 passages, moyenne [extrêmes] ; reformulations enregistrées dans
`eval/reformulation-resultats/2026-10-28.json` (`--rejouer` recalcule sans repayer). Coût :
1,04 $.

| Jeu | Question seule | Reformulation, RRF 5 passages | Une requête suffit |
|---|---|---|---|
| **Éloigné (20 q.)** | 5 % (1/20) | **58 %** [11-12/20] | 68 % [13-14/20] |
| Contrôle (47 q.) | 89 % (42/47) | 91 % [41-44/47] | 97 % [45-46/47] |
| Réglage (36 q.) | 100 % | 100 % [36-36] | 100 % |
| Examens (135 q.) | 47 % (64/135) | 68 % [90-94/135] | 88 % [117-119/135] |

**Décision : retenue.** Gain net sur le jeu éloigné (+53 points en moyenne, chacun des 3
passages ≥ 11/20) et sur les examens (+21 points), réglage inchangé, contrôle en hausse en
moyenne. Un passage sur trois perd 1 question de contrôle sous RRF (41/47) : sur les
questions déjà au rang 2 (« amélioration du processus de test en agile »), les
reformulations font remonter d'autres sections ; avec « une requête suffit », aucune perte
(la question d'origine reste lancée). Restent en échec au jeu éloigné notamment
« les développeurs ne lisent pas nos rapports de bugs », « le site est tombé deux jours »,
« compétences pour une plateforme de jeux en ligne ».

## Critères d'acceptation (vérifiables)

| # | Critère | Vérification |
|---|---|---|
| 1 | Import PDF/txt/md, texte extrait, sources conservées | `tests/test_extraction.py`, `test_bibliotheque.py` ; `inventaire` |
| 2 | Métadonnées (titre, code, niveau, domaine, version, langue, date, source, chemin) | `inventaire --json`, `manifeste.json` ; détection testée sur les titres réels FR |
| 3 | Pages et sections préservées, jamais de passage à cheval sur deux pages | `test_passages_ne_franchissent_pas_les_pages…` |
| 4 | Doublons exacts et changements de version détectés | `test_doublon_exact…`, `test_nouvelle_version_remplace…` ; doublon ATLaS réel écarté |
| 5 | Extractions défaillantes signalées (scan, encodage, corrompu, absent) | `test_pdf_sans_texte…`, `test_fichier_corrompu…`, `inventaire` (« À surveiller ») |
| 6 | Indexation incrémentale, réutilisable, reconstructible | `test_actualisation_incrementale…`, `test_index_reconstructible…` |
| 7 | Recherche par mots-clés, concepts/synonymes FR↔EN, thème, section, versions applicables | `tests/test_recherche.py` ; `evaluer` |
| 8 | Retour aux passages d'origine (lecture page / section / contexte) | `lire`, `page`, `section` ; `test_lire_passage…` |
| 9 | Base de connaissances avec tous les champs demandés, identifiant stable | `docs/schema.md`, `test_connaissances.py` |
| 10 | Déduplication avant insertion, mise à jour plutôt que création | `test_doublon_reformule…`, `test_doublon_detecte_entre_francais_et_anglais` |
| 11 | Taxonomie hiérarchique, multi-thèmes, sans redondance, historique conservé | `tests/test_taxonomie.py` |
| 12 | Modifications explicites et traçables | `journal`, `test_regles_de_statut` |
| 13 | Aucune référence ou page inventée | `test_references_istqb_verifiees…` |
| 14 | Recherche Web uniquement justifiée, jamais présentée comme ISTQB | règles du skill (non automatisable : relu en revue) |
| 15 | Fonctionne hors ligne une fois les documents installés | aucune dépendance réseau hors `catalogue`/`telecharger` |
| 16 | Disponibilité des sources officielles vérifiée | `test_sources_reelles.py` (vrai réseau), `catalogue --verifier` |

## Limites connues

- Les traductions françaises (CFTL) ne sont pas téléchargeables automatiquement : elles
  sont fournies par l'utilisateur. 12 codes n'existent localement qu'en anglais.
- CTEL-TM et CTEL-ITP (Expert, 2011) regroupent plusieurs modules dans un PDF : un seul code.
- Pas d'OCR : un PDF scanné est signalé « illisible », pas extrait.
- Le glossaire ISTQB (glossary.istqb.org) est une application Web sans export : non intégré ;
  les définitions se trouvent via les sections « Keywords » des syllabus.
- Les tableaux PDF sont extraits ligne à ligne (lisibles mais sans structure de colonnes).
- La recherche est lexicale : une notion absente du thésaurus et formulée autrement que
  dans le syllabus peut être manquée → ajouter le terme au thésaurus (une ligne JSON).

## Standard Agent Skills (#154, 2026-10-28)

Les skills suivent la [spécification Agent Skills](https://agentskills.io/specification),
vérifiée par son validateur de référence `skills-ref` 0.1.1 (CLI `agentskills validate`, Python
3.11+) : job CI `tests` et `tests/test_agent_skills.py` (ignoré avec la raison si `skills-ref`
est absent). Écarts assumés, tous propres à Claude Code
([doc des skills](https://code.claude.com/docs/en/skills), consultée le 2026-10-28) :

| Champ | Standard | Ce dépôt | Pourquoi |
|---|---|---|---|
| `argument-hint` (`bibliotheque`, `ajouter-syllabus`, `installer` de l'export) ; `disable-model-invocation` (`installer`) | hors liste : « Unexpected fields in frontmatter » | gardés **à la racine** de l'en-tête, tolérés par le test et seulement ceux-là | Claude Code ne les lit qu'à la racine ; sous `metadata:` ils seraient ignorés (« Claude Code doesn't act on its contents »), l'indice d'autocomplétion de `/bibliotheque` disparaîtrait. L'envoi sur claude.ai / API Skills les refuse : ces skills ne sont pas faits pour y être téléversés. |
| `allowed-tools` | chaîne séparée par des **espaces**, expérimental | **virgules** et motifs Claude Code avec espaces internes (`Bash(python qa.py idee chercher:*)`) | Claude Code accepte espaces, virgules ou liste YAML ; découper sur les espaces casserait les motifs à plusieurs mots. `skills-ref` 0.1.1 ne contrôle pas ce champ ; un autre agent qui le lirait au sens strict obtiendrait des règles fausses — il n'accorde de toute façon aucune permission hors Claude Code (Copilot l'ignore, la copie Gemini ne l'a pas). Non modifié : ce sont les permissions. |
| `compatibility` | facultatif, ≤ 500 caractères | déclaré dans les trois skills (Claude Code, Python 3.10+, CLI `qa.py`, réseau éventuel) | Accepté par Claude Code, sans effet ; recopié dans `plugin/skills/`. |

Les copies `.gemini/skills/` (générées) n'ont que `name` et `description` : elles sont
validées **sans aucune tolérance**, par `agentskills validate` dans la CI.

## Recherche sémantique : évaluation chiffrée (#107, 2026-10-22)

Jeux : contrôle (40 q.), réglage (36 q.) et un jeu **« éloigné »** (`evaluer --jeu
eloigne`, 5 q., exclu des deux autres) de questions formulées loin du vocabulaire ISTQB,
écrites avant le prototype : « comment éviter que nos tests cassent à chaque changement
d'écran », « on teste trop tard, comment avancer le test », « qui décide quand on arrête de
tester », « les développeurs ne lisent pas nos rapports de bugs », « combien de temps
faut-il prévoir pour tester ». Il est séparé du contrôle pour que le seuil de la CI
(`--min-rappel 0.80`) continue de mesurer le moteur livré. Machine : 4 cœurs CPU, sans GPU.
huggingface.co joignable depuis l'environnement (proxy) ; sans accès, copier le dossier du
modèle et pointer `QAK_MODELE_SEMANTIQUE` vers lui.

| Moteur | Contrôle (40 q.) | Réglage (36 q.) | Éloigné (5 q.) | Requête (CLI) | Indexation | Disque |
|---|---|---|---|---|---|---|
| Lexical (FTS5 + thésaurus), référence | 82 % · MRR 0,74 | 100 % · 0,92 | 20 % · 0,20 | 0,2-0,45 s | — | — |
| Hybride RRF + `intfloat/multilingual-e5-small` (MIT, 118 M param.) | 85 % · 0,74 | **97 %** · 0,87 | 20 % · 0,20 | 14,8 s (dont 11,5 s de chargement du modèle ; 0,05 s de calcul) | 610 s, 6 191 passages | vecteurs 4,8 Mo ; modèle 470 Mo ; dépendances 1,4 Go |

Première mesure (index précédent, contrôle de 28 q.) : e5-small hybride 82 % → 79 % au
contrôle, 100 % → 97 % au réglage ; `paraphrase-multilingual-MiniLM-L12-v2`
(Apache-2.0, indexation 193 s) 79 % (MRR 0,56) et 97 % ; e5-small seul (cosinus) 68 %.

**Décision : non retenue.** Le critère (des questions réalistes qui échouent malgré une
reformulation avec le terme ISTQB) est rempli, mais les embeddings multilingues légers ne
les résolvent pas (jeu éloigné inchangé), font perdre une question de réglage et coûtent
15 s par commande. Le prototype reste optionnel pour une réévaluation (autre modèle, ou
reformulation de la question par l'agent avant `chercher`, piste plus prometteuse : mesurée
et retenue dans #151, voir plus haut).

## Vérification des citations par NLI : étude (#108, 2026-10-22)

Question : un modèle d'inférence (NLI) multilingue peut-il signaler qu'un passage cité ne
**soutient pas** l'affirmation qu'on lui attribue (citation exacte mais à contresens) ?

- Jeu étiqueté `eval/nli/paires.json` : 48 paires (affirmation en français, passage cité
  EN ou FR) sur 12 passages ; affirmations « soutenues » tirées des essais réels
  (`eval/essais-resultats/2026-10-22/`, relues contre le passage), 12 contradictoires
  (négation / inversion), 24 non soutenues (12 plausibles sur le même sujet, 12 d'un autre
  passage). La base d'idées étant vide, aucune paire n'en vient.
- Modèle : `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (MIT, 279 M
  paramètres, 558 Mo), CPU 4 cœurs, `python scripts/etude_nli.py` (huggingface.co joignable).

| Mesure | Résultat |
|---|---|
| Exactitude 3 classes | 69 % (33/48) |
| Détection « pas soutenue » (non soutenue + contradictoire) | précision 89 %, rappel 86 % |
| Fausses alertes sur une citation juste | **4/12 (33 %)** |
| Contradictions jugées « soutenues » | 4/12 |
| Coût | 22 s de chargement, **4,7 s CPU par paire** (passage ≈ 1 400 caractères, tronqué à 512 jetons) |

**Décision : non retenue** (ni commande `verifier-citation`, ni avertissement dans
`idee ajouter`). Une citation juste sur trois serait signalée à tort, un tiers des
contresens passerait, et chaque contrôle coûte plusieurs secondes et 2 Go de dépendances.
La garde reste la règle du skill (lire avant de citer) et la vérification mot pour mot de
l'extrait. À réévaluer avec un modèle plus grand ou en découpant le passage en phrases
(prémisse = phrase la plus proche de l'affirmation) : le jeu et le script sont versionnés.

