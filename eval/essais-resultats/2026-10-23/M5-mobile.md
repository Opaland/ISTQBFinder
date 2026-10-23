# M5-mobile — thomas

**Question** : Comment mettre en place les tests d'une application mobile iOS et Android : choix des appareils, risques, automatisation ?

**Tours** : 14 · **coût** : 0.279 $ · **confiance annoncée** : 69 · **verdict** : ÉCHEC · **citations** : 13/14 lues · **Web** : 3 · **critères** : 6/6

## Réponse

Le syllabus ISTQB le plus utile est **CT-MAT 2019** (Mobile Application Testing, FR et EN). Il traite de la stratégie, des risques, du choix des appareils, des émulateurs, des laboratoires de test et de l'automatisation. Les syllabus CTAL-TAE v2.0 et CT-TAS v1.0 complètent pour les risques de déploiement et les licences des outils.

**Sources retenues**
- CT-MAT 2019 FR (v2019, 2019-05-03) : §1.1, §1.6, §4.3.2, §4.4, §5.1, §5.3, §5.4 lus.
- CTAL-TAE v2.0 FR : §4.2.1, lu en partie (le reste est à la p. 35).
- CT-TAS v1.0 FR : §2.1.2 lu.
- Base d'idées : aucune idée capitalisée sur le sujet.
- `chercher Appium XCUITest Espresso` : aucun passage dans la bibliothèque. J'ai donc fait une recherche Web ciblée sur les documentations officielles (Appium, Android, Apple).

**Hypothèse de contexte** : appli native ou hybride, équipe agile, livraisons régulières, pas de contrainte réglementaire forte. Je n'ai pas lu les §1.2 à 1.5 (modèles métier, types d'applications, architecture), donc je ne les cite pas.

**Méthode pas à pas**

1. **Partir des données d'usage pour choisir les appareils.**
   - Qui et quand : le QA Lead, en début de projet, puis à chaque trimestre.
   - Livrable : une liste priorisée d'appareils et de versions d'OS.
   - Source : le syllabus demande de choisir les appareils et leur priorité à partir de l'analytique (zone géographique, plateforme, version d'OS, répartition par type d'appareil) [CT-MAT v2019 FR, §1.1, p. 10]. Il cite aussi, comme critères, le rang de diffusion, l'OS et ses versions, la taille et la densité d'écran, la disponibilité et le coût, les particularités matérielles et l'importance pour le public cible [CT-MAT v2019 FR, §4.4, p. 46].

2. **Choisir une couverture.** Le syllabus propose trois approches [CT-MAT v2019 FR, §1.6, p. 18] :
   - plateforme unique ;
   - multiplateforme, c'est-à-dire un échantillon représentatif selon le trafic ;
   - couverture maximale, jugée généralement non viable économiquement.
   - Livrable : une matrice appareils × OS.

3. **Lister les risques mobiles et leur réponse.**
   - Qui et quand : l'équipe, à l'analyse des risques produit.
   - Livrable : un registre de risques.
   - Source : fragmentation du marché, coût multi-plateformes, nouvelles technologies, indisponibilité des appareils, usages réels. Les atténuations proposées sont l'échantillon des appareils les plus courants, l'analyse des plateformes utilisées, les versions préproduction, l'accès distant ou le crowd testing, et les tests sur le terrain [CT-MAT v2019 FR, §1.6, p. 20]. Les défis associés sont listés en §1.7 [CT-MAT v2019 FR, p. 18-19].

4. **Répartir émulateurs/simulateurs, appareils réels et laboratoire.**
   - Source : émulateurs et simulateurs tôt, appareils réels ensuite [CT-MAT v2019 FR, §1.6, p. 17]. Les simulateurs réseau et GPS sont utiles car ils sont difficiles à reproduire sur de vrais appareils [CT-MAT v2019 FR, §4.3.2, p. 46].
   - Un laboratoire distant (cloud) sert aux régressions complètes et aux tests non fonctionnels. Il est souvent moins adapté pour le multi-touch, les gestes, le NFC/Bluetooth et la batterie [CT-MAT v2019 FR, §4.4, p. 47 ; §5.4, p. 51].
   - Un labo sur site bien entretenu peut valoir un labo distant [CT-MAT v2019 FR, §5.4, p. 52].
   - Livrable : une politique « quoi tester où ».

5. **Choisir l'approche et l'outil d'automatisation.**
   - Distinguer les tests basés sur l'agent utilisateur (web mobile uniquement) des tests basés sur l'appareil (tous types d'applications). Le web mobile se teste avec les outils web habituels, les applications natives peuvent demander des outils spécifiques ou ceux de la plateforme [CT-MAT v2019 FR, §5.1, p. 48-49].
   - Critères techniques d'évaluation : biométrie (FaceID, empreintes), conditions réseau, données de test, rapports, exécution à grande échelle, intégration, support [CT-MAT v2019 FR, §5.3, p. 50-51].
   - Livrable : une grille d'évaluation et un POC.

6. **Prévoir les risques de déploiement de l'automatisation.**
   - Les appareils réels doivent être allumés, chargés, connectés au réseau et avoir accès à l'application sous test. Packaging, logs et mises à jour sont aussi à prévoir [CTAL-TAE v2.0 FR, §4.2.1, p. 34].
   - La stabilité du labo conditionne la fiabilité d'un job CI [CT-MAT v2019 FR, §5.4, p. 51].
   - Les fermes d'appareils cloud sont facturées à l'usage (licence d'exécution) [CT-TAS v1.0 FR, §2.1.2, p. 21].

7. **Compléter par des tests hors automatisation (interprétation).** Les tests de compatibilité matérielle, d'installation, les tests sur le terrain et la conformité aux magasins d'applications ne s'automatisent pas tous. Ils sont dans le plan CT-MAT §2.1, §3.1 et §3.2, que je n'ai pas lus.

**Outils : ce que dit le Web** (hors ISTQB, consulté le 2026-10-23)
- Appium fournit des drivers `uiautomator2` (Android) et `xcuitest` (iOS) : [Appium Drivers](https://appium.io/docs/en/2.3/ecosystem/drivers/). Depuis Appium 2, les drivers s'installent séparément : [Migrating to Appium 2](https://appium.io/docs/en/2.5/guides/migrating-1-to-2/).
- Espresso est le framework natif Android pour piloter l'interface d'une seule application. Pour Jetpack Compose, Google renvoie vers des API distinctes : [Behavior UI tests](https://developer.android.com/training/testing/ui-tests/behavior).
- XCTest/XCUITest est le framework natif Apple : [XCTest](https://developer.apple.com/documentation/xctest). La documentation archivée date de l'époque Xcode 7, à utiliser avec prudence.
- Interprétation : les frameworks natifs sont plus rapides et plus stables, avec une couverture limitée à une plateforme. Appium offre un code commun aux deux plateformes, mais il est plus lent et plus fragile. Aucun syllabus ne tranche ce choix.

**Exemple de mise en œuvre** (fictif, interprétation)
Dans une équipe Scrum de 6 personnes avec une appli de réservation, livrée toutes les 2 semaines :
- J'extrais les analytics des 90 derniers jours et je retiens les appareils qui couvrent environ 80 % du trafic (étapes 1-2).
- Je garde 2 iPhone et 3 Android physiques sur site, le reste en émulateurs (étape 4).
- Les smoke tests tournent à chaque merge sur émulateurs, les régressions complètes chaque nuit sur ferme cloud (étapes 4-6).
- Un tour de tests exploratoires sur appareils réels avant chaque publication (étape 7).

**Adaptation par domaine**

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Mobile (le vôtre) | Fragmentation, réseaux, capteurs, cycles d'approbation des magasins | CT-MAT §1.6-1.7, §4.4, §5 |
| Santé / réglementé | Évaluer la sécurité du fournisseur de labo distant ; la bibliothèque ne contient pas de syllabus santé (IEC 62304 absent) | CT-MAT §4.4 p. 47 ; Web pour la norme |
| Web | Le web mobile se teste avec les outils web ; la bibliothèque n'a pas de syllabus web dédié | CT-MAT §5.1 |
| Embarqué / IoT | Les objets connectés ou wearables sont des « companion devices » | CT-MAT §1.3 |
| API | Les tests côté serveur sont à traiter à part (cache, connexions ouvertes) | CT-MAT §1.7 ; CTAL-TTA §2.7 non lu |

**Par quoi je commencerais**
1. Matrice d'appareils issue des analytics : impact fort, effort faible.
2. Smoke tests automatisés sur émulateurs/simulateurs dans la CI : impact fort, effort moyen.
3. Ferme d'appareils cloud pour la régression nocturne : impact moyen, effort moyen (coût à l'usage).

**Où creuser ensuite**
- `section CT-MAT-2019-fr 2.1` : tests de compatibilité matérielle.
- `section CT-MAT-2019-fr 3.1` : tests d'installabilité.
- `section CT-MAT-2019-fr 3.2` : tests sur le terrain et approbation des magasins.
- `section CT-MAT-2019-fr 5.2` : méthodes d'automatisation.

**Confiance : 69/100** (moyenne). Calcul : base 82 × 0,6 = 49 ; 8 passages lus +20 ; 2 syllabus concordants +10 ; Web −10. Limites : CT-MAT date de 2019 et ne parle d'aucun outil actuel. Le Web est limité à un résumé de recherche, sans page ouverte en entier.

**Questions à choix**
1. Quel est le type de votre application ?
   1. Native (Swift/Kotlin)
   2. Multiplateforme (Flutter, React Native)
   3. Web mobile / PWA
2. Quelle contrainte domine ?
   1. Budget serré
   2. Réglementation ou sécurité forte
   3. Délais courts avec livraisons fréquentes
3. Quelle suite voulez-vous ?
   1. Approfondir la matrice d'appareils (§1.1, §4.4)
   2. Comparer Appium et les frameworks natifs
   3. Capitaliser (`/ajouter-syllabus` ne s'impose pas : CT-MAT est présent)

**À capitaliser ?** (aucun doublon trouvé ; rien n'est enregistré sans votre accord)

```json
{
  "titre": "Parc d'appareils mobiles guidé par analytics, émulateurs tôt, labo distant en complément",
  "resume": "Choisir les appareils à tester d'après les données d'usage, utiliser émulateurs/simulateurs au début, appareils réels ensuite, et compléter par un laboratoire distant pour la régression.",
  "probleme": "La fragmentation des appareils et OS rend la couverture exhaustive impossible et coûteuse.",
  "principe": "Approche multiplateforme : échantillon représentatif issu des analytics, répartition émulateurs / appareils réels / labo distant selon le niveau et le type de test.",
  "theme_principal": "environnements",
  "themes_secondaires": ["strategie-automatisation", "priorisation"],
  "domaine_application": "Application mobile native ou hybride iOS et Android, équipe agile",
  "prerequis": "Accès aux données d'usage (analytics, stores) ; budget pour quelques appareils réels",
  "benefices": "Couverture proportionnée au risque, coûts maîtrisés, régression stable en CI",
  "limites": "Syllabus de 2019 ; le NFC, le Bluetooth et la batterie se testent mal dans le cloud ; analytics à renouveler régulièrement",
  "maturite": "documentee",
  "statut": "a_evaluer",
  "provenance": "Recherche du 2026-10-23 : « mise en place des tests d'une application mobile iOS et Android »",
  "references": [
    {"type": "istqb", "doc_id": "CT-MAT-2019-fr", "pages": "18", "section": "1.6", "extrait": "Approche multiplateforme : Réduire la portée à une sélection représentative d’appareils"},
    {"type": "istqb", "doc_id": "CT-MAT-2019-fr", "pages": "51", "section": "5.4", "extrait": "Laboratoire de test d’appareils distant"}
  ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher mobile appareils automatisation 2>&1 | head -40; echo ----; python qa.py chercher mobile testing devices 2>&1 | head -40; echo ----; python qa.py chercher tests mobiles appa`
- `python qa.py section CT-MAT-2019-fr 1.6 --max-caracteres 9000 2>&1; echo =====; python qa.py section CT-MAT-2019-fr 1.8 --max-caracteres 5000 2>&1`
- `python qa.py section CTAL-TAE-2.0-fr 4.2.1 --max-caracteres 4000 2>&1; echo =====; python qa.py section CT-TAS-1.0-fr 2.1.2 --max-caracteres 4000 2>&1; echo ====; python qa.py chercher mobile test aut`
- `python qa.py section CT-MAT-2019-fr 5.1 --max-caracteres 6000 2>&1; echo =====; python qa.py section CT-MAT-2019-fr 5.4 --max-caracteres 6000 2>&1; echo =====; python qa.py section CT-MAT-2019-fr 4.3.`
- `python qa.py plan CT-MAT-2019-fr 2>&1 | head -80; python qa.py chercher Appium XCUITest Espresso 2>&1 | head -12`
- `python qa.py section CT-MAT-2019-fr 1.1 --max-caracteres 3500 2>&1; echo =====; python qa.py section CT-MAT-2019-fr 4.4 --max-caracteres 4500 2>&1; echo ====; python qa.py section CT-MAT-2019-fr 5.3 -`
- `WebSearch {"query": "Appium documentation XCUITest driver UiAutomator2 driver", "mode": "standard", "allowed_domains": ["appium.io`
- `WebSearch {"query": "Android Espresso testing documentation developer.android.com UI tests", "mode": "standard", "allowed_domains"`
- `WebSearch {"query": "Apple XCTest UI testing XCUITest documentation", "mode": "standard", "allowed_domains": ["developer.apple.com`
- `python qa.py confiance --help 2>&1 | head -30; python qa.py idee doublons --titre "Choisir le parc d'appareils mobiles par analytics puis compléter par labo distant" --resume "Sélection des appareils `
- `python qa.py themes 2>&1 | head -50; python qa.py confiance --base 42 --lus 8 --concordants 2 --ancien 0 --web 1 2>&1`
- `python qa.py confiance --base 82 --lus 8 --concordants 2 --ancien 0 --web 1 2>&1; python qa.py idee doublons --titre "Parc d'appareils mobiles guidé par analytics, émulateurs tôt, labo distant en comp`
