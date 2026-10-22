# M1-rbt-agile — thomas

**Question** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

**Tours** : 11 · **coût** : 0.168 $ · **confiance annoncée** : 81 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 11/11

## Réponse

**Sources retenues**
- CTAL-AT v2.0 EN (2026-04-17), §3.1.1 : lu.
- CTFL-AT 2014 EN, §3.2.1 : lu. Ce syllabus est en retrait, remplacé par CTAL-AT.
- CTAL-TA v4.0 EN et FR, §2.1 et §2.2 : lu.
- CTAL-TM v3.0 FR, §1.3.6 : lu.
- La base d'idées ne contient rien sur ce sujet.
- Je n'ai pas fait de recherche Web, parce que ta question porte sur ce que propose l'ISTQB.

L'ISTQB n'a pas de chapitre unique qui "intègre le RBT en agile". La démarche se reconstitue à partir de ces syllabus : on analyse les risques avec toute l'équipe lors des planifications de release et d'itération, on dimensionne l'effort de test selon le niveau de risque, puis on réévalue à chaque itération.

Hypothèse de contexte : équipe Scrum ou équivalente, sans contrainte réglementaire forte. Je n'ai pas de contexte projet.

**Méthode pas à pas**
1. **Planification de release : survol des risques qualité.**
   - Les représentants métier donnent une vue d'ensemble des risques. Toute l'équipe, testeurs compris, aide à les identifier et à les évaluer. [CTFL-AT 2014 EN, §3.2.1, p. 32]
   - Le syllabus actuel ajoute les objectifs de test de la release, les niveaux, types et techniques nécessaires pour atténuer ces risques, et une stratégie de test de release. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
   - Livrable : stratégie de test de release.
2. **Planification d'itération : séance de risk-storming.**
   - Le testeur anime la séance avec les représentants métier et les développeurs, pour identifier les risques et prioriser les activités de test. [CTAL-AT v2.0 EN, §3.1.1, p. 24-25]
   - La séance définit aussi les conditions de test de haut niveau et affine les critères d'acceptation.
   - Livrable : liste de risques par élément du backlog.
3. **Évaluer chaque risque.**
   - Le syllabus 2014 donne six étapes : réunir l'équipe, lister les éléments du backlog, identifier les risques par caractéristique qualité, évaluer (catégorie, impact, probabilité), proportionner l'effort, choisir les techniques. [CTFL-AT 2014 EN, §3.2.1, p. 32]
   - Les facteurs d'évaluation sont la fréquence d'usage, la criticité métier, le dommage financier ou de réputation, la qualité de la base de test et les exigences légales ou de sécurité. [CTAL-TA v4.0 EN, §2.1, p. 25]
   - Livrable : niveau de risque par élément.
4. **Piloter l'ordre et l'effort sur le task board.** Les tâches à risque élevé démarrent plus tôt et reçoivent plus de tests, celles à risque faible démarrent plus tard avec moins de tests. [CTFL-AT 2014 EN, §3.2.1, p. 32]
5. **Atténuer aussi sans exécuter de tests.** Par exemple, si l'identification des risques révèle des problèmes dans les user stories, l'équipe les relit de près. [CTFL-AT 2014 EN, §3.2.1, p. 32] Dans l'esprit du shift-left, on choisit l'activité qui réduit le risque le plus tôt. [CTAL-TA v4.0 EN, §2.1, p. 25]
6. **Réévaluer à chaque itération.**
   - Dans un cycle itératif, le suivi des risques se fait à une fréquence choisie par l'équipe, probablement une fois par itération. Le testeur met à jour le registre des risques. [CTAL-TA v4.0 EN, §2.1, p. 25]
   - L'analyse des risques est continue et itérative, pas une activité de début de projet. [CTAL-TM v3.0 FR, §1.3.6, p. 34]
7. **Mesurer en rétrospective.**
   - Questions à poser : les parties prenantes étaient-elles impliquées ? Les défauts critiques sont-ils sortis tôt ? Les tests ignorés étaient-ils moins risqués que ceux exécutés ? [CTAL-TM v3.0 FR, §1.3.6, p. 34]
   - Le même passage liste des pièges : évaluation difficile (solution : données historiques), complaisance du « déjà vu », risques importants non identifiés faute des bonnes personnes.

**Exemple de mise en œuvre** (fictif, interprétation)
Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines :
- Au lancement de la release, 30 minutes avec le product owner pour lister les 5 à 8 risques majeurs (étape 1).
- À chaque planification, 20 minutes de risk-storming sur les stories retenues (étape 2). Chaque story reçoit une note impact × probabilité de 1 à 3, écrite sur le ticket (étape 3).
- Les stories à risque 6 ou plus passent en premier, avec exploratoire et revue des critères d'acceptation. Les stories à risque faible reposent sur l'automatisation existante (étapes 4 et 5).
- Chaque rétrospective, on relit les défauts échappés et on corrige les notes (étapes 6 et 7).

**Adaptation par domaine**

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Plus de traçabilité et de preuves d'audit : accent sur les quadrants 2 et 4. [CTAL-AT v2.0 EN, §3.1.2, p. 25] Pas de syllabus santé dans la bibliothèque (IEC 62304 absent) : Web nécessaire pour la norme. | CTAL-AT §3.1.2 |
| Web | Aucun syllabus web dédié : les principes ci-dessus se transposent. | CTAL-AT §3.1 |
| Embarqué | Non lu pour cette question. | CTEL-TM §8.3.3, CT-AuT |
| Mobile | Non lu pour cette question. | CT-MAT §1.8 |
| API | Non lu pour cette question. | CTAL-TTA §2.7 |

**Par quoi je commencerais**
1. Risk-storming de 20 minutes à la planification d'itération : impact fort, effort faible.
2. Révision du registre de risques à chaque rétrospective : impact moyen, effort faible.
3. Survol des risques à la planification de release, avec le métier : impact fort, effort moyen.

**Où creuser ensuite**
- `section CTAL-AT-2.0-en 3.1` : planification et stratégie en agile.
- `section CTAL-TM-3.0-fr 1.3` : le RBT côté management, y compris les techniques (non lues ici).
- `section CTAL-TA-4.0-en 2` : le rôle du Test Analyst.

**Confiance : 81/100 (élevée)** — base 85 × 0,6 = 51 ; 6 passages lus +20 ; 3 syllabus courants concordants +20 ; raisonnement sans source −10 (l'exemple et la grille 1-3). Une source citée est ancienne (CTFL-AT 2014), mais le syllabus actuel couvre l'essentiel.

**Questions à choix**
1. Quel est ton domaine ?
   1. Web / SaaS
   2. Réglementé (santé, finance)
   3. Embarqué, mobile ou API
2. Quelle suite veux-tu ?
   1. Approfondir les techniques de RBT dans CTAL-TM §1.3
   2. Comparer le RBT agile avec le RBT séquentiel
   3. Capitaliser l'idée proposée ci-dessous

**À capitaliser ?**
Aucun doublon trouvé (`idee doublons` : « Aucune idée similaire »).
```json
{
  "titre": "Risk-storming à chaque planification (release et itération)",
  "resume": "Intégrer le RBT en agile par des séances de risk-storming animées par le testeur en planification de release et d'itération.",
  "principe": "Analyser les risques qualité avec toute l'équipe, dimensionner l'effort de test selon le niveau de risque, réévaluer à chaque itération.",
  "theme": "rbt",
  "references": [
    {"document": "CTAL-AT-2.0-en", "page": 25, "extrait": "Testers can contribute by facilitating risk-storming sessions with business representatives and developers to identify risks and prioritize test activities"},
    {"document": "CTAL-TM-3.0-fr", "page": 34, "extrait": "L'analyse des risques est donc une activité continue et itérative qui ne doit pas être réalisée une seule fois au début du projet."}
  ]
}
```
Le champ `document` et la structure exacte sont à confirmer avec `python qa.py idee modele` avant `idee ajouter`. Je ne l'ai pas lancé.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-144/.claude/skills/qa-knowled`
- `python qa.py idee chercher risk-based testing agile`
- `python qa.py chercher risk-based testing agile`
- `python qa.py chercher analyse des risques itération agile`
- `python qa.py section CTFL-AT-2014-en 3.2.1 --max-caracteres 6000; python qa.py chercher "product risk" agile "CTAL-AT"; python qa.py lire 4576 --contexte 1 --max-caracteres 3500; python qa.py lire 195`
- `python qa.py lire 4576 --contexte 1; python qa.py lire 1954 --contexte 1; python qa.py lire 1762 --contexte 1; python qa.py chercher "quality risk" "release planning" CTAL-AT --doc CTAL-AT`
- `python qa.py section CTAL-AT-2.0-en 3.1.1 --max-caracteres 7000; python qa.py section CTAL-AT-2.0-en 3.1.2 --max-caracteres 6000`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Risk-storming à la planification d'itération et de release" --resume "Intégrer le test basé sur les risques en agile via s`
- `python qa.py confiance --base 85 --lus 6 --concordants 3 --raisonnement 1; python qa.py themes | grep -i -E "risk|risq"`
- `python qa.py idee doublons --titre "Risk-storming à chaque planification (release et itération)" --resume "Intégrer le RBT en agile par des séances de risk-storming en planification de release et d'it`
