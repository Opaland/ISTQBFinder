# M4-embarque — thomas

**Question** : Comment organiser les niveaux de test et le test d'intégration matériel/logiciel d'un système embarqué (calculateur industriel) ?

**Tours** : 10 · **coût** : 0.175 $ · **confiance annoncée** : 68 · **citations** : 5/5 lues · **Web** : 0 · **critères** : 7/7

## Réponse

Pour un calculateur industriel, la bibliothèque couvre bien l'intégration matériel/logiciel. Les sources viennent surtout de l'automobile (CT-AuT) et d'un syllabus Expert de 2011 (CTEL-TM).

**Sources retenues**
- CTEL-TM 2011 EN, §8.3.3.
- CT-AuT v2.1.1 EN, §2.4.2, §3.2.3.2 et §3.2.4.3.
- CTAL-TTA v4.0 EN, §4.1.
- CT-ATLaS BoK v2.0 FR, §3.2.
- Base d'idées : rien de capitalisé sur ce sujet.
- Il n'existe aucun syllabus « industriel » ni IEC 61508 dédié. Un extrait du TTA §2.8.2 (IEC 61508, niveaux d'intégrité) est apparu dans une recherche, mais je ne l'ai pas lu. Je ne le cite pas.
- Je n'ai pas fait de recherche Web : la question ne nomme ni outil ni norme précise.

**Hypothèse de contexte :** calculateur (ECU/PLC) avec firmware et logiciel applicatif, cycle en V ou hybride, sans exigence de sûreté certifiée. La réponse change si une norme s'applique (voir les questions de cadrage).

## Méthode pas à pas

1. **Nommer les niveaux selon un vocabulaire commun.**
   - Le CTFL réserve « système » au logiciel seul, alors que ISO 26262 et ASPICE désignent un produit matériel + logiciel.
   - Fixe donc un glossaire dès le départ. Livrable : tableau de correspondance de tes niveaux.
   - Correspondance proposée par CT-AuT : composant/unité → intégration de composants → test du logiciel embarqué sur cible matérielle → intégration système → système de systèmes → validation. [CT-AuT v2.1.1 EN, §2.4.2, p. 30-31]
2. **Associer un environnement à chaque niveau.**
   - MiL pour valider la conception.
   - SiL pour les tests de composants et d'intégration logicielle.
   - HiL pour les tests système. [CT-AuT v2.1.1 EN, §3.2.4.3, p. 40]
   - Le HiL peut servir aux niveaux composant, intégration et système, avec un HiL « composant » (un calculateur) et un HiL « système » (plusieurs calculateurs, échanges entre eux). [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37]
   - Le HiL tourne en temps réel et ne peut pas être mis en pause. [CT-AuT v2.1.1 EN, §3.2.3.2, p. 37]
   - Livrable : matrice niveau × environnement × types de test.
3. **Remonter les tests vers les niveaux virtuels, moins chers.** C'est l'un des trois critères d'optimisation cités : réduire les risques produit, réduire le coût de test, être conforme aux normes. Garde le non-fonctionnel propre au niveau, par exemple la performance au niveau système sur HiL. [CT-AuT v2.1.1 EN, §3.2.4.3, p. 40]
4. **Prévoir un laboratoire d'intégration séparé.**
   - Il isole le matériel et le firmware non testés de l'environnement de test logiciel.
   - Le matériel et le firmware doivent « graduer » du labo avant d'entrer en test système. [CTEL-TM 2011 EN, §8.3.3, p. 65]
   - Livrable : critères de sortie du labo d'intégration.
5. **Planifier avec les contraintes matérielles.**
   - Prévoir plus de temps pour monter les configurations de test.
   - Prévoir des indisponibilités (prototypes, outils de diagnostic) et un moyen d'employer les ressources pendant les pannes. [CTEL-TM 2011 EN, §8.3.3, p. 65]
   - Le Test Manager coordonne les plannings des composants et peut réordonner les livraisons de fonctionnalités. [CTEL-TM 2011 EN, §8.3.3, p. 65]
6. **Se méfier du matériel prototype.**
   - Il peut avoir un comportement que la série n'aura pas, et dans ce cas un rapport d'anomalie n'est pas forcément approprié.
   - Il peut aussi être fautif alors que le logiciel accepte ce défaut, ce qui masque un problème qui n'apparaîtra qu'avec du matériel correct. [CTEL-TM 2011 EN, §8.3.3, p. 65]
   - Travaille en lien étroit avec les développeurs matériel et firmware, et prévois un peu d'expertise matériel/firmware dans l'équipe de test.
7. **Placer les tests non fonctionnels à chaque niveau, selon les risques.** Par exemple : benchmark de performance et consommation de ressources dès le test de composants temps réel/embarqués, puis fiabilité (recouvrement) en test système. [CTAL-TTA v4.0 EN, §4.1, p. 28]

## Exemple de mise en œuvre (fictif — interprétation)

« Pour un calculateur de régulation, je ferais ceci :
- Étape 2 : tests unitaires et d'intégration logicielle sur SiL en intégration continue.
- Étape 4 : un banc d'intégration où chaque nouvelle carte ou révision de firmware passe un jeu de tests d'entrée.
- Étape 2 : un HiL composant pour le logiciel sur cible, puis un HiL système si plusieurs calculateurs communiquent.
- Étape 5 : un planning commun de livraisons matériel / firmware / logiciel, géré par le Test Manager. »

## Adaptation par domaine

| Domaine | Ce qui change | Où lire |
|---|---|---|
| Embarqué / industriel | Couvert par CT-AuT (HiL/SiL, niveaux) et CTEL-TM §8.3.3. À transposer, car les syllabus parlent de véhicule. | passages lus ci-dessus |
| Santé / réglementé | Pas de syllabus dispositif médical (IEC 62304 absent). Niveaux d'intégrité à creuser dans TTA §2.8.2 (non lu). Web nécessaire pour la norme. | CTAL-TTA v4.0 §2.8.2 |
| Web / API / mobile | Hors sujet ici : pas de matériel dédié à intégrer. | non traité |

## Par quoi je commencerais

1. Glossaire et matrice niveau × environnement (étapes 1-2). Impact fort, effort faible.
2. Critères de « graduation » du labo d'intégration (étape 4). Impact fort, effort moyen.
3. Transfert des tests vers le SiL (étape 3). Impact moyen à fort, effort fort, car il faut construire le modèle d'environnement.

## Où creuser ensuite

- `section CT-AuT-2.1.1-en 3.2` : MiL, SiL, PiL, HiL, ViL.
- `section CT-AuT-2.1.1-en 2.2` : tables de méthodes ISO 26262 par niveau d'intégrité.
- `section CTAL-TTA-4.0-en 2.8.2` : systèmes liés à la sécurité (IEC 61508).
- `section CTEL-TM-2011-en 8.3` : le contexte de l'extrait lu.

**Confiance : 68/100 (moyenne).**
- La confiance documentaire est élevée (87 sur la meilleure requête), et j'ai lu 5 passages de 4 syllabus.
- J'ai retiré des points parce que le cœur vient d'un syllabus Expert de 2011 et d'un syllabus automobile transposé à l'industriel. Cette transposition est mon interprétation.

## Questions de cadrage

1. Une norme s'applique-t-elle ?
   1. IEC 61508 / sûreté fonctionnelle.
   2. Aucune norme.
   3. Autre (précise).
2. Quel est le cycle de développement ?
   1. En V séquentiel.
   2. Agile avec livraisons matérielles tardives.
   3. Hybride.

## Questions à choix

1. Quelle suite veux-tu ?
   1. Approfondir HiL/SiL (CT-AuT §3.2).
   2. Creuser les niveaux d'intégrité IEC 61508 (TTA §2.8.2).
   3. Capitaliser la proposition ci-dessous.

## À capitaliser ?

J'ai vérifié les doublons avec `idee chercher` : rien d'équivalent. Mon contrôle `idee doublons` a été refusé par le shell, donc il reste à relancer. Rien n'est enregistré.

```json
{
 "titre": "Laboratoire d'intégration matériel/firmware avec critère de graduation avant le test système",
 "resume": "Isoler le matériel et le firmware non testés de l'environnement de test logiciel dans un labo d'intégration. Ils n'entrent en test système qu'après avoir gradué.",
 "probleme": "Les changements répétés de matériel, firmware et logiciel provoquent des ré-intégrations qui cassent l'avancement de l'équipe de test.",
 "principe": "Labo d'intégration séparé, critères de sortie explicites, planning de livraison des composants coordonné par le Test Manager.",
 "theme_principal": "environnements",
 "themes_secondaires": ["test-management"],
 "domaine_application": "Systèmes embarqués et combinaisons matériel/logiciel (calculateur industriel)",
 "prerequis": "Équipes matériel, firmware et logiciel qui partagent un planning de livraisons",
 "benefices": "Moins d'arrêts dus aux équipements prototypes ; test système plus stable",
 "limites": "Source ancienne (CTEL-TM 2011) ; coût d'un second banc de test",
 "maturite": "documentee",
 "statut": "a_evaluer",
 "provenance": "Recherche du 2026-10-22 : niveaux de test et intégration matériel/logiciel d'un calculateur industriel",
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

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-90/.claude/skills/qa-knowledg`
- `python qa.py idee chercher "embarqué intégration matériel logiciel niveaux de test"; python qa.py idee chercher "embedded hardware software integration"`
- `python qa.py chercher "test levels embedded systems hardware software integration"; echo ----; python qa.py chercher "niveaux de test système embarqué intégration matériel logiciel"; echo ----; python`
- `python qa.py section CTEL-TM-2011-en 8.3.3; echo ======; python qa.py section CT-AuT-2.1.1-en 2.4.2; echo ======; python qa.py section CT-AuT-2.1.1-en 3.2.4.3; echo =====; python qa.py section CT-AuT-`
- `python qa.py lire 10502 --contexte 1; echo =====; python qa.py lire 8889 --contexte 1`
- `python qa.py idee modele`
- `python qa.py themes | head -60`
- `python qa.py idee doublons <<'JSON'
{"titre":"Laboratoire d'intégration matériel/firmware avec critère de « graduation » avant le test système","resume":"Isoler le matériel et le firmware non testés d`
- `python qa.py idee chercher "laboratoire d'intégration matériel firmware graduate système"; python qa.py idee chercher "HiL SiL niveaux de test calculateur ECU"`
