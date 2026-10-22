# C1-ambigu — skill

**Question** : Comment on gère les risques ?

**Tours** : 6 · **coût** : 0.268 $ · **confiance annoncée** : 79 · **verdict** : réussi · **citations** : 4/4 lues · **Web** : 0 · **critères** : 3/3

## Réponse

**Hypothèse :** je lis « on » comme « comment l'ISTQB gère les risques en test » (test basé sur les risques), et non comme « comment ce dépôt gère les risques ». Dites-moi si vous visiez autre chose. La base d'idées ne contient rien sur le sujet. Tout ce qui suit vient des syllabus.

## Le processus de gestion des risques

**Test Manager** [CTAL-TM v3.0 FR, §1.3.1, p. 29] :
- Un **risque produit** est une situation potentielle où des problèmes de qualité peuvent exister dans le produit. Un test qui trouve des défauts a atténué le risque. Un test qui n'en trouve pas indique un risque plus faible que prévu.
- Le **test basé sur les risques** suit le processus générique de gestion du risque, en deux temps :
  - **analyse des risques** : identification puis évaluation ;
  - **contrôle des risques** : suivi puis atténuation.
- Ces activités sont séquentielles, mais elles peuvent se chevaucher.
- L'analyse doit **inclure diverses parties prenantes**. Le Test Manager la modère.
- Le suivi des tests inclut le suivi des risques : nouveaux risques et ajustement du **registre des risques**.
- Le Test Manager doit aussi participer à la gestion des **risques projet** liés à l'assurance qualité. Le syllabus cite des exigences ambiguës et des environnements de test insuffisants.

## L'atténuation se répartit sur tout le cycle de test

Selon le même passage [CTAL-TM v3.0 FR, §1.3.1, p. 29] :
- **Planification** : les résultats de l'analyse concentrent les tests sur les bons domaines, avec les bonnes techniques.
- **Analyse des tests** : le niveau de risque guide le choix des conditions de test à couvrir.
- **Exécution** : la hiérarchisation par les risques fixe l'ordre d'exécution.

## Qui fait quoi

- **Évaluation (probabilité × impact)** [CTAL-TTA v4.0 FR, §1.2.2, pp. 11-12] :
  - Le Technical Test Analyst propose le niveau de **probabilité**, selon les lignes directrices du Test Manager. Le Test Manager peut le modifier après avoir entendu toutes les parties prenantes.
  - L'**impact métier** est normalement déterminé par le Test Analyst.
  - Facteurs de risque produit cités : complexité de la technologie ou du code, volume de changements, historique des défauts, problèmes d'interfaces et d'intégration.
  - Facteurs de risque projet cités : conflits entre parties prenantes, distribution géographique, outils et compétences, pression sur le temps et les ressources, taux de changement des exigences.
- **Réduction** [CTAL-TTA v4.0 FR, §1.2.3, p. 12] :
  - concevoir des cas de test pour les zones à haut risque ;
  - aider à évaluer le **risque résiduel** ;
  - appliquer les mesures d'atténuation et de contingence prévues au plan de test.
- **Contrôle** [CTAL-TA v4.0 FR, §2.2, p. 28] :
  - Les risques **évoluent dans le temps**, donc le pilotage doit être régulier : une fois par itération en cycle itératif, sinon à la fréquence fixée par le Test Manager.
  - Le Test Analyst met à jour le référentiel des risques.
  - Il ajuste les actions d'atténuation : revues, techniques de test et couverture adaptées, types de tests, régression.

## Interprétation (hors syllabus)

En pratique, cela donne un registre des risques qualité (risque, probabilité, impact, niveau, réponse de test) revu à chaque itération ou jalon. Chaque ligne se relie à des conditions de test et à une priorité d'exécution. Cette mise en forme est de moi, pas du syllabus.

**Confiance : 79/100 (élevée).** Calcul : couverture lexicale 82 × 0,6 = 49, plus 20 pour 3 passages lus, plus 20 pour 3 syllabus courants concordants, moins 10 pour l'interprétation sans source.

## Questions à choix

1. Quel contexte ?
   1. Agile / itératif
   2. Cycle en V / séquentiel
   3. Produit réglementé (santé, finance…)
2. Quel angle ?
   1. Mettre en place un registre et une matrice risque
   2. Prioriser les tests de régression
   3. Comparer plusieurs syllabus, avec Thomas

## Par quoi je commencerais

1. **Atelier d'analyse des risques qualité avec les parties prenantes.** Impact élevé, effort faible.
2. **Registre des risques relié aux conditions de test et à l'ordre d'exécution.** Impact élevé, effort moyen.
3. **Revue du registre à chaque itération.** Impact moyen, effort faible.

À lire ensuite : CTAL-TM §1.2.7, qui traite de l'évaluation des risques dans le plan de test. Je n'ai lu que l'extrait de recherche, donc je ne le cite pas. Je peux aussi proposer de capitaliser une idée « processus de gestion des risques qualité », mais seulement avec votre accord.

## Commandes exécutées

- `Skill {"skill": "qa-knowledge"}`
- `python qa.py idee chercher risques gestion risk-based 2>&1 | head -40; echo ----; python qa.py chercher "gestion des risques risk management" 2>&1 | head -60`
- `python qa.py section CTAL-TM-3.0-fr 1.3.1 --max-caracteres 4000 2>&1; echo ======; python qa.py section CTAL-TA-4.0-fr 2.2 --max-caracteres 3000 2>&1; echo =====; python qa.py lire 5641 --contexte 1 2`
- `python qa.py confiance --base 82 --lus 3 --concordants 3 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0 2>&1`
