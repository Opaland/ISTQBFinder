# Capitalisation dans la base QA

## Ce qui mérite d'être capitalisé

Oui : technique de test, méthode d'amélioration, pattern ou anti-pattern, comparaison
argumentée entre approches, retour d'expérience, recommandation opérationnelle étayée.
Non : définition triviale, paraphrase d'un paragraphe, hypothèse non étayée sans
intérêt durable, résultat de recherche brut.

## Procédure

1. Gabarit : `python qa.py idee modele`.
2. Rédiger le JSON (champs obligatoires : `titre`, `resume`, `probleme`, `principe`,
   `theme_principal`). Champs utiles : `themes_secondaires`, `domaine_application`,
   `prerequis`, `benefices`, `limites`, `maturite`, `provenance`, `references`.
3. Thèmes : `theme proposer "<titre + résumé>"`, puis vérifier dans `themes`.
4. Doublons : `idee doublons` avec le JSON sur l'entrée standard (heredoc, voir plus bas).
   - « doublon probable » (≥ 0,6) → NE PAS créer ; proposer `idee modifier QA-xxxx`
     (les références et thèmes s'ajoutent, rien n'est perdu) ou `idee lier`.
   - « proche » (0,35-0,6) → créer seulement si la différence est réelle, puis lier
     (`variante`, `complementaire`, `contradictoire`, `prerequis`, `remplace`).
5. Ajout : `idee ajouter` avec le même JSON sur l'entrée standard. En cas de doublon
   assumé : `--forcer --motif "en quoi elle diffère"`.
6. Annoncer l'identifiant créé et les avertissements éventuels.

Le JSON se passe **sans fichier temporaire** (un sous-agent ne peut pas écrire de
fichier ; `--fichier` reste possible pour un JSON que l'utilisateur a déjà) :

```bash
python qa.py idee doublons <<'JSON'
{ "titre": "...", "resume": "...", "probleme": "...", "principe": "...", "theme_principal": "rbt" }
JSON
python qa.py idee ajouter <<'JSON'
{ "titre": "...", "resume": "...", "probleme": "...", "principe": "...",
  "theme_principal": "rbt", "maturite": "documentee",
  "references": [{"type": "istqb", "doc_id": "CTAL-TM-3.0-fr", "pages": "29-30",
                  "section": "1.3.2", "extrait": "phrase recopiée mot pour mot du passage lu"}] }
JSON
```

## Références

- `istqb` : `doc_id` (ou code), `pages` et/ou `section`, `extrait` recommandé. L'outil
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
(`journal`, `journal --cible QA-xxxx`). La base se versionne avec Git via
`connaissances/connaissances.jsonl` et `journal.jsonl` : proposer un commit
après une session de capitalisation.
