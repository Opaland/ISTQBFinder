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
              referentiel/taxonomie.json   39 thèmes hiérarchiques + mots-clés FR/EN       [versionné]
              referentiel/thesaurus.json   ~130 concepts, ~1000 termes FR↔EN              [versionné]
```

Modules (`qak/`) : `extraction` (PDF → pages, plan, passages) · `bibliotheque` (import,
métadonnées, doublons, versions, index) · `catalogue` (istqb.org) · `recherche` (FTS5 +
thésaurus + reclassement) · `connaissances` (idées, déduplication, références vérifiées) ·
`taxonomie` · `journal` · `evaluation` · `cli`.

Aucun serveur, aucune interface graphique, aucune clé d'API. Dépendance unique : `pypdf`.

## Choix et compromis

| Sujet | Choix | Pourquoi / compromis |
|---|---|---|
| Point d'entrée | **Un skill** + une CLI | Le skill porte la méthode (ordre de recherche, citations, capitalisation) ; la CLI porte les garanties (vérifications, déduplication, journal). Pas de sous-agent : rien ne le justifie aujourd'hui, et il perdrait le contexte de la conversation. |
| Stockage | **SQLite** (stdlib) | Local, sans service, transactionnel, FTS5 intégré. |
| Recherche | **FTS5 BM25 + thésaurus FR/EN + reclassement par couverture** | Les syllabus sont un vocabulaire contrôlé : la recherche lexicale suffit si l'on traduit les concepts (FR → EN). Voir « Mesures ». |
| Fautes de frappe, mots coupés | **Correction ciblée + recollage à l'extraction** (#106) | Un mot de la question absent à la fois de l'index et du thésaurus est remplacé par le mot connu le plus proche (difflib ≥ 0,8 sur les mots du thésaurus, ≥ 0,85 sur le vocabulaire `fts5vocab` de l'index), avec avertissement ; un mot connu n'est jamais touché, donc aucune question bien orthographiée ne change. Les fragments « utilisabilit é » sont recollés dans les passages quand le mot réuni existe dans le document et qu'un fragment n'est pas un mot (3 136 → 662 coupures probables). Pas de table `trigram` : la correction suffit sur le jeu, et le repli n'aurait servi qu'aux requêtes sans résultat. |
| Recherche sémantique | **Évaluée (#107), non retenue** — prototype optionnel conservé (`qak/semantique.py`, `requirements-semantique.txt`, `actualiser --semantique`, `chercher/evaluer --semantique`), désactivé par défaut | Mesure ci-dessous : la fusion hybride BM25 + cosinus (RRF) **baisse** le contrôle et le réglage et ne résout aucune des questions formulées loin du vocabulaire ISTQB ; coût : 1,4 Go de dépendances (torch CPU), modèle 470 Mo, 12 s de chargement par commande. |
| Versionnement de la base | **JSONL miroir** + SQLite de travail | Un `.db` binaire se fusionne mal dans Git. Le JSONL (une idée par ligne, trié) donne des diffs lisibles ; après un `git pull`, l'empreinte du JSONL change et la base est reconstruite automatiquement. |
| PDF sources | **Versionnés** (≈ 33 Mo) | Un clone suffit pour travailler hors ligne, et les traductions françaises fournies à la main ne se perdent pas. La notice ISTQB autorise la copie si la source est citée (le manifeste la cite). Le manifeste garde les métadonnées et retrouve chaque fichier par empreinte. |
| Pages | **Page physique du PDF** + page imprimée si différente | La page physique est non ambiguë (c'est celle qu'ouvre un lecteur PDF) ; la page imprimée (« Page 12 de 80 ») est conservée quand elle diffère. Un passage ne franchit jamais une page. |
| Sections | Signets PDF si numérotés, sinon **plus longue chaîne de titres à numérotation cohérente** | Les syllabus FR n'ont souvent pas de signets. La programmation dynamique écarte les listes numérotées du préambule ; les titres répétés par les objectifs d'apprentissage sont écartés au profit du vrai titre. |
| Taxonomie | Fichier JSON, codes stables, statut `obsolete` + `remplace_par` | Un thème n'est jamais supprimé ; les idées gardent leur classement historique et les requêtes suivent le remplaçant. |
| Déduplication | Signature = concepts du thésaurus + racines, + thème principal commun et noms propres partagés | « Partitions d'équivalence » et « Equivalence partitioning » ont la même signature ; un nom propre absent du thésaurus partagé par les deux titres (Herzberg) pèse fortement, le thème principal commun un peu ; seuil 0,6 = doublon probable (bloquant), 0,35 = proche (signalé). |
| Références ISTQB | **Vérifiées à l'écriture** | Document présent, page existante, section présente sur les pages citées, extrait recopié mot pour mot (suite contiguë du texte normalisé, ≥ 6 mots significatifs, espaces parasites des PDF recollés) : une citation inventée, inversée ou en vrac est refusée par l'outil, pas seulement déconseillée par le skill. Limite : une citation exacte mais sortie de son contexte n'est pas détectable. |

## Mesures de la recherche (bibliothèque réelle : 42 fichiers, 26 codes EN + 14 FR)

`python qa.py evaluer --jeu reglage|controle` — rappel@5 = la réponse attendue
(code + section) figure dans les 5 premiers résultats. La CI exige `evaluer --jeu controle --min-rappel 0.80`
(code retour 2 sous le seuil, ou si aucune question n'a pu être évaluée).

| Version du moteur | Jeu de réglage (36 q.) | Jeu de contrôle (16 q., jamais utilisées pour régler) |
|---|---|---|
| FTS5 + thésaurus, « ET strict puis OU » | 75 % | — |
| + reclassement par couverture, concepts scindés, lexique FR→EN | 94 % | — |
| + rétrogradation annexes / notes de version | 100 % (MRR 0,82) | 88 % (MRR 0,76) |
| contrôle élargi à 18 q. (issue #4 : « shift-left », maintenance de l'automatisation) — avant correctif | 100 % (MRR 0,81) | 83 % (MRR 0,69) |
| + priorité aux sections dont le titre nomme la notion, thésaurus « maintainability » | 100 % (MRR 0,91) | **89 %** (MRR 0,81) |

Le 100 % du jeu de réglage est optimiste par construction ; le chiffre honnête est celui
du jeu de contrôle. Les questions ajoutées au contrôle l'ont été AVANT la correction qu'elles motivent. Les deux échecs du contrôle sont des requêtes très courtes faites de
mots omniprésents (« principes du test », « contenu d'un plan de test ») : la même
question avec le terme ISTQB anglais (« testing principles », « purpose and content of a
test plan ») trouve la bonne section en 1re ou 2e position. Le skill demande donc
d'ajouter le terme anglais quand il est connu.

Temps : une recherche ≈ 50 ms ; import initial ≈ 3 s par syllabus (≈ 2-3 min pour 42) ;
actualisation sans changement < 1 s.

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

## Recherche sémantique : évaluation chiffrée (#107, 2026-10-22)

Jeu : contrôle (28 q., dont 5 questions « loin du vocabulaire ISTQB » ajoutées avant le
prototype : « comment éviter que nos tests cassent à chaque changement d'écran », « on teste
trop tard, comment avancer le test », « qui décide quand on arrête de tester », « les
développeurs ne lisent pas nos rapports de bugs », « combien de temps faut-il prévoir pour
tester ») et réglage (36 q.). Machine : 4 cœurs CPU, sans GPU. huggingface.co joignable
depuis l'environnement (proxy) ; sans accès, copier le dossier du modèle et pointer
`QAK_MODELE_SEMANTIQUE` vers lui.

| Moteur | Contrôle rappel@5 · MRR | Réglage rappel@5 · MRR | Requête (CLI) | Indexation | Disque |
|---|---|---|---|---|---|
| Lexical (FTS5 + thésaurus), référence | 82 % (23/28) · 0,72 | 100 % · 0,91 | 0,23 s | — | — |
| Hybride RRF + `intfloat/multilingual-e5-small` (MIT, 118 M param.) | 79 % (22/28) · 0,74 | 97 % · 0,88 | 14,8 s (dont 11,5 s de chargement du modèle ; 0,05 s de calcul) | ≈ 10 min, 6 191 passages | vecteurs 4,8 Mo ; modèle 470 Mo ; dépendances 1,4 Go |
| Hybride RRF + `paraphrase-multilingual-MiniLM-L12-v2` (Apache-2.0) | 79 % (22/28) · 0,56 | 97 % · 0,90 | idem | 193 s | vecteurs 4,8 Mo ; modèle ≈ 470 Mo |
| e5-small **seul** (cosinus, sans dédoublonnage) | 68 % (19/28) | — | — | — | — |

Les 3 questions éloignées qui échouent en lexical échouent aussi en sémantique (attendu
hors des 5 premiers, rang 11 à « absent des 50 »). **Décision : non retenue.** Le critère
de `docs/architecture.md` (des questions réalistes qui échouent malgré une reformulation
avec le terme ISTQB) est rempli, mais les embeddings multilingues légers ne les résolvent
pas sur ce corpus. Le prototype reste optionnel pour une réévaluation (autre modèle,
reformulation de la question par l'agent avant `chercher`, piste plus prometteuse).

