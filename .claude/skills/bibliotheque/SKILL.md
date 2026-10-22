---
name: bibliotheque
description: Maintenance de la bibliothèque ISTQB locale — état de l'index, syllabus manquants (par langue), réindexation, références des idées à revérifier ; sert aussi à détecter les nouvelles versions publiées sur istqb.org. À utiliser quand l'utilisateur demande quels syllabus sont présents ou manquants, s'il existe de nouvelles versions, ou de vérifier / remettre en état la bibliothèque. Pour installer un fichier ou une version précise, enchaîner sur /ajouter-syllabus.
argument-hint: "[etat | manquants | versions | reparer]"
allowed-tools: Bash(python qa.py chercher:*), Bash(python3 qa.py chercher:*), Bash(python qa.py lire:*), Bash(python3 qa.py lire:*), Bash(python qa.py section:*), Bash(python3 qa.py section:*), Bash(python qa.py page:*), Bash(python3 qa.py page:*), Bash(python qa.py plan:*), Bash(python3 qa.py plan:*), Bash(python qa.py inventaire:*), Bash(python3 qa.py inventaire:*), Bash(python qa.py manquants:*), Bash(python3 qa.py manquants:*), Bash(python qa.py catalogue:*), Bash(python3 qa.py catalogue:*), Bash(python qa.py themes:*), Bash(python3 qa.py themes:*), Bash(python qa.py couverture:*), Bash(python3 qa.py couverture:*), Bash(python qa.py journal:*), Bash(python3 qa.py journal:*), Bash(python qa.py evaluer:*), Bash(python3 qa.py evaluer:*), Bash(python qa.py idee chercher:*), Bash(python3 qa.py idee chercher:*), Bash(python qa.py idee lister:*), Bash(python3 qa.py idee lister:*), Bash(python qa.py idee voir:*), Bash(python3 qa.py idee voir:*), Bash(python qa.py idee doublons:*), Bash(python3 qa.py idee doublons:*), Bash(python qa.py idee modele:*), Bash(python3 qa.py idee modele:*), Bash(python qa.py idee verifier-refs:*), Bash(python3 qa.py idee verifier-refs:*), Bash(python qa.py theme proposer:*), Bash(python3 qa.py theme proposer:*), Bash(python qa.py confiance:*), Bash(python3 qa.py confiance:*), Bash(python qa.py diagnostic:*), Bash(python3 qa.py diagnostic:*), Bash(python qa.py --help:*), Bash(python3 qa.py --help:*), Bash(git status:*), Bash(git diff:*)
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
