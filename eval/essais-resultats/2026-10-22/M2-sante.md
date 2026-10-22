# M2-sante — thomas

**Question** : Je suis Test Manager sur le logiciel d'un dispositif médical. Comment mettre en place la traçabilité des exigences vers les tests et un test basé sur les risques ?

**Tours** : 6 · **coût** : 0.163 $ · **confiance annoncée** : 55 · **citations** : 9/9 lues · **Web** : 1 · **critères** : 7/7

## Réponse

## Sources retenues

- **Lus dans la bibliothèque :**
  - CTFL v4.0.1 EN §1.4.4 (traçabilité).
  - CTAL-TM v3.0 FR et EN §1.3 à 1.3.6 (test basé sur les risques).
  - CT-FT v1.0 EN §3.3 (matrices risques → conditions de test → résultats).
  - CTAL-TA v4.0 §2.1 : lu seulement en introduction, rien n'en est cité plus bas.
- **Base d'idées :** aucune idée capitalisée sur ce sujet.
- **Rien trouvé :** aucun syllabus santé / dispositif médical. `chercher "IEC 62304 dispositif médical"` ne renvoie que des passages sans rapport (ASPICE, accessibilité…).
- **Web :** je l'ai utilisé pour IEC 62304 et ISO 14971, que la bibliothèque ne couvre pas. Les sources sont des blogs et des éditeurs d'outils, pas le texte des normes.

**Hypothèse de contexte :** logiciel de dispositif médical, soumis à IEC 62304 et ISO 14971, avec audit réglementaire. Je ne connais ni la classe de sécurité du logiciel, ni le cycle de vie, ni l'outillage.

## Méthode pas à pas

1. **Fixer le périmètre et la chaîne de traçabilité** (Test Manager, au démarrage, dans le plan de test). Éléments à relier : exigences système, exigences logicielles, risques et mesures de maîtrise, conditions et cas de test, résultats, défauts. La traçabilité sert à vérifier la couverture, mesurer l'impact des changements, faciliter les audits et rendre compte [CTFL v4.0.1 EN, §1.4.4, p. 20-21]. Le Web indique que IEC 62304 §5.1.1 demande de la prévoir entre exigences système, exigences logicielles, tests système et mesures de maîtrise des risques [Web — DQS, dqsglobal.com, consulté le 2026-10-22]. À vérifier dans la norme.
2. **Faire l'analyse de risques avec les parties prenantes** (atelier avec qualité/réglementaire, cliniciens, développeurs, support ; livrable : registre des risques). Techniques : ateliers, entretiens, checklists, retours d'expérience [CTAL-TM v3.0 FR, §1.3.2, p. 29-30]. Le niveau de risque combine probabilité et impact. Pour la sûreté, les besoins de sûreté font partie des facteurs d'impact [§1.3.3, p. 30-31].
   - *Interprétation :* utilise l'analyse ISO 14971 comme registre unique, sans le dupliquer côté test. Les risques « qualité » du syllabus se rattachent alors aux dangers et situations dangereuses.
3. **Rattacher chaque risque à une exigence, puis à un test** (Test Analyst, en analyse et conception ; livrable : matrice risque → exigence → condition de test → cas de test → résultat). Les matrices relient les risques aux conditions de test, puis aux résultats [CT-FT v1.0 EN, §3.3, p. 27]. Le Web décrit la même chaîne : mesure de maîtrise → exigence → implémentation → test → vérification [Web — Matrix One, matrixone.health, consulté le 2026-10-22].
4. **Moduler la rigueur selon le risque** (Test Manager, planification). L'effort est proportionnel au niveau de risque : les risques élevés sont testés tôt et avec des techniques plus rigoureuses. Les facteurs à examiner sont les éléments testés, les niveaux et types de test, l'équipe et l'indépendance [CTAL-TM v3.0 FR, §1.3.4, p. 32 ; EN, p. 30-31]. Les normes de sûreté peuvent imposer des techniques et une couverture selon le niveau d'intégrité, et le Test Manager doit s'assurer qu'elles sont suivies [CTAL-TM v3.0 EN, §1.3.4, p. 31].
   - *Interprétation :* ce niveau d'intégrité correspond à la classe de sécurité A/B/C de IEC 62304. Le syllabus cite IEC 61508 comme exemple, pas IEC 62304.
5. **Prioriser l'exécution** (planification, puis exécution). Deux approches : *depth-first*, par ordre strict de risque décroissant, et *breadth-first*, au moins un test par risque en priorité haute. En pratique on commence en depth-first puis on bascule en breadth-first quand le temps manque [CTAL-TM v3.0 EN, §1.3.4, p. 31].
6. **Suivre et piloter par le risque résiduel** (pendant l'exécution ; livrable : rapports d'avancement exprimés en risques). Le suivi des tests inclut le suivi des risques et l'ajustement du registre [CTAL-TM v3.0 FR, §1.3.1, p. 29]. Le reporting se fait en risque résiduel, ce qui sert à décider d'une livraison ou d'accepter le risque restant [CTAL-TM v3.0 EN, §1.3.4, p. 31]. La traçabilité résultats → risques permet d'évaluer ce risque résiduel [CTFL v4.0.1 EN, §1.4.4, p. 21].
7. **Mesurer en rétrospective** (fin de cycle ou de release). Questions à se poser : parties prenantes représentées ? défauts critiques trouvés tôt ? tests sautés moins risqués que les tests exécutés ? [CTAL-TM v3.0 FR, §1.3.6, p. 34].

## Exemple de mise en œuvre (fictif, interprétation)

Logiciel de pompe à perfusion, classe C, cycle en V avec itérations, outil ALM ou outil dédié.
- Chaque danger de l'analyse de risques a un identifiant (étape 2).
- Chaque mesure de maîtrise devient une exigence logicielle taguée « sécurité ». Chaque exigence est liée à au moins un cas de test (étapes 1 et 3).
- Les exigences taguées C reçoivent des techniques plus fortes (valeurs limites, injection de fautes) et une revue indépendante. Les exigences de classe inférieure reçoivent moins (étape 4).
- Un rapport hebdomadaire liste les risques dont aucun test n'est passé ou dont un test a échoué (étape 6).
- Avant la release, un contrôle vérifie qu'aucune exigence ou mesure de maîtrise n'est orpheline (étape 1).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| **Santé / réglementé (ton cas)** | Les syllabus ne couvrent pas IEC 62304, ISO 14971 ni les exigences d'audit. Seuls des principes transposables existent. Il faut lire les normes elles-mêmes. | CTAL-TM §1.3.4 ; CTAL-TTA v4.0 §2.8.2 (à lire, non lu ici) ; CT-AuT §2.1.2.6 (traçabilité ASPICE, analogie automobile, non lu en entier) |
| Web / embarqué / mobile / API | Non traités, la question portait sur le dispositif médical. | `section CTEL-TM-2011-en 8.3.3` pour l'embarqué (non lu) |

## Par quoi je commencerais

1. **Impact fort, effort faible :** identifier chaque exigence et chaque risque de façon unique, et relier risque → exigence → test dans l'outil existant (étapes 1 et 3).
2. **Impact fort, effort moyen :** organiser l'atelier de risques commun avec le réglementaire (étape 2).
3. **Impact moyen, effort moyen :** moduler la rigueur selon la classe de sécurité et passer au reporting en risque résiduel (étapes 4 et 6).

## Où creuser ensuite

- `section CTAL-TM-3.0-fr 1.3` (en entier, jusqu'à §1.3.5 Techniques RBT, que je n'ai pas lu).
- `section CTAL-TTA-4.0-en 2.8` (couverture par niveau d'intégrité).
- `section CT-AuT-2.1.1-en 2.1.2` (traçabilité bidirectionnelle, par analogie).
- Les textes de IEC 62304 et ISO 14971 : je n'ai pas lu les normes, seulement des blogs.

## Confiance : 55/100 (moyenne)

- La confiance documentaire est de 100/100, avec plusieurs syllabus concordants et lus.
- Moins 10 : l'adaptation à IEC 62304 / ISO 14971 repose sur le Web, et sur des sources secondaires.
- Moins 10 : le lien avec la classe de sécurité est mon interprétation.
- Plafonné à 60 : les normes ne sont couvertes ni par un syllabus ni par leur texte.

## Questions de cadrage

- Quelle classe de sécurité (A, B ou C) et quel cycle de vie (en V ou agile) ?
- Quel outillage (Jira, Polarion, Excel, outil dédié) pour la traçabilité ?

## À capitaliser ?

Aucune proposition. Les références utiles sont déjà lues, mais la chaîne risque → exigence → test dans un contexte réglementé repose surtout sur le Web et sur mon interprétation. Je ne l'enregistre pas sans source ISTQB solide.

## Questions à choix

1. Quelle suite veux-tu ?
   1. Approfondir CTAL-TM §1.3.5 (techniques RBT) et §1.3.6.
   2. Comparer avec la traçabilité ASPICE (CT-AuT) comme modèle d'un domaine réglementé.
   3. Ajouter un syllabus avec `/ajouter-syllabus <code>` si un syllabus santé existe. La couverture est nulle ici.
2. Quel est ton contexte ?
   1. Classe C, cycle en V.
   2. Classe B, agile.
   3. Autre : précise.

Sources :
- [DQS — IEC 62304 traceability framework](https://www.dqsglobal.com/en/explore/blog/iec62304-traceability-framework)
- [Matrix One — software risk control measures](https://matrixone.health/guides/software-risk-control-measures-implementation)
- [jamb — IEC 62304 risk management](https://jamb.readthedocs.io/en/stable/iec-62304/risk-management.html)

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher traçabilité risques exigences dispositif médical; python qa.py chercher traçabilité exigences tests; python qa.py chercher risk-based testing risk analysis`
- `python qa.py lire 11487 --contexte 1; python qa.py section CTAL-TM-3.0-fr 1.3 | head -150; python qa.py chercher IEC 62304 dispositif médical | head -20; python qa.py chercher safety-critical integrit`
- `WebSearch {"query": "IEC 62304 traceability requirements tests ISO 14971 risk control verification software medical device", "mode`
- `python qa.py lire 6874 --contexte 1; python qa.py lire 11094 --contexte 1; python qa.py lire 11295 --contexte 0; python qa.py lire 8676 --contexte 0`
