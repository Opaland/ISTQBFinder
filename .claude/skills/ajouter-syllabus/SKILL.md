---
name: ajouter-syllabus
description: Ajoute un syllabus ou document QA à la bibliothèque — PDF officiel ISTQB (téléchargé depuis istqb.org) ou fichier fourni par l'utilisateur (traduction CFTL, PDF, .txt, .md) — avec détection et contrôle des métadonnées, doublons et versions. À utiliser pour installer un fichier ou un code précis (ex. « importe ce PDF », « télécharge CT-AI », « installe la nouvelle version du CTFL »). Pour savoir ce qui manque ou s'il existe de nouvelles versions → /bibliotheque.
argument-hint: "<chemin du fichier | code ISTQB>"
allowed-tools: Bash(python qa.py chercher:*), Bash(python3 qa.py chercher:*), Bash(python qa.py lire:*), Bash(python3 qa.py lire:*), Bash(python qa.py section:*), Bash(python3 qa.py section:*), Bash(python qa.py page:*), Bash(python3 qa.py page:*), Bash(python qa.py plan:*), Bash(python3 qa.py plan:*), Bash(python qa.py inventaire:*), Bash(python3 qa.py inventaire:*), Bash(python qa.py manquants:*), Bash(python3 qa.py manquants:*), Bash(python qa.py catalogue:*), Bash(python3 qa.py catalogue:*), Bash(python qa.py themes:*), Bash(python3 qa.py themes:*), Bash(python qa.py couverture:*), Bash(python3 qa.py couverture:*), Bash(python qa.py journal:*), Bash(python3 qa.py journal:*), Bash(python qa.py evaluer:*), Bash(python3 qa.py evaluer:*), Bash(python qa.py idee chercher:*), Bash(python3 qa.py idee chercher:*), Bash(python qa.py idee lister:*), Bash(python3 qa.py idee lister:*), Bash(python qa.py idee voir:*), Bash(python3 qa.py idee voir:*), Bash(python qa.py idee doublons:*), Bash(python3 qa.py idee doublons:*), Bash(python qa.py idee modele:*), Bash(python3 qa.py idee modele:*), Bash(python qa.py idee verifier-refs:*), Bash(python3 qa.py idee verifier-refs:*), Bash(python qa.py theme proposer:*), Bash(python3 qa.py theme proposer:*), Bash(python qa.py confiance:*), Bash(python3 qa.py confiance:*), Bash(python qa.py diagnostic:*), Bash(python3 qa.py diagnostic:*), Bash(python qa.py --help:*), Bash(python3 qa.py --help:*), Bash(git status:*), Bash(git diff:*), Read
---

# Ajouter un syllabus

## 1. Identifier la source

- **Code officiel** (ex. `CTFL`, `CT-AI`) : `python qa.py catalogue` pour vérifier qu'il
  existe, puis `python qa.py telecharger <code>`. Seul istqb.org est accepté : ne jamais
  télécharger un syllabus depuis un autre site.
- **Fichier fourni** (traduction française, version récente) :
  `python qa.py importer "<chemin>"` (fichier ou dossier ; PDF, .txt, .md). Si
  l'utilisateur a déposé le fichier dans `bibliotheque/sources/`, `python qa.py actualiser`.
- **Document interne / confidentiel** (rapport, procédure, bilan de projet) : le dépôt
  est PUBLIC. `python qa.py importer "<chemin>" --prive` — copié dans
  `bibliotheque/prive/` (exclu de Git, manifeste privé), indexé localement ; ou déposé
  dans `bibliotheque/prive/` puis `actualiser`. **Jamais** dans `sources/`, et pas
  d'étape 4 (ni commit ni PR).
- Document non ISTQB (norme, guide interne) : accepté, mais sa provenance doit être
  claire ; prévenir qu'il ne doit pas être cité comme « ISTQB ».

## 2. Contrôler ce qui a été détecté

La sortie affiche `code`, `type`, `version`, `langue`, `date`. Vérifie avec l'utilisateur
(ou sur la page de garde : `python qa.py page <doc_id> 1`). Si c'est faux :
`python qa.py corriger <doc_id> --code CTAL-TM --version 3.0 --langue fr --date 2024-03-28`
(les champs corrigés ne seront plus écrasés).

Cas à signaler explicitement :
- `doublon` : contenu identique (SHA-256) à un fichier déjà présent — rien n'est ajouté ;
- `version : … remplacé par …` : dire quelle version devient « courante » ;
- `extraction partiel / illisible` : pages sans texte (scan) — l'indexation sera incomplète ;
- code non reconnu : proposer `corriger --code` (ou l'ajout au catalogue s'il s'agit
  d'une nouvelle certification ISTQB).

## 3. Vérifier que la recherche le trouve

`python qa.py plan <doc_id>` (sections détectées), puis une recherche sur un thème du
document avec `--doc <doc_id>`. `python qa.py manquants` pour l'état d'ensemble.

## 4. Versionner (documents publics seulement)

Les PDF sont versionnés avec le dépôt (© ISTQB, copie autorisée avec citation de la
source). Proposer une branche + PR contenant `bibliotheque/sources/<fichier>` et
`bibliotheque/manifeste.json` (règle : jamais de commit direct sur `main`).
