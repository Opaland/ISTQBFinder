<!-- Fichier généré par scripts/generer_integrations.py depuis .claude/skills/qa-knowledge/reference/capitalisation.md : ne pas modifier, relancer le script. -->

# Capitalisation dans la base QA

## Ce qui mérite d'être capitalisé

Oui : technique de test, méthode d'amélioration, pattern ou anti-pattern, comparaison
argumentée entre approches, retour d'expérience, recommandation opérationnelle étayée.
Non : définition triviale, paraphrase d'un paragraphe, hypothèse non étayée sans
intérêt durable, résultat de recherche brut.

## Procédure

1. Gabarit : lance `python qa.py idee modele` **avant** d'écrire le moindre JSON, même
   une simple proposition « À capitaliser ? », et pars de sa sortie : mêmes clés, mêmes
   types. Ne devine jamais un champ de mémoire. Sans `idee modele` lancé dans la session,
   présente l'idée **en clair** (titre, principe, source), sans JSON : le JSON se rédige
   après l'accord de l'utilisateur.
2. Rédiger le JSON (champs obligatoires : `titre`, `resume`, `probleme`, `principe`,
   `theme_principal`). Champs utiles : `themes_secondaires`, `domaine_application`,
   `prerequis`, `benefices`, `limites`, `maturite`, `provenance`, `references`.
   Erreurs déjà rencontrées. `idee ajouter` refuse une erreur de forme (clé inconnue,
   champ manquant, mauvais type) en les **listant toutes en une fois** : corrige-les
   toutes avant de relancer. La vérification d'une référence ISTQB (page, section,
   extrait) ne vient qu'ensuite, et s'arrête à la première erreur.
   - `theme` → `theme_principal` (et `themes_secondaires` pour les autres) ;
   - dans une référence, `document` → `doc_id` exact (ex. `CTAL-TM-3.0-fr`, en-tête de
     `lire`), `page` → `pages`, de préférence **en texte** (`"29"`, `"29-30"`) comme dans
     `idee modele` ; un entier (`29`) est accepté et converti en texte ;
   - `extrait` : au moins 6 mots significatifs recopiés mot pour mot (une phrase entière
     du passage lu, pas un groupe nominal).
3. Thèmes : `theme proposer "<titre + résumé>"`, puis vérifier dans `themes`.
4. Doublons : `idee doublons` en **une ligne**, champs en options (voir plus bas), avec
   la référence ISTQB prévue (`--doc`, `--pages`, `--section`, `--extrait`) : `idee ajouter`
   en tient compte, la vérification doit le faire aussi pour rendre le même verdict.
   Une référence commune n'est qu'un indice : seule, elle ne rend jamais « doublon
   probable » deux idées dont le texte n'est pas déjà proche (deux idées distinctes
   citent souvent le même passage).
   - « doublon probable » (≥ 0,6) → NE PAS créer ; proposer `idee modifier QA-xxxx`
     (les références et thèmes s'ajoutent, rien n'est perdu) ou `idee lier`.
   - « proche » (0,35-0,6) → créer seulement si la différence est réelle, puis lier
     (`variante`, `complementaire`, `contradictoire`, `prerequis`, `remplace`).
5. Ajout : `idee ajouter` avec le même JSON sur l'entrée standard. En cas de doublon
   assumé : `--forcer --motif "en quoi elle diffère"`.
6. Annoncer l'identifiant créé et les avertissements éventuels.

Rien ne passe par un fichier temporaire (un sous-agent ne peut pas écrire de fichier ;
`--fichier` reste possible pour un JSON que l'utilisateur a déjà). `idee doublons`, en
lecture seule, s'écrit **en une ligne sans JSON** : en `claude -p` et pour un
sous-agent, Claude Code bloque toute commande où une accolade côtoie un guillemet
(« Contains brace with quote character »), donc tout heredoc JSON ; la forme en une
ligne est couverte par l'autorisation `Bash(python qa.py idee doublons:*)`. `idee
ajouter` garde le JSON sur l'entrée standard : il demande de toute façon l'accord de
l'utilisateur.

Exemple complet (les exemples JSON des consignes sont passés à `idee ajouter` par
`tests/test_consignes_capitalisation.py`, avec le syllabus cité) :

```bash
python qa.py idee doublons --titre "Identifier les risques qualité avec toutes les parties prenantes" --resume "Recueillir les risques auprès d'un échantillon large de parties prenantes." --principe "Entretiens, ateliers, rétrospectives, checklists ; liste des participants convenue avec le chef de projet." --theme rbt --doc CTAL-TM-3.0-fr --pages 29-30 --section 1.3.2 --extrait "La tâche du Test Manager consiste à recueillir les risques auprès des parties prenantes"
python qa.py idee ajouter <<'JSON'
{ "titre": "Identifier les risques qualité avec toutes les parties prenantes",
  "resume": "Recueillir les risques auprès d'un échantillon large de parties prenantes.",
  "probleme": "Des risques produit importants passent inaperçus quand une partie prenante clé est absente.",
  "principe": "Entretiens, ateliers, rétrospectives, checklists ; liste des participants convenue avec le chef de projet.",
  "theme_principal": "rbt", "maturite": "documentee",
  "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "29-30", "section": "1.3.2",
                  "extrait": "La tâche du Test Manager consiste à recueillir les risques auprès des parties prenantes"}] }
JSON
```

## Confidentialité : le dépôt est PUBLIC

Tout ce qui est capitalisé (idées, retours d'expérience, références, journal) est publié
sur GitHub. Avant d'enregistrer, **anonymiser** : ni client, ni personne, ni montant, ni
projet nommé, ni adresse e-mail ou téléphone — « un client du secteur aéronautique »,
« un projet de migration », « un budget serré », jamais « Airbus », « A350 » ou
« 120 k€ ». L'outil bloque les adresses e-mail, montants et numéros de téléphone
(passage seulement avec `--forcer --motif "…"`, sur décision explicite de
l'utilisateur) et avertit sur toute référence `interne`. Les noms de clients, de
personnes ou de projets ne sont pas détectables automatiquement : la règle repose ici
sur l'agent. Un document interne se range dans `bibliotheque/prive/` (exclu de Git),
jamais dans `bibliotheque/sources/`.

## Références

- `istqb` : `doc_id` (ou code), `pages` et/ou `section`, `extrait` recommandé. Un code
  présent en plusieurs langues (CTAL-TM EN et FR) est départagé par la langue de l'extrait ;
  sans extrait, donner le `doc_id` exact (ex. `CTAL-TM-3.0-fr`). L'outil
  refuse une page inexistante (ou mal écrite : « 31 », « 31-33 », « 4, 6 »), une section
  absente des pages citées, et un extrait qui n'est pas recopié **mot pour mot** (suite
  continue d'au moins 6 mots significatifs, sans reformulation ni « … ») ; il signale
  une version remplacée.
- `web` / `article` : `url` obligatoire, `titre`, `note` (ce que la source apporte) ;
  `consulte_le` est ajouté automatiquement.
- `norme`, `livre`, `interne`, `conversation` : `titre` + précision utile.

## Maturité et statut (ne pas surévaluer)

- `maturite` : `hypothese` (non étayée) · `documentee` (source fiable) · `pratiquee`
  (répandue dans l'industrie) · `eprouvee` (validée dans NOTRE contexte, avec retour).
  `documentee` et `pratiquee` sont **refusées sans au moins une référence**.
- `statut` à la création : `a_explorer` ou `a_evaluer`. `validee`, `abandonnee`,
  `experimentee` : `idee statut QA-xxxx <statut> --motif "…"`, sur décision de
  l'utilisateur, motif d'au moins 10 caractères (« ok » refusé) ; `validee` exige au
  moins une référence ou un retour d'expérience ; `experimentee` exige un retour
  (`idee retour QA-xxxx --contexte … --resultat …`).

## Traçabilité

Chaque création / modification / changement de statut / relation / thème est journalisé
avec son auteur et un horodatage avec fuseau (`journal`, `journal --cible QA-xxxx`,
`--details` pour l'avant/après). Le journal se fusionne sans conflit entre postes
(`merge=union`) ; si un JSONL contient encore des marqueurs `<<<<<<<`, l'outil indique
le fichier et la ligne : résoudre le conflit avant toute autre commande. La base se versionne avec Git via
`connaissances/connaissances.jsonl` et `journal.jsonl` : proposer un commit
après une session de capitalisation.

- Ne jamais éditer `connaissances.jsonl` à la main : passer par `idee modifier`, et
  pour supprimer `idee retirer QA-xxxx --motif "…"` (instantané conservé dans le
  journal, relations retirées, identifiant jamais réattribué). Préférer
  `idee statut … abandonnee` quand l'idée garde une valeur historique.
- Si le fichier a été modifié hors de l'outil (édition, fusion, `git revert`), la base
  est reconstruite, les règles sont recontrôlées (statut, références, relations
  orphelines) et l'écart est journalisé (`modification_externe`) : relayer
  l'avertissement « ⚠ » à l'utilisateur.
