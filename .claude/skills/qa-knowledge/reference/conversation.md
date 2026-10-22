# Mode conversationnel : clarifier, valider les sources, proposer des suites

But : laisser l'utilisateur orienter la recherche au lieu de répondre « d'un bloc ».
Quatre temps : **comprendre → plan de recherche → réponse → suites proposées**.
Ne pas questionner une question claire : clarifier seulement quand le gain est réel.

## Où et comment poser une question

| Situation | Comment |
|---|---|
| Session interactive Claude Code (conversation principale, ou `claude --agent thomas`) | outil **AskUserQuestion** : une question à la fois, 3 options au plus (« Autre » est ajouté par l'outil), multi-sélection si plusieurs choix se cumulent |
| Sous-agent (`@agent-thomas`, `@agent-sylvie`) | AskUserQuestion est retiré à tout sous-agent par Claude Code : **rendre** les questions et leurs options dans le rapport, section « Questions à choix » ; la conversation principale les pose avec AskUserQuestion |
| Non interactif (`claude -p`, essais automatiques), Copilot, Gemini | liste numérotée en texte |

**Ne jamais bloquer** hors session interactive : poursuivre avec des hypothèses
explicites (« Hypothèse : domaine web, équipe Scrum ») et finir par les questions à choix.

## 1. Comprendre

Clarifier avant de chercher plus loin si la question est ambiguë, trop large, ou ne se
rapproche d'aucun syllabus (`chercher` : confiance documentaire < 50, aucun titre de
section correspondant). Une à trois questions à choix, par exemple :

- **Angle** : définition · mise en place · audit de ma démarche (→ Sylvie) · comparaison
- **Domaine** : santé / réglementé · web · embarqué / intégré · mobile · API · autre
- **Niveau de détail** : synthèse courte · méthode détaillée · sections à lire

## 2. Plan de recherche (avant de rédiger)

Après un premier balayage (`chercher`), montrer **ce qui a été trouvé et où**, avec
langue et version, puis demander quoi approfondir :

```
Trouvé : CTAL-TM v3.0 §1.3 (FR + EN) · CTFL-AT 2014 §3.2.1 (FR + EN, ancien)
· CTFL v4.0.1 §5.1.5 (EN seulement) · rien dans CT-MAT.
Lesquels j'approfondis ?  1. CTAL-TM §1.3  2. CTFL-AT §3.2.1  3. Autre angle
```

Session interactive : AskUserQuestion (multi-sélection). Sinon : approfondir par défaut
les 2-3 sources les plus pertinentes, et donner ce plan en tête de réponse
(« Sources retenues ») pour que l'utilisateur puisse réorienter.

## 3. Réponse

Sur les sources validées, au format de [strategie.md](strategie.md) : pistes pour une
question de connaissance, gabarit « mise en place » pour une question de mise en place.

## 4. Suites proposées (à choix)

Approfondir une section · comparer · capitaliser · **ajouter un syllabus** quand la
couverture est partielle :

| Constat | Proposition |
|---|---|
| Sujet trouvé seulement en anglais (traduction FR absente : `manquants --langue fr`) | « `/ajouter-syllabus` avec la traduction CFTL de <code> (fichier à fournir) » |
| Seulement dans une version ancienne ou remplacée | « `catalogue --verifier` puis `/ajouter-syllabus <code>` » |
| Syllabus du catalogue officiel non téléchargé (`manquants`) | « `/ajouter-syllabus <code exact>` » |

Toujours le code exact ; ne rien télécharger sans accord.
