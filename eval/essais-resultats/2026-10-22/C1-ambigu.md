# C1-ambigu — skill

**Question** : Comment on gère les risques ?

**Tours** : 4 · **coût** : 0.123 $ · **confiance annoncée** : 82 · **citations** : 1/1 lues · **Web** : 0 · **critères** : 3/3

## Réponse

**Hypothèse :** vous parlez de la gestion des risques **produit/qualité** dans un projet de test, pas des risques projet en général. Je n'ai pas de contexte sur votre projet (cycle de vie, criticité, réglementation).

## Ce que disent les syllabus (passages lus)

**Le processus** [CTAL-TM v3.0 FR, §1.3.1, p. 29]
- Le test basé sur les risques suit le processus générique de gestion du risque. Il a deux grandes activités :
  - **l'analyse des risques** (identification, puis évaluation) ;
  - **le contrôle des risques** (suivi et atténuation).
- Ces activités sont séquentielles dans l'ordre, mais elles peuvent se chevaucher.
- L'analyse doit associer **diverses parties prenantes**. Le Test Manager en est la partie prenante principale et doit pouvoir la modérer.
- Le suivi des tests inclut le suivi des risques. Il couvre l'évolution des risques connus, l'analyse des nouveaux risques et l'ajustement du **registre des risques**.
- Les niveaux de risque guident ensuite tout le test :
  - planification : où concentrer l'effort et avec quelles techniques ;
  - analyse : quelles conditions de test couvrir ;
  - exécution : l'ordre des tests.

**Le choix de la technique** [CTAL-TM v3.0 FR, §1.3.5, pp. 33-34]
- **Techniques lourdes** (formelles, documentées, larges groupes de parties prenantes, souvent pour les systèmes critiques en sécurité) :
  - analyse des dangers ;
  - coût de l'exposition ;
  - AMDE (analyse des modes de défaillance et de leurs effets) ;
  - arbres de défaillance.
- **Techniques légères** (moins d'effort, facteurs réduits à probabilité × impact sur une échelle ordinale, usage courant hors systèmes critiques en sécurité) :
  - SST (tests systématiques de logiciels) ;
  - PRAM (analyse et gestion pragmatiques des risques) ;
  - PRISMA (gestion des risques produit).
- Le choix dépend du projet, du processus et du produit.

## Pistes à creuser (non lues en détail, donc à ne pas citer)
- CTFL v4.0.1 EN, §5.2 (« Risk Management ») et §5.2.3-5.2.4, pour la version de base : analyse, puis contrôle (mitigation et monitoring).
- CTAL-TA v4.0 FR, §2.2 (contrôle des risques) et §3.5.1 (choisir les techniques de test pour atténuer les risques produit).
- CTAL-TTA v4.0 FR, §1.2.2 (évaluation des risques).
- CT-PT 2018 FR, §3.3 (risques de performance) et CT-TAS 1.0 FR, §4.2.2 (risques de l'automatisation).

La base d'idées capitalisées ne contient rien sur ce sujet.

**Confiance : 82/100.** Deux sections consacrées au sujet ont été lues en entier dans le CTAL-TM. Je retire des points parce que les autres syllabus ne sont connus que par des extraits et parce que votre contexte est inconnu.

## Questions à choix
1. **Criticité du produit** : (a) critique en sécurité ou réglementé, (b) métier standard, (c) non critique.
2. **Votre besoin** : (a) mettre en place un processus d'analyse des risques, (b) choisir entre une technique lourde et une légère, (c) relier les risques à la priorisation des tests, (d) risques de l'automatisation ou de la performance.

## Par quoi je commencerais
1. **Un atelier d'analyse légère avec les parties prenantes** (impact × probabilité, échelle ordinale) : impact fort, effort faible.
2. **Un registre des risques relié au suivi des tests**, mis à jour à chaque point d'avancement : impact moyen, effort faible.
3. **Une AMDE sur les seules zones critiques**, si le produit s'y prête : impact fort, effort élevé.

Dites-moi le cadrage et je peux faire une recherche plus approfondie, par exemple avec l'agent Thomas.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher "gestion des risques" 2>&1 | head -40; python qa.py chercher "gestion des risques produit" 2>&1 | head -60`
- `python qa.py section CTAL-TM-3.0-fr 1.3.1 2>&1 | head -70; python qa.py section CTAL-TM-3.0-fr 1.3.5 2>&1 | head -50; python qa.py chercher "risk-based testing" --doc CTFL 2>&1 | head -25`
