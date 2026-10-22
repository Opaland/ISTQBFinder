# M4-embarque — thomas

**Question** : Comment organiser les niveaux de test et le test d'intégration matériel/logiciel d'un système embarqué (calculateur industriel) ?

**Tours** : 12 · **coût** : 0.216 $ · **confiance annoncée** : 68 · **citations** : 9/9 lues · **Web** : 0 · **critères** : 4/7 (manquent : methode, etapes_sourcees, exemple)

## Réponse

Pour un calculateur industriel, la bibliothèque ne contient aucun syllabus dédié à l'embarqué ou à l'industriel. Les meilleures sources sont le CT-AuT (automobile, anglais) et le CTEL-TM 2011, transposés. La base d'idées est vide sur ce sujet (`idee chercher` : aucun résultat).

## Sources retenues
- **CTEL-TM 2011 EN, §8.3.3** « Hardware/Software and Embedded Systems » : lu. Source ancienne, anglais seulement.
- **CT-AuT v2.1.1 EN, §2.4.2, §3.2.3, §3.2.4** : lus. Niveaux de test, HiL, MiL et SiL.
- **CTFL v4.0.1 EN, §2.2.1** et **CTAL-TM v3.0 EN, §1.2.5** : lus. Niveaux de test et tâches du Test Manager par niveau.
- **CTAL-TTA v4.0 EN, §4.1** : lu. Tests non fonctionnels à chaque niveau.
- **CTAL-TTA v4.0 FR, §2.8.2** : lu. Sécurité fonctionnelle (IEC 61508).
- Résultat sans intérêt : CT-GT §3.6.5, sur l'intégration matériel des machines de casino. Je ne l'ai pas lu.
- Pas de recherche Web : la question ne nomme aucun outil ni norme précis.

Hypothèse de contexte : calculateur industriel avec cycle en V ou hybride, logiciel embarqué sur une cible matérielle, éventuellement soumis à une norme de sécurité fonctionnelle (IEC 61508). Rien de tout cela n'est confirmé.

## Pistes par syllabus

**CTFL v4.0.1 — §2.2.1 Niveaux de test**
- Cinq niveaux : composant, intégration de composants, système, intégration système, acceptation. Ils se distinguent par l'objet de test, les objectifs, la base de test, les défauts et les responsabilités [CTFL v4.0.1 EN, §2.2.1, p. 29].
- Le CTFL emploie « système » pour le logiciel seul. Pour un calculateur, il faut donc redéfinir ce que couvre chaque niveau. *Interprétation de ma part.*

**CT-AuT v2.1.1 — §2.4.2 Correspondance des niveaux**
- Le tableau relie les niveaux ISTQB à ISO 26262 et ASPICE. Le « système » y désigne un produit matériel + logiciel, alors que le CTFL ne parle que du logiciel [CT-AuT v2.1.1 EN, §2.4.2, p. 30-31].
- Le niveau « System testing » correspond au test du logiciel embarqué sur le matériel cible (ISO 26262 6-11) [CT-AuT v2.1.1 EN, §2.4.2, p. 31, note 19].
- L'intégration matériel/logiciel d'un élément est une phase explicite, suivie de l'intégration des éléments entre eux, puis de l'intégration avec les autres items [CT-AuT v2.1.1 EN, §2.4.2, p. 31, note 18].

**CT-AuT v2.1.1 — §3.2 Environnements XiL**
- MiL, SiL et HiL sont affectés à des niveaux de test. SiL convient au composant et à l'intégration. HiL convient au système, et aussi au composant et à l'intégration [CT-AuT v2.1.1 EN, §3.2.4.3, p. 40 ; §3.2.3.2, p. 37].
- Distinction « component HiL » (un calculateur seul) et « system HiL » (plusieurs calculateurs, échanges de données) [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37].
- HiL tourne en temps réel : pas de pause possible. Il comprend alimentation, unité d'injection de fautes (coupures de câble, courts-circuits), boîte de dérivation et bus résiduel [CT-AuT v2.1.1 EN, §3.2.3.1, p. 37].
- Le Test Manager répartit le périmètre entre environnements. Le but est d'éviter les doublons et de tester dans l'environnement le plus adapté. L'objectif de coût est de déplacer les tests vers des niveaux virtuels plus précoces [CT-AuT v2.1.1 EN, §3.2.4.2-3, p. 40].

**CTEL-TM 2011 — §8.3.3 Matériel/logiciel et embarqué**
- Prévoir plus de temps pour monter les configurations de test. Le matériel prototype tombe en panne et crée des indisponibilités [CTEL-TM 2011 EN, §8.3.3, p. 65].
- Un prototype peut avoir un comportement que le matériel de série n'aura pas. Le logiciel peut aussi accepter un comportement matériel erroné, ce qui masque un défaut qui n'apparaîtra qu'avec du matériel correct [idem].
- Un laboratoire d'intégration sépare l'équipement et le firmware non testés de l'environnement de test logiciel. Ils doivent y « graduer » avant le test système [idem].
- Le Test Manager coordonne les calendriers des composants et réordonne les livraisons de fonctionnalités [idem].

**CTAL-TM v3.0 — §1.2.5**
- Par niveau, le Test Manager détermine les séquences d'intégration avec les développeurs. Il veille aussi à ce que l'avancement reste cohérent avec les stratégies de test système et d'acceptation [CTAL-TM v3.0 EN, §1.2.5, p. 24].

**CTAL-TTA v4.0**
- §4.1 : le test des caractéristiques non fonctionnelles peut se faire à tout niveau. Pour l'embarqué temps réel, on fait des benchmarks de performance et de consommation de ressources dès le composant [CTAL-TTA v4.0 EN, §4.1, p. 28].
- §2.8.2 : en cas de système lié à la sécurité, une norme impose des niveaux de couverture selon les niveaux d'intégrité (SIL de l'IEC 61508) [CTAL-TTA v4.0 FR, §2.8.2, p. 20]. J'ai lu le début de cette section, pas le tableau des SIL.

## Proposition d'organisation (interprétation, étayée par les pistes ci-dessus)

| Niveau | Objet | Environnement probable | Source de la piste |
|---|---|---|---|
| Composant / unité | Modules logiciels, pilotes | PC, simulateur (SiL) | CT-AuT §3.2.4.3 |
| Intégration logicielle | Couches applicatives, RTOS | SiL ou cible | CTFL §2.2.1 |
| **Intégration matériel/logiciel** | Logiciel sur la carte cible, E/S, bus, firmware | Laboratoire d'intégration, bancs prototypes | CTEL-TM §8.3.3 ; CT-AuT note 18 |
| Système | Calculateur complet, exigences système | HiL composant | CT-AuT §3.2.3.2 |
| Intégration système | Calculateur + automates, capteurs, réseaux, autres équipements | HiL système, banc d'essai | CT-AuT §3.2.3.2 |
| Acceptation | Site client, essais d'usine | Matériel de série | CTAL-TM §1.2.5 |

## Ce que j'en retiens
- La décision structurante est de définir ce que « système » veut dire (logiciel seul ou calculateur complet). Les syllabus listent les niveaux mais ne donnent aucune règle générique pour un calculateur industriel.
- Le CT-AuT fournit le meilleur modèle : un niveau est associé à un environnement (SiL, HiL) et à un critère de sortie.
- Le principal risque non fonctionnel est la dérive matériel/firmware. Prototype et matériel de série n'ont pas le même comportement.

## Par quoi je commencerais
1. **Glossaire des niveaux et critères de sortie** (impact fort, effort faible). Définir ce que couvre chaque niveau et ce qu'il faut atteindre pour passer au suivant.
2. **Laboratoire d'intégration avec critère de « graduation »** (impact fort, effort moyen), pour isoler les livraisons matériel/firmware instables.
3. **Affectation des tests aux environnements** (impact moyen, effort moyen), pour réduire les coûts en déplaçant les tests vers le virtuel quand c'est possible.

## Adaptation par domaine
La question porte sur un calculateur industriel : le domaine « embarqué » ci-dessus est développé et les autres sont omis. Pour un calculateur à fonction de sécurité, le CT-AuT (ISO 26262, ASIL) et le CTAL-TTA §2.8.2 (IEC 61508) sont les points d'entrée. Aucun syllabus industriel ou ferroviaire n'est présent dans la bibliothèque.

## Où creuser ensuite
- `section CT-AuT-2.1.1-en 3.2` (XiL en entier) et `4.2.3` (injection de fautes).
- `section CTEL-TM-2011-en 8.3` (autres contextes particuliers).
- `section CTAL-TTA-4.0-fr 2.8` (le tableau des SIL, non lu).
- `section CTAL-TM-3.0-en 1.2` (stratégie par niveau).

**Confiance : 68/100 (moyenne)**
- La confiance documentaire est de 100, avec 5 syllabus qui couvrent les notions.
- Mais je retire 10 points parce que la transposition automobile → industriel et le tableau d'organisation sont mon raisonnement, et 15 points parce que le seul texte sur l'intégration matériel/logiciel est celui de 2011.
- J'ajoute 5 points pour la concordance de plusieurs syllabus courants.
- Je n'ai fait aucune recherche Web sur les normes industrielles (IEC 61508, IEC 61131).

## À capitaliser ?
Une proposition, à valider. La vérification de doublons par `idee doublons` a échoué (blocage du shell sur le JSON). `idee chercher` sur deux formulations ne renvoie rien. Relance `idee doublons` avant d'ajouter.

```json
{"titre":"Laboratoire d'intégration matériel/firmware avec critère de sortie avant le test système","resume":"Isoler matériel et firmware non testés de l'environnement de test logiciel dans un laboratoire d'intégration ; ils doivent y être validés avant le test système.","probleme":"Matériel, firmware et logiciel changent en continu, ce qui répète l'intégration et bloque la progression de l'équipe de test.","principe":"Laboratoire d'intégration séparé, critère de sortie explicite, calendrier des livraisons coordonné par le Test Manager.","theme_principal":"environnements","themes_secondaires":["niveaux-test"],"domaine_application":"Systèmes embarqués, calculateurs industriels","prerequis":"Livraisons matériel/firmware planifiées et versionnées","benefices":"Moins de blocages sur le test système","limites":"Source ancienne (2011), anglais seulement","maturite":"documentee","statut":"a_evaluer","provenance":"Recherche du 2026-10-22 : niveaux de test et intégration matériel/logiciel d'un calculateur industriel","references":[{"type":"istqb","doc_id":"CTEL-TM-2011-en","pages":"65","section":"8.3.3","extrait":"An integration test lab is often used to separate the untested equipment/firmware from the software testing environment"}]}
```

Remarque : `niveaux-test` n'apparaît pas dans les 40 premières lignes de `themes`. Vérifie le code avant d'enregistrer.

## Questions à choix
1. Quel est le contexte du calculateur ?
   1. Fonction de sécurité (SIL ou ASIL)
   2. Sans exigence de sécurité
   3. Je ne sais pas encore
2. Que veux-tu faire ensuite ?
   1. Approfondir le HiL et les environnements XiL (CT-AuT §3.2)
   2. Comparer la stratégie CTAL-TM avec celle du CT-AuT
   3. Capitaliser la proposition ci-dessus
3. La couverture est partielle (aucun syllabus industriel). Veux-tu :
   1. Lancer une recherche Web sur IEC 61508 / IEC 61131 (avec ton accord)
   2. `/ajouter-syllabus <code>` pour un syllabus complémentaire
   3. Rester sur la bibliothèque actuelle

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher "embarqué intégration matériel logiciel" ; python qa.py idee chercher "niveaux de test système embarqué"`
- `python qa.py chercher "hardware software integration testing embedded" ; python qa.py chercher "intégration matériel logiciel embarqué" ; python qa.py chercher "test levels embedded systems" ; python `
- `python qa.py lire 9430 --contexte 1 ; echo ======; python qa.py section CT-AuT-2.1.1 2.4.2 ; echo ======; python qa.py lire 9973 --contexte 1 ; echo =====; python qa.py lire 9981 --contexte 1`
- `python qa.py lire 8889 --contexte 1 ; echo =====; python qa.py lire 11507 --contexte 1; echo =====; python qa.py lire 11078 --contexte 1`
- `python qa.py section CT-AuT-2.1.1-en 2.4.2 | head -60; echo =====; python qa.py lire 12387 --contexte 1 | head -40`
- `python qa.py idee modele`
- `python qa.py themes | head -40; python qa.py idee doublons <<'JSON'
{"titre":"Laboratoire d'intégration matériel/firmware avec critère de sortie avant le test système","resume":"Isoler le matériel et `
- `python qa.py themes | head -40`
- `cat > /tmp/claude-0/-tmp-claude-0--home-user-da9346e2-ce5e-5882-830a-19be129b35c4-scratchpad-wt-90/d621859d-0762-4cbd-a4af-b0f1bfd6d7c7/scratchpad/idee.json <<'EOF'
{"titre":"Laboratoire d'intégration`
- `python qa.py idee chercher "laboratoire intégration firmware" ; python qa.py idee chercher "integration lab hardware firmware"`
