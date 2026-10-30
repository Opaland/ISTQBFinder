# S1-rbt — sylvie

**Question** : J'ai vu qu'on pouvait mettre en place une stratégie de test basée sur les risques. Je pense faire ceci : un atelier en début de release avec le PO pour lister les fonctionnalités risquées, on teste ces fonctionnalités en premier et plus en profondeur, et on ne fait que du smoke test sur le reste. Est-ce que je suis aligné ISTQB ? Quel est le niveau de maturité de ma démarche ?

**Tours** : 7 · **coût** : 0.2 $ · **confiance annoncée** : 70 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0 · **fidélité** (juge LLM, indicatif) : 0.72 sur 3 lignes citées, 0 contradiction(s)

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

Ta démarche est dans l'esprit du test basé sur les risques, mais elle est partiellement alignée. Elle n'évalue pas les risques (probabilité × impact). Elle ne prévoit aucun suivi des risques pendant le projet. Elle ne laisse que du smoke test sur le reste, ce qui est plus binaire que ce que décrit le syllabus. Tout est à l'état d'intention, donc le niveau atteint reste plafonné à 1.

## Pratiques reformulées

- P1 : un atelier en début de release avec le PO pour lister les fonctionnalités risquées (intention).
- P2 : tester ces fonctionnalités en premier et plus en profondeur (intention).
- P3 : ne faire que du smoke test sur les autres fonctionnalités (intention).

## Verdicts

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Atelier avec le PO pour lister les fonctionnalités risquées | Intention | Partiellement aligné | Les ateliers sur les risques font partie des techniques d'identification. L'analyse doit inclure diverses parties prenantes, dont la liste est complète et convenue avec le chef de projet. Le PO seul risque d'oublier des parties prenantes clés (technique, exploitation, sécurité, support…). Lister n'est pas évaluer : le syllabus demande la probabilité et l'impact de chaque risque, combinés en un niveau de risque, par exemple dans une matrice de risque. | [CTAL-TM v3.0 FR, §1.3.2, p. 30] ; [CTAL-TM v3.0 FR, §1.3.3, p. 30] ; [CTAL-TM v3.0 FR, §1.3.3, p. 31] |
| P2 Tester d'abord et plus en profondeur les fonctionnalités risquées | Intention | Aligné | Plus le niveau de risque est élevé, plus les tests commencent tôt et plus l'effort est intense. Les tests à risque élevé utilisent des techniques plus rigoureuses. L'ordre d'exécution suit les niveaux de risque (approche « profondeur d'abord »). | [CTAL-TM v3.0 FR, §1.3, p. 29] ; [CTAL-TM v3.0 FR, §1.3.4, p. 32] ; [CTAL-TM v3.0 FR, §1.3.4, p. 33] |
| P3 Smoke test seul sur le reste | Intention | Partiellement aligné | Le syllabus proportionne l'effort au niveau de risque : les risques faibles sont testés plus tard avec des techniques moins rigoureuses. Il ne parle pas de smoke test seul. L'approche « largeur d'abord » donne au moins un test par risque, pour que chaque élément de risque soit testé au moins une fois. Un smoke test unique n'est pas une couverture graduée. Le syllabus cite aussi parmi les autres mesures possibles le plan d'urgence, le transfert et l'acceptation du risque. Accepter de ne pas tester le reste doit donc être une décision de risque explicite, validée par les parties prenantes. | [CTAL-TM v3.0 FR, §1.3.4, p. 32] ; [CTAL-TM v3.0 FR, §1.3.4, p. 33] |

Je n'ai trouvé aucun passage lu qui contredise tes trois pratiques. Aucune n'est donc en « Écart ».

## Ce qui manque

- **Évaluation du risque.** Il manque la probabilité et l'impact par élément, combinés en un niveau de risque. Le syllabus précise que cette évaluation est le plus souvent qualitative, sur des échelles ordinales, avec une matrice de risque. Il cite aussi des facteurs de probabilité (complexité, taux de changement, pression…) et d'impact (fréquence d'usage, criticité, perte de revenus…). [CTAL-TM v3.0 FR, §1.3.3, p. 31]
- **Catégorisation des risques.** Il manque le classement par type (produit ou projet) et par caractéristique de qualité impactée. Ce classement oriente les types de tests à prévoir. [CTAL-TM v3.0 FR, §1.3.3, p. 30] ; [CTAL-TM v3.0 FR, §1.3.4, p. 32]
- **Suivi et contrôle des risques.** Rien n'est prévu pendant la release : suivre les risques connus, analyser les nouveaux, ajuster le registre des risques. L'analyse n'est pas à faire une seule fois au début, car les parties prenantes et les risques changent. Ton atelier « en début de release » seul est donc insuffisant. [CTAL-TM v3.0 FR, §1.3.1, p. 29] ; [CTAL-TM v3.0 FR, §1.3.6, p. 34]
- **Choix du contexte d'atténuation.** Il manque le choix des techniques selon les éléments du test, les caractéristiques de qualité, les niveaux de test, le cycle de vie, l'équipe (les plus qualifiés sur les risques les plus élevés) et les exigences réglementaires. [CTAL-TM v3.0 FR, §1.3.4, p. 32]
- **Reporting en risque résiduel.** Il manque le compte rendu de l'avancement par niveau de risque résiduel. Il permet aussi de recommander au management de prolonger les tests ou d'accepter le risque restant si le temps manque. [CTAL-TM v3.0 FR, §1.3.4, p. 32] ; [CTAL-TM v3.0 FR, §1.3.4, p. 33]
- **Rétrospective sur le test basé sur les risques.** Il manque la mesure du succès : parties prenantes impliquées, défauts prioritaires trouvés tôt, tests ignorés moins risqués que les tests exécutés, incidents en production. [CTAL-TM v3.0 FR, §1.3.6, p. 34]

## Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné

- **Pourquoi 1.** Toutes les pratiques sont des intentions, sans preuve de mise en place (pas de document, de registre ni d'atelier déjà tenu). La grille du dépôt plafonne alors le niveau à 1.
- **Niveau visé.** Tes intentions relèvent d'un niveau 1 bien structuré. Elles ne couvrent pas encore les critères du niveau 2 de la grille du dépôt : stratégie écrite, planification, supervision et contrôle.
- **Pour atteindre le niveau 2.**
  1. Rédiger la stratégie de test basée sur les risques.
  2. Tenir l'atelier avec les bonnes parties prenantes et garder la trace (registre des risques).
  3. Évaluer probabilité × impact.
  4. Traduire les niveaux de risque en priorité et en profondeur de test, y compris pour le « reste » : au moins un test par risque, ou une acceptation explicite.
  5. Suivre les risques et l'avancement des tests pendant la release.
- **Niveaux 3 à 5.** Leurs critères sont une adaptation du dépôt, non détaillée dans les syllabus lus. Il s'agit de la standardisation à l'échelle de l'organisation, du pilotage par indicateurs et de l'optimisation continue.

## Confiance : 70/100 (moyenne)

Calcul : base 84 × 0,6 = 50 ; 13 passages lus +20 ; 2 syllabus courants concordants +10 ; raisonnement sans source −10 → 70.

- La couverture lexicale est élevée et les passages lus du CTAL-TM v3.0 sont concordants. La version FR a été lue en entier sur les points cités, la version EN seulement sur §1.3.1.
- Le niveau de capacité repose sur la grille du dépôt appliquée à ton récit (raisonnement). C'est ce qui baisse le score.

### Limites

- Le contexte n'est pas précisé : agile ou séquentiel, secteur, réglementation. Aucun syllabus de la bibliothèque ne couvre ton cadre réglementaire éventuel, donc toute exigence qui en dépend est non vérifiable.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque. Toute conformité ISO est non vérifiable ici.
- Je n'ai pas lu l'adaptation agile du test basé sur les risques (CTFL-AT 2014, en retrait). Elle est signalée seulement en extrait de recherche.

## Questions à choix

**Dans quel cycle de vie travailles-tu ?**
1. Agile (sprints / releases fréquentes)
2. Séquentiel ou en V
3. Mixte ou autre

**Un cadre réglementaire s'applique-t-il ?**
1. Non
2. Oui, sûreté de fonctionnement ou dispositif médical
3. Oui, banque, finance ou autre

**Quelle suite veux-tu ?**
1. Une liste de contrôle JSON du test basé sur les risques, à conserver
2. Une lecture de la technique de §1.3.5 (matrice de risque, etc.)
3. Un téléchargement d'un syllabus agile via `/ajouter-syllabus CTAL-AT` si utile

## Où creuser ensuite

- À lire : CTAL-TM v3.0 FR §1.3.5 (techniques pour le test basé sur les risques).
- À lire : CTAL-TTA v4.0 EN §1.2.3 (atténuation par le testeur technique).
- À lire : CTFL-AT 2014 FR §3.2.1 (risques qualité en agile, syllabus en retrait).
- À lire : CT-SEC 2016 EN §1.3.2 (échelle de matrice de risque, côté sécurité).

## Traçabilité

- **Date de l'avis :** 2026-10-30.
- **Documents lus :**
  - CTAL-TM-3.0-fr, v3.0, publié le 2024-03-28. Sections lues : §1.3 (p. 29), §1.3.1 (p. 29), §1.3.2 (p. 29-30), §1.3.3 (p. 30-31), §1.3.4 (p. 32-33), §1.3.6 (p. 34).
  - CTAL-TM-3.0-en, v3.0, publié le 2024-05-03. Section lue : §1.3.1 (p. 28).
- **Requête `chercher` :** `"risk-based testing" identification évaluation atténuation`.
- **Commande de confiance :** `confiance --autorite 0 --base 84 --lus 13 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0`.

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/referentiel/grille-m`
- `python qa.py chercher "risk-based testing" identification évaluation atténuation`
- `python qa.py section CTAL-TM-3.0-fr 1.3 --max-caracteres 9000`
- `python qa.py section CTAL-TM-3.0-en 1.3.1 --max-caracteres 5000`
- `python qa.py section CTAL-TM-3.0-fr 1.3.4 --max-caracteres 7000; python qa.py section CTAL-TM-3.0-fr 1.3.6 --max-caracteres 4000`
- `python qa.py confiance --autorite 0 --base 84 --lus 13 --concordants 2 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0`
