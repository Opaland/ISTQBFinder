# M5-mobile — thomas

**Question** : Comment mettre en place les tests d'une application mobile iOS et Android : choix des appareils, risques, automatisation ?

**Tours** : 14 · **coût** : 0.362 $ · **confiance annoncée** : 58 · **verdict** : réussi · **citations** : 11/11 lues · **Web** : 0 · **critères** : 7/7 · **fidélité** (juge LLM, indicatif) : 0.83 sur 10 lignes citées, 0 contradiction(s)

## Réponse

**Sources retenues** : CT-MAT v2019 (FR et EN) §1.6, §1.8, §3.1, §4.3, §4.4 et §5.1, lus. CTAL-TAE v2.0 EN §4.2.1, lu. La base d'idées n'a rien donné (« Aucune idée capitalisée »). J'ai écarté CT-FT §6.4, qui n'est qu'un extrait vu dans `chercher` (« à lire : CT-FT v1.0 EN §6.4 »). Pas de recherche Web : la question ne nomme aucun outil.

Les syllabus ISTQB traitent cette question dans le syllabus dédié CT-MAT, de 2019. Les OS, les outils et les stores ont changé depuis, donc les principes tiennent mais pas les exemples d'outils.

**Hypothèse de contexte** : appli native (ou hybride) iOS + Android, équipe agile avec CI, aucune contrainte réglementaire.

## Méthode pas à pas

1. **Cadrer le contexte produit** : modèle économique (freemium, transactionnel, entreprise), marché cible, canaux de distribution. Qui : QA Lead + produit. Livrable : note de contexte. Le syllabus pose le risque suivant : sans les données de répartition des appareils d'une zone géographique, on ne peut pas choisir durablement les appareils de test [CT-MAT 2019 FR, §1.6, p. 17].
2. **Analyser les risques propres au mobile** : fragmentation du marché, coût du multi-plateforme, nouveaux OS ou appareils, indisponibilité d'appareils, usage en mobilité. Chaque risque a sa parade dans le tableau du syllabus [CT-MAT 2019 EN, §1.8, p. 18]. Livrable : registre de risques.
3. **Choisir une approche de couverture des appareils** [CT-MAT 2019 FR, §1.6, p. 18].
   - Plateforme unique : un seul appareil, OS, opérateur et réseau.
   - Multiplateforme : une sélection représentative de ce que les clients du marché cible utilisent, d'après les analytics.
   - Couverture maximale : jugée « généralement pas économiquement viable ».
   - Les critères de sélection cités sont le rang de diffusion, l'OS et ses versions, la taille et la densité d'écran, la disponibilité, le coût, les caractéristiques spéciales et l'importance pour le public ciblé [CT-MAT 2019 FR, §4.4, p. 46]. Livrable : matrice appareils × OS, revue chaque trimestre à partir des analytics (interprétation pour le rythme).
4. **Répartir émulateurs/simulateurs et appareils réels** :
   - Les émulateurs et simulateurs servent surtout tôt. Ils permettent de régler réseau, orientation, interruptions et GPS, ce qui est coûteux avec des appareils réels. Un simulateur modélise l'environnement d'exécution, un émulateur le matériel [CT-MAT 2019 FR, §4.3.1, p. 45 ; §4.3.2, p. 46].
   - Ils ne remplacent pas un appareil réel : le multitouch ou l'accéléromètre peuvent ne pas être pris en charge [CT-MAT 2019 FR, §4.3.1, p. 45].
   - La stratégie du syllabus : émulateurs/simulateurs tôt, appareils réels ensuite [CT-MAT 2019 FR, §1.6, p. 17].
5. **Constituer le laboratoire (sur site, distant, ou les deux)** [CT-MAT 2019 FR, §4.4, p. 46-47].
   - Le labo sur site offre proximité, tests de capteurs et batterie, et sécurité accrue. Son budget d'achat et d'entretien est important.
   - Le labo distant est rentable en usage sporadique et plus cher en usage long sur un large parc. Il peut offrir bras robotiques, VPN, opérateurs cellulaires et services d'automatisation. Évaluer chaque fournisseur, surtout sur la sécurité.
   - NFC, Bluetooth et batterie sont souvent difficiles à tester dans le cloud.
   - Autres sources d'appareils : crowd testing, réseau personnel, chasse aux défauts [CT-MAT 2019 FR, §1.6, p. 18].
6. **Choisir les types de tests mobiles** : installation, mise à jour et désinstallation, permissions refusées, interruptions, conservation des données [CT-MAT 2019 EN, §3.1.1, p. 28]. Ajouter le stress sur l'appareil (CPU, mémoire, disque, batterie, réseau faible) [CT-MAT 2019 EN, §3.1.2, p. 28-29]. Sécurité, performance, utilisabilité, localisation et accessibilité : à lire en §3.1.3 à 3.1.8.
7. **Automatiser selon le type d'appli** :
   - Les tests sur l'appareil valent pour tous les types d'applications. Le test par agent utilisateur ne vaut que pour le web mobile [CT-MAT 2019 FR, §5.1, p. 48].
   - Les approches classiques (capture/playback, pilotées par les données ou les mots-clés, BDD) s'appliquent au mobile [CT-MAT 2019 FR, §5.1, p. 49].
   - Un framework doit offrir identification et opérations sur les objets, rapports, API extensibles, documentation et intégrations [CT-MAT 2019 FR, §5.1, p. 49].
   - Prévoir un pilote : avec des appareils réels, ils doivent être allumés, chargés, en réseau et joignables. Les mises à jour automatiques d'agents ou d'appareils sont un risque courant, à contenir par des alimentations adaptées, un réseau fiable et un plan de configuration [CTAL-TAE v2.0 EN, §4.2.1, p. 31-32].
   - Exécution à l'échelle ou en CI : un labo distant aide, et la stabilité du labo conditionne la fiabilité des tests. Des appareils sur site bien entretenus peuvent valoir un labo distant [CT-MAT 2019 FR, §5.4, p. 51-52].

## Exemple de mise en œuvre (fictif, interprétation)

Équipe Scrum de 6 personnes, appli de banque en ligne, sprints de 2 semaines :
- Étapes 1-3 : les analytics du marché cible donnent environ 6 appareils iOS/Android couvrant la majorité des utilisateurs, plus 1 appareil d'entrée de gamme.
- Étape 4 : émulateurs et simulateurs dans la CI à chaque commit.
- Étape 5 : 4 appareils réels sur site, plus un labo distant avant chaque release.
- Étape 7 : smoke tests automatisés à chaque build, régression sur le parc avant release, test exploratoire manuel sur NFC et batterie.

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Mobile | Couvert directement par CT-MAT (version 2019) | CT-MAT §1.6, §4, §5 |
| Santé / réglementé | **Pas de syllabus santé** : normes à chercher sur le Web | CTAL-TTA v4.0 §2.8.2 (à lire) |
| Web | Le web mobile se teste avec les outils web habituels [CT-MAT 2019 FR, §5.1, p. 48] | CT-MAT §5.1 |
| Embarqué | Appareils compagnons (wearables, IoT) cités en §1.3 | CT-MAT §1.3 (à lire) |
| API | Le backend relève d'autres syllabus (perf : CT-PT) | CTAL-TTA v4.0 §2.7 (à lire) |

## Par quoi je commencerais

1. **Impact fort, effort faible** : extraire les analytics et fixer la matrice d'appareils (étapes 1-3).
2. **Impact fort, effort moyen** : smoke tests automatisés sur émulateurs/simulateurs, puis sur appareils réels ou labo distant.
3. **Impact moyen, effort fort** : labo sur site, ou contrat de labo distant après évaluation sécurité.

## Où creuser ensuite

- `section CT-MAT-2019-fr 1.7` (défis) et `section CT-MAT-2019-en 3.1.3` à `3.1.8`.
- `section CT-MAT-2019-fr 4` (outils, labo) et `section CT-MAT-2019-fr 5` (automatisation).
- `section CTAL-TAE-2.0-en 4.2` (pilote et déploiement).
- À lire : CT-FT v1.0 EN §6.4 (matrice appareil/réseau, clouds d'appareils).

**Confiance : 58/100** (moyenne). Calcul : base 63 × 0,6 = 38 ; 5 passages lus +20 ; 2 syllabus concordants +10 ; raisonnement sans source −10 (exemple et rythme de revue) → 58. Le syllabus date de 2019.

## Questions à choix

**Quel est ton domaine ou ton contexte principal ?**
1. Appli grand public (e-commerce, média)
2. Appli financière ou santé (réglementée)
3. Appli d'entreprise interne

**Quelle suite veux-tu ?**
1. Approfondir l'automatisation (CT-MAT §5 + CTAL-TAE)
2. Détailler les types de tests mobiles (§3.1)
3. Capitaliser l'idée ci-dessous

## À capitaliser ?

Aucun doublon trouvé. Le thème `mobile` n'existe pas, j'ai donc pris `niveaux-types` (à confirmer).

```json
{
 "titre": "Choisir les appareils de test mobile selon les données d'usage",
 "resume": "Parc représentatif iOS/Android issu des analytics du marché cible, complété par émulateurs/simulateurs et labo distant.",
 "probleme": "Fragmentation des appareils et OS : impossible de tout tester, coût élevé.",
 "principe": "Approche multiplateforme : sélectionner les appareils et OS les plus utilisés (analytics), émulateurs/simulateurs tôt, appareils réels ensuite, labo distant en complément.",
 "theme_principal": "niveaux-types",
 "themes_secondaires": ["automatisation"],
 "domaine_application": "Application mobile native ou hybride, iOS et Android",
 "prerequis": "Accès aux données d'usage du marché cible",
 "benefices": "Couverture ciblée à coût maîtrisé",
 "limites": "Syllabus de 2019 ; NFC, Bluetooth et batterie difficiles à tester dans le cloud",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-30 : « mise en place des tests mobiles iOS/Android »",
 "references": [
  {
   "type": "istqb",
   "doc_id": "CT-MAT-2019-fr",
   "pages": "18",
   "section": "1.6",
   "extrait": "Approche multiplateforme : Réduire la portée à une sélection représentative d’appareils"
  }
 ]
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/.claude/skills/qa-kn`
- `python qa.py idee chercher mobile iOS Android appareils automatisation`
- `python qa.py chercher mobile app testing devices`
- `python qa.py chercher tests applications mobiles choix des appareils`
- `python qa.py section CT-MAT-2019-fr 1.6 --max-caracteres 7000; python qa.py section CT-MAT-2019-fr 5.4 --max-caracteres 7000`
- `python qa.py section CT-MAT-2019-en 1.8 --max-caracteres 6000; python qa.py section CT-MAT-2019-fr 5.1 --max-caracteres 6000`
- `python qa.py section CTAL-TAE-2.0-en 4.2.1 --max-caracteres 6000`
- `python qa.py section CT-MAT-2019-fr 4.3 --max-caracteres 5000; python qa.py section CT-MAT-2019-fr 4.4 --max-caracteres 5000`
- `python qa.py section CT-MAT-2019-en 1.2 --max-caracteres 3500; python qa.py section CT-MAT-2019-en 3.1 --max-caracteres 3500`
- `python qa.py confiance --base 63 --lus 5 2>&1 | tail -8; python qa.py idee doublons --titre "Choisir les appareils de test mobile selon les données d'usage" --resume "Sélection d'un parc représentatif`
- `python qa.py themes | head -40; python qa.py confiance --base 63 --lus 5 --concordance 2 2>&1 | tail -6`
- `python qa.py confiance --base 63 --lus 5 --syllabus 2 2>&1 | head -12; python qa.py idee doublons --titre "Choisir les appareils de test mobile selon les données d'usage" --resume "Parc représentatif `
- `python qa.py confiance --base 63 --lus 5 --concordants 2 --raisonnement 1 2>&1 | head -12`
