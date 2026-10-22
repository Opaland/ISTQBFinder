# T2-rbt-agile — thomas

**Question** : Recherche des idées pour intégrer le risk-based testing dans une équipe produit agile.

**Tours** : 13 · **coût** : 0.261 $ · **confiance annoncée** : 81 · **verdict** : réussi · **citations** : 16/16 lues · **Web** : 0

## Réponse

## Sources retenues

- **Base d'idées** : rien de capitalisé sur le sujet (`idee chercher` ne renvoie aucun résultat, `idee doublons` ne trouve rien de similaire).
- **Syllabus lus** :
  - CTFL v4.0.1 EN, §5.1.2 et §5.2.
  - CTAL-TM v3.0 EN, §1.3 à 1.3.5, et FR §1.3.6.
  - CTAL-TA v4.0 EN, §2.1.
  - CTAL-AT v2.0 EN (2026-04-17), §3.1.1 et §3.1.2.
  - CT-ATLaS-BoK v2.0 FR, §4.2.
  - CTFL-AT 2014 EN, §3.2.1. Ce syllabus est **en retrait** et remplacé par CTAL-AT.
- **Web** : non utilisé, car aucun outil ni technologie n'est nommé.
- **Hypothèse de contexte** : équipe Scrum d'environ 6 personnes, appli web, itérations de 2 semaines, pas de contrainte réglementaire forte.

Les syllabus décrivent le risk-based testing (RBT) comme un cycle analyse puis contrôle des risques, relancé à chaque itération.

## Pistes par syllabus

**CTFL v4.0.1 — §5.1.2 et §5.2**
- En *release planning*, les testeurs participent aux analyses de risques projet et qualité. En *iteration planning*, ils participent à l'analyse détaillée des risques par user story. [CTFL v4.0.1 EN, §5.1.2, p. 48-49]
- Le RBT se résume à deux activités. L'analyse comprend l'identification et l'évaluation. Le contrôle comprend l'atténuation et le suivi. [CTFL v4.0.1 EN, §5.2, p. 51]
- Le niveau de risque est la combinaison de la probabilité et de l'impact. Il peut être quantitatif (produit des deux) ou qualitatif (matrice de risques). [CTFL v4.0.1 EN, §5.2.3, p. 53]
- Le résultat de l'analyse détermine le périmètre, les niveaux et types de test, les techniques, la couverture et l'effort. Il sert aussi à prioriser pour trouver tôt les défauts critiques. [CTFL v4.0.1 EN, §5.2.3, p. 53]
- Les réponses au risque ne passent pas toutes par des tests. On peut aussi accepter le risque, le transférer ou prévoir un plan de contingence. Côté tests, on peut choisir des testeurs adaptés, ajuster l'indépendance, faire des revues ou de l'analyse statique. [CTFL v4.0.1 EN, §5.2.4, p. 53]

**CTAL-AT v2.0 (2026) — §3.1 Planification des tests en agile**
- En planification d'itération, on identifie les risques, on priorise les activités de test, on définit des conditions de test de haut niveau et on affine les critères d'acceptation. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
- En planification de release, on évalue les risques qualité sur tout le périmètre et on choisit niveaux, types et techniques pour les atténuer. Le testeur peut animer des *risk-storming sessions* ou un atelier de cartographie mentale. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
- La stratégie de test dépend de l'appétence au risque de l'organisation. Une organisation averse au risque ou réglementée favorise des approches lourdes, traçables et chiffrées. [CTAL-AT v2.0 EN, §3.1.2, p. 26]
- La stratégie doit être revue périodiquement, par exemple après les rétrospectives. [CTAL-AT v2.0 EN, §3.1.2, p. 27]
- *À creuser* : le reste du §3.1.2 (quadrants de test, maturité du produit, observabilité en production).

**CTAL-TM v3.0 — §1.3 Test basé sur les risques**
- Techniques d'identification : entretiens d'experts, ateliers de risques, brainstorming, checklists, rétrospectives, retours d'expérience. Les parties prenantes doivent être le plus larges possible, et les absents clés doivent être repérés. [CTAL-TM v3.0 EN, §1.3.2, p. 28-29]
- Le risque n'est pas uniforme dans l'objet testé. Il faut découper en éléments de test (*test items*) et évaluer chacun séparément. [CTAL-TM v3.0 EN, §1.3.2, p. 29]
- Les facteurs de probabilité incluent la complexité technique, la pression de délai, le taux de changement élevé et le manque d'assurance qualité précoce. Les facteurs d'impact incluent la fréquence d'usage, la criticité, la réputation et l'absence de contournement. [CTAL-TM v3.0 EN, §1.3.3, p. 29-30]
- Le niveau de risque pilote aussi les revues, l'indépendance et l'étendue de la régression. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- Le reporting peut se faire en **risque résiduel**, ce qui aide à décider de la mise en production. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- Deux ordres d'exécution existent. *Depth-first* traite les risques les plus hauts d'abord. *Breadth-first* assure au moins un test par risque. En pratique on commence en profondeur, puis on passe en largeur quand le temps se réduit. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
- Il existe des techniques « lourdes » (FMEA, analyse d'arbre de défaillances, coût d'exposition) pour les systèmes critiques. Les techniques « légères » (PRAM, PRISMA) s'appuient sur une échelle ordinale probabilité × impact. [CTAL-TM v3.0 EN, §1.3.5, p. 31-32]
- Difficultés fréquentes et remèdes, avec des questions de rétrospective pour mesurer le RBT. [CTAL-TM v3.0 FR, §1.3.6, p. 34]
  - Les risques « déjà vus » entraînent de la complaisance.
  - Les risques importants ne sont pas identifiés.
  - Les parties prenantes changent, donc l'analyse doit être itérative et continue, pas faite une seule fois au départ.
  - Le niveau de risque est difficile à estimer.

**CTAL-TA v4.0 — §2.1 Analyse des risques**
- Le suivi du risque se fait à la fréquence choisie par l'équipe, probablement une fois par itération. L'analyste de test (TA) met à jour le registre des risques. [CTAL-TA v4.0 EN, §2.1, p. 25]
- Les facteurs d'évaluation sont la fréquence d'usage, la criticité, les dommages (financiers, environnementaux, de réputation), la qualité de la base de test, et les besoins légaux ou de sécurité. [CTAL-TA v4.0 EN, §2.1, p. 25]
- Il faut proposer pour chaque risque l'activité de test qui l'atténue **le plus tôt possible** (*shift left*), statique ou dynamique. [CTAL-TA v4.0 EN, §2.1, p. 25]
- Le TA catégorise les risques selon le modèle de qualité ISO/IEC 25010. [CTAL-TA v4.0 EN, §2.1, p. 25]

**CTFL-AT 2014 (en retrait, à utiliser comme illustration seulement) — §3.2.1**
- L'analyse des risques se fait à deux endroits. En *release planning*, les représentants métier donnent une vue de haut niveau. En *iteration planning*, toute l'équipe identifie et évalue. [CTFL-AT 2014 EN, §3.2.1, p. 32]
- Le syllabus propose un déroulé en 6 étapes en planification d'itération :
  1. Réunir l'équipe, testeurs inclus.
  2. Lister les éléments du backlog d'itération.
  3. Identifier les risques par élément.
  4. Évaluer chaque risque (catégorie et niveau).
  5. Définir l'étendue des tests proportionnellement au niveau.
  6. Choisir la ou les techniques de test.
  
  [CTFL-AT 2014 EN, §3.2.1, p. 32]
- Les tâches à risque élevé démarrent plus tôt et reçoivent plus de tests. Une revue approfondie des user stories peut déjà atténuer le risque avant l'exécution. [CTFL-AT 2014 EN, §3.2.1, p. 32]

**CT-ATLaS-BoK v2.0 — §4.2 (organisation à l'échelle)**
- Le leader de test agile **conseille** sur le RBT mais ne l'impose pas. Il doit éviter les anti-modèles « Tout normaliser » et « Être la police des tests ». [CT-ATLaS-BoK v2.0 FR, §4.2, p. 58-59]

## Tableau : lourd ou léger ?

| Approche | Principe | Quand l'utiliser | Source |
|---|---|---|---|
| Léger (PRAM, PRISMA, matrice ordinale) | Probabilité × impact sur échelle ordinale, parties prenantes plus restreintes | Contexte non critique, cadence courte : cas par défaut d'une équipe agile | [CTAL-TM v3.0 EN, §1.3.5, p. 32] |
| Lourd (FMEA, arbre de défaillances, coût d'exposition) | Procédures formelles, formules, large groupe de parties prenantes | Systèmes critiques | [CTAL-TM v3.0 EN, §1.3.5, p. 31-32] |

## Ce que j'en retiens (interprétation)

- Le plus rentable est de loger l'analyse de risques dans des rituels existants : affinage du backlog et planification d'itération. Un nouveau processus à côté n'est pas nécessaire. L'ISTQB le prévoit à deux niveaux, release et itération.
- Des échelles ordinales simples suffisent. Le syllabus recommande le léger hors contextes critiques.
- Le risque doit se lire dans les indicateurs : risque résiduel, tests ignorés moins risqués que les tests exécutés, défauts critiques détectés tôt. Sans cela, le RBT reste un exercice formel.
- Les risques de dérive sont la routine (« déjà vu »), des parties prenantes absentes, et un RBT imposé de l'extérieur à l'équipe.

## Par quoi je commencerais

1. **Impact fort, effort faible** : ajouter 15 minutes de risk-storming en affinage ou planification d'itération. On y lie un niveau de risque à chaque user story, et on en déduit une profondeur de test et un ordre d'exécution.
2. **Impact fort, effort faible** : lire la clôture d'itération en termes de risque. On regarde ce qui a été testé, ce qui a été ignoré et quel risque reste.
3. **Impact moyen, effort moyen** : tenir un registre des risques léger, mis à jour une fois par itération, avec les questions de rétrospective du §1.3.6 de CTAL-TM.

## Où creuser ensuite

- `section CTAL-TM-3.0-en 1.3.6`
- `section CTAL-AT-2.0-en 3.1`
- `section CTAL-TA-4.0-en 2.2` (contrôle des risques)
- `section CTFL-4.0.1-en 5.2`

**Confiance : 81/100** (élevée). Calcul : `base 85 × 0,6 = 51 ; 8 passages lus +20 ; 4 syllabus concordants +10… +20 selon l'outil ; raisonnement sans source −10 → 81`. Quatre syllabus courants concordent, mais la section « Ce que j'en retiens » est de l'interprétation. Le syllabus agile le plus détaillé sur la démarche en étapes (CTFL-AT 2014) est en retrait. Je n'ai pas relu les sections TA §2.2 ni CTAL-AT hors §3.1.

## Questions à choix

1. Quel est ton contexte ?
   1. Web / SaaS non réglementé.
   2. Produit réglementé ou critique (santé, finance, embarqué).
   3. Autre (mobile, API…).
2. Quelle suite veux-tu ?
   1. Approfondir : méthode pas à pas avec exemple d'équipe Scrum.
   2. Comparer lourd / léger (FMEA, PRAM, PRISMA).
   3. Capitaliser l'idée ci-dessous.

## À capitaliser ?

Aucun doublon trouvé (`idee doublons`, thème `rbt`).

```json
{
 "titre": "Analyse de risque qualité légère à chaque planification d'itération",
 "resume": "Intégrer le RBT en agile : analyse de risque en planification de release puis d'itération, effort de test proportionnel au niveau de risque, réévaluation à chaque itération.",
 "probleme": "Une équipe agile n'a pas de moyen explicite de décider où concentrer l'effort de test dans une itération courte.",
 "principe": "Lister les éléments du backlog, identifier et évaluer les risques qualité (probabilité × impact sur échelle ordinale), proportionner l'effort et choisir les techniques, puis réévaluer à chaque itération.",
 "theme_principal": "rbt",
 "themes_secondaires": ["agile", "priorisation"],
 "domaine_application": "Équipe produit agile (Scrum), contexte non critique",
 "prerequis": "Testeurs et représentants métier présents en affinage ou planification d'itération",
 "benefices": "Priorisation justifiée, reporting en risque résiduel, détection plus précoce des défauts critiques",
 "limites": "Estimation subjective du risque ; risque de routine ('déjà vu') ; parties prenantes absentes",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-22 : « idées pour intégrer le risk-based testing dans une équipe produit agile »",
 "references": [
  {
   "type": "istqb",
   "doc_id": "CTAL-AT-2.0-en",
   "pages": "25",
   "section": "3.1.1",
   "extrait": "assessing quality risks across the release scope"
  },
  {
   "type": "istqb",
   "doc_id": "CTAL-TM-3.0-en",
   "pages": "31",
   "section": "1.3.4",
   "extrait": "risk-based testing facilitates the provision of a justified recommendation to management"
  }
 ]
}
```

Rien n'est enregistré. Si tu es d'accord, la conversation principale lancera `idee ajouter`.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher risk-based testing agile; python qa.py idee chercher "risque agile"`
- `python qa.py chercher "risk-based testing agile"; python qa.py chercher "risk-based testing"; python qa.py chercher "tests basés sur les risques agile"; python qa.py chercher "quality risk analysis it`
- `python qa.py lire 4841 --contexte 1 --max-caracteres 5000; echo ------; python qa.py lire 1520 --contexte 1 --max-caracteres 5000; echo ------; python qa.py lire 4576 --contexte 1 --max-caracteres 500`
- `python qa.py lire 1762 --contexte 1 --max-caracteres 4000; echo -----; python qa.py lire 3841 --contexte 1 --max-caracteres 3000; echo ----; python qa.py chercher "risk-based testing" --doc CTAL-AT-2.`
- `python qa.py lire --help | head -20; python qa.py section --help | head -20`
- `python qa.py lire 4841 --contexte 1; echo ------; python qa.py lire 1520 --contexte 1; echo ------; python qa.py lire 4576 --contexte 1; echo -----; python qa.py lire 2832 --contexte 1`
- `python qa.py lire 1762 --contexte 1; echo -----; python qa.py lire 1524 --contexte 1; echo ----; python qa.py lire 3841 --contexte 1`
- `python qa.py section CTAL-TM-3.0-en 1.3 --max-caracteres 14000; echo; echo =======; python qa.py section CTFL-4.0.1-en 5.2 --max-caracteres 7000`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Analyse de risque qualité à chaque planification d'itération" --resume "Intégrer le RBT en agile via une analyse légère de`
- `python qa.py confiance --base 85 --lus 8 --concordants 4 --raisonnement 1; python qa.py themes | head -40`
- `python qa.py idee doublons --titre "Analyse de risque qualité légère à chaque planification d'itération" --resume "Intégrer le RBT en agile : analyse de risque en planification de release puis d'itéra`
