---
name: bibliotheque
description: Maintenance de la bibliothèque ISTQB locale — état de l'index, syllabus manquants (par langue), nouvelles versions publiées sur istqb.org, réindexation, références des idées à revérifier. À utiliser quand l'utilisateur demande quels syllabus sont présents ou manquants, s'il existe de nouvelles versions, ou de vérifier / remettre en état la bibliothèque.
argument-hint: "[etat | manquants | versions | reparer]"
allowed-tools: Bash(python qa.py:*), Bash(python3 qa.py:*), Bash(git status:*), Bash(git diff:*)
---

# Maintenance de la bibliothèque

Commandes lancées depuis la racine du dépôt (`python3` si `python` est absent). Rends
compte en français, en tableau quand il y a une liste, sans rien modifier sans accord.

## 1. État (toujours en premier)

1. `python qa.py inventaire` — documents, versions, extractions « À surveiller ».
   Si l'index est vide ou absent : `python qa.py actualiser` (≈ 3 min sur un clone neuf).
2. `python qa.py manquants` — pour chaque code du catalogue officiel : version courante
   en anglais, en français, ou manquante. Résume : « N syllabus en anglais, M traduits,
   absents en français : … ».

## 2. Nouvelles versions officielles

`python qa.py catalogue --verifier` interroge istqb.org. « ⚠ NOUVEAU FICHIER » = l'ISTQB
sert un autre fichier que celui relevé : probablement une nouvelle version. Propose
`python qa.py telecharger <code>` ; l'ancienne version reste consultable et passe
« remplacée » automatiquement. Après téléchargement : `python qa.py idee verifier-refs`
(références des idées vers une version remplacée).

## 3. Réparer

| Symptôme | Action |
|---|---|
| Index absent / corrompu | `python qa.py actualiser` (reconstruit depuis `bibliotheque/sources/`) |
| Extraction « partiel » / « illisible » | montrer les pages vides ; un scan demande un OCR externe puis réimport |
| Métadonnée fausse (version, langue, date) | `python qa.py corriger <doc_id> --version … --date AAAA-MM-JJ` |
| Doublon / document à retirer | `python qa.py retirer <doc_id>` puis déplacer le fichier hors de `sources/` |
| Amélioration de l'extracteur livrée | `python qa.py actualiser` réextrait tout (VERSION_EXTRACTEUR) |

## 4. Clôture

Si des fichiers ont changé (`git status`) : `bibliotheque/sources/`, `manifeste.json`,
`connaissances/` → proposer une branche + PR (règle du dépôt : jamais de commit direct
sur `main`). Pour ajouter un syllabus fourni par l'utilisateur : skill `/ajouter-syllabus`.
