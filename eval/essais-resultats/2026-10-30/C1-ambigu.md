# C1-ambigu — skill

**Question** : Comment on gère les risques ?

**Tours** : 7 · **coût** : 0.244 $ · **confiance annoncée** : 87 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 3/3 · **fidélité** (juge LLM, indicatif) : 0.94 sur 5 lignes citées, 0 contradiction(s)

## Réponse

## La gestion des risques en test (ISTQB)

**Hypothèse :** vous parlez des risques *qualité/produit* côté tests, pas de la gestion de projet au sens large. La base d'idées capitalisées n'a rien sur le sujet.

### Le processus : deux activités, quatre étapes
Le CTFL v4.0.1 pose le cadre : l'**analyse des risques** (identification, puis évaluation) et le **contrôle des risques** (atténuation, puis suivi). L'approche de test qui s'appuie dessus s'appelle le *risk-based testing* [CTFL v4.0.1 EN, §5.2, p. 51].

- **Définition.** Un risque se caractérise par sa *probabilité* et son *impact*. Les deux ensemble donnent le *niveau de risque* [CTFL v4.0.1 EN, §5.2.1, p. 52].
- **Deux familles.**
  - Les risques *projet* touchent délais, budget, personnes, fournisseurs ou outils.
  - Les risques *produit* touchent la qualité : calculs faux, sécurité, performance, expérience utilisateur [CTFL v4.0.1 EN, §5.2.2, p. 52].
- **Identification.** Ateliers, entretiens, brainstorming, diagrammes cause-effet [CTFL v4.0.1 EN, §5.2.3, p. 52]. Le CTAL-TM ajoute les rétrospectives, les checklists, les évaluations indépendantes et le retour d'expérience. Il insiste sur le choix des parties prenantes : en oublier une clé est « très problématique » [CTAL-TM v3.0 FR, §1.3.2, p. 30].
- **Évaluation.** Deux approches :
  - **Quantitative** : niveau = probabilité × impact.
  - **Qualitative** : matrice de risques [CTFL v4.0.1 EN, §5.2.3, p. 53].
- **Ce que l'analyse pilote.** Le périmètre, les niveaux et types de test, les techniques et la couverture visée, l'effort, la priorisation, et d'éventuelles actions autres que le test [CTFL v4.0.1 EN, §5.2.3, p. 53].
- **Contrôle.** Atténuer par le test (testeurs adaptés, indépendance, revues, analyse statique, techniques et régression adaptées). Les autres réponses possibles : accepter, transférer ou prévoir un plan de contingence. Le suivi vérifie que les actions marchent et repère les risques émergents [CTFL v4.0.1 EN, §5.2.4, p. 53].

### Le point de vue du Test Manager (CTAL-TM v3.0)
- Il recueille les risques auprès des parties prenantes, modère l'analyse et participe à la gestion des risques projet liés à la qualité (exigences ambiguës, environnements insuffisants).
- Les activités se suivent logiquement mais peuvent se chevaucher.
- **Le suivi des tests inclut le suivi des risques** : nouveaux risques, ajustement du registre.
- L'atténuation se répartit sur toutes les activités : planification, analyse (le niveau de risque guide les conditions de test) et exécution (l'ordre d'exécution suit le risque) [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- Un test sans défaut trouvé indique un niveau de risque plus faible que prévu [CTAL-TM v3.0 FR, §1.3.1, p. 29].
- Le risque n'est pas réparti uniformément : il faut l'évaluer par objet de test [CTAL-TM v3.0 FR, §1.3.2, p. 30].

### Où creuser ensuite (non lu, donc sans page)
- CTAL-TM v3.0 FR §1.3.5 : techniques formelles (PRAM, PRISMA).
- CTAL-TA v4.0 §2.2 : le contrôle des risques côté Test Analyst.
- CTEL-TM 2011 §6.3 : gestion des risques projet (ancien).
- CT-ATLaS v2.0 FR §5.1.5 : risques organisationnels à l'échelle.

**Confiance : 87/100** (élevée). Calcul : couverture lexicale 95 × 0,6 = 57, plus 20 (cinq passages lus) et 10 (deux syllabus courants concordants, CTFL et CTAL-TM) = 87.

**Questions à choix** (contexte de votre équipe)
1. Cycle de vie : (a) agile/itératif (b) en V/cascade (c) mixte
2. Besoin : (a) démarrer une analyse de risques (b) la faire vivre dans le suivi (c) priorisation des tests

**Par quoi je commencerais**
1. Un atelier de risques avec les parties prenantes clés, évaluation qualitative par matrice : fort impact, effort modéré.
2. Relier chaque risque à des conditions de test et à l'ordre d'exécution : impact élevé, effort moyen.
3. Mettre le registre à jour à chaque point de suivi : impact moyen, effort faible.

Souhaitez-vous que j'approfondisse un de ces points (par exemple PRAM/PRISMA via `/thomas`) ?

## Commandes exécutées

- `Skill {"skill": "qa-knowledge", "args": "Comment on gère les risques ?"}`
- `python qa.py idee chercher risques gestion des risques 2>&1 | head -40; echo ======; python qa.py chercher "gestion des risques" 2>&1 | head -60; echo =====; python qa.py chercher "risk management" 2>`
- `python qa.py section CTFL-4.0.1-en 5.2 2>&1; echo =======; python qa.py section CTAL-TM-3.0-fr 1.3.1 2>&1`
- `python qa.py section CTAL-TM-3.0-fr 1.3.2 2>&1 | head -80`
- `python qa.py confiance --base 95 --lus 5 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 0 --non-couvert 0 --autorite 0 2>&1`
