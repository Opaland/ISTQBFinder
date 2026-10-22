# M5-mobile — thomas

**Question** : Comment mettre en place les tests d'une application mobile iOS et Android : choix des appareils, risques, automatisation ?

**Tours** : 13 · **coût** : 0.205 $ · **confiance annoncée** : 80 · **verdict** : réussi · **citations** : 12/12 lues · **Web** : 0 · **critères** : 6/6

## Réponse

Le syllabus **CT-MAT 2019** (Mobile Application Testing) couvre presque toute ta question. Les syllabus d'automatisation (CTAL-TAE, CT-TAS) et CT-FT complètent sur les appareils réels et le cloud. Rien n'est encore capitalisé sur ce sujet dans la base d'idées.

**Hypothèse de contexte :** appli grand public (iOS + Android), équipe de taille moyenne, livraisons régulières, pas de cadre réglementaire. Je n'ai pas fait de recherche Web : aucun outil n'est nommé dans ta question.

## Méthode pas à pas

1. **Recenser les risques et défis propres au mobile** (testeurs et responsable produit, au démarrage ; livrable : registre de risques).
   - Risques typiques : fragmentation des appareils, indisponibilité des appareils, nouvelles plateformes en cours de vie, installation et mise à niveau avec conservation des données, réseaux et opérateurs. [CT-MAT v2019 FR, §1.6, p. 17]
   - Défis : plateformes multiples, matériel variable, appareils à faibles ressources, validation par les stores (Google Play, App Store). [CT-MAT v2019 FR, §1.7, p. 18-19]

2. **Associer chaque risque à une atténuation** (QA Lead, avant le plan de test ; livrable : tableau risque → réponse).
   - Fragmentation : tester les appareils les plus courants.
   - Coût multi-plateforme : analyser les plateformes réellement utilisées et écarter celles qui sont hors périmètre.
   - Nouveautés : utiliser les préversions.
   - Appareils manquants : accès distant ou crowd testing.
   - Usages réels : tests sur le terrain. [CT-MAT v2019 FR, §1.8, p. 20]
   - Les méthodes classiques d'analyse de risques restent applicables. [CT-MAT v2019 FR, §1.8, p. 20]

3. **Choisir une approche de couverture des appareils** (QA Lead avec le produit ; livrable : matrice appareils / OS / réseaux).
   - Le syllabus décrit trois approches : plateforme unique, multiplateforme (sélection représentative d'après les analytics du marché cible) et couverture maximale (« généralement pas économiquement viable »). [CT-MAT v2019 FR, §1.6, p. 18]
   - Critères de choix des appareils : part de marché, OS et versions, taille et densité d'écran, disponibilité et coût, capteurs spéciaux, importance pour le public cible. [CT-MAT v2019 FR, §4.4, p. 46]

4. **Répartir émulateurs / simulateurs, appareils réels et laboratoire distant** (livrable : stratégie d'environnements).
   - Émulateurs et simulateurs au début du développement, appareils réels ensuite. Ils sont utiles pour le réseau, le GPS et les interruptions, qui sont coûteux à reproduire sur des appareils réels. [CT-MAT v2019 FR, §1.6, p. 17 ; §4.3.2, p. 46]
   - Laboratoire sur site : bon pour la batterie, le toucher et la sécurité, mais budget élevé. [CT-MAT v2019 FR, §4.4, p. 46]
   - Laboratoire distant (cloud) : à ajouter pour les régressions complètes et les tests non fonctionnels à grande échelle. [CT-MAT v2019 FR, §5.4, p. 51]

5. **Définir la stratégie d'automatisation** (TAE et QA Lead ; livrable : choix d'outils et périmètre).
   - Les approches classiques s'appliquent : capture/rejeu, pilotée par les données, par mots-clés, BDD. [CT-MAT v2019 FR, §5.1, p. 49]
   - Identification des objets : par objets (plus rapide, mais peut identifier des objets cachés, d'où des faux négatifs) ou par image/OCR (fragile dès que la mise en page change). [CT-MAT v2019 FR, §5.2, p. 49-50]
   - Critères d'outil : fonctions récentes (FaceID, empreintes), conditions réseau, données de test, exécution à grande échelle (local ou cloud), reporting, intégration à l'existant. [CT-MAT v2019 FR, §5.3, p. 50-51]
   - Facteurs de stratégie : calendrier, expertise, matériel de test, licences. Les clouds d'appareils sont facturés à l'exécution. [CT-TAS v1.0 FR, §2.1.2-2.1.3, p. 21]

6. **Anticiper les risques de déploiement de l'automatisation** (TAE ; livrable : projet pilote).
   - Avec des appareils réels, il faut qu'ils soient allumés, chargés, connectés au réseau et qu'ils accèdent au SUT. [CTAL-TAE v2.0 FR, §4.2.1, p. 34]
   - Le versionnage du testware est aussi important que celui du SUT. [CTAL-TAE v2.0 FR, §4.2.1, p. 34]
   - Réduire l'instabilité avec des localisateurs fiables, des attentes explicites et une préparation/nettoyage idempotents. Définir une matrice appareils/réseaux et préférer les frameworks de la plateforme. [CT-FT v1.0 EN, §6.4, p. 46] (source du domaine finance, transposée ici)

7. **Piloter par les risques et les retours** (interprétation) : suivre les défauts par appareil, les avis des stores et les statistiques d'usage, puis ajuster la matrice à chaque trimestre.

## Exemple de mise en œuvre (fictif, interprétation)

Une équipe de 6 personnes publie une appli de commande en ligne toutes les 2 semaines.
- **Matrice (étape 3) :** 2 iPhone (iOS actuel et N-1), 3 Android (un haut de gamme, un milieu de gamme, un modèle à faibles ressources), choisis d'après les analytics.
- **Environnements (étape 4) :** émulateurs en intégration continue à chaque commit, laboratoire cloud la nuit sur la matrice complète.
- **Automatisation (étape 5) :** parcours critiques (connexion, paiement) automatisés avec identification par objets. Les tests d'installation, de mise à jour et de réseau dégradé restent exploratoires ou sur le terrain.
- **Pilote (étape 6) :** 2 sprints pour mesurer l'instabilité avant d'élargir.

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Mobile (ton cas) | Tout ce qui précède | CT-MAT §1.6, §4.4, §5 |
| Santé / réglementé | Pas de syllabus santé ni IEC 62304 dans la bibliothèque. Les contraintes de sécurité et de chiffrement se lisent dans CT-FT (finance). | CT-FT §6.4 |
| Web | Pas de syllabus web dédié. CT-MAT traite aussi les applis web mobiles (principes transposés). | CT-MAT §2 |
| Embarqué | Hors sujet pour un téléphone. Les appareils connectés (wearables, IoT) sont mentionnés. | CT-MAT §1.3 |
| API | Pas de syllabus API dédié. À traiter côté serveur, car les défis réseau agissent sur les performances serveur. | CT-MAT §1.7 |

## Par quoi je commencerais
1. **Matrice d'appareils fondée sur tes analytics** : impact fort, effort faible.
2. **Émulateurs en CI et cloud pour la régression** : impact fort, effort moyen.
3. **Pilote d'automatisation limité aux parcours critiques** : impact moyen, effort moyen.

## Où creuser ensuite
- `section CT-MAT-2019-fr 2` : types de tests mobiles (connectivité, capteurs, interruptions, installation).
- `section CT-MAT-2019-fr 3` : niveaux de test et tests sur le terrain.
- `section CTAL-TAE-2.0-fr 4.2` : risques de déploiement de l'automatisation.

**Limite :** CT-MAT date de 2019, donc les pratiques récentes (clouds d'appareils actuels, outils d'automatisation) y sont peu ou pas décrites.

**Confiance : 80/100 (élevée).** Base 84 ; 5 passages lus (+20) ; 2 syllabus concordants (+10). Le calcul est fait par l'outil `confiance`.

## Questions à choix
1. Quel est ton contexte ?
   1. Appli grand public
   2. Appli métier (BtoB)
   3. Appli réglementée (banque, santé)
2. Quelle suite ?
   1. Approfondir les types de tests mobiles (CT-MAT §2)
   2. Comparer les outils d'automatisation (avec recherche Web)
   3. Capitaliser la méthode

## À capitaliser ?
Pas de doublon trouvé. Il n'existe pas de thème « mobile », donc j'ai pris `strategie` (à ajuster si tu préfères `niveaux-types`). Les extraits sont copiés des passages lus.

```json
{
  "titre": "Matrice d'appareils mobiles fondée sur les données d'usage",
  "resume": "Réduire la combinatoire iOS/Android par une sélection représentative d'appareils et d'OS issue des analytics, avec émulateurs tôt, appareils réels et laboratoire cloud ensuite.",
  "principe": "Choisir les appareils selon la part de marché, l'OS, l'écran, le coût et l'importance pour le public cible plutôt que viser la couverture maximale.",
  "theme": "strategie",
  "references": [
    {
      "document": "CT-MAT-2019-fr",
      "section": "1.6",
      "page": 18,
      "extrait": "Approche multiplateforme : Réduire la portée à une sélection représentative d’appareils et de systèmes d’exploitation utilisés par la majorité des clients sur le marché cible, en fonction du trafic mobile ou d’autres données analytiques."
    },
    {
      "document": "CT-MAT-2019-fr",
      "section": "4.4",
      "page": 46,
      "extrait": "La sélection de l’appareil peut se faire sur la base de divers facteurs tels que le r ang de diffusion de l’appareil (comme on le trouve dans Google ou d’autres analyses), le système d’exploitation et les versions, les dimensions et la densité de l’écran, la disponibilité et le coût"
    }
  ]
}
```

Avant de l'enregistrer, vérifie que les champs correspondent bien à `python qa.py idee modele`. Je n'ai rien enregistré.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher mobile appareils automatisation`
- `python qa.py chercher mobile application testing devices`
- `python qa.py chercher tests applications mobiles appareils`
- `python qa.py section CT-MAT-2019-fr 1.6 --max-caracteres 7000; python qa.py section CT-MAT-2019-fr 1.8 --max-caracteres 5000`
- `python qa.py lire 4083 --contexte 1 --max-caracteres 4000; python qa.py lire 189 --contexte 1 --max-caracteres 3000; python qa.py lire 3468 --contexte 1 --max-caracteres 3000`
- `python qa.py chercher emulators simulators real devices mobile --doc CT-MAT`
- `python qa.py page CT-MAT-2019-fr 19-20 --max-caracteres 6000; python qa.py page CT-MAT-2019-fr 46 --max-caracteres 5000; python qa.py lire 4083 --contexte 1; python qa.py lire 189 --contexte 1`
- `python qa.py chercher automatisation tests mobiles outils --doc CT-MAT; python qa.py lire 3468 --contexte 1`
- `python qa.py page CT-MAT-2019-fr 49-51 --max-caracteres 9000`
- `python qa.py confiance --base 84 --lus 5 --concordants 2 2>&1 | tail -5; python qa.py idee doublons --titre "Choisir les appareils mobiles par données d'usage" --resume "Matrice appareils/OS issue des`
- `python qa.py themes | head -40; python qa.py idee doublons --titre "Matrice d'appareils mobiles fondée sur les données d'usage" --resume "Sélection représentative d'appareils/OS, émulateurs tôt, appar`
