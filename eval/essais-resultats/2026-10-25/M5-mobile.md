# M5-mobile — thomas

**Question** : Comment mettre en place les tests d'une application mobile iOS et Android : choix des appareils, risques, automatisation ?

**Tours** : 8 · **coût** : 0.164 $ · **confiance annoncée** : 72 · **verdict** : réussi · **citations** : 8/8 lues · **Web** : 0 · **critères** : 6/6

## Réponse

Je termine : j'ai lu les passages utiles du syllabus Mobile (CT-MAT) et du syllabus Automatisation (CTAL-TAE). Voici le rapport.

**Sources retenues** : CT-MAT 2019 (FR + EN) §1.6, §1.8, §3.4, §4.3.2, §5.3, §5.4, et CTAL-TAE v2.0 §4.2.1. Base d'idées : rien de capitalisé sur ce sujet. Pas de recherche Web : aucun outil n'est nommé dans ta question.

**Hypothèse de contexte** : app grand public iOS + Android, équipe agile, pas de contrainte réglementaire.

## Méthode pas à pas

1. **Analyser les risques mobiles** — QA Lead avec le produit, au cadrage, livrable : registre de risques. Le syllabus cite la fragmentation du marché, le coût de support multi-plateformes, les nouvelles plateformes, le manque d'appareils et l'usage « en déplacement ». Chaque risque a une parade [CT-MAT 2019 EN, §1.8, p. 18].
2. **Choisir la matrice d'appareils** — QA + product owner, livrable : matrice appareils/OS/réseaux. Il faut connaître la répartition des appareils sur ton marché, sinon on ne peut pas choisir durablement [CT-MAT 2019 FR, §1.6, p. 17]. Trois approches sont décrites : plateforme unique, multiplateforme (sélection représentative d'après le trafic ou les analytics) et couverture maximale. La couverture maximale est « généralement pas économiquement viable » [CT-MAT 2019 FR, §1.6, p. 18]. Pour iOS + Android, c'est l'approche multiplateforme.
3. **Répartir émulateurs/simulateurs et appareils réels** — émulateurs tôt, appareils réels ensuite [CT-MAT 2019 FR, §1.6, p. 17]. Les émulateurs reproduisent facilement réseau dégradé, GPS et interruptions [CT-MAT 2019 FR, §4.3.2, p. 46]. Ils servent aussi en test système quand les appareils manquent [CT-MAT 2019 EN, §3.4.2, p. 35].
4. **Combler le manque d'appareils** — laboratoires distants, crowd testing, réseau de collègues, « bug hunt » [CT-MAT 2019 FR, §1.6, p. 18].
5. **Adapter le processus de test** — ajouter à la planification et à l'analyse les combinaisons d'appareils, les tests terrain, l'approbation des stores et l'installation/mise à jour [CT-MAT 2019 EN, §3.4.1, p. 34]. Lancer les contrôles des stores avant soumission évite un rejet.
6. **Automatiser avec discernement** — évaluer les outils selon l'adéquation organisationnelle et technique : FaceID, empreinte, conditions réseau, exécution à grande échelle, intégration, support [CT-MAT 2019 EN, §5.3, p. 40-41]. Le syllabus note que les apps mobiles « inversent » souvent la pyramide des tests, donc beaucoup de tests manuels [CT-MAT 2019 EN, §3.4.2, p. 35].
7. **Monter le laboratoire d'exécution** — appareils sur site + émulateurs en début de projet. Pour la régression complète, un laboratoire distant complète le parc. Une fois en CI, la stabilité du laboratoire compte plus que son emplacement. Un laboratoire sur site bien tenu peut valoir un laboratoire distant [CT-MAT 2019 EN, §5.4, p. 41].
8. **Anticiper les risques de déploiement de l'automatisation** — les appareils réels doivent être allumés, chargés, en réseau et avoir accès au SUT [CTAL-TAE v2.0 FR, §4.2.1, p. 34].

## Exemple de mise en œuvre (fictif — interprétation)

Équipe Scrum de 6 personnes, livraison toutes les 2 semaines :
- Je retiens 6 à 8 appareils couvrant l'essentiel du trafic, avec les deux dernières versions majeures d'OS (étape 2).
- Les tests unitaires et les smoke tests tournent sur émulateurs à chaque commit (étape 3).
- La régression nocturne passe sur un laboratoire distant (étape 7).
- Chaque release a une session de test exploratoire sur appareil réel et un contrôle des règles des stores (étape 5).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Mobile | Domaine de ta question, traité ci-dessus | CT-MAT 2019 |
| Santé / réglementé | Traçabilité et validation en plus ; pas de syllabus santé dans la bibliothèque, un Web ciblé sur la norme serait nécessaire | non couvert |
| Web | PWA et navigateurs mobiles : compatibilité inter-navigateurs | CT-MAT §2 (non lu) |
| Embarqué/IoT | Appareils compagnons et wearables | CT-MAT §1.3 (non lu) |
| API | Backend partagé iOS/Android, tests de contrat | CTAL-TTA v4.0 §2.7 (non lu) |

## Par quoi je commencerais

1. **Matrice d'appareils fondée sur tes analytics** — impact fort, effort faible.
2. **Registre de risques mobiles** (§1.8) — impact fort, effort faible.
3. **Smoke tests automatisés sur émulateurs en CI, puis laboratoire distant** — impact fort, effort moyen.

## Où creuser ensuite

- `section CT-MAT-2019-en 4.4` : comparaison des laboratoires sur site et distants.
- `section CT-MAT-2019-fr 2` : types de tests (compatibilité, connectivité, utilisabilité).
- `section CT-TAS-1.0-en 2.1.2` : modèles de licence et fermes d'appareils cloud (vu seulement dans un extrait de recherche).
- `section CTAL-TAE-2.0-fr 4.2.1` : suite de la section sur `page CTAL-TAE-2.0-fr 35`.

**Limite** : CT-MAT date de 2019. Je ne l'ai pas recoupé avec le Web, donc les outils actuels (Appium, XCUITest, Espresso, fermes cloud) ne sont pas couverts.

**Confiance : 72/100 (moyenne)** — base 86, 5 passages lus (+20), 2 syllabus concordants (+10), raisonnement sans source pour l'exemple et les domaines (−10).

## Questions à choix

**Quel est ton contexte principal ?**
1. App grand public (B2C)
2. App métier en entreprise (B2B)
3. App réglementée (santé, finance)

**Quelle suite veux-tu ?**
1. Approfondir l'automatisation (outils, pyramide, CI)
2. Détailler la matrice d'appareils
3. Capitaliser les idées ci-dessous

## À capitaliser ?

Pas de doublon trouvé.

```json
{
  "titre": "Choisir la matrice d'appareils mobiles par données d'usage",
  "resume": "Au lieu de viser une couverture maximale, retenir une sélection représentative d'appareils et d'OS d'après les analytics du marché cible. Émulateurs tôt, appareils réels ensuite.",
  "principe": "Approche multiplateforme guidée par les données de répartition des appareils.",
  "theme": "automatisation",
  "references": [
    {
      "document": "CT-MAT-2019-fr",
      "section": "1.6",
      "page": 18,
      "extrait": "Approche multiplateforme : Réduire la portée à une sélection représentative d’appareils et de systèmes d’exploitation utilisés par la majorité des clients sur le marché cible, en fonction du trafic mobile ou d’autres données analytiques."
    }
  ]
}
```

Avant `idee ajouter`, vérifie les champs avec `python qa.py idee modele`. Le thème `automatisation` est mon choix : la matrice d'appareils relève plutôt de la stratégie de test. Rien n'est enregistré sans ton accord.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-K178/.claude/skills/qa-knowle`
- `python qa.py idee chercher mobile appareils automatisation; python qa.py chercher mobile test devices; python qa.py chercher "mobile application testing"; python qa.py chercher "tests mobiles appareil`
- `python qa.py section CT-MAT-2019-fr 1.6 --max-caracteres 5000; python qa.py section CT-MAT-2019-fr 1.8 --max-caracteres 6000; python qa.py section CT-MAT-2019-fr 4.3.2 --max-caracteres 4000`
- `python qa.py section CTAL-TAE-2.0-fr 4.2.1 --max-caracteres 4000; python qa.py chercher "mobile test automation tools cloud device farm" ; python qa.py section CT-MAT-2019-en 3.4 --max-caracteres 4000`
- `python qa.py section CT-MAT-2019-en 5.4 --max-caracteres 4500; python qa.py section CT-MAT-2019-en 1.8 --max-caracteres 5000; python qa.py section CT-MAT-2019-en 5.3 --max-caracteres 3500`
- `python qa.py idee doublons --titre "Choisir la matrice d'appareils mobiles par données d'usage" --resume "Sélection représentative d'appareils/OS selon analytics du marché cible, émulateurs tôt, appar`
- `python qa.py confiance --base 86 --lus 5 --concordants 2 --raisonnement 1 2>&1 | tail -6; python qa.py confiance --help | head -15`
