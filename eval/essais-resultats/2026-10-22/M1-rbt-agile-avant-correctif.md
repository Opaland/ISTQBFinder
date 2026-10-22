# M1-rbt-agile — thomas

**Question** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

**Tours** : 8 · **coût** : 0.193 $ · **confiance annoncée** : 82 · **citations** : 7/7 lues · **Web** : 0 · **critères** : 6/11 (manquent : methode, etapes_sourcees, exemple, domaines:embarqu, domaines:mobile)

## Réponse

## Intégrer le risk-based testing (RBT) en agile : ce que disent les syllabus ISTQB

**Sources retenues.** J'ai lu 5 syllabus : CTFL-AT 2014 EN (§3.2.1), CTAL-AT v2.0 EN (§3.1.1), CTFL v4.0.1 EN (§5.1.2), CTAL-TA v4.0 FR (§2.2) et CTAL-TM v3.0 FR (§1.3.6). La base d'idées ne contient rien sur le sujet. Je n'ai pas fait de recherche Web, car la question porte sur la position de l'ISTQB et pas sur un outil.

**Hypothèse de contexte :** équipe Scrum classique, sans contrainte réglementaire forte.

**Pistes par syllabus**

- **CTFL-AT 2014 (Agile Tester) — §3.2.1 Assessing Quality Risks in Agile Projects.** C'est la réponse la plus directe, mais le syllabus est ancien (2014).
  - Le niveau de risque est égal à la probabilité multipliée par l'impact. On distingue les risques produit (qualité) des risques projet. [CTFL-AT 2014 EN, §3.2.1, p. 31]
  - L'analyse des risques qualité a lieu à deux endroits. En planification de release, les représentants métier donnent une vue de haut niveau et toute l'équipe aide à évaluer. En planification d'itération, toute l'équipe identifie et évalue les risques. [CTFL-AT 2014 EN, §3.2.1, p. 32]
  - Les tâches à risque élevé démarrent plus tôt et reçoivent plus d'effort de test. Celles à risque faible démarrent plus tard avec moins d'effort. [CTFL-AT 2014 EN, §3.2.1, p. 32]
  - Le syllabus décrit 6 étapes en planification d'itération :
    1. Réunir l'équipe, testeur compris.
    2. Lister les éléments du backlog de l'itération.
    3. Identifier les risques de chacun.
    4. Les évaluer (catégorie, impact, probabilité).
    5. Proportionner l'étendue des tests au niveau de risque.
    6. Choisir les techniques de test.
  - L'analyse est ajustée périodiquement : nouveaux risques, réévaluation, efficacité de la mitigation. Un risque peut aussi être atténué avant l'exécution, par exemple par une revue des user stories. [CTFL-AT 2014 EN, §3.2.1, p. 32]

- **CTAL-AT v2.0 (2026) — §3.1.1 Test Planning in Agile.** C'est la version à jour.
  - En planification d'itération, le testeur anime des séances de *risk-storming* avec le métier et les développeurs pour identifier les risques, prioriser les tests et affiner les critères d'acceptation. [CTAL-AT v2.0 EN, §3.1.1, p. 24-25]
  - En planification de release, on évalue les risques qualité sur tout le périmètre et on définit les objectifs de test et la stratégie de release. Le testeur peut animer des ateliers de *mind-mapping* ou de risk-storming. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
  - À creuser : §3.1.2 (stratégie de test du projet).

- **CTFL v4.0.1 — §5.1.2.** En release planning, le testeur participe aux analyses de risques projet et qualité. En iteration planning, il participe à l'analyse de risque détaillée des user stories. [CTFL v4.0.1 EN, §5.1.2, p. 48-49]
  - À creuser : §5.2, sur l'analyse et le contrôle des risques.

- **CTAL-TA v4.0 — §2.2 Contrôle des risques.**
  - Les risques évoluent. En cycle itératif, le pilotage se fait à la fréquence choisie par l'équipe, « vraisemblablement une fois par itération ». [CTAL-TA v4.0 FR, §2.2, p. 28]
  - Le testeur met à jour le registre des risques et ajuste les actions de mitigation. [CTAL-TA v4.0 FR, §2.2, p. 28]
  - Le périmètre de régression doit être revu à chaque cycle. [CTAL-TA v4.0 FR, §2.2.1, p. 28]

- **CTAL-TM v3.0 — §1.3.6 Métriques et difficultés du RBT.**
  - Il propose des questions de rétrospective. Par exemple : les parties prenantes étaient-elles bien impliquées ? Les tests ignorés avaient-ils un risque plus faible que les tests exécutés ? Peut-on expliquer les résultats de test en termes de risque ? [CTAL-TM v3.0 FR, §1.3.6, p. 34]
  - Il liste des pièges et leurs remèdes : estimation difficile, « déjà vu », risques importants manqués, parties prenantes qui changent. L'analyse doit être continue et itérative, pas faite une fois au début. [CTAL-TM v3.0 FR, §1.3.6, p. 34]

**Ce que j'en retiens** (interprétation)
- L'ISTQB ne décrit pas d'« intégration » en processus séparé. Le RBT se greffe sur les deux cérémonies de planification, release (vue large) et itération (détaillée). La réévaluation se fait à chaque itération.
- L'ISTQB insiste sur le collectif : toute l'équipe et le métier participent, et le testeur anime plus qu'il ne décide seul.
- Le point faible d'une mise en place est la dérive. Les risques doivent être revus, et la rétrospective sert à mesurer si le RBT apporte quelque chose (TM §1.3.6).

**Par quoi je commencerais**
1. Ajouter un créneau de risk-storming de 15 à 30 minutes à la planification d'itération, en suivant les 6 étapes de CTFL-AT. Impact fort, effort faible.
2. Ajouter 2-3 questions de la liste TM §1.3.6 à la rétrospective. Impact moyen, effort faible.
3. Mettre en place un registre de risques vivant, relié aux tâches du task board, pour piloter la régression. Impact moyen, effort moyen.

**Où creuser ensuite** : `section CTAL-AT-2.0-en 3.1`, `section CTAL-TM-3.0-fr 1.3`, `section CTFL-4.0.1-en 5.2`, `section CTAL-TA-4.0-fr 2.1`.

**Confiance : 82/100 (élevée).** Quatre syllabus courants concordent et j'ai lu les passages. En revanche, la description détaillée en 6 étapes vient de CTFL-AT 2014, un syllabus ancien. J'ai retiré quelques points pour cela et parce que je n'ai pas lu les §5.2 de CTFL ni les §1.3.1-1.3.5 de CTAL-TM.

**Questions de cadrage** : quel est ton cadre (Scrum, Kanban, SAFe, à l'échelle) ? Y a-t-il une contrainte réglementaire qui impose un registre de risques formalisé ?

**À capitaliser ?** Je propose une idée, avec ses références ISTQB. La vérification des doublons n'a pas pu s'exécuter : l'outil bash a bloqué la commande à cause du JSON en entrée. Seul `idee chercher` a donné « aucune idée » plus haut. Il faudra lancer `idee doublons` avant d'ajouter.

```json
{
  "titre": "Analyse des risques qualité à chaque planification d'itération (RBT agile)",
  "resume": "Toute l'équipe, testeur inclus, identifie et évalue les risques qualité des éléments du backlog d'itération, proportionne l'effort de test et réajuste périodiquement.",
  "probleme": "Prioriser et dimensionner les tests dans une itération courte, sans phase de test séparée.",
  "principe": "Risk-storming en planification de release (vue haut niveau) puis d'itération (détaillée) ; effort et ordre des tâches proportionnels au niveau de risque ; réévaluation périodique.",
  "theme_principal": "rbt",
  "themes_secondaires": ["agile", "priorisation"],
  "domaine_application": "Équipe agile ou itérative (Scrum, Kanban)",
  "prerequis": "Testeur présent à la planification ; représentants métier disponibles",
  "benefices": "Effort de test ciblé ; tests des risques élevés démarrés tôt",
  "limites": "Estimation impact/probabilité subjective ; description détaillée issue d'un syllabus ancien (CTFL-AT 2014)",
  "maturite": "documentee",
  "statut": "a_evaluer",
  "provenance": "Recherche du 2026-10-22 : « Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ? »",
  "references": [
    {
      "type": "istqb",
      "doc_id": "CTFL-AT-2014-en",
      "pages": "32",
      "section": "3.2.1",
      "extrait": "Tasks associated with high er risks should start earlier and involve more testing effort"
    },
    {
      "type": "istqb",
      "doc_id": "CTAL-AT-2.0-en",
      "pages": "24-25",
      "section": "3.1.1",
      "extrait": "Testers can contribute by facilitating risk-storming sessions with business representatives and developers"
    }
  ]
}
```

**Questions à choix**
1. Que veux-tu faire ensuite ?
   1. Approfondir : lire en entier CTAL-AT §3.1 et CTFL §5.2.
   2. Comparer les approches RBT du CTAL-TM (§1.3) et du CTAL-AT.
   3. Capitaliser l'idée ci-dessus, après vérification des doublons.
2. Peux-tu préciser ton contexte ?
   1. Scrum ou Kanban, équipe unique.
   2. Agile à l'échelle (SAFe, etc.). Dans ce cas, `/ajouter-syllabus` pour le syllabus ATLaS, s'il manque.
   3. Contexte réglementé. Dans ce cas, je regarderai CTAL-AT §3.1.2 et le contexte réglementé.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher risk-based testing agile; python qa.py chercher "risk-based testing agile"; python qa.py chercher "tests basés sur les risques agile"; python qa.py chercher "risk analysis i`
- `python qa.py lire 9556 --contexte 1; echo ======; python qa.py lire 8244 --contexte 1; echo ======; python qa.py lire 11560 --contexte 1; echo =====; python qa.py lire 11296 --contexte 1; echo =====; `
- `python qa.py idee modele | head -50`
- `python qa.py themes | grep -i -E "risk|risq|agile"; cat > /tmp/claude-0/-tmp-claude-0--home-user-da9346e2-ce5e-5882-830a-19be129b35c4-scratchpad-wt-90/edf74a91-d466-4096-b483-d3817fcb93c4/scratchpad/i`
- `python qa.py themes | head -40`
- `python qa.py idee doublons <<'JSON'
{"titre": "Analyse des risques qualité à chaque planification d'itération (RBT agile)", "resume": "Toute l'équipe, testeur inclus, identifie et évalue les risques q`
