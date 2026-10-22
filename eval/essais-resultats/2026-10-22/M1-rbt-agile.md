# M1-rbt-agile — thomas

**Question** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

**Tours** : 7 · **coût** : 0.166 $ · **confiance annoncée** : 80 · **citations** : 11/11 lues · **Web** : 0 · **critères** : 11/11

## Réponse

Je finalise le rapport. J'ai lu les passages clés et je n'ai pas pu lancer `idee doublons` (la commande a été bloquée par le bac à sable). Je m'appuie donc sur `idee chercher`, qui n'a rien trouvé de capitalisé.

## Sources retenues

- **CTFL-AT 2014 EN**, §3.2 et §3.2.1, p. 31-32. Les versions FR et EN sont indexées. Ce syllabus date de 2014, donc il est ancien.
- **CTFL v4.0.1 EN**, §5.1.2, p. 48-49.
- **CTAL-AT v2.0 EN** (2026), §3.1 et §3.1.1, p. 24-25.
- **CTAL-TA v4.0 FR**, §2.1.1 et §2.2, p. 27-28.
- **CTAL-TM v3.0 FR**, §1.3.6, p. 34.
- Je n'ai pas consulté le Web. Les passages ISTQB couvrent la question.

L'ISTQB ne décrit pas une méthode unique « RBT en agile ». Il propose d'étendre les pratiques de risque classiques aux cérémonies agiles, à deux niveaux (release et itération), avec une réévaluation continue.

**Hypothèse de contexte :** équipe Scrum ou similaire, application web, sans contrainte réglementaire forte.

## Méthode pas à pas

1. **Cadrer le niveau de risque.** Distinguer les risques produit (qualité) des risques projet. Le niveau de risque se calcule avec la probabilité et l'impact. [CTFL-AT 2014 EN, §3.2.1, p. 31]
2. **En planification de release : vue d'ensemble.** Les représentants métier donnent un aperçu des risques. Toute l'équipe, testeurs compris, aide à les identifier et à les évaluer. Le livrable est une base pour l'approche de test. [CTFL-AT 2014 EN, §3.2.1, p. 32 ; CTFL v4.0.1 EN, §5.1.2, p. 48]
3. **En planification d'itération : analyse détaillée.** Les testeurs participent à l'analyse de risque des user stories. [CTFL v4.0.1 EN, §5.1.2, p. 48] La version avancée recommande d'animer des sessions de *risk-storming* avec le métier et les développeurs. [CTAL-AT v2.0 EN, §3.1.1, p. 24-25] Le syllabus 2014 donne six étapes :
   - réunir l'équipe, testeurs inclus ;
   - lister les éléments du backlog de l'itération ;
   - identifier les risques qualité de chaque élément ;
   - les catégoriser et déterminer leur niveau (impact × probabilité) ;
   - proportionner l'effort de test au niveau de risque ;
   - choisir les techniques de test adaptées. [CTFL-AT 2014 EN, §3.2.1, p. 32]
4. **Prioriser les tâches.** Les tâches à risque élevé démarrent plus tôt et reçoivent plus d'effort de test. Celles à risque faible démarrent plus tard avec moins d'effort. [CTFL-AT 2014 EN, §3.2.1, p. 32]
5. **Atténuer aussi avant l'exécution.** Si l'identification des risques révèle des problèmes dans les user stories, une revue approfondie de ces stories est une mesure d'atténuation. [CTFL-AT 2014 EN, §3.2.1, p. 32] Le shift-left consiste à proposer l'activité qui réduit le risque le plus tôt. [CTAL-TA v4.0 FR, §2.1.1, p. 27]
6. **Réévaluer à chaque itération.** Il faut ajuster périodiquement l'analyse : nouveaux risques, niveaux revus, efficacité de l'atténuation. [CTFL-AT 2014 EN, §3.2.1, p. 32] En cycle itératif, le pilotage se fait « vraisemblablement une fois par itération ». [CTAL-TA v4.0 FR, §2.2, p. 28]
7. **Mesurer en rétrospective.** Les parties prenantes étaient-elles impliquées ? Les défauts graves sont-ils apparus tôt ? Les tests ignorés étaient-ils moins risqués que ceux exécutés ? Peut-on expliquer les résultats en termes de risque ? [CTAL-TM v3.0 FR, §1.3.6, p. 34] Le reporting agile inclut la couverture des risques. [CTAL-AT v2.0 EN, §3.1, p. 24]

## Exemple de mise en œuvre (fictif — interprétation)

Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines :
- Au planning, 20 minutes de risk-storming (étape 3). Chaque story reçoit un niveau de risque faible, moyen ou élevé, noté sur le tableau.
- Les stories à risque élevé (paiement, par exemple) sont testées en premier, avec une revue de la story en amont (étapes 4-5). Les stories à risque faible reçoivent surtout des tests automatisés de base.
- À la rétrospective, on vérifie si les bugs sont apparus là où on l'attendait (étape 7).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Traçabilité renforcée et couverture par niveau d'intégrité. Aucun syllabus santé ou IEC 62304 n'est présent : le Web serait nécessaire pour la norme. | CTAL-TTA v4.0 §2.8.2, CTAL-AT v2.0 §3.1.2 (à lire avant de citer) |
| Web | Pas de syllabus dédié. Les principes se transposent, avec les risques de performance par architecture. | CT-PT §3.2 (à lire) |
| Embarqué | Le matériel limite les itérations rapides. Couverture surtout automobile, en anglais. | CT-AuT, CTEL-TM §8.3.3 (à lire) |
| Mobile | Syllabus dédié, version 2019. | CT-MAT §1.8 (à lire) |
| API | Pas de syllabus dédié. Tests de contrat en anglais seulement. | CT-QDO §3.2.2 (à lire) |

Je n'ai lu aucune des sections de ce tableau. Ce sont des repères à vérifier, pas des citations.

## Par quoi je commencerais

1. **Risk-storming de 15-20 minutes au planning d'itération.** Impact fort, effort faible.
2. **Lier le niveau de risque à l'ordre des tâches et à l'effort de test.** Impact fort, effort faible.
3. **Réévaluation en rétrospective avec les questions du CTAL-TM §1.3.6.** Impact moyen, effort faible.

## Où creuser ensuite

- `section CTAL-AT-2.0-en 3.1` : planification agile, quadrants de test et définition de « terminé ».
- `section CTAL-TM-3.0-fr 1.3` : techniques et difficultés du test basé sur les risques.
- `section CTAL-TA-4.0-fr 2` : analyse et contrôle des risques produit.
- `section CTFL-4.0.1-en 5.2` : analyse et contrôle des risques. Je n'ai pas lu ce passage, il n'est mentionné que par renvoi.

**Confiance : 80/100 (élevée).** La confiance documentaire de `chercher` est de 100/100 et plusieurs syllabus concordent (+5). Je retire 15 points : la source la plus détaillée (CTFL-AT 2014) est ancienne, et l'exemple, ainsi que une partie de l'ordre des étapes, relèvent de mon interprétation.

## Questions à choix

1. Quel est ton contexte ?
   1. Scrum ou Kanban, application web.
   2. Agile à l'échelle ou multi-équipes.
   3. Secteur réglementé (santé, finance).
2. Quelle suite veux-tu ?
   1. Approfondir le CTAL-AT v2.0 §3.1 (risk-storming).
   2. Comparer le RBT en agile avec le cycle séquentiel (CTAL-TM §1.3).
   3. `/ajouter-syllabus` pour un domaine non couvert.

## À capitaliser ?

```json
{
 "titre": "Risk-storming à la planification d'itération pour piloter l'effort de test",
 "resume": "À chaque planification d'itération, l'équipe identifie et évalue les risques qualité par story. Le niveau de risque ordonne les tâches et dimensionne l'effort de test, puis est réévalué à chaque itération.",
 "probleme": "Prioriser et doser les tests dans des itérations courtes avec des exigences changeantes.",
 "principe": "Analyse de risque en release planning (vue globale) et en iteration planning (par story). Niveau = impact × probabilité. Risque élevé : démarrage plus tôt, plus de tests. Réévaluation périodique et mesure en rétrospective.",
 "theme_principal": "rbt",
 "themes_secondaires": ["agile", "priorisation"],
 "domaine_application": "Équipes agiles (Scrum) avec itérations courtes",
 "prerequis": "Présence du métier, des développeurs et des testeurs au planning ; backlog d'itération disponible.",
 "benefices": "Effort de test aligné sur le risque ; échanges plus clairs avec les parties prenantes ; défauts graves détectés tôt.",
 "limites": "Estimation difficile de la probabilité et de l'impact ; risque de complaisance si les mêmes risques reviennent chaque fois.",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-22 : « Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ? »",
 "references": [
  {
   "type": "istqb",
   "doc_id": "CTFL-AT-2014-en",
   "pages": "32",
   "section": "3.2.1",
   "extrait": "Tasks associated with higher risks should start earlier and involve more testing effort."
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

L'extrait du CTFL-AT peut être refusé par la vérification automatique à cause des espaces coupés dans l'extraction (« high er »). Dans ce cas, on raccourcit l'extrait lors de `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher risk-based testing agile; python qa.py chercher risk-based testing agile; python qa.py chercher "analyse des risques agile itération"; python qa.py chercher "risk based test`
- `python qa.py lire 9555 --contexte 1; python qa.py lire 9556 --contexte 1; python qa.py lire 11560 --contexte 1; python qa.py lire 8243 --contexte 1; python qa.py lire 11296 --contexte 1; python qa.py `
- `python qa.py idee modele | head -40; python qa.py idee doublons <<'JSON'
{"titre":"Analyse des risques qualité à chaque planification d'itération (agile)","description":"Risk-storming en planification`
- `python qa.py idee modele | head -40`
- `python qa.py themes | head -40`
