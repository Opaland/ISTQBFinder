# C1-ambigu — skill

**Question** : Comment on gère les risques ?

**Tours** : 6 · **coût** : 0.261 $ · **confiance annoncée** : 82 · **citations** : 5/5 lues · **Web** : 0 · **critères** : 1/3 (manquent : questions_choix, hypotheses)

## Réponse

La base d'idées ne contient rien sur ce sujet. Les réponses ci-dessous viennent donc des syllabus locaux (CTAL-TM v3.0 FR et CTAL-TA v4.0 FR), dont j'ai lu les passages cités.

## Le principe : un processus en deux temps

Le CTAL-TM décrit le test basé sur les risques (RBT) comme le « processus générique de gestion du risque ». Il a deux activités, enchaînées logiquement mais qui peuvent se chevaucher [CTAL-TM v3.0 FR, §1.3.1, p. 29] :

- **Analyse des risques** : identification, puis évaluation.
- **Contrôle des risques** : suivi et atténuation.

Le syllabus distingue les risques qualité/produit, qui guident les tests, des risques projet. Il demande au Test Manager de participer activement à la gestion des risques projet, surtout ceux liés à l'assurance qualité. Ses exemples sont des exigences ambiguës et des environnements de test insuffisants [CTAL-TM v3.0 FR, §1.3.1, p. 29].

## Pistes par étape

- **Identifier et évaluer** :
  - L'analyse doit inclure diverses parties prenantes, et le Test Manager doit savoir la modérer [CTAL-TM, §1.3.1, p. 29].
  - Il y a deux familles de techniques [CTAL-TM, §1.3.5, p. 33-34]. Les techniques lourdes comme l'AMDE (sévérité, priorité, taux de détection) ou l'analyse par arbres de défaillance. Les techniques légères, où les facteurs se réduisent à l'impact et à la probabilité sur une échelle ordinale. Le syllabus cite PRAM et PRISMA parmi les techniques légères, et SST avec une limite : elle exige des spécifications.
  - Quand le risque n'est pas uniforme, on décompose l'objet de test en éléments (composants, interfaces, caractéristiques) et on évalue chacun [CTAL-TA v4.0 FR, §2.1.1, p. 27].
- **Atténuer** :
  - Le niveau de risque oriente la planification (zones et techniques), l'analyse (conditions de test à couvrir) et l'exécution (ordre des tests) [CTAL-TM, §1.3.1, p. 29].
  - L'analyste de test propose des activités statiques et dynamiques, et indique niveaux, types, techniques, indépendance et exhaustivité. Il privilégie ce qui atténue le risque le plus tôt (shift-left) [CTAL-TA, §2.1.1, p. 27].
- **Suivre** :
  - Le suivi des tests inclut celui des risques : nouveaux risques et ajustement du registre [CTAL-TM, §1.3.1, p. 29].
  - Les risques évoluent, donc le pilotage est régulier : en général une fois par itération en cycle itératif [CTAL-TA, §2.2, p. 28].
  - Quand le temps manque, on réduit les régressions sur critères et on révise leur périmètre à chaque cycle [CTAL-TA, §2.2.1, p. 28].
- **Mesurer en rétrospective** [CTAL-TM, §1.3.6, p. 34] :
  - Les bonnes parties prenantes étaient-elles impliquées ?
  - Les défauts prioritaires sont-ils apparus tôt ?
  - Les incidents critiques en production ont-ils été traités ?
  - Les tests ignorés étaient-ils moins risqués que ceux exécutés ?
  - Les résultats ont-ils pu être expliqués aux parties prenantes en termes de risque ?

## Où creuser ensuite

D'autres syllabus traitent le sujet et je ne les ai pas lus en détail : CT-ATLaS §5.1.5 (risques organisationnels en agile à l'échelle), CT-TAS §4.2.3 (risques de déploiement de l'automatisation) et CTAL-TTA §1.2.2 (évaluation des risques côté technique).

## Par quoi je commencerais (interprétation, pas du syllabus)

1. **Impact élevé, effort faible** : un registre des risques qualité avec un tableau impact × probabilité, élaboré en atelier avec les parties prenantes (technique légère).
2. **Impact moyen, effort faible** : relier chaque risque à des conditions de test et à une priorité d'exécution, puis revoir le registre à chaque itération.
3. **Impact élevé, effort plus élevé** : une AMDE réservée aux zones critiques ou réglementées.

**Confiance : 82/100.** Le socle est solide : passages lus, plusieurs syllabus concordants. Je retire des points parce que votre contexte est inconnu (cycle de vie, taille d'équipe, réglementation) et que je n'ai pas lu les syllabus ATLaS, TAS et TTA en entier.

## Pour cadrer

- Votre cycle de vie est-il agile/itératif ou séquentiel ?
- Visez-vous le risque produit (priorisation des tests) ou les risques projet de l'équipe QA ?
- Y a-t-il des contraintes réglementaires ?

Voulez-vous que je creuse une de ces pistes ? Je peux aussi proposer de capitaliser une idée « démarrer le RBT en version légère » dans la base, mais je n'enregistre rien sans votre accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `(python qa.py idee chercher "gestion des risques" 2>&1 | head -40)`
- `python qa.py idee chercher "gestion des risques"`
- `python qa.py chercher "risk-based testing gestion des risques"`
- `python qa.py section CTAL-TM-3.0-fr 1.3.1; python qa.py lire 11294 --contexte 1; python qa.py lire 8679 --contexte 1`
