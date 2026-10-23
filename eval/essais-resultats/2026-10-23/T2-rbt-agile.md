# T2-rbt-agile — thomas

**Question** : Recherche des idées pour intégrer le risk-based testing dans une équipe produit agile.

**Tours** : 8 · **coût** : 0.148 $ · **confiance annoncée** : 81 · **verdict** : réussi · **citations** : 6/6 lues · **Web** : 0

## Réponse

Je n'ai pas de mise en place à te livrer d'après un seul syllabus. Les pistes viennent de quatre documents que j'ai lus : CTAL-AT v2.0, CTFL-AT 2014, CTAL-TM v3.0 et CTAL-TA v4.0. Le CTAL-AT v2.0 est le plus récent et le plus utile pour ton cas. Le CTFL-AT 2014 donne la méthode la plus détaillée, mais il est en retrait.

**Sources retenues**
- Base d'idées : aucune idée capitalisée sur le sujet.
- CTAL-AT v2.0 EN, §3.1 et §3.1.1 : lu.
- CTFL-AT 2014 EN, §3.2.1 : lu. ⚠ Ce syllabus est en retrait, son successeur est le CTAL-AT.
- CTAL-TM v3.0 FR, §1.3.6 : lu.
- CTAL-TA v4.0 EN, §2 et §2.1 : lu.
- Web : non utilisé, aucun outil nommé dans la question.
- Le CTFL v4.0.1 §5.2 (analyse et contrôle des risques) n'est cité qu'en renvoi par le CTAL-TA. Je ne l'ai pas lu.

**Hypothèse de contexte** : équipe Scrum d'environ 6 personnes, produit web, itérations de 2 semaines, sans contrainte réglementaire forte.

**Méthode pas à pas**
1. **Séance de risk-storming à la planification d'itération.** Le testeur l'anime avec le métier et les développeurs. Elle identifie les risques, priorise les activités de test, définit les conditions de test de haut niveau et affine les critères d'acceptation. [CTAL-AT v2.0 EN, §3.1.1, p. 24-25]
2. **Analyser les risques à deux niveaux.**
   - À la planification de release, le métier donne une vue de haut niveau des risques.
   - À la planification d'itération, toute l'équipe identifie et évalue les risques qualité. [CTFL-AT 2014 EN, §3.2.1, p. 32]
3. **Appliquer les 6 étapes du CTFL-AT 2014** sur les items du tableau de tâches de l'itération. Le livrable est un niveau de risque par item.
   - Lister les items de l'itération.
   - Identifier les risques qualité de chaque item, pour toutes les caractéristiques de qualité.
   - Évaluer chaque risque (catégorie, impact × probabilité).
   - Dimensionner l'effort de test selon le niveau de risque.
   - Choisir les techniques de test.
   - [CTFL-AT 2014 EN, §3.2.1, p. 32]
4. **Prioriser les tâches selon le risque.** Les tâches à risque élevé démarrent plus tôt et reçoivent plus de test, celles à risque faible démarrent plus tard avec moins de test. [CTFL-AT 2014 EN, §3.2.1, p. 32]
5. **Relier le risque à la Definition of Done et aux métriques.**
   - La DoD précise comment les résultats de test et la couverture contribuent à l'atteinte de chaque item. [CTAL-AT v2.0 EN, §3.1.1, p. 25]
   - Le syllabus cite la couverture des risques parmi les métriques de reporting. [CTAL-AT v2.0 EN, §3.1, p. 24]
6. **Réévaluer à chaque itération.** Le registre des risques est mis à jour à une fréquence choisie par l'équipe, probablement une fois par itération. [CTAL-TA v4.0 EN, §2, p. 25] Cela inclut les nouveaux risques, les niveaux révisés et l'efficacité des mitigations. [CTFL-AT 2014 EN, §3.2.1, p. 32]
7. **Mesurer en rétrospective.** Questions utiles :
   - Les bonnes parties prenantes ont-elles participé ?
   - Les défauts critiques ont-ils été trouvés tôt ?
   - Les tests ignorés étaient-ils moins risqués que ceux exécutés ?
   - [CTAL-TM v3.0 FR, §1.3.6, p. 34]

**Autres pistes**
- Mitiger avant l'exécution : si le risk-storming révèle des problèmes dans les user stories, relire les stories en profondeur. [CTFL-AT 2014 EN, §3.2.1, p. 32]
- Critères de niveau de risque (CTAL-TA v4.0 EN, §2.1, p. 25) :
  - fréquence d'usage et criticité des fonctions ;
  - dommage financier ou de réputation ;
  - qualité de la base de test ;
  - exigences légales.
- Évaluer le risque par élément testé (composant, interface, fonction), car il n'est pas uniforme sur l'objet. [CTAL-TA v4.0 EN, §2.1, p. 25]
- Appliquer le shift left : choisir l'activité de test la plus précoce qui mitige le risque. [CTAL-TA v4.0 EN, §2.1, p. 25]
- Pièges documentés avec leurs solutions [CTAL-TM v3.0 FR, §1.3.6, p. 34] :
  - niveau de risque difficile à estimer : utiliser des données historiques ;
  - « déjà vu » : les mêmes risques reviennent à chaque projet ;
  - risques importants non identifiés : former et impliquer les bonnes personnes ;
  - parties prenantes qui changent : refaire l'analyse, pas une seule fois au départ.
- Les quadrants de test aident à choisir types et niveaux de test. [CTAL-AT v2.0 EN, §3.1, p. 24]

**Exemple de mise en œuvre** (fictif, interprétation)
- Au raffinement, le PO signale les stories sensibles, par exemple le paiement.
- À la planification, 30 minutes de risk-storming avec le métier, les développeurs et le testeur. Chaque story reçoit un niveau de risque (H/M/L) sur le tableau de tâches (étapes 1 à 3).
- Les stories H démarrent en premier et reçoivent des tests exploratoires et d'API en plus des tests unitaires. Les stories L n'ont que des tests automatisés de base (étape 4).
- La DoD ajoute « risques H couverts » (étape 5).
- En rétrospective, on regarde si les défauts critiques sont apparus tôt et on met le registre à jour (étapes 6 et 7).

**Adaptation par domaine**

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Pas de syllabus dédié (IEC 62304 absent) ; la couverture par niveau d'intégrité est à vérifier. | CTAL-TTA v4.0 §2.8.2, à lire avant de citer |
| Web | Pas de syllabus web dédié ; principes transposés. Risques de performance et de facilité d'utilisation fréquents. | CT-PT §3.2, à lire avant de citer |
| Embarqué | Surtout couvert par l'automobile (ISO 26262), en anglais. | CT-AuT, à lire avant de citer |
| Mobile | Syllabus dédié, version 2019. | CT-MAT §1.8, à lire avant de citer |
| API | Pas de syllabus dédié. | CTAL-TTA v4.0 §2.7, à lire avant de citer |

Je n'ai pas lu les sections des lignes « Où lire » : ce sont des repères, pas des citations.

**Par quoi je commencerais**
1. Risk-storming de 30 minutes à la planification d'itération. Impact fort, effort faible.
2. Niveau de risque visible sur chaque story du tableau de tâches, relié à la DoD. Impact fort, effort faible.
3. Trois questions de rétrospective tirées du CTAL-TM §1.3.6. Impact moyen, effort faible.

**Où creuser ensuite**
- `section CTAL-AT-2.0-en 3.1`
- `section CTAL-TM-3.0-fr 1.3`
- `section CTAL-TA-4.0-en 2.1`
- `section CT-ATLaS-2.0-en 5.1.2` : le passage trouvé évoque les « impediments and risk boards » pour coordonner plusieurs équipes. Je ne l'ai pas lu.

**Confiance : 81/100 (élevée)** : base 85 × 0,6 = 51 ; 4 passages lus +20 ; 3 syllabus concordants +10 ; interprétation sans source (l'exemple fictif) −10 → 81 selon l'outil. Le calcul affiche aussi +20 pour les concordants, ce qui donne bien 81.

**Questions à choix**

Quel est ton contexte ?
1. Web / SaaS
2. Réglementé ou critique
3. Mobile ou embarqué

Quelle suite ?
1. Approfondir les métriques de risque et la rétrospective
2. Comparer le RBT agile du CTAL-AT avec le CTAL-TM
3. Capitaliser la piste ci-dessous

**À capitaliser ?**

Doublons vérifiés : « Aucune idée similaire ». Les extraits JSON des références ne sont pas inclus, car ils doivent être copiés mot pour mot depuis le passage lu. La conversation principale peut générer le modèle avec `python qa.py idee modele`.

```json
{
  "titre": "Risk-storming à la planification d'itération",
  "resume": "Intégrer l'analyse des risques qualité dans la planification d'itération agile",
  "principe": "Risques évalués par l'équipe entière, effort de test proportionnel au niveau de risque, réévalués à chaque itération",
  "theme": "rbt"
}
```

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher risk-based testing agile risque`
- `python qa.py chercher "risk-based testing agile" && python qa.py chercher "product risk analysis iteration planning"`
- `python qa.py lire 1518 --contexte 1 --max-caracteres 6000; python qa.py lire 2832 --contexte 1 --max-caracteres 6000; python qa.py lire 4576 --contexte 1 --max-caracteres 5000; python qa.py lire 1762 `
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Risk-storming à la planification d'itération" --resume "Intégrer l'analyse des risques qualité dans le raffinement et la p`
- `python qa.py confiance --base 85 --lus 4 --concordants 3 --raisonnement 1; python qa.py themes | grep -i -E "risq|risk"`
- `python qa.py idee doublons --titre "Risk-storming à la planification d'itération" --resume "Intégrer l'analyse des risques qualité dans la planification d'itération" --principe "Risques évalués par l'`
