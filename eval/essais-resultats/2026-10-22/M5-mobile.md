# M5-mobile — thomas

**Question** : Comment mettre en place les tests d'une application mobile iOS et Android : choix des appareils, risques, automatisation ?

**Tours** : 9 · **coût** : 0.197 $ · **confiance annoncée** : 72 · **verdict** : réussi · **citations** : 10/10 lues · **Web** : 0 · **critères** : 6/6

## Réponse

Pour tester une appli iOS et Android, le syllabus ISTQB le plus utile est **CT-MAT 2019 (Mobile Application Testing)**, en FR et en EN. Il traite la stratégie (§1.6), les risques (§1.7-1.8), les émulateurs et laboratoires (§4.3-4.4) et l'automatisation (§5.2, §5.4). CTAL-TAE v2.0 et CT-TAS v1.0 apportent les risques de déploiement de l'automatisation. La base d'idées ne contient rien sur ce sujet.

Aucun outil n'est nommé dans ta question, donc je n'ai pas fait de recherche Web.

**Sources retenues**
- CT-MAT 2019 FR : §1.6, §4.3, §4.4, §5.2, §5.4, lus en entier.
- CTAL-TAE v2.0 FR : §4.2.1, lu.
- CT-TAS v1.0 et CT-FT v1.0 : repérés par la recherche, non lus, donc non cités.
- Base d'idées : aucun résultat.
- Web : non utilisé.

**Hypothèse de contexte** : appli grand public (e-commerce ou service) livrée en continu, équipe de 5 à 10 personnes, pas de contrainte réglementaire forte.

## Méthode pas à pas

1. **Collecter les données d'usage.** Qui : QA Lead avec le produit. Quand : avant toute décision. Livrable : répartition des appareils et des versions d'OS par marché cible. L'ISTQB range comme risque typique le fait de ne pas connaître cette répartition. Dans ce cas, on ne peut pas choisir durablement les appareils à tester. [CT-MAT 2019 FR, §1.6, p. 17]
2. **Analyser les risques propres au mobile.** Livrable : registre de risques. Le syllabus cite la fragmentation du marché, le coût multiplateforme, les nouvelles technologies, l'indisponibilité d'appareils et les usages réels (réseau, déplacement). Chacun a une atténuation proposée. [CT-MAT 2019 FR, §1.8, p. 20]
3. **Choisir l'approche de couverture des appareils.** Livrable : matrice d'appareils validée. Le syllabus distingue trois approches : plateforme unique, multiplateforme (une sélection représentative selon les analytics) et couverture maximale. Cette dernière est « généralement pas économiquement viable ». [CT-MAT 2019 FR, §1.6, p. 18] Les critères de sélection cités sont :
   - le rang de diffusion ;
   - l'OS et sa version ;
   - la taille et la densité d'écran ;
   - la disponibilité et le coût ;
   - les caractéristiques spéciales ;
   - l'importance pour le public cible. [CT-MAT 2019 FR, §4.4, p. 46]
4. **Répartir émulateurs/simulateurs et appareils réels par phase.** Émulateurs et simulateurs en début de développement, appareils réels ensuite. [CT-MAT 2019 FR, §1.6, p. 17] Les émulateurs permettent de régler réseau, GPS et orientation. Ils ne remplacent pas un appareil, par exemple pour le multitouch ou l'accéléromètre. [CT-MAT 2019 FR, §4.3.1-4.3.2, p. 45-46] Pour iOS, c'est un simulateur et non un émulateur. Il est compilé dans une version dédiée, donc plus limité. [CT-MAT 2019 FR, §4.3.1, p. 45]
5. **Combler les manques d'appareils.** Utilise un laboratoire distant, du crowd testing, ton réseau personnel ou une chasse aux défauts. [CT-MAT 2019 FR, §1.6, p. 18] Le laboratoire sur site est meilleur pour les capteurs, la batterie et la sécurité. Le laboratoire distant est rentable en usage ponctuel mais plus cher sur la durée. NFC, Bluetooth et batterie y sont difficiles à tester. [CT-MAT 2019 FR, §4.4, p. 46-47]
6. **Automatiser en choisissant la méthode d'identification d'objets.** L'identification d'objets est plus rapide et résiste aux changements de mise en page. La comparaison image/OCR échoue dès que la mise en page change. Un objet caché peut aussi donner des faux négatifs. [CT-MAT 2019 FR, §5.2, p. 49-50]
7. **Monter le laboratoire d'automatisation.** Appareils locaux plus émulateurs au début, laboratoire distant pour la régression complète, fonctionnelle et non fonctionnelle. En CI, la stabilité du laboratoire est essentielle. [CT-MAT 2019 FR, §5.4, p. 51-52] Les appareils réels doivent être allumés, chargés, connectés au réseau et avoir accès au SUT. [CTAL-TAE 2.0 FR, §4.2.1, p. 34]

## Exemple de mise en œuvre (fictif, interprétation)

Une équipe de 6 personnes livre une appli de réservation toutes les 2 semaines.
- Elle extrait les analytics (étape 1) et retient environ 8 appareils : 4 Android de marques et tailles d'écran variées, 4 iPhone dont l'OS le plus ancien encore supporté (étape 3).
- Les développeurs testent sur émulateur/simulateur, la QA sur les 8 appareils réels (étape 4).
- Le smoke test est automatisé par identification d'objets et tourne en CI sur un petit parc local (étapes 6-7).
- Avant chaque release, un cloud d'appareils lance la régression sur les modèles manquants (étape 5).
- Le réseau dégradé et le GPS sont testés par émulation, puis sur le terrain avant la sortie (étape 2).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Mobile (ton cas) | Tout ce qui précède | CT-MAT 2019 §1.6, §4.4, §5 |
| Santé / réglementé | Le laboratoire distant impose une évaluation de la sécurité du fournisseur. La bibliothèque n'a pas de syllabus dispositif médical. | CT-MAT §4.4 ; Web pour la norme |
| Web / API | Le syllabus mobile ne couvre pas ces domaines | CT-PT §3.2 (risques de performance mobile, non lu) |
| Embarqué | Capteurs et batterie : privilégier le laboratoire sur site | CT-MAT §4.4 |

## Par quoi je commencerais

1. **Matrice d'appareils fondée sur les analytics** : impact fort, effort faible.
2. **Émulateurs en amont, appareils réels ensuite** : impact fort, effort faible.
3. **Smoke test automatisé en CI sur parc réduit, puis cloud** : impact moyen à fort, effort moyen.

## Où creuser ensuite

- `section CT-MAT-2019-fr 3.1` : types de tests mobiles.
- `section CT-MAT-2019-fr 4.4` : comparaison complète des laboratoires.
- `section CTAL-TAE-2.0-fr 4.2` : risques de déploiement de l'automatisation.
- CT-TAS §2.1.2 : licences et clouds d'appareils (repéré, non lu).

**Confiance : 72/100 (moyenne)** : base 86 × 0,6 = 52 ; 5 passages lus +20 ; 2 syllabus concordants +10 ; raisonnement sans source −10 (l'exemple fictif). CT-MAT date de 2019, donc rien sur les pratiques récentes des clouds d'appareils.

## Questions à choix

1. **Plateforme de l'appli ?** (1) native iOS + Android (2) multiplateforme (Flutter, React Native) (3) hybride/web
2. **Suite ?** (1) approfondir l'automatisation (CTAL-TAE) (2) détailler les types de tests mobiles (§3.1) (3) comparer avec CT-TAS sur clouds d'appareils

## À capitaliser ?

Je n'ai pas fait la vérification de doublons : la commande a été refusée par le sandbox. Je ne te donne donc pas de JSON non vérifié. Pour capitaliser, l'idée serait « Matrice d'appareils mobiles fondée sur les analytics, avec émulateurs en amont ». Elle s'appuierait sur CT-MAT 2019 FR §1.6 p. 18 et §4.4 p. 46. Je peux en produire le JSON si tu le souhaites.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-127/.claude/skills/qa-knowled`
- `python qa.py idee chercher mobile appareils automatisation; python qa.py chercher "mobile testing devices" | head -60; python qa.py chercher "tests mobiles appareils" | head -60`
- `python qa.py section CT-MAT-2019-fr 1.6; python qa.py lire 10808 --contexte 1; python qa.py chercher "mobile app automation emulators cloud device farm" | head -30`
- `python qa.py section CT-MAT-2019-fr 5.4; python qa.py section CT-MAT-2019-fr 4.3`
- `python qa.py section CT-MAT-2019-fr 5.2 --max-caracteres 5000; python qa.py section CT-MAT-2019-fr 4.4 --max-caracteres 5000; python qa.py idee modele | head -40`
- `python qa.py confiance --base 86 --lus 5 --syllabus 3 2>&1 | tail -5; python qa.py confiance --help | head -20`
- `python qa.py confiance --base 86 --lus 5 --concordants 2 --raisonnement 1; python qa.py idee doublons <<'JSON'
{"titre":"Choisir la stratégie d'appareils mobiles selon les données d'usage","resume":"R`
- `python qa.py confiance --base 86 --lus 5 --concordants 2 --raisonnement 1; python qa.py themes | head -40`
