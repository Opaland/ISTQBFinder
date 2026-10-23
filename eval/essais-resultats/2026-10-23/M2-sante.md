# M2-sante — thomas

**Question** : Je suis Test Manager sur le logiciel d'un dispositif médical. Comment mettre en place la traçabilité des exigences vers les tests et un test basé sur les risques ?

**Tours** : 9 · **coût** : 0.196 $ · **confiance annoncée** : 73 · **verdict** : réussi · **citations** : 11/11 lues · **Web** : 1 · **critères** : 7/7

## Réponse

**Sources retenues**
- Base d'idées : rien de capitalisé sur ce sujet.
- CTFL v4.0.1 EN §1.4.4 (p. 20-21).
- CTAL-TM v3.0 EN §1.3 (p. 28-31).
- CTAL-TA v4.0 EN §2.2 (p. 26).
- CT-FT v1.0 EN §3.3 (p. 27).
- CTAL-TTA v4.0 EN §2.8.2 (p. 19).
- CT-AuT v2.1.1 EN §2.1.2.6 (p. 23).
- Web : sources secondaires seulement, voir plus bas.
- Rien sur les dispositifs médicaux : la bibliothèque n'a **aucun syllabus santé**, et IEC 62304 et ISO 14971 en sont absents. Pour la norme, les syllabus ne donnent que l'analogie avec la sécurité fonctionnelle et l'automobile.

Hypothèse de contexte : logiciel dispositif médical (SaMD ou embarqué), cycle plutôt séquentiel, soumis à IEC 62304 et ISO 14971, avec un audit réglementaire à passer.

## Méthode pas à pas

1. **Définir la base de test et le modèle de traçabilité.** Le test manager pose les types d'éléments et de liens : exigence, risque, condition de test, cas de test, résultat, anomalie. Livrable : une règle de traçabilité dans le plan de test. L'ISTQB demande de maintenir ces liens tout au long du processus de test [CTFL v4.0.1 EN, §1.4.4, p. 20]. Le CTAL-TM v3.0 aligne le CTAL-TA v4.0 sur le même principe (§2.2).
2. **Mener l'analyse de risques avec les bonnes parties prenantes.** Fais-le au début du projet, en atelier, avec les experts cliniques, la qualité/affaires réglementaires, le développement et le test. Le test manager modère. Livrable : un registre des risques. [CTAL-TM v3.0 EN, §1.3.1-1.3.2, p. 28-29]
3. **Évaluer le niveau de risque.** Combine probabilité et impact. L'impact inclut les besoins de sécurité (« safety needs ») et les sanctions légales. Une matrice qualitative est la norme, sauf données statistiques solides. [CTAL-TM v3.0 EN, §1.3.3, p. 30]
   - Dans ton cas, la sévérité d'ISO 14971 et la classe de sécurité d'IEC 62304 remplacent ou alimentent cette échelle (interprétation).
4. **Choisir une technique lourde.** En système critique pour la sécurité, le CTAL-TM indique que ce sont « très souvent » des techniques lourdes (formelles, documentées, larges groupes de parties prenantes) [CTAL-TM v3.0 EN, §1.3.5, p. 31]. Le CT-FT cite FMEA, FTA et PRISMA comme techniques de priorisation [CT-FT v1.0 EN, §3.3, p. 27].
5. **Dériver les tests des risques et relier les deux.** Le niveau de risque proportionne l'effort et la rigueur des techniques [CTAL-TM v3.0 EN, §1.3.4, p. 30]. Les standards de sécurité peuvent imposer techniques et couverture selon le niveau d'intégrité [CTAL-TM v3.0 EN, §1.3.4, p. 31 ; CTAL-TTA v4.0 EN, §2.8.2, p. 19]. Livrable : une matrice qui relie les risques aux conditions de test, puis les conditions aux résultats [CT-FT v1.0 EN, §3.3, p. 27].
6. **Boucler la traçabilité exigences ↔ tests ↔ risques.** Les cas de test vers les exigences vérifient la couverture. Les résultats vers les risques évaluent le risque résiduel [CTFL v4.0.1 EN, §1.4.4, p. 21]. Prévois la bidirectionnalité, comme l'exige ASPICE dans l'automobile [CT-AuT v2.1.1 EN, §2.1.2.6, p. 23] : chaque exigence a un test, chaque test a une exigence ou un risque, et aucune mesure de maîtrise de risque n'est orpheline.
7. **Exploiter et maintenir.** Lance les tests par ordre de risque (depth-first, puis breadth-first quand le temps manque). Rapporte en risque résiduel pour décider de la mise en production. [CTAL-TM v3.0 EN, §1.3.4, p. 31]
   - Sur changement, la matrice mesure l'impact sur les tests, et le registre des risques pilote la sélection des tests de régression [CTAL-TA v4.0 EN, §2.2, p. 26].
   - Un outil de gestion de configuration peut automatiser cette sélection (même passage).

## Exemple de mise en œuvre (fictif, interprétation)
Pour une application mobile de suivi de glycémie de classe B, voici ce que je ferais.
- J'organise un atelier de risques avec le médecin référent, la qualité, le développement et le test (étape 2).
- Chaque danger du dossier de gestion des risques devient un identifiant, noté par gravité et probabilité (étape 3).
- Chaque mesure de maîtrise devient une exigence logicielle avec un test de vérification, et un test d'efficacité si c'est pertinent (étapes 5-6).
- Le rapport de fin de test indique, par danger, le statut des tests et le risque résiduel (étape 7).

## Adaptation par domaine
| Domaine | Ce qui change | Où lire |
|---|---|---|
| **Santé / réglementé (ton cas)** | Traçabilité bidirectionnelle exigée par l'audit. Rigueur graduée selon la classe de sécurité. Dossier de gestion des risques lié aux exigences. | CTAL-TTA §2.8.2 ; CTAL-TM §1.3.4-1.3.5 ; CTEL-TM 2011 §8.3.4 (ancien). **Pas de syllabus dispositif médical.** |
| Web | Traçabilité surtout outillée (tickets). | CT-QDO §3.1.2 |
| Embarqué | Exigences matériel/logiciel, intégrité par niveau. | CT-AuT §2.1.2 (analogie) |
| Mobile / API | Pas de spécificité de traçabilité ici. | non couvert |

## Le Web, pour la norme
J'ai consulté le Web parce que la bibliothèque ne couvre ni IEC 62304 ni ISO 14971. Ces sources sont des éditeurs d'outils et des cabinets de conseil, donc secondaires. Elles disent que :
- le dossier de risques doit tracer chaque danger jusqu'à sa mesure de maîtrise, puis jusqu'aux exigences et aux tests ;
- la vérification porte sur l'implémentation et sur l'efficacité de la mesure ;
- les écarts fréquents en audit sont une mesure sans exigence ni test, ou une fonction de sécurité sans danger associé ;
- la profondeur de vérification dépend de la classe de sécurité (B/C plus exigeantes).

Sources : [Risk Management Integration (jamb)](https://jamb.readthedocs.io/en/stable/iec-62304/risk-management.html) ; [ISO 14971 risk control traceability gap analysis](https://meddeviceguide.com/blog/iso-14971-risk-control-traceability-gap-analysis-guide) ; [Matrix One, risk control measures](https://matrixone.health/guides/software-risk-control-measures-implementation), consultées le 2026-10-23. Vérifie chaque exigence de clause dans les textes des normes.

## Par quoi je commencerais
1. Un modèle de liens unique, avec les identifiants danger → exigence → test. Impact **fort**, effort **faible**.
2. Un atelier de risques avec une matrice ancrée sur la sévérité ISO 14971. Impact **fort**, effort **moyen**.
3. Un outillage de traçabilité bidirectionnelle avec contrôle automatique des orphelins. Impact **fort**, effort **fort**.

## Où creuser ensuite
- `section CTAL-TM-3.0-en 1.3.5` (techniques lourdes/légères) et `1.3.6` (métriques de succès).
- `section CTAL-TTA-4.0-en 2.8` (couverture et sécurité).
- `section CTAL-TA-4.0-en 2.2` (régression et traçabilité).
- `section CT-FT-1.0-en 3.3` (matrice risques ↔ conditions de test).

**Confiance : 73/100 (moyenne)**, calcul : base 88 × 0,6 = 53 ; 6 passages lus +20 ; 3 syllabus concordants +20 ; Web −10 ; raisonnement −10. Les principes ISTQB sont solides. Les exigences propres à IEC 62304 et ISO 14971 reposent sur des sources secondaires.

## Questions à choix
**Quelle est la classe de sécurité logicielle IEC 62304 ?**
1. Classe A
2. Classe B
3. Classe C

**Quelle suite veux-tu ?**
1. Approfondir les techniques lourdes de RBT (FMEA/FTA)
2. Comparer la traçabilité ISTQB et celle d'ASPICE
3. Capitaliser la chaîne risque-exigence-test

## À capitaliser ?
Pas de doublon (`idee doublons`, thème `rbt`).

```json
{
  "titre": "Chaîne de traçabilité risque-exigence-test en logiciel de dispositif médical",
  "resume": "Relier danger, mesure de maîtrise, exigence et test, avec contrôle des orphelins, pour piloter la couverture et le risque résiduel.",
  "principe": "Un registre de risques alimente les conditions de test ; une matrice bidirectionnelle relie risques, exigences, tests et résultats ; le rapport de test exprime le risque résiduel.",
  "theme": "rbt",
  "references": [
    {"document": "CTFL-4.0.1-en", "page": 21, "extrait": "Traceability of test results to risks can be used to evaluate the level of residual risk in a test object."},
    {"document": "CT-FT-1.0-en", "page": 27, "extrait": "traceability matrices can be created by linking risks to test conditions and the test conditions to test results."}
  ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher traçabilité exigences risques dispositif médical; python qa.py chercher traçabilité exigences tests; python qa.py chercher risk-based testing traceability; python qa.py cher`
- `python qa.py lire 4768 --contexte 1 --max-caracteres 3500; python qa.py lire 149 --contexte 1 --max-caracteres 4000; python qa.py lire 1766 --contexte 1 --max-caracteres 3500; python qa.py chercher "r`
- `python qa.py section CTAL-TM-3.0-en 1.3 --max-caracteres 9000; python qa.py lire 2142 --contexte 0 --max-caracteres 2500`
- `python qa.py page CTAL-TM-3.0-en 31 --max-caracteres 5000; python qa.py lire 3204 --contexte 0 --max-caracteres 2500; python qa.py idee doublons --titre "Traçabilité exigences-risques-tests en disposi`
- `WebSearch {"query": "IEC 62304 ISO 14971 software verification traceability risk control measures requirements tests", "mode": "st`
- `python qa.py themes | head -30; python qa.py idee doublons --titre "Chaîne risque-exigence-test en dispositif médical" --resume "Matrice reliant risques, exigences et tests" --principe "Relier risques`
- `python qa.py idee doublons --titre "Chaîne risque-exigence-test en dispositif médical" --resume "Matrice reliant risques, exigences et tests" --principe "Relier risques, exigences et tests pour pilote`
