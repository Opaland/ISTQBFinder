---
name: bibliotheque
description: Maintenance de la bibliothèque ISTQB locale — état de l'index, syllabus manquants (par langue), réindexation, références des idées à revérifier ; sert aussi à détecter les nouvelles versions publiées sur istqb.org. À utiliser quand l'utilisateur demande quels syllabus sont présents ou manquants, s'il existe de nouvelles versions, ou de vérifier / remettre en état la bibliothèque. Pour installer un fichier ou une version précise, enchaîner sur /ajouter-syllabus.
argument-hint: "[etat | manquants | versions | reparer]"
allowed-tools: Bash(qa chercher:*), Bash(qa lire:*), Bash(qa section:*), Bash(qa page:*), Bash(qa plan:*), Bash(qa inventaire:*), Bash(qa manquants:*), Bash(qa catalogue:*), Bash(qa themes:*), Bash(qa couverture:*), Bash(qa journal:*), Bash(qa evaluer:*), Bash(qa idee chercher:*), Bash(qa idee lister:*), Bash(qa idee voir:*), Bash(qa idee doublons:*), Bash(qa idee modele:*), Bash(qa idee verifier-refs:*), Bash(qa theme proposer:*), Bash(qa confiance:*), Bash(qa diagnostic:*), Bash(qa --help:*), Bash(git status:*), Bash(git diff:*), mcp__plugin_istqbfinder_istqbfinder__*
---
<!-- Fichier généré par scripts/generer_integrations.py depuis .claude/skills/bibliotheque/SKILL.md : ne pas modifier, relancer le script. -->

> **Version plugin** d'ISTQBFinder (Claude Code hors du clone ; source unique : `.claude/skills/bibliotheque/SKILL.md` du dépôt).
> - `qa <commande>` remplace `python qa.py <commande>` : lanceur fourni par le plugin, utilisable depuis n'importe quel dossier (CLI du clone, Python de son venv).
> - Lecture : les outils MCP `chercher`, `lire`, `section`, `page`, `plan`, `idee_chercher`, `idee_voir`, `confiance`, `passages_lus` du serveur `istqbfinder` donnent les mêmes sorties que les commandes du même nom (`idee_chercher` = `idee chercher`) ; `passages_lus` dit si une référence a été lue dans la session. Toute écriture passe par `qa`, avec l'accord explicite de l'utilisateur.
> - Les chemins `bibliotheque/`, `referentiel/`, `connaissances/`, `docs/` sont relatifs au clone : `${CLAUDE_PLUGIN_ROOT}/..`.

# Maintenance de la bibliothèque

Commandes lancées depuis la racine du dépôt (`python3` si `python` est absent). Rends
compte en français, en tableau quand il y a une liste, sans rien modifier sans accord.

## 1. État (toujours en premier)

1. `qa inventaire` — documents, versions, extractions « À surveiller ».
   Si l'index est vide ou absent : `qa actualiser` (≈ 3 min sur un clone neuf).
2. `qa manquants` — pour chaque code du catalogue officiel : version courante
   en anglais, en français, ou manquante. Résume : « N syllabus en anglais, M traduits,
   absents en français : … ».

## 2. Nouvelles versions officielles

`qa catalogue --verifier` interroge istqb.org. « ⚠ NOUVEAU FICHIER » = l'ISTQB
sert un autre fichier que celui relevé : probablement une nouvelle version. Propose
`qa telecharger <code>` ; l'ancienne version reste consultable et passe
« remplacée » automatiquement. Après téléchargement : `qa idee verifier-refs`
(références des idées vers une version remplacée).

## 3. Réparer

| Symptôme | Action |
|---|---|
| Index absent / corrompu | `qa actualiser` (reconstruit depuis `bibliotheque/sources/`) |
| Extraction « partiel » / « illisible » | montrer les pages vides ; un scan demande un OCR externe puis réimport |
| Métadonnée fausse (version, langue, date) | `qa corriger <doc_id> --version … --date AAAA-MM-JJ` |
| Doublon / document à retirer | `qa retirer <doc_id>` puis déplacer le fichier hors de `sources/` |
| Amélioration de l'extracteur livrée | `qa actualiser` réextrait tout (VERSION_EXTRACTEUR) |

## 4. Clôture

Si des fichiers ont changé (`git status`) : `bibliotheque/sources/`, `manifeste.json`,
`connaissances/` → proposer une branche + PR (règle du dépôt : jamais de commit direct
sur `main`). Pour ajouter un syllabus fourni par l'utilisateur : skill `/ajouter-syllabus`.
