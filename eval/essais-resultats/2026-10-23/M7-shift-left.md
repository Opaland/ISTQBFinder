# M7-shift-left — thomas

**Question** : Je veux mettre en place une démarche shift left testing, comment faire ? Qu'est-ce que cela impose ?

**Tours** : 11 · **coût** : 0.167 $ · **confiance annoncée** : 90 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0 · **critères** : 7/7

## Réponse

**Sources retenues**
- Base d'idées : rien sur le sujet (`idee chercher`).
- CTFL v4.0.1 EN : §2.1.5 « Shift Left », §3.1.2, p. 27 et 33.
- CTAL-AT v2.0 EN : §4 « Shift Left » et §4.2, p. 31 et 36.
- CTAL-TA v4.0 EN : §5.2, p. 50.
- CT-TAS v1.0 EN : §3.1.3, p. 24-25.
- CT-QDO v1.0 EN : §2.1.3, p. 24.
- Non lus en entier : les autres sous-sections de CTAL-AT §4 (4.1 : testboarding, example mapping, découpage des user stories). Je ne les cite que par leurs objectifs d'apprentissage.
- Aucun syllabus santé ni web dédié. Aucune recherche Web : les syllabus couvrent bien le sujet.

L'ISTQB ne donne pas de procédure unique pour le shift left. Il décrit un principe (tester plus tôt), une liste de bonnes pratiques (CTFL) et un chapitre entier dans le CTAL-AT v2.0.

**Hypothèse de contexte** : équipe agile ou DevOps, produit web ou API, sans contrainte réglementaire forte. Si ce n'est pas ton cas, les étapes 5 et 6 changent.

## Méthode pas à pas

1. **Convaincre et cadrer** : sponsor et parties prenantes, avant tout démarrage. Livrable : un accord sur l'investissement initial. « Le shift left peut demander plus de formation, d'effort et de coûts au début, mais devrait économiser ensuite. Il est important que les parties prenantes y adhèrent » [CTFL v4.0.1 EN, §2.1.5, p. 27]. Le shift left ne signifie pas négliger les tests plus tard dans le cycle (même passage).
2. **Revoir les spécifications avec un regard de testeur** : en continu, dès qu'un brouillon existe. Livrable : anomalies d'ambiguïté, d'incomplétude et d'incohérence trouvées avant le code [CTFL v4.0.1 EN, §2.1.5, p. 27]. Le test statique s'applique à presque tout : exigences, backlog, code, plans de test, modèles. Il crée aussi une compréhension partagée si on y associe de nombreux profils [CTFL v4.0.1 EN, §3.1.1-3.1.2, p. 33].
3. **Améliorer la base de test (exigences, user stories)** : testeurs, product owner et développeurs, pendant l'affinage du backlog. Livrable : des stories testables. Le CTAL-AT v2.0 consacre son chapitre 4 à ce point (testboarding, example mapping, découpage des stories, ATDD/BDD) [CTAL-AT v2.0 EN, §4, p. 31]. Il rattache aussi l'ingénierie des exigences au shift left : élicitation continue, analyse, spécification, validation [CTAL-AT v2.0 EN, §4.2, p. 36].
4. **Modéliser et contenir les défauts dans leur phase** : analyste de test, pendant l'analyse. Livrable : modèles (partitions, états, scénarios) qui révèlent les trous. Objectif de la « phase containment » : retirer un défaut dans la phase où il est apparu, ce qui réduit le coût de la qualité [CTAL-TA v4.0 EN, §5.2, p. 50]. Le même passage rapproche cette politique du shift left en agile.
5. **Tests avant ou avec le code, CI/CD, analyse statique** : développeurs et testeurs, à chaque commit. Livrable : tests de composants dans un harnais pendant l'implémentation, pipeline CI/CD avec retour rapide, analyse statique automatisée [CTFL v4.0.1 EN, §2.1.5, p. 27]. Le test continu repose sur « tester tôt et souvent », sur la responsabilité partagée de la qualité et sur l'automatisation dans le pipeline [CT-QDO v1.0 EN, §2.1.3, p. 24].
6. **Descendre les tests non fonctionnels et automatisés vers le bas** : tech lead et testeurs, par itérations.
   - Les tests non fonctionnels démarrent dès le niveau composant [CTFL v4.0.1 EN, §2.1.5, p. 27].
   - Pour rééquilibrer l'automatisation, on procède de bas en haut : on comble d'abord les trous de couverture au niveau composant, puis on améliore la qualité de ces tests (TDD, ateliers de techniques de test) [CT-TAS v1.0 EN, §3.1.3, p. 24].
   - On ajoute des tests de composants UI et API avec des doublures (mocks, stubs), ainsi que des tests de contrat [CT-TAS v1.0 EN, §3.1.3, p. 25].
7. **Mesurer et ajuster** : rétrospectives, indicateurs. Le CTAL-AT recommande de traiter chaque amélioration comme une hypothèse à tester, avec des métriques visibles mais pas de comparaison entre équipes. Il demande aussi de gérer la résistance au changement [CTAL-AT v2.0 EN, §3.4.2, p. 30].

## Exemple de mise en œuvre (fictif, interprétation)
Équipe Scrum de 6 personnes, appli web livrée toutes les 2 semaines.
- Le testeur rejoint l'affinage et applique l'étape 2 puis l'étape 3 : critères d'acceptation en exemples.
- Les développeurs écrivent leurs tests de composants avec les mocks (étape 5).
- Le pipeline bloque sur l'analyse statique et les tests de composants.
- Un test de contrat par API consommée remplace des tests UI de bout en bout (étape 6).
- La rétrospective suit deux indicateurs : défauts trouvés après le sprint et défauts de spécification trouvés avant le code (étape 7).

## Adaptation par domaine
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Pas de syllabus dédié, norme IEC 62304 absente : un Web ciblé serait justifié. Les revues restent à tracer. | CTAL-TTA v4.0 §2.8.2, CTAL-AT v2.0 §3.1.2 (non lus) |
| Web | Tests de composants UI avec doublures, tests de contrat, non fonctionnel tôt. | CT-TAS §3.1.3 (lu) |
| Embarqué | Tests tôt sur simulateur ou HiL. Non vérifié. | CT-AuT, CTEL-TM §8.3.3 |
| Mobile | Non vérifié pour le shift left. | CT-MAT 2019 |
| API | Tests de contrat, mocks, graphe d'appels. | CT-TAS §3.1.3 (lu), CT-QDO §3.2.2 (non lu) |

## Ce que cela impose (interprétation à partir des sources lues)
- **Accord des parties prenantes**, avec un coût initial accepté.
- **Une équipe qui partage la qualité**, pas seulement des testeurs [CT-QDO §2.1.3].
- **Des compétences et de la formation** : modélisation, TDD, BDD.
- **Un pipeline CI/CD et de l'automatisation à entretenir.** Le CTFL liste ces risques : définir le pipeline, maintenir les outils, ressources pour l'automatisation [CTFL v4.0.1 EN, §2.1.4, p. 27].
- **Des tests manuels et tardifs maintenus**, dont ceux du point de vue utilisateur [CTFL §2.1.4 et §2.1.5].

## Par quoi je commencerais
1. Revue des stories par un testeur avant le sprint : impact fort, effort faible.
2. Analyse statique et tests de composants dans la CI : impact fort, effort moyen.
3. Example mapping / ATDD-BDD : impact moyen à fort, effort moyen.

## Où creuser ensuite
- `section CTAL-AT-2.0-en 4.1` : testboarding, example mapping, user story slicing.
- `section CT-TAS-1.0-en 3.1` : distribution de l'automatisation, shift right.
- `section CTAL-TA-4.0-en 5.2` : modélisation et revues.

**Confiance : 90/100 (élevée)** : base 100 × 0,6 ; 8 passages lus +20 ; 5 syllabus concordants +20 ; interprétation sur l'impact et l'effort −10. Pour CTAL-AT §4.1 je n'ai lu que les objectifs d'apprentissage.

## Questions à choix
**Quel est ton contexte principal ?**
1. Agile / DevOps web ou API
2. Cycle séquentiel (V) ou réglementé
3. Mobile ou embarqué

**Quelle suite veux-tu ?**
1. Approfondir CTAL-AT §4 (example mapping, ATDD/BDD)
2. Établir un plan d'indicateurs de validation
3. Capitaliser cette démarche (proposition ci-dessous)

## À capitaliser ?
Pas de doublon (`idee doublons`). Les thèmes suggérés sont statique, shift et exigences. J'ai pris `statique` pour le thème principal, à confirmer. Je n'ai pas repassé l'extrait au vérificateur : c'est `idee ajouter` qui le fera.

```json
{
  "titre": "Démarche shift left : revues, tests de composants et CI",
  "resume": "Déplacer les activités de test plus tôt : revue des spécifications, tests avant ou avec le code, CI/CD, analyse statique, non fonctionnel dès le composant.",
  "probleme": "Défauts découverts tard, rework coûteux, retours lents.",
  "principe": "Revue des specs par les testeurs, base de test améliorée (ATDD/BDD), tests de composants avec doublures et tests de contrat, analyse statique dans le pipeline, rétrospectives.",
  "theme_principal": "statique",
  "themes_secondaires": ["shift", "exigences"],
  "domaine_application": "Équipes agiles ou DevOps ; transposable ailleurs.",
  "prerequis": "Adhésion des parties prenantes ; pipeline CI/CD ; compétences en modélisation et TDD.",
  "benefices": "Moins de rework et retours plus rapides, économies attendues plus tard.",
  "limites": "Coût initial en formation et effort ; ne dispense pas des tests tardifs.",
  "maturite": "documentee",
  "statut": "a_evaluer",
  "provenance": "Recherche du 2026-10-23 : « mettre en place un shift left testing »",
  "references": [
    {"type": "istqb", "doc_id": "CTFL-4.0.1-en", "pages": "27", "section": "2.1.5", "extrait": "Shift left might result in extra training, effort and/or costs earlier in the process"},
    {"type": "istqb", "doc_id": "CTAL-AT-2.0-en", "pages": "36", "section": "4.2", "extrait": "Shift left moves quality activities earlier in the software development lifecycle"},
    {"type": "istqb", "doc_id": "CT-TAS-1.0-en", "pages": "25", "section": "3.1.3", "extrait": "helps achieve a shift left from expensive, slow, and unreliable tests"}
  ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher shift left testing`
- `python qa.py chercher shift left`
- `python qa.py chercher "tests précoces, static testing early involvement"`
- `python qa.py lire 4784 --contexte 1 --max-caracteres 4000; python qa.py section CTAL-AT-2.0-en 4.2 --max-caracteres 6000`
- `python qa.py section CT-TAS-1.0-en 3.1.3 --max-caracteres 6000; python qa.py lire 4798 --contexte 1 --max-caracteres 3500`
- `python qa.py chercher "shift left DevOps continuous testing pipeline" ; python qa.py chercher "early testing 1.3 principle cost of defects"`
- `python qa.py lire 1832 --contexte 1 --max-caracteres 3500; python qa.py lire 972 --contexte 0 --max-caracteres 3000; python qa.py lire 1537 --contexte 1 --max-caracteres 3500`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Shift left : démarche et prérequis" --resume "Déplacer les activités de test plus tôt dans le cycle" --principe "Revue des`
- `python qa.py confiance --base 100 --lus 8 --concordants 5 --raisonnement 1; python qa.py idee modele | head -50`
