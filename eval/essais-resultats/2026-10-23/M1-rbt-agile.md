# M1-rbt-agile — thomas

**Question** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

**Tours** : 12 · **coût** : 0.174 $ · **confiance annoncée** : 81 · **verdict** : réussi · **citations** : 6/6 lues · **Web** : 0 · **critères** : 11/11

## Réponse

**Sources retenues**
- Base d'idées : rien de capitalisé sur le sujet.
- CTFL-AT 2014 EN §3.2.1 : la démarche pas à pas. ⚠ Ce syllabus est en retrait par l'ISTQB, successeur CTAL-AT.
- CTAL-AT v2.0 EN (2026) §3.1.2 et §3.4.2 : le cadre actuel.
- CTFL v4.0.1 EN §5.1.2, CTAL-TA v4.0 FR §2.2 et CTAL-TM v3.0 FR §1.3.6.
- Je n'ai trouvé aucune section « risk-based testing en agile » dans CTAL-AT v2.0. L'idée n'y apparaît que de façon indirecte. La démarche détaillée vient donc du syllabus de 2014.

Hypothèse de contexte : équipe Scrum ou similaire, itérations courtes, domaine web, non réglementé.

## Méthode pas à pas

1. **Analyser les risques à deux moments.** Pendant la planification de release, les représentants métier donnent une vue d'ensemble des risques et toute l'équipe aide à les identifier. Pendant la planification d'itération, toute l'équipe identifie et évalue les risques qualité. [CTFL-AT 2014 EN, §3.2.1, p. 32]. Le CTFL v4.0.1 dit la même chose : le testeur participe à l'analyse des risques projet et qualité en release planning, puis à l'analyse détaillée des user stories en iteration planning [CTFL v4.0.1 EN, §5.1.2, p. 48].
2. **Lister, identifier, évaluer.** Réunir l'équipe, testeur compris. Lister les éléments du backlog de l'itération. Identifier les risques qualité de chaque élément, sur toutes les caractéristiques de qualité. Catégoriser chaque risque et déterminer son niveau (impact × probabilité). [CTFL-AT 2014 EN, §3.2.1, p. 32]
3. **Proportionner l'effort au risque.** Choisir la technique de test selon le risque, son niveau et la caractéristique de qualité. Les tâches à risque élevé démarrent plus tôt et reçoivent plus de tests. [CTFL-AT 2014 EN, §3.2.1, p. 32]
4. **Atténuer avant l'exécution.** Le syllabus donne un exemple : si l'identification des risques révèle des problèmes dans les user stories, l'équipe les relit à fond. [CTFL-AT 2014 EN, §3.2.1, p. 32]
5. **Réévaluer régulièrement.** Ajuster périodiquement : nouveaux risques, niveaux revus, efficacité des mesures d'atténuation. [CTFL-AT 2014 EN, §3.2.1, p. 32]. En contexte itératif, le pilotage se fait à la fréquence choisie par l'équipe, « vraisemblablement une fois par itération ». Le testeur met à jour le référentiel des risques. [CTAL-TA v4.0 FR, §2.2, p. 28]
6. **Aligner par des ateliers de risques.** Ce sont des *joint risk workshops* avec le métier, les testeurs et les développeurs, pour partager une vision des risques produit critiques. [CTAL-AT v2.0 EN, §3.4.2, p. 29]
7. **Mesurer en rétrospective.** Les questions à poser :
   - Les parties prenantes ont-elles participé à l'analyse ?
   - Les défauts prioritaires sont-ils trouvés tôt ?
   - Les tests ignorés étaient-ils moins risqués que ceux exécutés ?
   
   Le syllabus liste aussi des pièges : estimation difficile, risques répétitifs, parties prenantes qui changent. [CTAL-TM v3.0 FR, §1.3.6, p. 34]

Les étapes 1 à 5 sont décrites pour l'agile. Les étapes 6 et 7 sont plus générales, ou issues de l'amélioration de processus.

## Exemple de mise en œuvre (fictif, interprétation)
Une équipe Scrum de 6 personnes livre une appli web toutes les 2 semaines.
- **Release planning** (étape 1) : un atelier de 45 min avec le Product Owner fait émerger les 5 risques majeurs.
- **Planning d'itération** (étapes 2-3) : chaque story reçoit une cote simple, faible / moyen / élevé. Les stories « élevé » ont un testeur dédié dès le départ, plus des tests exploratoires. Les autres s'en tiennent à des tests automatisés de base.
- **Revue de backlog** (étape 4) : les stories à risque élevé et floues sont relues avant le développement.
- **Revue de mi-itération** (étape 5) : 10 min pour réviser la liste des risques.
- **Rétrospective** (étape 7) : un indicateur, « défauts échappés vs risque coté ».

## Adaptation par domaine
Je n'ai pas lu les sections de domaine ci-dessous : ce sont des pistes, à vérifier avant de les citer.

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Traçabilité et documentation exigées. CTAL-AT §3.1.2 note qu'une organisation réglementée ou averse au risque tend vers des approches plus lourdes [CTAL-AT v2.0 EN, §3.1.2, p. 26]. **Aucun syllabus santé ni IEC 62304** : le dire, Web nécessaire. | CTAL-AT §1.3 (test formel) ; CTAL-TTA §2.8.2 |
| Web | Pas de syllabus web dédié, principes transposés. | CT-PT §3.2 |
| Embarqué | Principalement le syllabus automobile (CT-AuT), en anglais. | CT-AuT |
| Mobile | Syllabus dédié CT-MAT 2019. | CT-MAT §1.8 |
| API | Pas de syllabus API dédié. | CTAL-TTA §2.7 |

## Par quoi je commencerais
1. **Une cote de risque par story au planning d'itération** (étapes 2-3) : impact fort, effort faible.
2. **Un atelier de risques en release planning** (étapes 1 et 6) : impact fort, effort moyen.
3. **Une revue de risques par itération et un indicateur en rétrospective** (étapes 5 et 7) : impact moyen, effort faible.

## Où creuser ensuite
- `section CTFL-AT-2014-en 3.2` : le texte complet de la démarche.
- `section CTAL-TM-3.0-fr 1.3` : techniques de RBT, métriques et pièges.
- `section CTAL-TA-4.0-fr 2` : le rôle du testeur dans l'analyse et le contrôle des risques.
- `section CTAL-AT-2.0-en 3.1` : la stratégie de test agile (quadrants, appétence au risque).

**Confiance : 81/100 (élevée).** Calcul : base 85 × 0,6 = 51 ; 7 passages lus +20 ; 4 syllabus concordants +20 ; exemple et domaines en interprétation −10. Limite : la démarche détaillée vient d'un syllabus 2014 en retrait. Le syllabus agile actuel (CTAL-AT v2.0) est peu explicite sur le RBT.

## Questions à choix
**1. Quel est ton contexte ?**
1. Équipe Scrum ou Kanban, web, non réglementé
2. Contexte réglementé (santé, finance…)
3. Agile à l'échelle (plusieurs équipes)

**2. Quelle suite veux-tu ?**
1. Approfondir les techniques de cotation des risques (CTAL-TM §1.3)
2. Comparer l'ancien CTFL-AT 2014 avec CTAL-AT v2.0
3. Capitaliser l'idée ci-dessous

## À capitaliser ?
Aucun doublon trouvé.

```json
{
  "titre": "Analyse des risques qualité à deux niveaux en agile",
  "resume": "Analyse des risques en planification de release puis d'itération, réévaluée périodiquement, pour proportionner l'effort de test par story.",
  "principe": "Le niveau de risque (impact × probabilité) dimensionne l'effort et le moment des tests de chaque story, et est réévalué à chaque itération.",
  "theme": "rbt",
  "references": [
    {
      "document": "CTFL-AT-2014-en",
      "section": "3.2.1",
      "page": 32,
      "extrait": "Iteration planning : the whole team identifies and assesses the quality risks."
    },
    {
      "document": "CTAL-TA-4.0-fr",
      "section": "2.2",
      "page": 28,
      "extrait": "Dans un cycle de vie itératif, cette surveillance est effectuée à une fréquence déterminée par l'équipe (vraisemblablement une fois par itération)."
    }
  ]
}
```

Les champs sont ceux que j'ai déduits du modèle d'idée, sans lancer `idee modele`. Vérifie-les avant `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher risk-based testing agile`
- `python qa.py chercher risk-based testing agile`
- `python qa.py chercher analyse de risques qualité itération`
- `python qa.py lire 2831 --contexte 1 --max-caracteres 6000; python qa.py lire 2832 --contexte 1 --max-caracteres 5000`
- `python qa.py lire 4576 --contexte 1 --max-caracteres 5000; python qa.py lire 1954 --contexte 1 --max-caracteres 4000`
- `python qa.py chercher risk CTAL-AT --doc CTAL-AT-2.0-en; python qa.py chercher "risk-based testing" agile --doc CTAL-AT`
- `python qa.py lire 1524 --contexte 1 --max-caracteres 5000; python qa.py lire 1535 --contexte 0 --max-caracteres 3500; python qa.py lire 4841 --contexte 0 --max-caracteres 2500`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Analyse des risques qualité à deux niveaux en agile" --resume "Analyse des risques en planification de release puis d'itér`
- `python qa.py themes | head -40; python qa.py confiance --base 85 --lus 7 --concordants 4 --raisonnement 1`
- `python qa.py idee doublons --titre "Analyse des risques qualité à deux niveaux en agile" --resume "Analyse des risques en planification de release puis d'itération, revue périodique" --principe "Le ni`
