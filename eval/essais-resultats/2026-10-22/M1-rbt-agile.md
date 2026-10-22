# M1-rbt-agile — thomas

**Question** : Comment l'ISTQB propose-t-il d'intégrer le risk-based testing dans une équipe agile ?

**Tours** : 11 · **coût** : 0.181 $ · **confiance annoncée** : 66 · **verdict** : réussi · **citations** : 7/7 lues · **Web** : 0 · **critères** : 11/11

## Réponse

L'ISTQB n'a pas de chapitre « RBT en agile ». Il décrit une analyse des risques qualité faite à deux moments (release et itération), reprise ensuite par les syllabus Advanced. La base d'idées est vide sur le sujet. Le passage le plus détaillé vient d'un syllabus en retrait, CTFL-AT 2014, car CTAL-AT v2.0 (2026) ne traite le RBT que par touches.

**Hypothèse de contexte :** équipe Scrum ou Kanban, produit web, sans contrainte réglementaire forte. Je n'ai pas de contexte projet, voir les questions de cadrage plus bas.

**Sources retenues :**
- CTFL-AT 2014, FR et EN (en retrait, successeur CTAL-AT) : §3.2.1.
- CTAL-AT v2.0 EN (2026) : §3.1.2, §3.4.2, §5.1.4.
- CTAL-TA v4.0 EN et FR : §2.1, §2.2.
- CTAL-TM v3.0 FR : §1.3.6.
- Rien dans la base d'idées. Aucune recherche Web, elle n'était pas nécessaire.

## Méthode pas à pas

1. **Poser les définitions communes.** Le risque est la possibilité d'un événement négatif. Son niveau se mesure par la vraisemblance et l'impact. Les risques produit (qualité) se distinguent des risques projet. Livrable : un vocabulaire partagé. [CTFL-AT 2014 EN, §3.2.1, p. 31]
2. **Faire une première analyse à la planification de release.** Les représentants métier donnent une vue d'ensemble des risques, et toute l'équipe, testeurs compris, aide à les identifier et à les évaluer. Livrable : une liste de risques de haut niveau. [CTFL-AT 2014 EN, §3.2.1, p. 32]
3. **Analyser les risques à chaque planification d'itération.** Le texte donne 6 sous-étapes : [CTFL-AT 2014 EN, §3.2.1, p. 32]
   - réunir l'équipe, testeurs inclus ;
   - lister les éléments du backlog de l'itération ;
   - identifier les risques de chaque élément, en couvrant toutes les caractéristiques qualité ;
   - évaluer chaque risque (catégorie, puis niveau selon impact et probabilité) ;
   - dimensionner l'effort de test proportionnellement au niveau de risque ;
   - choisir les techniques de test qui réduisent chaque risque.

   Livrable : des tâches de test priorisées sur le task board.
4. **Prioriser les tâches selon le risque.** Les tâches à risque élevé démarrent plus tôt et reçoivent plus d'effort de test. Celles à risque faible démarrent plus tard avec moins d'effort. [CTFL-AT 2014 EN, §3.2.1, p. 32]
5. **Réduire les risques avant même l'exécution des tests.** Si l'identification des risques révèle des problèmes dans les user stories, l'équipe peut les relire de près. [CTFL-AT 2014 EN, §3.2.1, p. 32]
6. **Réévaluer en continu.** Pendant le projet, l'équipe ajuste l'analyse : nouveaux risques, niveaux revus, efficacité des mesures de réduction. Le TM v3.0 dit la même chose : l'analyse est « continue et itérative » et ne se fait pas une seule fois au départ. [CTFL-AT 2014 EN, §3.2.1, p. 32 ; CTAL-TM v3.0 FR, §1.3.6, p. 34]
7. **Faire vivre le suivi.** En cycle itératif, le suivi des risques a lieu à la fréquence choisie par l'équipe, vraisemblablement une fois par itération. Le Test Analyst met à jour le registre des risques et ajuste les actions de réduction. [CTAL-TA v4.0 EN, §2.1, p. 25]
8. **Relier les risques aux charters exploratoires.** Les charters peuvent être créés à partir des risques produit, et leur priorité peut venir du niveau de risque. [CTAL-AT v2.0 EN, §5.1.4, p. 40]

Pour l'étape 3, le TA peut estimer le niveau de risque avec ces critères : fréquence d'usage, criticité métier, dommages financiers ou de réputation, qualité de la base de test, contraintes légales. Il peut aussi classer les risques par caractéristique qualité ISO 25010. [CTAL-TA v4.0 EN, §2.1, p. 25]

Le syllabus mentionne aussi les ateliers de risques conjoints (métier, test, dev) pour concentrer l'effort de test. [CTAL-AT v2.0 EN, §3.4.2, p. 29]

## Exemple de mise en œuvre (fictif, interprétation)

Dans une équipe Scrum de 6 personnes qui livre une appli web toutes les 2 semaines :
- Au sprint planning (étape 3), 20 minutes avec dev, PO et testeur : une colonne « risque H/M/B » sur chaque story.
- Les stories à risque H reçoivent des tests en début de sprint et une session exploratoire (étape 8).
- Au daily, on ajoute les nouveaux risques repérés.
- À la rétrospective, on réajuste (étape 6).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Santé / réglementé | Pas de syllabus dispositif médical dans la bibliothèque. Une organisation réglementée tend vers des approches plus lourdes, avec couverture documentée. | [CTAL-AT v2.0 EN, §3.1.2, p. 26] |
| Web | Pas de syllabus web dédié, principes transposés. Exemples de risques : calculs, temps de réponse, utilisabilité. | [CTFL-AT 2014 EN, §3.2.1, p. 32] |
| Embarqué | Non étudié ici. À creuser dans CT-AuT et CTEL-TM. | à lire |
| Mobile | Non étudié ici. À creuser dans CT-MAT §1.8. | à lire |
| API | Non étudié ici. Aucun syllabus API dédié. | à lire |

## Par quoi je commencerais

1. **Impact fort, effort faible :** ajouter un niveau de risque sur chaque story au sprint planning (étape 3).
2. **Impact fort, effort moyen :** brancher les charters exploratoires sur les risques (étape 8).
3. **Impact moyen, effort faible :** réévaluer les risques à chaque rétrospective (étapes 6 et 7).

## Où creuser ensuite

- `section CTFL-AT-2014-en 3.2.1` : le texte complet et ses exemples.
- `section CTAL-TM-3.0-fr 1.3` : techniques RBT, métriques et pièges.
- `section CTAL-TA-4.0-en 2` : le rôle du testeur dans l'analyse des risques.
- `section CTAL-AT-2.0-en 3.1` : la stratégie de test et son équilibre entre quadrants.

**Limite :** CTAL-AT v2.0 ne donne pas de méthode RBT détaillée. Ma méthode repose donc sur un syllabus en retrait, CTFL-AT 2014, et les étapes 7 et 8 viennent de syllabus plus récents. Une recherche ciblée dans CTAL-AT v2.0 n'a pas trouvé de section dédiée. Je n'ai pas lu CTAL-AT v2.0 en entier.

**Confiance : 66/100 (moyenne)**, calcul : base 85 × 0,6 = 51 ; 7 passages lus +20 ; 3 syllabus concordants +20 ; seul un syllabus ancien couvre le cœur de la méthode −15 ; une partie en raisonnement sans source (l'exemple) −10.

## Questions à choix

1. Quel est ton contexte ?
   1. Web, Scrum.
   2. Réglementé (santé, finance).
   3. Mobile ou embarqué.
2. Quelle suite ?
   1. Approfondir les techniques RBT du TM (§1.3) : registre, matrice, métriques.
   2. Comparer l'analyse de risque CTFL-AT 2014 avec CTAL-AT v2.0.
   3. Capitaliser la piste ci-dessous.

## À capitaliser ?

Pas de doublon trouvé (`idee doublons`, thème `rbt`). Le JSON suit le modèle des champs `idee modele` tel que je le comprends. Je n'ai pas relancé `idee modele`, donc les noms de champs sont à vérifier avant `idee ajouter`.

```json
{
  "titre": "Analyse des risques qualité à chaque planification d'itération",
  "resume": "En agile, l'analyse des risques qualité se fait à la planification de release puis à chaque itération, par toute l'équipe. L'effort de test est dimensionné selon le niveau de risque et l'analyse est réajustée en continu.",
  "principe": "Dimensionner l'effort de test selon le niveau de risque, en continu",
  "theme": "rbt",
  "references": [
    {
      "document": "CTFL-AT-2014-en",
      "page": 32,
      "extrait": "Iteration planning : the whole team identifies and assesses the quality risks."
    },
    {
      "document": "CTAL-TM-3.0-fr",
      "page": 34,
      "extrait": "L'analyse des risques est donc une activité continue et itérative"
    }
  ]
}
```

Sources : passages lus dans la bibliothèque locale (CTFL-AT 2014, CTAL-AT v2.0, CTAL-TA v4.0, CTAL-TM v3.0), aucune source Web.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-G/.claude/skills/qa-knowledge`
- `python qa.py idee chercher risk-based testing agile`
- `python qa.py chercher "risk-based testing agile"; python qa.py chercher "analyse des risques agile itération"; python qa.py chercher "product risk agile quality risk analysis"`
- `python qa.py lire 2832 --contexte 1 --max-caracteres 6000; python qa.py lire 2831 --max-caracteres 3000; python qa.py chercher "risk agile" --doc CTAL-AT; python qa.py lire 4576 --max-caracteres 3500;`
- `python qa.py lire 2832 --contexte 1; python qa.py lire 1535 --contexte 1; python qa.py lire 4576; python qa.py lire 1762 --contexte 1; python qa.py lire 1954`
- `python qa.py chercher "product risk" --doc CTAL-AT; python qa.py chercher "risk-based testing" --doc CTAL-AT`
- `python qa.py lire 1524 --contexte 1; python qa.py lire 1566`
- `python qa.py confiance --help | head -30; python qa.py idee doublons --titre "Analyse des risques qualité à chaque planification d'itération" --resume "RBT agile: risques à la planification de release`
- `python qa.py confiance --base 85 --lus 7 --concordants 3 --ancien 1 --raisonnement 1; python qa.py themes | grep -i -E "risk|risq"`
- `python qa.py idee doublons --titre "Analyse des risques qualité à chaque planification d'itération" --resume "RBT agile: risques à la planification de release et d'itération, par toute l'équipe, rééva`
