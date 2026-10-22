# ISTQBFinder — QA Knowledge Agent

Assistant de connaissances QA **utilisé en conversation** dans Claude Code (référence),
GitHub Copilot ou Gemini CLI (voir « Où l'utiliser »).
Il cherche dans une bibliothèque locale de syllabus ISTQB (FR et EN, pages et sections
citées), dans une base d'idées QA capitalisées au fil du temps, et sur le Web seulement
quand c'est justifié. Il ne « s'entraîne » pas : il enrichit une mémoire documentaire
persistante, vérifiable et versionnée avec Git.

Pas de serveur, pas d'interface graphique, pas de clé d'API. Python ≥ 3.10 + `pypdf`.

## Où l'utiliser

| Environnement | Pris en charge | Remarque |
|---|---|---|
| **Claude Code en ligne de commande** (`claude`, lancé à la racine du dépôt) | oui | skills, agents Thomas et Sylvie, permissions de `.claude/settings.json` |
| **Appli de bureau Claude, onglet Code** (dossier du dépôt ouvert) | oui | même fonctionnement que la ligne de commande |
| **VS Code + GitHub Copilot Chat** (mode agent) | oui, non essayé en réel | skills lus dans `.claude/skills/`, agents `.github/agents/` générés, consignes `AGENTS.md` — voir [Utiliser avec GitHub Copilot](#utiliser-avec-github-copilot) |
| **GitHub Copilot CLI** (`copilot`) | oui, chargement vérifié | idem ; réponses non essayées faute de compte Copilot |
| **Gemini CLI** (`gemini`) | oui, chargement vérifié | skills `.gemini/skills/`, sous-agents `@thomas` / `@sylvie`, commandes `/thomas` / `/sylvie`, tous générés — voir [Utiliser avec Gemini CLI](#utiliser-avec-gemini-cli) |
| **claude.ai** (conversation Web ou appli, onglet Chat) | **non** | voir ci-dessous |

Pourquoi pas claude.ai : le skill n'est pas autonome. Il pilote la CLI `python qa.py`
(code `qak/`) et lit les données à la racine du dépôt — `bibliotheque/` (PDF et index,
plus de 30 Mo), `referentiel/`, `connaissances/` — qu'un skill importé sur claude.ai
n'emporte pas. Ses en-têtes sont propres à Claude Code (`allowed-tools`
`Bash(python qa.py …)`, `argument-hint`), les agents `.claude/agents/` (Thomas, Sylvie)
n'y existent pas, et `telecharger` / `catalogue --verifier` supposent un accès réseau à
istqb.org depuis la machine. Un paquet dédié à claude.ai (consultation seule) reste une
évolution possible, non décidée.

## Installation

```bash
git clone https://github.com/Opaland/ISTQBFinder && cd ISTQBFinder
./installer.sh               # Windows : powershell -ExecutionPolicy Bypass -File installer.ps1
```

Le script (relançable) vérifie Python ≥ 3.10, crée le venv `.venv`, installe les
dépendances, indexe les 42 PDF fournis (≈ 3 min la première fois) puis affiche un
diagnostic OK/KO (`python qa.py diagnostic`). Option `--assistant claude|copilot|gemini|tous`.
Procédure pas à pas, par assistant (Claude Code, GitHub Copilot, Gemini CLI) :
**[docs/installation.md](docs/installation.md)**. Lancer ensuite l'assistant venv activé
(`source .venv/bin/activate`).

Ajouter d'autres documents : `python qa.py importer chemin/vers/fichiers/` ; nouvelles
versions officielles : `python qa.py catalogue --verifier` puis `telecharger <code>`.

(`python3` sous Linux/macOS.) Ensuite tout se fait en conversation : le skill
`.claude/skills/qa-knowledge/` est chargé automatiquement par Claude Code dès qu'une
question porte sur le test logiciel ou la qualité (ou via `/qa-knowledge`).

## Utilisation

### Les agents

| Agent | Rôle | Lancer |
|---|---|---|
| **Thomas** | chercheur QA : explore la base d'idées et tous les syllabus, ouvre des pistes sourcées | `@agent-thomas <question>` dans une conversation, ou `claude --agent thomas` pour toute la session |
| **Sylvie** | auditrice : vérifie qu'une démarche est alignée sur les pratiques ISTQB, liste les manques, donne un niveau de capacité inspiré du TMMi (grille `referentiel/grille-maturite.md`) ; avis indicatif, pas une attestation | `@agent-sylvie <ta démarche>` ou `claude --agent sylvie` |

Exemple : « @agent-sylvie Je veux mettre en place une stratégie basée sur les risques :
atelier avec le PO pour lister les risques, priorisation des tests critiques, revue en
fin de sprint. Suis-je aligné ISTQB ? Quel niveau de maturité ? »

Sans agent nommé, le skill `qa-knowledge` se déclenche aussi tout seul sur une question QA.

Exemples de demandes, en langage naturel :

- « Quelles techniques ISTQB permettent d'améliorer la couverture des tests ? »
- « Recherche des idées pour intégrer le risk-based testing dans une équipe produit agile. »
- « Comment réduire le coût de maintenance de nos tests Playwright ? »
- « Compare les techniques de priorisation de l'ISTQB avec des retours d'expérience récents. »
- « Retrouve les idées déjà capitalisées sur le shift-left. » · « Classe cette nouvelle idée. »
- « Identifie les thèmes sur lesquels notre base est encore pauvre. »

Voir [docs/exemples-conversations.md](docs/exemples-conversations.md) (sorties réelles).

La CLI reste utilisable directement (`python qa.py --help`) :

| Besoin | Commande |
|---|---|
| Chercher dans les syllabus | `chercher <notions> [--doc CTAL-TM] [--theme rbt] [--section 1.3] [--langue fr]` |
| Confiance d'une réponse | `confiance --base N --lus N --concordants N [--web 1] [--non-couvert 1] …` (calcul affiché) |
| Lire avant de citer | `lire <passage> [--contexte 1]` · `section <doc> <num>` · `page <doc> <p[-q]>` (sorties bornées : `--max-caracteres`, défaut 15 000) · `plan <doc>` |
| Base d'idées | `idee chercher …` · `idee lister [--theme] [--statut]` · `idee voir QA-20261022-7f3a` |
| Capitaliser | `idee modele` · `idee doublons <<'JSON'` · `idee ajouter <<'JSON'` (JSON sur l'entrée standard) |
| Faire évoluer | `idee modifier` · `idee statut … --motif` · `idee retour` · `idee lier` · `journal` |
| Taxonomie | `themes` · `theme proposer "<texte>"` · `theme ajouter …` · `theme obsolete …` · `couverture` |
| Syllabus manquants | `manquants [--langue fr]` · skills `/bibliotheque` (maintenance) et `/ajouter-syllabus` |
| Bibliothèque | `catalogue [--verifier]` · `telecharger` · `importer` · `actualiser` · `inventaire` · `corriger` · `retirer` |
| Qualité de la recherche | `evaluer --jeu controle` |
| Contrôle de l'installation | `diagnostic [--assistant claude\|copilot\|gemini\|tous]` |

## Utiliser avec GitHub Copilot

Prérequis : l'installation ci-dessus (Python, `python qa.py actualiser`), puis VS Code avec
l'extension GitHub Copilot Chat en **mode agent**, ou [Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli)
(`npm install -g @github/copilot`, puis `copilot` à la racine du dépôt). Rien à copier :
tout est versionné dans le dépôt.

| Élément | Fichier lu par Copilot | Source unique |
|---|---|---|
| Skills `qa-knowledge`, `bibliotheque`, `ajouter-syllabus` | `.claude/skills/` lu **directement** (VS Code et Copilot CLI) | `.claude/skills/` |
| Agents Thomas et Sylvie | `.github/agents/thomas.agent.md`, `sylvie.agent.md` — **générés** | `.claude/agents/*.md` |
| Consignes (citation, lire avant de citer, score de confiance, règles de dev) | `AGENTS.md` (Copilot lit aussi `CLAUDE.md`) | `AGENTS.md`, importé par `CLAUDE.md` |

- **Lancer les agents** : VS Code, sélecteur d'agents du chat → `thomas` ou `sylvie` ;
  Copilot CLI, `/agent` puis le choisir, ou `copilot --agent thomas -p "<question>"`.
  Skills : `/skills list` dans une session, `copilot skill list` dans le terminal.
- **Après modification** d'un agent ou d'un skill : `python scripts/generer_integrations.py`
  (le test `tests/test_integrations.py`, lancé par la CI, échoue si on l'oublie).
- **Permissions** : l'équivalent de l'allowlist en lecture seule de `.claude/settings.json`
  n'est pas versionnable. VS Code : réglage `chat.tools.terminal.autoApprove` (clés =
  préfixes de commande, valeur `true`), par exemple
  `{"python qa.py chercher": true, "python qa.py lire": true, "python qa.py section": true}` ;
  une valeur `false` redemande confirmation. Copilot CLI : approuver à la demande, ou
  `--allow-tool 'shell(python qa.py chercher)'` pour la session. Ne pré-approuvez jamais les
  commandes qui écrivent (`idee ajouter`, `importer`, `actualiser`…, liste dans `AGENTS.md`).

Limites connues :

- **Non essayé en réel** côté réponses : faute de compte Copilot dans l'environnement de
  développement, aucune question n'a été posée à Thomas ni à Sylvie dans Copilot. Vérifié avec
  Copilot CLI 1.0.102 : `copilot skill list` voit les trois skills de `.claude/skills/`,
  `copilot instruction list` charge `AGENTS.md` et `CLAUDE.md`. Le chargement des agents
  `.github/agents/` exige une session authentifiée et n'a pas pu être vérifié.
- Copilot ne précharge pas un skill dans un agent (champ `skills:` propre à Claude Code) :
  l'agent généré commence par lire `.claude/skills/qa-knowledge/SKILL.md`.
- VS Code lit aussi `.claude/agents/` (format Claude) : Thomas et Sylvie peuvent y apparaître
  deux fois ; les deux versions ont le même prompt.
- Les en-têtes `allowed-tools` et `argument-hint` des skills sont propres à Claude Code et
  ignorés par Copilot : ils ne donnent aucune permission.

Documentation consultée (2026-10-22) :
[VS Code — Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) ·
[VS Code — Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents) ·
[VS Code — Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) ·
[VS Code — Approvals](https://code.visualstudio.com/docs/agents/approvals) ·
[Copilot — custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) ·
[Copilot CLI — skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) ·
[Copilot CLI — custom agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli) ·
[Copilot CLI — instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions) ·
[Copilot CLI — outils autorisés](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools).

## Utiliser avec Gemini CLI

Prérequis : l'installation ci-dessus, puis [Gemini CLI](https://geminicli.com/docs/)
(`npm install -g @google/gemini-cli`, Node.js 20+), lancé avec `gemini` à la racine du dépôt.
Au premier lancement, **faire confiance au dossier** : sinon Gemini ignore les réglages,
les sous-agents et les commandes du projet. Les skills sont activés par défaut
(`skills.enabled`, plus de préversion à activer en 0.65).

| Élément | Fichier lu par Gemini (généré) | Source unique |
|---|---|---|
| Consignes | `AGENTS.md`, via `context.fileName` de `.gemini/settings.json` | `AGENTS.md` |
| Skills | `.gemini/skills/<skill>/` (copie, liens `reference/` conservés) | `.claude/skills/` |
| Thomas, Sylvie en sous-agents | `.gemini/agents/thomas.md`, `sylvie.md` → `@thomas <question>` | `.claude/agents/*.md` |
| Thomas, Sylvie en commandes | `.gemini/commands/thomas.toml`, `sylvie.toml` → `/thomas <question>` | `.claude/agents/*.md` |
| Lecture seule pré-approuvée | `tools.allowed` de `.gemini/settings.json` | `.claude/settings.json` (`allow`) |

- **Sous-agent ou commande** : `@thomas` délègue à un sous-agent qui rend un rapport ;
  `/thomas` fait jouer Thomas dans la conversation principale (il peut alors poser lui-même
  les questions de cadrage).
- Gemini ne lit pas `.claude/` : d'où les copies générées. Elles sont dans `.gemini/skills/`
  et non dans `.agents/skills/`, que Copilot lit aussi (les skills y apparaîtraient en double).
- Contrôle sans compte : `gemini skills list` ; dans une session, `/skills list` et
  `/commands list`.

Limites connues :

- **Non essayé en réel** côté réponses : aucune clé Gemini ni compte Google dans
  l'environnement de développement ; aucune question n'a été posée à Thomas ni à Sylvie.
  Vérifié avec Gemini CLI 0.65.0 : `gemini skills list` voit les trois skills et `AGENTS.md`
  est chargé (journal `--debug`). Les sous-agents et les commandes ont été chargés par les
  chargeurs mêmes de Gemini CLI 0.65.0 (`loadAgentsFromDirectory`, `FileCommandLoader`,
  appelés depuis Node) : aucune erreur, `{{args}}` remplacé.
- `tools.allowed` est signalé **obsolète** par Gemini CLI 0.65 (« Migrate to Policy Engine »),
  mais le niveau « Workspace » du moteur de règles est documenté comme non fonctionnel :
  c'est donc la seule pré-approbation versionnable à ce jour. Une règle n'autorise qu'un
  préfixe de commande ; les commandes enchaînées (`&&`, `;`) sont vérifiées une à une.
- Depuis le 18 juin 2026, Google remplace Gemini CLI par Antigravity CLI pour les comptes
  gratuits et Google One (bandeau de la documentation) : non vérifié avec Antigravity.

Documentation consultée (2026-10-22) :
[Skills](https://geminicli.com/docs/cli/skills/) ·
[Commandes personnalisées](https://geminicli.com/docs/cli/custom-commands/) ·
[Sous-agents](https://geminicli.com/docs/core/subagents/) ·
[Configuration](https://geminicli.com/docs/reference/configuration/) ·
[Outils](https://geminicli.com/docs/reference/tools/) ·
[Commande shell](https://geminicli.com/docs/tools/shell/) ·
[Policy Engine](https://geminicli.com/docs/reference/policy-engine/).

## Ce qui est versionné

| Versionné (Git) | Non versionné (reconstructible) |
|---|---|
| `connaissances/connaissances.jsonl` — les idées | `connaissances/base.db` — reconstruite depuis le JSONL |
| `connaissances/journal.jsonl` — l'historique | `bibliotheque/index.db` — reconstruit par `actualiser` |
| `bibliotheque/manifeste.json` — métadonnées des documents | |
| `bibliotheque/sources/` — les PDF (≈ 33 Mo) | `bibliotheque/prive/` — documents internes (`importer --prive`) |
| `referentiel/` (taxonomie, thésaurus), `catalogue/`, `eval/` | |

Le dépôt est **public** : anonymiser toute idée (ni client, ni personne, ni projet, ni
montant) et importer les documents internes avec `importer --prive`, jamais dans `sources/`.

Après une session de capitalisation : commiter `connaissances/` (et
`referentiel/taxonomie.json` si un thème a été ajouté). Sur un autre poste, un `git pull`
suffit : la base locale se resynchronise toute seule.

## État de la bibliothèque (relevé du 2026-10-21)

- **Catalogue officiel** : 26 syllabus recensés sur istqb.org (Foundation, Advanced,
  Expert, Specialist, dont CT-AI v2.0, CT-GenAI v1.1, CT-QDO, CT-STE) — tous téléchargés,
  extraits et indexés en anglais (`inventaire`).
- **Français** : 14 codes fournis par l'utilisateur (CTAL-TA v4.0 et 2019, CTAL-TM v3.0,
  CTAL-TAE v2.0, CTAL-TTA v4.0, CTAL-ATT, CT-ATLaS + Body of Knowledge, CTEL-ITP, CTFL-AT,
  CT-AcT, CT-MAT, CT-MBT, CT-PT, CT-TAS, CT-UT). Le CTAL-TA 2019 est marqué « remplacé »
  par la v4.0 ; un doublon exact (ATLaS) a été écarté.
- **Absents en français** : notamment CTFL v4.0, CT-AI, CT-GenAI, CT-QDO, CT-SEC/STE, CTEL-TM
  (disponibles en anglais). Les déposer dans `bibliotheque/sources/` puis `actualiser`.
- **Non intégré** : le glossaire ISTQB (application Web sans export officiel).

## Fiabilité : ce que l'outil garantit

- Une référence ISTQB enregistrée pointe vers un document présent, une page qui existe
  et un extrait réellement présent sur ces pages — sinon l'enregistrement est refusé.
- Les versions remplacées sont exclues des recherches par défaut et signalées.
- Aucune idée n'est créée en double sans motif explicite ; aucun statut « validée » sans motif.
- Chaque modification est journalisée. Un seul domaine de téléchargement accepté : istqb.org.

Le skill impose le reste (règles non automatisables) : lire avant de citer, distinguer
ISTQB / Web / base / interprétation, justifier toute recherche Web, ne capitaliser
qu'avec l'accord de l'utilisateur.

## Limites

- Recherche **lexicale** (FTS5 + thésaurus FR/EN) : rappel@5 = 82 % sur 40 questions de
  contrôle jamais vues (dont des questions volontairement difficiles), 100 % sur le jeu
  de réglage. Les requêtes très courtes et génériques réussissent mieux avec le terme
  ISTQB anglais. Pas de recherche sémantique : bénéfice non démontré
  ([docs/architecture.md](docs/architecture.md)).
- Pas d'OCR (PDF scanné = « illisible »). Certains PDF produisent des espaces parasites
  dans les mots (« sélecti on ») : l'extraction recolle les fragments quand le mot réuni
  existe dans le document (≈ 80 % des coupures) ; une expression exacte peut encore être
  manquée sur les pages restantes. Une faute de frappe dans la question (« priorisasion »)
  est corrigée vers le mot connu le plus proche, avec un avertissement.
- La bibliothèque locale n'est pas l'ensemble des connaissances : l'assistant le dit
  quand elle ne couvre pas une question.

## Maintenance

- Actualisation des documents : [docs/actualisation.md](docs/actualisation.md).
- Schéma des données : [docs/schema.md](docs/schema.md).
- Architecture, choix, mesures, critères d'acceptation : [docs/architecture.md](docs/architecture.md).
- Essais réels des agents (questions, réponses, citations vérifiées, coût) :
  [docs/essais-reponses.md](docs/essais-reponses.md), `python scripts/essais_agents.py`.
- Tests : `python -m pytest tests -q -rs` (≈ 15 s ; `test_sources_reelles.py`
  appelle vraiment istqb.org et s'ignore, avec la raison, si le site est injoignable).
- Enrichir le thésaurus (`referentiel/thesaurus.json`) quand une notion n'est pas trouvée ;
  ajouter la question au jeu de contrôle `eval/requetes.json` avant de toucher au moteur.

## Droits

Les syllabus sont © ISTQB® ; leur notice autorise la copie, en tout ou partie, si la
source est citée. Les PDF de `bibliotheque/sources/` sont versionnés à ce
titre, source citée dans `bibliotheque/manifeste.json` (page officielle istqb.org ou
traduction fournie par l'utilisateur). La licence MIT du dépôt couvre le code et la
documentation, **pas** les syllabus, qui restent la propriété de l'ISTQB® et de leurs
traducteurs : exclusion explicite dans `LICENSE`, liste des documents avec ayant droit,
traducteur (CFTL pour les traductions françaises) et source dans [`NOTICE.md`](NOTICE.md).
