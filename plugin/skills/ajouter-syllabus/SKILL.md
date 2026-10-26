---
name: ajouter-syllabus
description: Ajoute un syllabus ou document QA à la bibliothèque — PDF officiel ISTQB (téléchargé depuis istqb.org) ou fichier fourni par l'utilisateur (traduction CFTL, PDF, .txt, .md) — avec détection et contrôle des métadonnées, doublons et versions. À utiliser pour installer un fichier ou un code précis (ex. « importe ce PDF », « télécharge CT-AI », « installe la nouvelle version du CTFL »). Pour savoir ce qui manque ou s'il existe de nouvelles versions → /bibliotheque.
argument-hint: "<chemin du fichier | code ISTQB>"
allowed-tools: Bash(qa chercher:*), Bash(qa lire:*), Bash(qa section:*), Bash(qa page:*), Bash(qa plan:*), Bash(qa inventaire:*), Bash(qa manquants:*), Bash(qa catalogue:*), Bash(qa themes:*), Bash(qa couverture:*), Bash(qa journal:*), Bash(qa evaluer:*), Bash(qa idee chercher:*), Bash(qa idee lister:*), Bash(qa idee voir:*), Bash(qa idee doublons:*), Bash(qa idee modele:*), Bash(qa idee verifier-refs:*), Bash(qa theme proposer:*), Bash(qa confiance:*), Bash(qa diagnostic:*), Bash(qa --help:*), Bash(git status:*), Bash(git diff:*), Read, mcp__plugin_istqbfinder_istqbfinder__*
---
<!-- Fichier généré par scripts/generer_integrations.py depuis .claude/skills/ajouter-syllabus/SKILL.md : ne pas modifier, relancer le script. -->

> **Version plugin** d'ISTQBFinder (Claude Code hors du clone ; source unique : `.claude/skills/ajouter-syllabus/SKILL.md` du dépôt).
> - `qa <commande>` remplace `python qa.py <commande>` : lanceur fourni par le plugin, utilisable depuis n'importe quel dossier (CLI du clone, Python de son venv).
> - Lecture : les outils MCP `chercher`, `lire`, `section`, `page`, `plan`, `idee_chercher`, `idee_voir`, `confiance`, `passages_lus` du serveur `istqbfinder` donnent les mêmes sorties que les commandes du même nom (`idee_chercher` = `idee chercher`) ; `passages_lus` dit si une référence a été lue dans la session. Toute écriture passe par `qa`, avec l'accord explicite de l'utilisateur.
> - Les chemins `bibliotheque/`, `referentiel/`, `connaissances/`, `docs/` sont relatifs au clone : `${CLAUDE_PLUGIN_ROOT}/..`.

# Ajouter un syllabus

## 1. Identifier la source

- **Code officiel** (ex. `CTFL`, `CT-AI`) : `qa catalogue` pour vérifier qu'il
  existe, puis `qa telecharger <code>`. Seul istqb.org est accepté : ne jamais
  télécharger un syllabus depuis un autre site.
- **Fichier fourni** (traduction française, version récente) :
  `qa importer "<chemin>"` (fichier ou dossier ; PDF, .txt, .md). Si
  l'utilisateur a déposé le fichier dans `bibliotheque/sources/`, `qa actualiser`.
- **Document interne / confidentiel** (rapport, procédure, bilan de projet) : le dépôt
  est PUBLIC. `qa importer "<chemin>" --prive` — copié dans
  `bibliotheque/prive/` (exclu de Git, manifeste privé), indexé localement ; ou déposé
  dans `bibliotheque/prive/` puis `actualiser`. **Jamais** dans `sources/`, et pas
  d'étape 4 (ni commit ni PR).
- Document non ISTQB (norme, guide interne) : accepté, mais sa provenance doit être
  claire ; prévenir qu'il ne doit pas être cité comme « ISTQB ».

## 2. Contrôler ce qui a été détecté

La sortie affiche `code`, `type`, `version`, `langue`, `date`. Vérifie avec l'utilisateur
(ou sur la page de garde : `qa page <doc_id> 1`). Si c'est faux :
`qa corriger <doc_id> --code CTAL-TM --version 3.0 --langue fr --date 2024-03-28`
(les champs corrigés ne seront plus écrasés).

Cas à signaler explicitement :
- `doublon` : contenu identique (SHA-256) à un fichier déjà présent — rien n'est ajouté ;
- `version : … remplacé par …` : dire quelle version devient « courante » ;
- `extraction partiel / illisible` : pages sans texte (scan) — l'indexation sera incomplète ;
- code non reconnu : proposer `corriger --code` (ou l'ajout au catalogue s'il s'agit
  d'une nouvelle certification ISTQB).

## 3. Vérifier que la recherche le trouve

`qa plan <doc_id>` (sections détectées), puis une recherche sur un thème du
document avec `--doc <doc_id>`. `qa manquants` pour l'état d'ensemble.

## 4. Versionner (documents publics seulement)

Les PDF sont versionnés avec le dépôt (© ISTQB, copie autorisée avec citation de la
source). Proposer une branche + PR contenant `bibliotheque/sources/<fichier>` et
`bibliotheque/manifeste.json` (règle : jamais de commit direct sur `main`).
