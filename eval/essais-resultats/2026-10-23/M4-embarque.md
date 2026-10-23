# M4-embarque — thomas

**Question** : Comment organiser les niveaux de test et le test d'intégration matériel/logiciel d'un système embarqué (calculateur industriel) ?

**Tours** : 9 · **coût** : 0.172 $ · **confiance annoncée** : 67 · **verdict** : réussi · **citations** : 6/6 lues · **Web** : 0 · **critères** : 7/7

## Réponse

Je termine la rédaction : les passages sont lus, le contrôle des doublons est fait, et voici le rapport.

## Sources retenues

- **CTEL-TM 2011 EN**, §8.3.3 *Hardware/Software and Embedded Systems*, p. 65. Lu en entier. C'est une source ancienne (Expert Level, 2011).
- **CT-AuT v2.1.1 EN**, §2.4.2 (p. 30-31), §3.2.3.2 (p. 37) et §3.2.4.3 (p. 40). Lus. C'est la source la plus récente et la plus concrète.
- **CTAL-TTA v4.0 EN**, §4.1, p. 28. Lu.
- **Rien dans la base d'idées** pour ce sujet (deux recherches, aucun résultat).
- **Pas de syllabus dédié à l'embarqué industriel.** Le CT-AuT est automobile, donc je le transpose. Aucune recherche Web n'était nécessaire : la question ne nomme ni outil ni norme.

**Hypothèse de contexte :** calculateur industriel (cycle en V, sans doute sûreté fonctionnelle de type IEC 61508, que la bibliothèque ne couvre pas), matériel en partie prototype, équipe de taille moyenne.

## Ce que disent les syllabus

L'ISTQB ne donne pas de recette industrielle. Il fournit trois briques :
- une stratégie d'intégration avec un labo dédié ;
- une correspondance entre les niveaux de test ISTQB et ceux des normes (ISO 26262, ASPICE) ;
- une logique « environnement de test = niveau de test » (MiL, SiL, HiL).

## Méthode pas à pas

1. **Aligner le vocabulaire des niveaux.** Dans les normes, « système » désigne matériel et logiciel ensemble. Dans le CTFL, « système » ne désigne que le logiciel. Fais le mapping dès le départ.
   - Quand et qui : en début de projet, par le Test Manager avec les architectes.
   - Livrable : un tableau de correspondance.
   - Source : [CT-AuT v2.1.1 EN, §2.4.2, p. 30-31].
   - Le tableau fait correspondre composant, intégration de composants, test système, intégration système, système de systèmes et acceptation à leurs équivalents ASPICE et ISO 26262.
   - L'intégration « item » couvre trois phases : matériel + logiciel d'un élément, tous les éléments de l'item, puis l'item avec les autres items [CT-AuT, §2.4.2, p. 31, note 18].
   - Le test système correspond au test des exigences logicielles de sûreté exécutées **sur le matériel cible** [CT-AuT, p. 31, note 19].
2. **Créer un labo d'intégration séparé.** Il isole le matériel et le firmware non éprouvés de l'environnement de test logiciel. Le matériel doit « graduer » du labo avant d'entrer en test système [CTEL-TM 2011 EN, §8.3.3, p. 65].
   - Livrable : des critères de sortie du labo (graduation).
3. **Affecter un environnement à chaque niveau.** [CT-AuT, §3.2.4.3, p. 40]
   - MiL pour valider la conception.
   - SiL pour le composant et l'intégration, une fois le code compilé.
   - HiL pour le test système.
   - Les gains visés : risques produit réduits, coûts réduits en transférant des tests vers des niveaux virtuels, conformité aux normes.
4. **Distinguer le HiL composant du HiL système.** [CT-AuT, §3.2.3.2, p. 37]
   - HiL composant : un seul calculateur, pour tester ses fonctions.
   - HiL système : plusieurs calculateurs, pour l'échange de données et le test système.
   - Le HiL tourne toujours en temps réel et ne peut être ni mis en pause ni arrêté.
   - Choisir le mauvais point d'accès à l'objet testé peut rendre les résultats inutilisables.
5. **Planifier les contraintes du matériel prototype.** [CTEL-TM, §8.3.3, p. 65]
   - Prévoir plus de temps pour installer les configurations de test.
   - Prévoir les pannes d'équipement et une façon d'occuper les ressources pendant l'arrêt.
   - Un défaut observé sur un prototype n'est pas toujours à rapporter : le prototype peut avoir un comportement que la série n'aura pas.
   - Piège inverse : le logiciel peut accepter un comportement matériel erroné et masquer un problème qui n'apparaîtra qu'avec le matériel conforme.
6. **Coordonner les équipes et les livraisons.** C'est le rôle du Test Manager : réunions de planning, points d'avancement fréquents, réordonnancement des livraisons de fonctions. Sans cela, les changements continus matériel/firmware/logiciel provoquent des réintégrations répétées [CTEL-TM, §8.3.3, p. 65]. L'équipe doit aussi avoir une part d'expertise matériel/firmware.
7. **Ajouter les tests non fonctionnels « techniques » à chaque niveau, selon les risques.** [CTAL-TTA v4.0 EN, §4.1, p. 28]
   - Exemples : benchmarks de performance et usage des ressources dès le composant temps réel ou embarqué, récupération (recoverability) en test système.
   - Ces tests exigent souvent du matériel dédié et beaucoup de temps : à planifier dans le calendrier.

## Exemple de mise en œuvre (fictif — interprétation)

Calculateur industriel avec 2 cartes, du firmware et une application, 8 testeurs, cycle en V.
- Chaque nouvelle carte et chaque firmware passent d'abord au labo d'intégration (étape 2). Un test de fumée matériel/firmware définit la graduation.
- L'application est testée en SiL au niveau composant et intégration (étape 3). Elle passe ensuite sur un banc HiL composant, avec entrées/sorties simulées en temps réel (étape 4).
- Le test système a lieu sur un banc HiL ou un banc réel avec le matériel gradué.
- Les mesures de charge CPU et mémoire se font dès le niveau composant sur cible (étape 7).
- Un point hebdomadaire de coordination matériel/firmware/logiciel regroupe les changements (étape 6).

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Embarqué / industriel (ton cas) | Labo d'intégration, prototypes, bancs HiL, temps réel | CTEL-TM §8.3.3 ; CT-AuT §3.2 (non relu au-delà des passages cités) |
| Sûreté / réglementé | Niveaux de test imposés par les normes, techniques selon le niveau d'intégrité | CT-AuT §2.4.2 ; CTAL-TTA §2.8.2 (non lu, à vérifier). **IEC 61508 absente de la bibliothèque** |
| Web, mobile, API | Peu transposable | Non traité (hors sujet) |

## Par quoi je commencerais

| Piste | Impact | Effort |
|---|---|---|
| Tableau de correspondance des niveaux (étape 1) | Fort | Faible |
| Critères de graduation du labo d'intégration (étape 2) | Fort | Moyen |
| Matrice niveau → environnement MiL/SiL/HiL/réel (étapes 3-4) | Fort | Moyen à fort (bancs) |

## Où creuser ensuite
- `section CT-AuT-2.1.1-en 3.2` : MiL, SiL, HiL, et le tableau complet des environnements.
- `section CT-AuT-2.1.1-en 2.2` : méthodes de test par niveau d'intégrité ASIL.
- `section CTAL-TTA-4.0-en 2.8` : couverture et niveaux d'intégrité de sûreté.
- `section CTEL-TM-2011-en 8.3` : autres cas particuliers de gestion de test.

**Confiance : 67/100 (moyenne).** Calcul : base 79 × 0,6 = 47 ; 5 passages lus +20 ; 2 syllabus concordants +10 ; raisonnement sans source −10 (exemple et étape 6 en partie). Le CT-AuT est automobile, pas industriel, et le CTEL-TM date de 2011.

## Questions à choix

**1. Quel est ton contexte réglementaire ?**
1. Sûreté fonctionnelle de type IEC 61508 ou équivalent
2. Pas de norme imposée
3. Autre (à préciser)

**2. Quelle suite veux-tu ?**
1. Approfondir MiL/SiL/HiL (CT-AuT §3.2)
2. Détailler les critères de graduation du labo d'intégration
3. Capitaliser les propositions ci-dessous

## À capitaliser ?

Aucun doublon trouvé pour les deux propositions. Le thème `niveaux-test` n'existe pas : j'ai utilisé `niveaux-types`.

```json
{
  "titre": "Labo d'intégration matériel/logiciel et graduation avant le test système",
  "resume": "Isoler le matériel et le firmware non éprouvés dans un labo d'intégration ; ils doivent y réussir avant d'entrer en test système.",
  "probleme": "Les changements continus de matériel, firmware et logiciel provoquent des réintégrations répétées qui bloquent l'avancement du test.",
  "principe": "Un labo d'intégration sépare l'équipement non testé de l'environnement de test logiciel. Des critères de graduation définissent l'entrée en test système.",
  "theme_principal": "niveaux-types",
  "themes_secondaires": ["domaines-metier"],
  "domaine_application": "Systèmes embarqués et projets combinant matériel et logiciel (cycle en V)",
  "prerequis": "Équipement de labo dédié ; coordination entre équipes matériel, firmware et logiciel",
  "benefices": "Moins de retests dus à du matériel instable ; défauts matériels isolés avant le test système",
  "limites": "Source ancienne (2011) ; coût du labo ; les critères de graduation restent à définir",
  "maturite": "documentee",
  "statut": "a_evaluer",
  "provenance": "Recherche du 2026-10-23 : « organiser les niveaux de test et l'intégration matériel/logiciel d'un calculateur embarqué »",
  "references": [
    {
      "type": "istqb",
      "doc_id": "CTEL-TM-2011-en",
      "pages": "65",
      "section": "8.3.3",
      "extrait": "An integration test lab is often used to separate the untested equipment/firmware from the software testing environment."
    }
  ]
}
```

```json
{
  "titre": "Affecter MiL/SiL/HiL aux niveaux de test pour décaler les tests vers le virtuel",
  "resume": "Associer chaque niveau de test à l'environnement adapté (MiL, SiL, HiL) pour réduire les risques et les coûts.",
  "probleme": "Tester trop tard sur banc matériel coûte cher et trouve les défauts tardivement.",
  "principe": "MiL pour valider la conception, SiL pour composants et intégration, HiL pour le test système. HiL composant (un calculateur) distinct du HiL système (plusieurs).",
  "theme_principal": "niveaux-types",
  "themes_secondaires": ["domaines-metier"],
  "domaine_application": "Systèmes embarqués (syllabus automobile, transposable à l'industriel)",
  "prerequis": "Modèles simulables, banc HiL temps réel",
  "benefices": "Défauts trouvés plus tôt ; coûts de test réduits ; conformité aux tables de méthodes de la norme",
  "limites": "Syllabus automobile : transposition à l'industriel non vérifiée ; coût des bancs HiL",
  "maturite": "documentee",
  "statut": "a_evaluer",
  "provenance": "Recherche du 2026-10-23 : « organiser les niveaux de test et l'intégration matériel/logiciel d'un calculateur embarqué »",
  "references": [
    {
      "type": "istqb",
      "doc_id": "CT-AuT-2.1.1-en",
      "pages": "40",
      "section": "3.2.4.3",
      "extrait": "Transfer of tests to earlier, less costly and virtual test levels"
    }
  ]
}
```

Je n'ai rien enregistré. Si tu es d'accord, la conversation principale lancera `idee ajouter`.

Sources : toutes locales (aucune source Web). Références : [CTEL-TM-2011 EN §8.3.3 p. 65], [CT-AuT v2.1.1 EN §2.4.2 p. 30-31, §3.2.3.2 p. 37, §3.2.4.3 p. 40], [CTAL-TTA v4.0 EN §4.1 p. 28].

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/final2/.claude/skills/qa-knowled`
- `python qa.py idee chercher embarqué intégration matériel logiciel niveaux de test; python qa.py idee chercher hardware software integration embedded`
- `python qa.py chercher niveaux de test système embarqué; python qa.py chercher hardware software integration testing embedded; python qa.py chercher test levels embedded systems; python qa.py chercher `
- `python qa.py section CTEL-TM-2011-en 8.3.3 --max-caracteres 6000; python qa.py section CT-AuT-2.1.1-en 2.4.2 --max-caracteres 7000`
- `python qa.py section CT-AuT-2.1.1-en 3.2.3.2 --max-caracteres 5000; python qa.py section CT-AuT-2.1.1-en 3.2.4.3 --max-caracteres 5000; python qa.py section CTAL-TTA-4.0-en 4.1 --max-caracteres 3500`
- `python qa.py idee modele; python qa.py idee doublons --titre "Intégration matériel/logiciel embarqué : labo d'intégration et passage de relais vers le test système" --resume "Isoler le matériel/firmwa`
- `python qa.py themes | head -40; python qa.py confiance --base 79 --lus 5 --concordants 2 --ancien 0 --raisonnement 1`
- `python qa.py idee doublons --titre "Intégration matériel/logiciel embarqué : labo d'intégration et passage vers le test système" --resume "Isoler le matériel/firmware non éprouvé dans un labo d'intégr`
