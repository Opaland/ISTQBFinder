# M5-mobile — thomas

**Question** : Comment mettre en place les tests d'une application mobile iOS et Android : choix des appareils, risques, automatisation ?

**Tours** : 14 · **coût** : 0.197 $ · **confiance annoncée** : 68 · **citations** : 12/13 lues · **Web** : 0 · **critères** : 6/6

## Réponse

Je m'arrête sur la vérification des doublons : le shell a refusé la commande, et la base d'idées n'avait de toute façon rien sur le sujet. Voici le rapport.

## Sources retenues
- **Base d'idées** : `idee chercher` ne renvoie rien sur le mobile. Le contrôle de doublons de la proposition ci-dessous n'a pas pu tourner.
- **CT-MAT 2019 (Mobile Application Testing), FR et EN** : syllabus dédié, lu en §1.6, 1.7, 1.8, 4.3, 4.4, 5.1, 5.3 et 5.4. Il date de 2019 : le principe est solide, mais les outils cités sont anciens.
- **CTAL-TAE v2.0 FR** (§4.2.1), **CT-TAS v1.0 FR** (§2.1.2), **CT-FT v1.0 EN** (§6.4) : l'automatisation sur appareils réels et les fermes d'appareils.
- Je n'ai pas fait de recherche Web : ta question ne nomme aucun outil.

**Hypothèse de contexte** : appli native ou hybride, équipe agile, pas de contrainte réglementaire forte, budget limité.

## Méthode pas à pas
1. **Partir des données d'usage.** Le testeur doit pouvoir choisir et prioriser les appareils à partir des analytics (géographie, plateforme, version d'OS, type d'appareil) [CT-MAT 2019 FR, §1.1, p. 10]. Livrable : liste priorisée, par le QA lead et le produit, avant le premier sprint.
2. **Choisir l'approche de couverture.**

| Approche | Principe | Verdict |
|---|---|---|
| Plateforme unique | Un seul appareil, une version d'OS, un opérateur, un type de réseau | Trop étroite |
| Multiplateforme | Sélection représentative couvrant la majorité des clients, selon les analytics | **Le plus réaliste** |
| Couverture maximale | Tout couvrir | « Généralement pas économiquement viable » |

   [CT-MAT 2019 FR, §1.6, p. 18]
3. **Analyser les risques.** Les risques typiques et leur atténuation sont donnés par le syllabus [CT-MAT 2019 FR, §1.8, p. 20] :

| Risque | Atténuation possible |
|---|---|
| Fragmentation du marché | Tester les appareils les plus utilisés |
| Coût de plusieurs plateformes | Ne pas tester celles qui sortent du périmètre |
| Nouvelles technologies | Utiliser des versions de préproduction |
| Appareils indisponibles | Accès distant aux appareils ou test de foule |
| Modèles d'usage attendus | Tests sur le terrain |

   Les défis du §1.7 s'y ajoutent : réseaux variables, faibles ressources, cycles d'approbation des stores. Les méthodes classiques d'analyse de risque restent valables.
4. **Répartir émulateurs et appareils réels.**
   - Émulateurs et simulateurs tôt : déploiement rapide, réglage du réseau, du GPS, des interruptions.
   - Appareils réels ensuite. Un simulateur iOS compile une version différente de l'appli, et certaines fonctions manquent (multitouch, accéléromètre).
   - [CT-MAT 2019 FR, §1.6 p. 17 ; EN §4.3.1 p. 37 ; FR §4.3.2 p. 46]
5. **Monter le labo.**
   - Sur site : appareils choisis selon la diffusion, l'OS, l'écran, le coût et les capteurs [FR §4.4, p. 46].
   - Distant (cloud) : pour la régression complète, les tests fonctionnels et non fonctionnels [EN §5.4, p. 41].
   - Les deux se combinent. Un labo sur site bien tenu peut valoir un labo distant.
   - Les cloud d'appareils sont facturés à l'exécution [CT-TAS FR, §2.1.2, p. 21].
6. **Automatiser selon le type d'appli.**
   - Le Web mobile se teste avec les outils web habituels. Les apps natives peuvent exiger des outils spécifiques, ou ceux de la plateforme [CT-MAT FR, §5.1, p. 48-49].
   - Critères d'évaluation des outils : conditions réseau, données de test, exécution à grande échelle (local ou cloud), intégration CI, nouvelles fonctions comme FaceID ou les empreintes [FR §5.3, p. 50-51].
   - Pour fiabiliser : localisateurs fiables, attentes explicites, setup/teardown idempotents, matrice appareil/réseau, cloud d'appareils [CT-FT EN, §6.4, p. 46].
7. **Anticiper le déploiement de l'automatisation.**
   - Les appareils réels doivent être allumés, chargés, en réseau et joignables [CTAL-TAE FR, §4.2.1, p. 34].
   - Les mises à jour automatiques d'OS ou d'agents sont un risque courant [CTAL-TAE EN, §4.2.1, p. 32].
8. **Compléter par du manuel.** Le syllabus couvre les tests sur le terrain, l'approbation des stores et les techniques basées sur l'expérience (personae, tours, SBTM) [CT-MAT FR, plan §3.2-3.3]. Je ne les ai pas lus en détail.

## Exemple de mise en œuvre (fictif, interprétation)
Équipe Scrum de 6 personnes, appli de réservation sortie toutes les 2 semaines, avec 4 mois d'analytics :
- Les analytics donnent environ 8 modèles couvrant 80 % des utilisateurs (étapes 1-2).
- Ces appareils sont répartis en 3 iOS et 3 Android sur site, plus un cloud pour les anciennes versions d'OS (étape 5).
- Chaque merge passe les tests sur émulateur/simulateur en CI. La nuit, un sous-ensemble de bout en bout tourne sur 2 appareils réels, et un cloud sert pour la régression avant release (étapes 4 et 6).
- Une séance exploratoire par sprint, plus un test de réseau dégradé avant chaque store (étape 8).

## Adaptation par domaine
| Domaine | Ce qui change | Où lire |
|---|---|---|
| Mobile (ton cas) | Tout ce qui précède | CT-MAT 2019 |
| Santé / réglementé | Aucun syllabus dédié. Traçabilité et conformité à ajouter. | Web pour la norme ; CT-FT §2 pour un cas voisin (conformité financière) |
| Web | Hybride ou web mobile : outils web de bureau, tests basés sur l'agent utilisateur | CT-MAT §5.1 |
| Embarqué | Objets connectés et wearables comptent parmi les appareils | CT-MAT §1.3 |
| API | Le back-end est testé séparément ; la virtualisation de service aide | CT-MAT §5.3 (virtualisation côté serveur) ; CTAL-ATT §4.2 |

## Par quoi je commencerais
1. **Matrice d'appareils tirée des analytics** : impact fort, effort faible.
2. **Émulateurs en CI, puis un petit lot d'appareils réels et un cloud pour la régression** : impact fort, effort moyen.
3. **Cadrer le risque de déploiement de l'automatisation** (batterie, réseau, mises à jour d'OS) : impact moyen, effort faible.

## Où creuser ensuite
- `section CT-MAT-2019-fr 2.1` : tests de compatibilité matériel (capteurs, interruptions, énergie).
- `section CT-MAT-2019-fr 3.2` : tests sur le terrain et approbation des stores.
- `section CTAL-TAE-2.0-fr 4.2` : risques de déploiement de l'automatisation.
- Je n'ai pas lu §5.2 (méthodes d'automatisation) en détail.

**Confiance : 68/100 (moyenne)**
- Base : plusieurs passages lus dans 4 syllabus concordants, avec un syllabus dédié.
- Je retire des points parce que CT-MAT date de 2019. Il ne cite aucun outil actuel (Appium, XCUITest, Espresso, cloud d'appareils) et ne parle pas d'IA.
- Je retire aussi pour l'exemple et la ligne santé, qui sont de l'interprétation.

## Questions de cadrage
- Appli native, hybride ou web mobile ?
- Contrainte réglementaire (santé, finance) ?
- Équipe et rythme de livraison ? Y a-t-il déjà des analytics d'usage ?

## À capitaliser ?
```json
{
 "titre": "Matrice d'appareils mobiles pilotée par les analytics",
 "resume": "Choisir les appareils et OS à tester selon les données d'usage (approche multiplateforme), avec émulateurs tôt, appareils réels ensuite et labo distant en complément.",
 "probleme": "Fragmentation des appareils : impossible de tout couvrir, coût élevé.",
 "principe": "Sélection représentative des appareils couvrant la majorité des clients, priorisée par les analytics. Émulateurs/simulateurs tôt, appareils réels en régression.",
 "theme_principal": "strategie",
 "themes_secondaires": ["automatisation"],
 "domaine_application": "Application mobile iOS/Android, équipe agile",
 "prerequis": "Accès aux analytics d'usage (géographie, OS, modèles)",
 "benefices": "Couverture ciblée à coût maîtrisé",
 "limites": "Syllabus de 2019 ; la liste d'appareils doit être revue régulièrement",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-22 : mise en place des tests d'une application mobile iOS et Android",
 "references": [
  {"type": "istqb", "doc_id": "CT-MAT-2019-fr", "pages": "18", "section": "1.6", "extrait": "Approche multiplateforme"}
 ]
}
```
Je n'ai pas pu lancer `idee doublons`. Relance-le avant `idee ajouter`.

## Questions à choix
1. Que veux-tu approfondir ?
   1. Les tests de compatibilité matériel (CT-MAT §2.1)
   2. L'automatisation et le choix d'outils, avec une recherche Web sur Appium, XCUITest et Espresso
   3. Les tests sur le terrain et l'approbation des stores (§3.2)
2. Veux-tu capitaliser l'idée proposée ?
   1. Oui, après vérification des doublons
   2. Non
3. Quel est ton domaine ?
   1. Santé ou réglementé : je cherche la norme sur le Web, la bibliothèque n'a rien
   2. Grand public
   3. Autre

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher mobile appareils automatisation`
- `python qa.py chercher mobile application testing devices`
- `python qa.py chercher tests applications mobiles appareils`
- `python qa.py section CT-MAT-2019-fr 1.6; python qa.py section CT-MAT-2019-fr 1.8; python qa.py section CT-MAT-2019-fr 1.7 | head -60`
- `python qa.py lire 10805 --contexte 1; python qa.py lire 10191 --contexte 1; python qa.py lire 6914`
- `python qa.py chercher "mobile test automation emulator simulator real device" ; python qa.py chercher émulateur simulateur`
- `python qa.py section CT-MAT-2019-en 5.4 | head -70; python qa.py lire 7352 --contexte 1 | head -50; python qa.py lire 13140 --contexte 1 | head -40`
- `python qa.py plan CT-MAT-2019-fr | head -60`
- `python qa.py section CT-MAT-2019-fr 5.1 | head -60; python qa.py section CT-MAT-2019-fr 5.3 | head -40; python qa.py section CT-MAT-2019-fr 1.1 | head -20`
- `python qa.py idee modele | head -40`
- `python qa.py themes | grep -i -E "mobile|automat|risque|strat" | head; `
- `python qa.py idee doublons <<'JSON'
{"titre":"Matrice d'appareils mobiles pilotée par les données d'usage","resume":"Choisir les appareils/OS à tester à partir des analytics (géographie, OS, modèle), `
