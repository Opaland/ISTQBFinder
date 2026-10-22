# M2-sante — thomas

**Question** : Je suis Test Manager sur le logiciel d'un dispositif médical. Comment mettre en place la traçabilité des exigences vers les tests et un test basé sur les risques ?

**Tours** : 11 · **coût** : 0.194 $ · **confiance annoncée** : 73 · **verdict** : réussi · **citations** : 12/12 lues · **Web** : 1 · **critères** : 7/7

## Réponse

## Sources retenues

- **Lus :**
  - CTFL v4.0.1 EN, §1.4.4, p. 20-21.
  - CTAL-TM v3.0 EN, §1.3.1 à §1.3.4, p. 28-31. Je n'ai pas lu la fin du §1.3.4, qui traite du suivi du test basé sur les risques.
  - CTEL-TM 2011 EN, §8.3.4, p. 66.
  - CT-FT v1.0 EN, §2.4.1, p. 22.
  - CT-AuT v2.1.1 EN, §2.1.2.6, p. 23.
- **Rien dans la base d'idées** sur le sujet (`idee chercher` : aucun résultat).
- **Aucun syllabus santé / dispositif médical** dans la bibliothèque. IEC 62304 et ISO 14971 ne sont donc pas couvertes. J'ai fait une recherche Web ciblée pour combler ce manque.

Les syllabus donnent le « quoi » et le « pourquoi » de la traçabilité et du test basé sur les risques. La norme de ton secteur (IEC 62304 avec ISO 14971) donne le « combien » et le « quelles preuves ».

**Hypothèse de contexte :** logiciel de dispositif médical soumis à IEC 62304 (marquage CE ou FDA), cycle de vie plutôt séquentiel ou hybride, équipe de taille moyenne.

## Méthode pas à pas

1. **Définir la chaîne de traçabilité et ses identifiants.** Le Test Manager la fixe au démarrage, dans le plan de test.
   - Livrable : un schéma des liens, avec une ID unique par élément.
   - Les éléments à relier sont la base de test, les conditions de test, les risques, les cas de test, les résultats et les anomalies [CTFL v4.0.1 EN, §1.4.4, p. 20].
   - Pour un dispositif médical, j'ajouterais les dangers (hazards) et les mesures de maîtrise du risque (interprétation, voir étape 6).
2. **Rendre la traçabilité bidirectionnelle.**
   - Sens avant : exigence → cas de test. Sens arrière : résultat ou anomalie → exigence ou règle d'origine [CT-FT v1.0 EN, §2.4.1, p. 22].
   - Les cas de test relient aux exigences prouvent la couverture. Les résultats reliés aux risques donnent le risque résiduel [CTFL v4.0.1 EN, §1.4.4, p. 21].
   - Le même syllabus cite l'analyse d'impact des changements et la préparation des audits.
   - CT-AuT donne un modèle vertical et horizontal, plus un lien entre demandes de changement et anomalies [CT-AuT v2.1.1 EN, §2.1.2.6, p. 23]. Il s'agit d'ASPICE (automobile), à transposer.
3. **Analyser les risques qualité avec des parties prenantes variées.**
   - Techniques d'identification citées : entretiens d'experts, ateliers, brainstorming, listes de contrôle, retours d'expérience. Les parties prenantes participantes sont à valider avec le chef de projet [CTAL-TM v3.0 EN, §1.3.2, p. 28-29].
   - Dans ton contexte, cela suppose les affaires réglementaires, la gestion des risques et le clinique.
4. **Évaluer le niveau de risque.**
   - Le niveau combine la probabilité et l'impact. Souvent l'échelle est qualitative, avec une matrice de risque [CTAL-TM v3.0 EN, §1.3.3, p. 29-30].
   - Parmi les facteurs d'impact figurent la criticité de la fonction, les sanctions légales et les « safety needs ».
5. **Adapter l'effort de test au niveau de risque.**
   - Un risque élevé donne des tests plus tôt et plus rigoureux, un risque faible des tests plus tardifs et plus légers [CTAL-TM v3.0 EN, §1.3.4, p. 30].
   - Le niveau de risque influence aussi les revues des cas de test, l'indépendance du test et l'étendue de la régression [CTAL-TM v3.0 EN, §1.3.4, p. 31].
   - Il guide la sélection des conditions de test et l'ordre d'exécution [CTAL-TM v3.0 EN, §1.3.1, p. 28].
6. **Caler la rigueur sur la norme.**
   - Le syllabus prévoit que des normes de sûreté (il cite IEC 61508) imposent techniques et couverture selon le niveau d'intégrité. Le Test Manager doit s'assurer qu'elles sont suivies [CTAL-TM v3.0 EN, §1.3.4, p. 31].
   - Pour IEC 62304, des sources secondaires indiquent trois classes (A, B, C) fixées via ISO 14971. Les classes B et C appellent une traçabilité plus stricte et des tests plus poussés [Web — IEC 62304 Compliance guide, freyrsolutions.com, consulté le 2026-10-22].
   - Ces sources sont des blogs. **Vérifie les clauses dans le texte des normes.**
7. **Conserver les preuves et les versions.** Les exigences du secteur peuvent fixer le niveau de documentation, les outils permis, la couverture et les critères de sortie. Les documents sont versionnés et les changements validés. L'équipe maintient les matrices de traçabilité [CTEL-TM 2011 EN, §8.3.4, p. 66]. Pour l'auditabilité (preuves inaltérables, reproductibilité), CT-FT offre un modèle [CT-FT v1.0 EN, §2.4.1, p. 22], issu de la finance et à transposer.
8. **Suivre et rapporter par risque.** La surveillance des tests inclut celle des risques : nouveaux risques et mise à jour du registre [CTAL-TM v3.0 EN, §1.3.1, p. 28].

## Exemple de mise en œuvre (fictif, interprétation)

« Pour une pompe à perfusion pilotée par logiciel de classe C, je ferais ceci :
- Chaque exigence reçoit une ID (REQ-xxx), reliée à un danger du dossier de gestion des risques (HAZ-xx).
- Chaque danger a une mesure de maîtrise (RC-xx) et des cas de test (TC-xxx) qui la vérifient (étapes 1-2).
- Un atelier avec le clinique, la R&D et les affaires réglementaires classe les risques sur une matrice 5×5 (étapes 3-4).
- Les risques élevés reçoivent des tests de limites, des tests négatifs et une revue indépendante des cas. Les risques faibles reçoivent un test simple (étape 5).
- Chaque release produit un rapport de traçabilité : exigences non couvertes, risques résiduels, anomalies ouvertes par risque (étapes 7-8). »

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| **Santé / réglementé (ton cas)** | Les classes IEC 62304 et ISO 14971 fixent la rigueur. La documentation et les preuves sont auditables. | CTEL-TM §8.3.4, CTAL-TM §1.3.4, CT-FT §2.4. **Pas de syllabus dispositif médical** : lire les normes. |
| Web | Pas de contrainte d'audit. Traçabilité allégée via les user stories. | CT-QDO §3.1.2 |
| Embarqué | Tests matériel/logiciel intégrés, lab d'intégration. | CTEL-TM §8.3.3 |
| Mobile / API | Non pertinent ici. | — |

## Par quoi je commencerais

1. **Impact fort, effort faible :** définir la chaîne d'ID et la matrice exigences, risques, tests. Un tableur versionné suffit pour démarrer.
2. **Impact fort, effort moyen :** atelier d'analyse de risques avec toutes les parties prenantes, et lien entre risques et tests (étapes 3-5).
3. **Impact moyen, effort moyen :** obtenir ou lire IEC 62304 et ISO 14971, puis aligner les critères de sortie sur la classe de sécurité.

## Où creuser ensuite

- `section CTAL-TM-3.0-en 1.3` (la suite du §1.3.4, puis les §1.3.5 et §1.3.6 : techniques du test basé sur les risques, métriques).
- `section CTAL-TA-4.0-en 2` (rôle de l'analyste de test dans le test basé sur les risques).
- `section CT-FT-1.0-en 2.4` (auditabilité).
- `section CTEL-TM-2011-en 8.3.4` (systèmes critiques pour la sécurité).

**Confiance : 73/100 (moyenne)** — base 88 × 0,6 = 53 ; 9 passages lus +20 ; 3 syllabus concordants +10... le calcul de l'outil donne +20 pour les concordants ; Web −10 ; raisonnement sans source −10 → 73. Les syllabus concordent sur la traçabilité et le test basé sur les risques, mais les normes médicales n'ont été vues que via des sources secondaires.

## Questions à choix

1. **Quelle est la classe de sécurité IEC 62304 visée ?**
   1. A ou B.
   2. C.
   3. Pas encore déterminée.
2. **Quelle suite veux-tu ?**
   1. Approfondir le test basé sur les risques (techniques, métriques).
   2. Approfondir la traçabilité (outillage, audit).
   3. Capitaliser les propositions ci-dessous.

## À capitaliser ?

Les références ci-dessous reprennent des extraits lus. L'extrait de la proposition est à recopier tel quel au moment de `idee ajouter`.

```json
{
  "titre": "Chaîne risque-exigence-test pour logiciel réglementé",
  "resume": "Traçabilité bidirectionnelle exigences-risques-tests et rigueur de test proportionnée au niveau de risque, pour un logiciel soumis à une norme de sûreté.",
  "principe": "Le niveau de risque pilote la rigueur de test; la traçabilité fournit la preuve de couverture et le risque résiduel.",
  "theme": "reglementee",
  "references": [
    {"doc": "CTFL-4.0.1-en", "page": 21, "extrait": "Traceability of test cases to requirements can verify that the requirements are covered by test cases."},
    {"doc": "CTAL-TM-3.0-en", "page": 30, "extrait": "Testing for higher risk levels should start early and use more rigorous test techniques"}
  ]
}
```

Doublons vérifiés : aucune idée similaire. Le thème `tracabilite` n'existe pas ; `reglementee` convient, avec `rbt`, `couverture` et `exigences` en thèmes secondaires.

Sources :
- [IEC 62304 Compliance guide — Freyr Solutions](https://freyrsolutions.com/blog/iec-62304-compliance-the-complete-guide-to-medical-device-software-development-without-the-pitfalls) (secondaire, consulté le 2026-10-22)
- [Software Safety Classifications — jamb docs](https://jamb.readthedocs.io/en/latest/iec-62304/safety-classifications.html) (secondaire, consulté le 2026-10-22)

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher traçabilité exigences tests risques; python qa.py idee chercher dispositif médical`
- `python qa.py chercher traçabilité exigences tests; python qa.py chercher risk-based testing risk assessment; python qa.py chercher medical device regulated safety-critical traceability`
- `python qa.py lire 4768 --contexte 1 --max-caracteres 3500; python qa.py section CTAL-TM-3.0-en 1.3.1 --max-caracteres 4000; python qa.py lire 137 --contexte 1 --max-caracteres 3000; python qa.py lire `
- `python qa.py section CTAL-TM-3.0-en 1.3.2 --max-caracteres 4000; python qa.py section CTAL-TM-3.0-en 1.3.3 --max-caracteres 3500; python qa.py lire 3204 --contexte 1 --max-caracteres 3000`
- `python qa.py lire 4768 --contexte 1; python qa.py lire 137 --contexte 1; python qa.py lire 2707 --contexte 1; python qa.py lire 3204 --contexte 1; python qa.py section CTAL-TM-3.0-en 1.3.4 --max-carac`
- `WebSearch {"query": "IEC 62304 software safety classification traceability requirements tests ISO 14971 risk control verification"`
- `python qa.py idee doublons --titre "Traçabilité exigences-risques-tests pour dispositif médical" --resume "Chaîne de traçabilité bidirectionnelle et test basé sur les risques en contexte réglementé" -`
- `python qa.py themes | head -40; python qa.py confiance --base 88 --lus 9 --concordants 3 --web 1 --raisonnement 1`
- `python qa.py idee doublons --titre "Chaîne risque-exigence-test pour logiciel réglementé" --resume "Traçabilité bidirectionnelle exigences-risques-tests et rigueur de test proportionnée au niveau de r`
