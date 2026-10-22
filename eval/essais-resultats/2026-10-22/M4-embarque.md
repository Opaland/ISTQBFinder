# M4-embarque — thomas

**Question** : Comment organiser les niveaux de test et le test d'intégration matériel/logiciel d'un système embarqué (calculateur industriel) ?

**Tours** : 11 · **coût** : 0.174 $ · **confiance annoncée** : 66 · **verdict** : réussi · **citations** : 8/8 lues · **Web** : 0 · **critères** : 7/7

## Réponse

**Sources retenues**
- CTEL-TM 2011 EN, §8.3.3 (lu). Il est ancien (2011), mais c'est la seule source qui traite directement du matériel/logiciel embarqué.
- CT-AuT v2.1.1 EN (2025), §2.4.2 et §3.2 (lus).
- CTAL-TTA v4.0 EN, §4.1 et §2.8.2 (lus).
- Base d'idées : rien de capitalisé sur le sujet.
- Il n'existe aucun syllabus « embarqué industriel ». Le plus proche est l'automobile, que je transpose, et ce choix est une interprétation.
- Je n'ai pas fait de recherche Web : aucun outil ni norme précis n'est nommé dans la question.

Hypothèse de contexte : calculateur industriel avec firmware, cycle en V, matériel en prototype au début. Je n'ai pas supposé de norme de sécurité fonctionnelle imposée.

**Méthode pas à pas**
1. **Définir les niveaux en tenant compte du matériel.** CT-AuT note que, pour ASPICE et ISO 26262, un « système » mêle matériel et logiciel, alors que CTFL ne parle que de logiciel. Fixez donc un vocabulaire commun avec l'équipe. [CT-AuT v2.1.1 EN, §2.4.2, p. 30]
   - Correspondance proposée : composant/unité → intégration logicielle → test du logiciel embarqué sur cible → intégration système (matériel + logiciel) → validation. [CT-AuT v2.1.1 EN, §2.4.2, p. 31]
   - Pour ASPICE et ISO 26262, l'intégration d'un item passe par plusieurs phases : matériel + logiciel d'un élément, puis tous les éléments, puis l'item avec les autres items. [CT-AuT v2.1.1 EN, §2.4.2, p. 31, note 18]
2. **Associer un environnement à chaque niveau, pour décaler les tests vers le virtuel.** Voici la classification de CT-AuT. [CT-AuT v2.1.1 EN, §3.2.4.3, p. 40] [CT-AuT v2.1.1 EN, §3.2.2.2, p. 36]
   - **MiL** (modèle) : conception et fonctions, très tôt.
   - **SiL** (code compilé) : composants et intégration. C'est là qu'on repère les écarts entre modèle et code (flottant contre virgule fixe). Les tests de performance et de fiabilité y sont peu pertinents, car ils dépendent de la cible.
   - **HiL** : tests système sur le vrai matériel.
3. **Mettre en place un laboratoire d'intégration.** Le matériel ou firmware non testé y est isolé de l'environnement de test logiciel. Il doit y « graduer » avant d'entrer en test système. [CTEL-TM 2011 EN, §8.3.3, p. 65]
   - Livrable : un critère de sortie du labo (« graduation ») et une stratégie d'intégration écrite.
4. **Construire le banc HiL.** Il comprend alimentation, calculateur temps réel, pièces réelles, unité d'injection de fautes (coupures et courts-circuits de câbles), breakout box et simulation des bus manquants. [CT-AuT v2.1.1 EN, §3.2.3.1, p. 37]
   - Un HiL tourne en temps réel : on ne peut ni le mettre en pause ni l'arrêter. [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37]
   - Un seul calculateur : « component HiL ». Plusieurs calculateurs : « system HiL » (échanges de données entre eux). [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37]
   - Le choix des points d'accès compte : un mauvais point peut rendre les résultats inutilisables. [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37]
5. **Gérer le prototype et les changements en rafale.** (Test Manager, en continu.) [CTEL-TM 2011 EN, §8.3.3, p. 65]
   - Prévoir dans le planning les pannes d'équipement et des moyens d'occuper les ressources de test pendant ces arrêts.
   - Un comportement de prototype n'est pas forcément un défaut. À l'inverse, un matériel défaillant peut être accepté à tort par le logiciel, qui masque alors le problème.
   - Chaque évolution de matériel ou de firmware déclenche des tests d'intégration répétés : coordonnez les calendriers et réordonnez les livraisons de fonctions.
6. **Traiter les caractéristiques non fonctionnelles selon le niveau.** Benchmarks de performance et consommation de ressources dès le test de composant sur système temps réel ou embarqué. Fiabilité (reprise après incident) en test système. [CTAL-TTA v4.0 EN, §4.1, p. 28]
7. **Régler la profondeur sur le niveau d'intégrité, s'il y a une norme de sécurité.** IEC 61508 définit 4 SIL, avec une couverture structurelle recommandée croissante : 100 % des branches normalement exigé en SIL 3, et MC/DC fortement recommandé en SIL 4. [CTAL-TTA v4.0 EN, §2.8.2, p. 20]

**Exemple de mise en œuvre** (fictif, interprétation)
« Un calculateur de pilotage de presse, avec un firmware sur microcontrôleur et une carte d'E/S. Je ferais ainsi :
- Les tests unitaires et d'intégration logicielle tournent en SiL dans l'intégration continue (étape 2).
- La carte d'E/S prototype passe d'abord au labo d'intégration (étape 3). Elle n'entre dans le banc HiL qu'une fois le critère de graduation atteint.
- Sur le HiL, l'injection de fautes simule une coupure du capteur de position (étape 4).
- Le planning prévoit deux semaines de marge pour les remplacements de prototypes (étape 5). »

**Adaptation par domaine**
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Embarqué industriel (votre cas) | Pas de syllabus dédié. Transposer l'automobile (XiL, ASPICE) et le TM 2011 | CT-AuT §2.4, §3.2 ; CTEL-TM §8.3.3 |
| Santé / réglementé | IEC 62304 absente de la bibliothèque. Pour la couverture par niveau d'intégrité, voir TTA | CTAL-TTA §2.8.2 |
| Web, mobile, API | Sans objet pour le matériel. Les principes de niveaux restent valables | CTFL (niveaux) |

**Par quoi je commencerais**
1. Table de correspondance niveaux ↔ environnements (étapes 1-2). Impact fort, effort faible.
2. Critère de graduation du labo d'intégration (étape 3). Impact fort, effort moyen.
3. Banc HiL avec injection de fautes (étape 4). Impact fort, effort fort : à lancer en parallèle.

**Où creuser ensuite**
- `section CT-AuT-2.1.1-en 3.2.4.1` : avantages et inconvénients de chaque XiL.
- `section CT-AuT-2.1.1-en 4.2.3` : injection de fautes.
- `section CTEL-TM-2011-en 8.3` : autres cas de systèmes spécifiques.

**Confiance : 66/100** (moyenne). Calcul : base 60 × 0,6 = 36 ; 8 passages lus +20 ; 3 syllabus concordants +20 ; raisonnement sans source −10 (exemple et transpositions). Les sources principales sont automobiles ou anciennes (2011), donc la transposition au monde industriel est mon interprétation.

**À capitaliser ?**
```json
{
  "titre": "Intégration matériel/logiciel embarqué : laboratoire d'intégration et passage de relais",
  "resume": "Isoler le matériel/firmware non testé dans un labo d'intégration ; il doit y être validé avant d'entrer en test système.",
  "principe": "Faire graduer le matériel/firmware depuis le labo d'intégration avant le test système.",
  "theme": "niveaux-types",
  "references": [
    {"document": "CTEL-TM-2011-en", "page": 65, "section": "8.3.3", "extrait": "An integration test lab is often used to separate the untested equipment/firmware from the software testing environment. The equipment/firmware has to ―graduate‖ from the integration lab before it can enter the system testing phase."}
  ]
}
```
```json
{
  "titre": "Aligner chaque niveau de test sur un environnement XiL (MiL, SiL, HiL)",
  "resume": "Associer l'environnement de test au niveau pour décaler les tests vers des niveaux virtuels moins coûteux.",
  "principe": "MiL pour la conception, SiL pour composants et intégration, HiL pour le test système.",
  "theme": "niveaux-types",
  "references": [
    {"document": "CT-AuT-2.1.1-en", "page": 40, "section": "3.2.4.3", "extrait": "In system tests, certain functionalities of the test object have been entirely developed. The tester can execute the system test with a HiL test environment."}
  ]
}
```
Le contrôle de doublons n'en signale aucun pour ces deux propositions.

**Questions à choix**
1. Quelle contrainte réglementaire s'applique ?
   1. Sécurité fonctionnelle (IEC 61508 ou dérivée)
   2. Aucune norme particulière
   3. Autre norme (je chercherai sur le Web)
2. Que fait-on ensuite ?
   1. Approfondir les environnements XiL et l'injection de fautes
   2. Comparer avec les niveaux CTFL
   3. Capitaliser les deux idées ci-dessus

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher "embarqué intégration matériel logiciel niveaux de test" 2>&1 | head -40`
- `python qa.py chercher "embedded systems test levels hardware software integration" 2>&1 | head -60`
- `python qa.py chercher "systèmes embarqués intégration matériel logiciel" 2>&1 | head -60`
- `python qa.py section CTEL-TM-2011-en 8.3.3 --max-caracteres 5000 2>&1; echo ======; python qa.py section CT-AuT-2.1.1-en 2.4.2 --max-caracteres 6000 2>&1`
- `python qa.py section CT-AuT-2.1.1-en 3.2.3 --max-caracteres 7000 2>&1; echo ======; python qa.py section CTAL-TTA-4.0-en 4.1 --max-caracteres 4000 2>&1`
- `python qa.py section CT-AuT-2.1.1-en 3.2 --max-caracteres 3500 2>&1; echo ======; python qa.py section CTAL-TTA-4.0-en 2.8.2 --max-caracteres 4500 2>&1`
- `python qa.py section CT-AuT-2.1.1-en 3.2.4.3 --max-caracteres 3000 2>&1; echo =====; python qa.py section CT-AuT-2.1.1-en 3.2.2.2 --max-caracteres 2500 2>&1; echo ====; python qa.py confiance --help 2`
- `python qa.py confiance --base 60 --lus 8 --concordants 3 --raisonnement 1 2>&1; python qa.py idee doublons --titre "Intégration matériel/logiciel embarqué : laboratoire d'intégration et passage de rel`
- `python qa.py idee doublons --titre "Intégration matériel/logiciel embarqué : laboratoire d'intégration et passage de relais" --resume "Isoler le matériel/firmware non testé dans un labo d'intégration;`
