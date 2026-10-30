# T5-priorisation — thomas

**Question** : Compare les techniques de priorisation des tests décrites par l'ISTQB.

**Tours** : 5 · **coût** : 0.2 $ · **confiance annoncée** : 78 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **fidélité** (juge LLM, indicatif) : 0.95 sur 5 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : CTFL v4.0.1 EN (§5.1.5), CTAL-TM v3.0 EN (§1.3.4), CTAL-TA v4.0 EN (§2.2) et CTAL-AT v2.0 EN (§1.4), tous lus. Base d'idées : rien de capitalisé sur le sujet. Les syllabus FR de CTAL-TM et CTAL-TA existent aussi, mais je n'ai cité que les versions EN lues. Je n'ai pas fait de recherche Web, la question étant purement ISTQB.

Hypothèse : tu compares les techniques pour choisir l'ordre d'exécution des tests, et la sélection de tests de régression t'intéresse aussi. Le contexte projet (agile ou séquentiel, domaine) n'est pas donné.

**Pistes par syllabus**
- **CTFL v4.0.1 §5.1.5 : trois stratégies de base**
  - Priorisation par risque, par couverture (avec la variante « couverture additionnelle ») ou par exigences. [CTFL v4.0.1 EN, §5.1.5, p. 50]
  - Limites : les dépendances entre tests (le test moins prioritaire dont dépend un test prioritaire passe d'abord) et la disponibilité des ressources (outils, environnements, personnes) peuvent imposer un autre ordre. [CTFL v4.0.1 EN, §5.1.5, p. 50]
- **CTAL-TM v3.0 §1.3.4 : priorisation par les risques, en deux variantes**
  - *Depth-first* : ordre strictement décroissant de niveau de risque, pour traiter les plus gros risques le plus tôt possible.
  - *Breadth-first* : au moins un test par risque en priorité maximale, pour avoir tôt une vue d'ensemble de la qualité.
  - En pratique, on commence en depth-first puis on passe en breadth-first quand le temps manque. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
  - Si le temps s'épuise, cette approche permet de recommander à la direction de prolonger les tests ou d'accepter le risque résiduel. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- **CTAL-TA v4.0 §2.2 : sélection de tests de régression sous contrainte**
  - Pour les tests automatisés, l'analyse d'impact outillée est présentée comme la technique la plus fiable. [CTAL-TA v4.0 EN, §2.2, p. 26]
  - Pour les tests manuels, aucune technique n'est prouvée supérieure : le TA choisit selon la situation. [CTAL-TA v4.0 EN, §2.2, p. 26]
  - Techniques courantes citées : sélection par risque, par historique (tests ayant révélé des défauts, plus quelques tests non exécutés depuis longtemps), par couverture, et par matrice de traçabilité des exigences. [CTAL-TA v4.0 EN, §2.2, p. 26]
  - La page 27 est à lire pour la fin de la matrice de traçabilité en agile (§2.2 tronqué à l'affichage).
- **CTAL-AT v2.0 §1.4 : régression en agile**
  - Régression incrémentale : un sous-ensemble est lancé à chaque commit, choisi selon l'impact et la probabilité du risque, la localisation et les dépendances du changement.
  - Régression par les risques (ateliers fréquents), orientée DevOps (smoke tests comme barrières qualité), exploratoire et collaborative. [CTAL-AT v2.0 EN, §1.4, p. 17]
  - La traçabilité légère (tags récit utilisateur ↔ test) sert à cibler la régression. [CTAL-AT v2.0 EN, §1.4, p. 18]

| Technique | Principe | Quand l'utiliser | Source |
|---|---|---|---|
| Par risque (depth-first) | Risques décroissants d'abord | Les risques majeurs doivent être traités tôt | CTAL-TM §1.3.4 |
| Par risque (breadth-first) | Au moins un test par risque d'abord | Vue globale rapide de la qualité, temps limité | CTAL-TM §1.3.4 |
| Par couverture (et additionnelle) | La plus forte couverture d'abord, puis le meilleur gain marginal | Tests techniques avec une mesure de couverture | CTFL §5.1.5 |
| Par exigences | Priorité des exigences définie par les parties prenantes | Traçabilité exigences ↔ tests en place | CTFL §5.1.5 |
| Par historique | Tests ayant déjà trouvé des défauts ou sensibles au même type de changement | Régression manuelle | CTAL-TA §2.2 |
| Analyse d'impact | Tests liés aux éléments de configuration modifiés | Régression automatisée, avec outillage | CTAL-TA §2.2 |

**Ce que j'en retiens** (interprétation)
- Ces techniques ne s'excluent pas. Le CTFL les donne comme les plus courantes, et le CTAL-TM combine depth-first puis breadth-first.
- Le classement par priorité cède aux dépendances et aux ressources, d'après le CTFL.
- Le CTFL traite de l'ordre d'exécution, le CTAL-TA de la sélection de régression. Ce sont deux problèmes voisins, mais pas identiques.

**Par quoi je commencerais**
1. Priorisation par risque avec bascule depth-first vers breadth-first : impact fort, effort moyen (il faut un registre de risques).
2. Tags de traçabilité légère pour cibler la régression : impact moyen, effort faible.
3. Analyse d'impact outillée pour l'automatisé : impact fort, effort fort.

**Où creuser ensuite**
- `section CTAL-TM-3.0-en 1.3.5` (techniques du RBT)
- `page CTAL-TA-4.0-en 27`
- `section CTFL-4.0.1-en 5.2.3` (analyse de risque produit)
- à lire : CT-FT v1.0 EN §3.2–3.3 (risque en finance, non lu)

**Confiance : 78/100** (bonne). Calcul : base 80 × 0,6 = 48 ; 4 passages lus +20 ; 3 syllabus concordants +10. L'ISTQB ne propose pas de comparaison formelle de ces techniques : le tableau est ma synthèse.

**Questions à choix**
1. Quel est ton contexte ?
   1. Agile / CI-CD
   2. Cycle séquentiel
   3. Réglementé ou critique
2. Quelle suite veux-tu ?
   1. Approfondir le RBT (CTAL-TM §1.3.5)
   2. Détailler la sélection de régression (CTAL-TA)
   3. Capitaliser la synthèse

**À capitaliser ?** Une proposition, en clair (je n'ai pas lancé `idee modele`, donc pas de JSON) : « Combiner priorisation par risque depth-first puis breadth-first, sous contrainte de dépendances et de ressources. » Sources : CTAL-TM §1.3.4 et CTFL §5.1.5. Si tu es d'accord, la conversation principale lancera `idee modele` puis `idee doublons` avant d'enregistrer.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher priorisation des tests; python qa.py chercher "test prioritization" ; python qa.py chercher "priorisation des tests risque couverture"; python qa.py chercher "prioritizing t`
- `python qa.py section CTFL-4.0.1-en 5.1.5 --max-caracteres 4000; python qa.py section CTAL-TM-3.0-en 1.3.4 --max-caracteres 4000; python qa.py chercher "regression test selection prioritization history`
- `python qa.py page CTAL-TM-3.0-en 31 --max-caracteres 3500; python qa.py section CTAL-TA-4.0-en 2.2 --max-caracteres 5000; python qa.py section CTAL-AT-2.0-en 1.4 --max-caracteres 3500`
