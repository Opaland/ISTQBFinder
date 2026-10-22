# M7-shift-left — thomas

**Question** : Je veux mettre en place une démarche shift left testing, comment faire ? Qu'est-ce que cela impose ?

**Tours** : 8 · **coût** : 0.14 $ · **confiance annoncée** : 90 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 0 · **critères** : 7/7

## Réponse

Je termine le rapport. J'ai lu les passages CTFL, CTAL-AT et CT-TAS, et la confiance est calculée.

## Sources retenues
- **Base d'idées** : rien de capitalisé sur le sujet.
- **CTFL v4.0.1 EN** : §2.1.5 Shift Left (p. 27) et §3.1 Static Testing Basics (p. 33). Lus.
- **CTAL-AT v2.0 EN** (2026-04-17) : §4 « Shift Left », §4.1.1, §4.1.3, §4.2 (p. 31-36). Lus. C'est la source la plus riche.
- **CT-TAS v1.0 EN** : §3.1.3 (p. 24-25). Lu.
- **Non lus, repérés seulement** : CT-QDO §2.1.3 (Continuous Testing) et CT-ATLaS-BoK §4.1. Ce dernier précise que le chapitre n'approfondit pas le shift-left.
- Pas de recherche Web : aucun outil nommé, et la bibliothèque couvre bien le sujet.

Hypothèse de contexte : équipe agile ou DevOps sur un produit web ou API, sans contrainte réglementaire forte. Tu n'as pas donné ton contexte, donc le tableau couvre plusieurs domaines.

## Ce que l'ISTQB entend par shift left
Le shift left est le principe du « test précoce » (early testing). On teste plus tôt dans le cycle de vie (SDLC), sans négliger les tests plus tardifs. [CTFL v4.0.1 EN, §2.1.5, p. 27]

## Méthode pas à pas
1. **Obtenir l'adhésion des parties prenantes et accepter le surcoût initial.**
   - Qui : QA Lead, sponsor. Quand : au départ. Livrable : un accord sur l'objectif.
   - Le shift left peut coûter de la formation, de l'effort et de l'argent au début, mais il est censé faire économiser ensuite. Les parties prenantes doivent y adhérer. [CTFL v4.0.1 EN, §2.1.5, p. 27]
2. **Améliorer la base de test (test basis) avant le code.**
   - Qui : testeurs, PO, développeurs. Quand : affinage du backlog (backlog refinement). Livrable : des user stories avec critères d'acceptation testables.
   - Revoir les spécifications du point de vue des testeurs : cela révèle ambiguïtés, incomplétudes et incohérences. [CTFL v4.0.1 EN, §2.1.5, p. 27]
   - Le testware (critères d'acceptation, scénarios BDD, chartes) peut servir d'exigences vivantes. [CTAL-AT v2.0 EN, §4.1.1, p. 32]
   - L'example mapping est une conversation structurée. Elle produit règles, exemples (qui deviennent des cas de test) et questions. Beaucoup de questions ou de règles signalent une story à découper. [CTAL-AT v2.0 EN, §4.1.3, p. 33]
   - Les testeurs et le PO utilisent l'example mapping, l'écriture collaborative des stories et le backlog refinement pour viser une Definition of Ready. [CTFL v4.0.1 EN, §3.1, p. 33]
3. **Valider les exigences tôt.**
   - Qui : analystes et testeurs. Quand : avant le développement. Livrable : des exigences revues, avec glossaire et modèles si besoin.
   - Elles doivent être correctes, non ambiguës, complètes, cohérentes et testables avant le développement. La validation passe par les revues, le prototypage et la modélisation. [CTAL-AT v2.0 EN, §4.2, p. 36]
4. **Écrire des tests avant ou avec le code.**
   - Qui : développeurs et testeurs. Quand : pendant l'implémentation. Livrable : des tests exécutables dans un harnais de test.
   - Écrire les tests avant le code et les faire tourner dans un test harness pendant l'implémentation. [CTFL v4.0.1 EN, §2.1.5, p. 27]
5. **Mettre en place l'intégration continue (CI) avec analyse statique.**
   - Qui : équipe, DevOps. Quand : à chaque commit. Livrable : un pipeline avec tests de composants et analyse statique.
   - Utiliser la CI, et mieux la CD (livraison continue), pour un retour rapide. Faire l'analyse statique avant les tests dynamiques ou en automatique. [CTFL v4.0.1 EN, §2.1.5, p. 27]
   - L'analyse statique est souvent intégrée aux frameworks de CI. [CTFL v4.0.1 EN, §3.1, p. 33]
6. **Rééquilibrer l'automatisation vers le bas de la pyramide.**
   - Qui : responsable de l'automatisation. Quand : en continu. Livrable : une feuille de route (roadmap) et un backlog priorisé.
   - Si la distribution est déséquilibrée, procéder par le bas : si la couverture de code est faible, ajouter des tests de composants, puis en améliorer la qualité. [CT-TAS v1.0 EN, §3.1.3, p. 24]
   - Les tests de composants UI et API avec des doublures de test (mocks, stubs) évitent le recours aux services réels et donnent un retour précoce adapté à la CI/CD. [CT-TAS v1.0 EN, §3.1.3, p. 25]
   - Les tests de contrat permettent de trouver plus tôt les causes racines. [CT-TAS v1.0 EN, §3.1.3, p. 25]
7. **Tester le non-fonctionnel dès le niveau composant, puis compléter par du shift right.**
   - Le non-fonctionnel démarre au niveau composant quand c'est possible. [CTFL v4.0.1 EN, §2.1.5, p. 27]
   - Le shift right déplace des tests après la livraison, avec observabilité, canary releases et dark launches. Il complète le shift left et ne le remplace pas. [CT-TAS v1.0 EN, §3.1.3, p. 25]

## Exemple de mise en œuvre (fictif, interprétation)
Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines, je ferais ceci :
- Un trimestre de pilote, avec un indicateur de départ : la part de défauts détectés après la livraison.
- Une session d'example mapping de 25 minutes par story, avant la planification du sprint (étapes 2 et 3).
- Un seuil d'analyse statique bloquant dans le pipeline, et des tests de composants écrits avec les développeurs (étapes 4 et 5).
- Un chantier de remplacement progressif des tests UI lents par des tests de composants et de contrat (étape 6).

## Adaptation par domaine
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Aucun syllabus santé dans la bibliothèque (IEC 62304 absent). Il faut garder la traçabilité des exigences et des revues, donc probablement une recherche Web sur la norme. | CTAL-AT §4.2 (à transposer) |
| Web | Principes transposés : CI/CD et tests de composants. Pas de syllabus web dédié. | CTFL §2.1.5, CT-TAS §3.1.3 |
| Embarqué | Matériel et HiL (hardware-in-the-loop) limitent les tests précoces. Syllabus surtout automobile (CT-AuT), non lu. | À creuser : CT-AuT §4 |
| Mobile | CT-MAT 2019 existe mais je ne l'ai pas lu. | À chercher |
| API | Doublures, tests de contrat et call graph. | CT-TAS §3.1.3 |

## Ce que le shift left impose
- Accepter un surcoût au départ et obtenir l'adhésion des parties prenantes. [CTFL v4.0.1 EN, §2.1.5, p. 27]
- Faire travailler ensemble testeurs, PO et développeurs dès l'affinage du backlog.
- Mettre en place un pipeline CI avec analyse statique.
- Garder les tests tardifs et y ajouter le shift right, sans les supprimer.

## Par quoi je commencerais
1. **Impact fort, effort faible** : revue des specs et example mapping en affinage (étape 2).
2. **Impact fort, effort moyen** : analyse statique dans la CI (étape 5).
3. **Impact moyen, effort fort** : rééquilibrer la pyramide de tests (étape 6).

## Où creuser ensuite
- `section CTAL-AT-2.0-en 4.1.5` (découpage des user stories) et `4.1.2` (storyboarding, testboarding).
- `section CTFL-4.0.1-en 3.1.2` (valeur du test statique).
- `section CT-QDO-1.0-en 2.1.3` (Continuous Testing).

Le CTAL-AT §4 mentionne aussi des outils d'IA pour détecter les ambiguïtés dans les exigences. Ils doivent compléter l'analyse humaine, pas la remplacer. [CTAL-AT v2.0 EN, §4, p. 32]

**Confiance : 90/100 (élevée)** : base 100, 6 passages lus, 3 syllabus concordants (+20), raisonnement sans source pour l'exemple et l'adaptation par domaine (−10). Elle est plus basse pour les domaines santé, embarqué et mobile, que je n'ai pas lus.

## Questions à choix
**Quel est ton contexte ?**
1. Agile ou DevOps, web ou API
2. Réglementé (santé, finance)
3. Embarqué ou mobile

**Quelle suite veux-tu ?**
1. Approfondir l'example mapping et le découpage de stories (CTAL-AT §4.1)
2. Comparer shift left et shift right (CT-TAS)
3. Capitaliser l'idée (voir ci-dessous)

## À capitaliser ?
Aucun doublon trouvé. Les références proviennent de passages lus.

```json
{
  "titre": "Shift left : déplacer les activités qualité en amont",
  "resume": "Démarche shift left : revue des specs, tests avant le code, CI avec analyse statique, non-fonctionnel dès le niveau composant.",
  "principe": "Tester tôt sans négliger les tests tardifs. Accepter un surcoût initial et obtenir l'adhésion des parties prenantes.",
  "theme": "shift-left",
  "references": [
    {
      "document": "CTFL-4.0.1-en",
      "section": "2.1.5",
      "page": 27,
      "extrait": "Shift left basically suggests that testing should be done earlier (e.g., not waiting for code to be implemented or for components to be integrated), but it does not mean that testing later in the SDLC should be neglected."
    }
  ]
}
```

Les noms de champs sont à confirmer avec `python qa.py idee modele` avant `idee ajouter`. Je ne l'ai pas lancé.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-q/.claude/skills/qa-knowledge`
- `python qa.py idee chercher shift left testing 2>&1 | head -40; python qa.py chercher "shift left" 2>&1 | head -60`
- `python qa.py section CTFL-4.0.1-en 2.1.5 --max-caracteres 3500; python qa.py section CTAL-AT-2.0-en 4 --max-caracteres 5000; python qa.py section CT-TAS-1.0-en 3.1.3 --max-caracteres 5000`
- `python qa.py chercher "early testing static testing reviews requirements" 2>&1 | head -30; python qa.py chercher "shift left DevOps continuous testing pipeline" 2>&1 | head -30`
- `python qa.py section CTAL-AT-2.0-en 4.2 --max-caracteres 4500; python qa.py section CTAL-AT-2.0-en 4.1.3 --max-caracteres 2500; python qa.py section CTFL-4.0.1-en 3.1 --max-caracteres 3000`
- `python qa.py confiance --help 2>&1 | head -20; python qa.py idee doublons --titre "Shift left : déplacer les activités qualité en amont" --resume "Démarche shift left : revue des specs, tests avant co`
- `python qa.py confiance --base 100 --lus 6 --concordants 3 --raisonnement 1 2>&1 | tail -5; python qa.py themes 2>&1 | grep -i -E "shift|statique|agile|devops" | head`
