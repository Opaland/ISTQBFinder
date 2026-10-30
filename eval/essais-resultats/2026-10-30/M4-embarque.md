# M4-embarque — thomas

**Question** : Comment organiser les niveaux de test et le test d'intégration matériel/logiciel d'un système embarqué (calculateur industriel) ?

**Tours** : 9 · **coût** : 0.22 $ · **confiance annoncée** : 75 · **verdict** : réussi · **citations** : 5/5 lues · **Web** : 0 · **critères** : 8/8 · **fidélité** (juge LLM, indicatif) : 0.72 sur 4 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : base d'idées (`idee chercher` : rien de capitalisé sur le sujet). Syllabus lus, tous en anglais : CTEL-TM 2011 EN §8.3.3, CT-AuT v2.1.1 EN §2.4.2, §3.2.3.2 et §3.2.4.3, CTAL-TTA v4.0 EN §4.1 (début). La bibliothèque n'a ni syllabus embarqué industriel ni norme IEC 61508 en entier. Je n'ai pas fait de recherche Web, parce que la question ne nomme aucun outil. La couverture automobile (CT-AuT) est la plus proche, et ce que j'en tire pour un calculateur industriel est transposé.

Les syllabus donnent trois choses : un labo d'intégration où le matériel est qualifié avant le test système, une correspondance entre niveaux ISTQB et niveaux des normes, et une échelle d'environnements MiL/SiL/HiL.

Hypothèse de contexte : calculateur industriel (type automate ou ECU) avec firmware, développement en V ou hybride, sans domaine réglementaire précisé. Les adaptations selon le domaine figurent plus bas.

**Méthode pas à pas**
1. **Fixer le vocabulaire des niveaux.** Qui : Test Manager avec architecte système, au démarrage. Livrable : un tableau de correspondance partagé. Dans CT-AuT, « système » désigne un produit matériel + logiciel, alors que le CTFL ne parle que du logiciel. Le syllabus propose un mapping : composant → intégration composants → système (logiciel embarqué sur cible) → intégration système → système de systèmes → acceptation. [CT-AuT v2.1.1 EN, §2.4.2, p. 31]
2. **Associer un environnement à chaque niveau.** MiL pour valider la conception, SiL pour composants et intégration logicielle compilés, HiL pour le système. Un HiL « composant » teste un calculateur seul, un HiL « système » teste l'échange de données entre plusieurs calculateurs. [CT-AuT v2.1.1 EN, §3.2.4.3, p. 40] [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37]
3. **Décaler le plus possible vers les niveaux virtuels.** Objectif : réduire le coût et le risque, et garder pour chaque niveau les défauts qui lui sont propres (ex. performance au niveau système en HiL). [CT-AuT v2.1.1 EN, §3.2.4.3, p. 40]
4. **Écrire une stratégie d'intégration matériel/logiciel.** Qui : Test Manager, avant l'arrivée des prototypes. Livrable : plan d'intégration avec ordre de livraison des fonctions. Le syllabus recommande un labo d'intégration qui isole matériel et firmware non testés. Le matériel doit en « sortir diplômé » avant le test système. [CTEL-TM 2011 EN, §8.3.3, p. 65]
5. **Planifier les contraintes propres au matériel.** Prévoir plus de temps pour installer les configurations de test, des pannes d'équipement et des moyens de continuer à tester pendant les arrêts. Aligner les calendriers matériel, firmware et logiciel en réunions fréquentes. [CTEL-TM 2011 EN, §8.3.3, p. 65]
6. **Traiter les prototypes avec méthode.** Un prototype peut avoir un comportement que le produit final n'aura pas, et le logiciel peut accepter un comportement matériel erroné, ce qui masque un problème. Il faut donc décider au cas par cas si une anomalie est à déclarer. [CTEL-TM 2011 EN, §8.3.3, p. 65]
7. **Cibler les tests non fonctionnels par niveau.** En test de composant sur système temps réel : benchmarks de performance et consommation de ressources. En test système : fiabilité (reprise après panne). [CTAL-TTA v4.0 EN, §4.1, p. 28]

**Exemple de mise en œuvre** (fictif, interprétation)
Un calculateur de pilotage de machine avec firmware C :
- Je fais des tests unitaires et composants en SiL sur PC (étapes 2-3).
- Je monte un banc d'intégration avec cartes prototypes, où seul le firmware de base est testé (étape 4).
- Quand une carte passe un jeu de tests d'entrée défini (« graduation »), elle rejoint le banc HiL (étape 4).
- Ce banc sert d'abord à chaque calculateur seul, puis à l'ensemble des calculateurs reliés par le bus (étape 2).
- La performance temps réel est mesurée en HiL, car le temps y est réel (étapes 3 et 7).

**Adaptation par domaine**
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Embarqué industriel | Même logique ; la bibliothèque est surtout automobile, il faut transposer. | CT-AuT §2.4, §3.2 ; CTEL-TM §8.3.3 |
| Réglementé / sécurité | Les niveaux d'intégrité de sécurité (SIL, norme IEC 61508) ou ASIL conditionnent les techniques et la couverture exigées. | à lire : CTAL-TTA v4.0 EN §2.8.2 ; CT-AuT §2.2.5 |
| Santé | Pas de syllabus dispositif médical (IEC 62304 absente) ; Web nécessaire. | — |
| Web / mobile / API | Hors sujet ici. | — |

**Par quoi je commencerais**
1. Tableau de correspondance des niveaux et des environnements (impact fort, effort faible).
2. Critères de « graduation » du matériel et labo d'intégration (impact fort, effort moyen).
3. Banc HiL, avec un composant avant le système (impact fort, effort fort).

**Où creuser ensuite**
- `section CT-AuT-2.1.1-en 3.2` pour les environnements XiL, dont §3.2.4.2 sur le niveau de test attribué selon l'intégrité.
- `section CTAL-TTA-4.0-en 2.8.2` pour les systèmes liés à la sécurité.
- `section CTEL-TM-2011-en 8.3` pour les autres types de projets.

**Confiance : 75/100** (élevée) : base 75 × 0,6 = 45 ; 5 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10 (exemple et transposition industriel) → 75. CTEL-TM date de 2011, et la transposition à l'industriel reste mon interprétation.

**Questions à choix**
1. Quel est votre contexte ?
   1. Industriel sans exigence de sécurité fonctionnelle
   2. Sécurité fonctionnelle (SIL / IEC 61508)
   3. Autre domaine réglementé
2. Quelle suite voulez-vous ?
   1. Approfondir MiL/SiL/HiL (CT-AuT §3.2)
   2. Approfondir le niveau d'intégrité et la couverture (CTAL-TTA §2.8.2)
   3. Capitaliser la proposition ci-dessous

**À capitaliser ?** Rien n'est enregistré sans accord. Aucun doublon trouvé.
```json
{
 "titre": "Embarqué : labo d'intégration puis test système, avec environnements MiL/SiL/HiL par niveau",
 "resume": "Isoler le matériel et le firmware non testés dans un labo d'intégration avant le test système, et associer chaque niveau de test à un environnement (MiL, SiL, HiL).",
 "probleme": "Les changements répétés de matériel, firmware et logiciel provoquent des réintégrations qui bloquent la progression des tests.",
 "principe": "Le matériel doit réussir l'intégration avant d'entrer en test système ; on décale les tests vers des niveaux virtuels moins coûteux quand c'est possible.",
 "theme_principal": "niveaux-types",
 "themes_secondaires": [],
 "domaine_application": "Systèmes embarqués matériel + logiciel (calculateurs), cycle en V ou hybride",
 "prerequis": "Prototypes disponibles, simulateur ou banc HiL, calendriers alignés entre équipes",
 "benefices": "Moins de réintégrations, défauts trouvés au niveau adapté, coût de test réduit",
 "limites": "Syllabus de référence surtout automobile ; transposition à l'industriel non validée ; CTEL-TM date de 2011",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « niveaux de test et intégration matériel/logiciel d'un système embarqué (calculateur industriel) »",
 "references": [
  {"type": "istqb", "doc_id": "CTEL-TM-2011-en", "pages": "65", "section": "8.3.3", "extrait": "graduate"},
  {"type": "istqb", "doc_id": "CT-AuT-2.1.1-en", "pages": "40", "section": "3.2.4.3", "extrait": "Transfer of tests to earlier, less costly and virtual test levels"}
 ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher niveaux de test intégration matériel logiciel embarqué; python qa.py idee chercher embedded hardware software integration`
- `python qa.py chercher hardware software integration testing embedded; python qa.py chercher intégration matériel logiciel système embarqué; python qa.py chercher test levels embedded systems model-in-`
- `python qa.py section CTEL-TM-2011-en 8.3.3 --max-caracteres 6000; python qa.py section CT-AuT-2.1.1-en 2.4.2 --max-caracteres 6000`
- `python qa.py section CT-AuT-2.1.1-en 3.2.3.2 --max-caracteres 5000; python qa.py section CT-AuT-2.1.1-en 3.2.4.3 --max-caracteres 6000`
- `python qa.py section CTAL-TTA-4.0-en 4.1 --max-caracteres 3500; python qa.py idee doublons --titre "Intégration matériel/logiciel embarqué : labo d'intégration puis passage en système" --resume "Isole`
- `python qa.py themes | head -30; python qa.py confiance --base 75 --lus 5 --concordants 3 --raisonnement 1`
- `python qa.py idee doublons --titre "Intégration matériel/logiciel embarqué : labo d'intégration puis passage en test système" --resume "Isoler matériel/firmware non testé dans un labo d'intégration av`
