# S2-automatisation — sylvie

**Question** : On veut automatiser 100 % de nos tests de régression avec Playwright, les lancer à chaque commit et supprimer les tests manuels. Est-ce aligné avec les recommandations ISTQB ? Niveau de maturité ?

**Tours** : 6 · **coût** : 0.226 $ · **confiance annoncée** : 78 · **verdict** : réussi · **citations** : 9/9 lues · **Web** : 0 · **fidélité** (juge LLM, indicatif) : 0.66 sur 6 lignes citées, 0 contradiction(s)

## Réponse

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

Ta démarche est partiellement alignée. Automatiser la régression et l'intégrer à la CI va dans le sens de l'ISTQB. Les mots « 100 % » et « supprimer les tests manuels » sont en revanche un écart net. Aucune des trois pratiques n'est encore en place, donc le niveau atteint est plafonné à 1.

**Pratiques décrites**
- P1 : automatiser 100 % des tests de régression (intention).
- P2 : les lancer à chaque commit (intention).
- P3 : supprimer les tests manuels (intention).
- P4 : utiliser Playwright (intention).

| Pratique | Intention / en place | Verdict | Ce que dit l'ISTQB | Source |
|---|---|---|---|---|
| P1 Automatiser la régression | Intention | Partiellement aligné | La régression est la première cible naturelle de l'automatisation. La décision d'automatiser repose sur le risque et la valeur. Les tests qui ne échouent jamais ou dont le comportement change souvent sont de mauvais candidats. Le « 100 % » contredit ce critère de sélection. | [CT-TAS v1.0 EN, §6.1.1, p. 45] ; [CTAL-AT v2.0 EN, §6.1, p. 49] |
| P2 Exécution à chaque commit | Intention | Partiellement aligné | La régression incrémentale déclenche à chaque commit un sous-ensemble choisi selon le risque, la probabilité, la localisation et les dépendances. Si l'automatisation fait attendre le pipeline, on réduit les tests intégrés aux plus critiques (smoke). La suite complète de régression se lance séparément ou à la demande. | [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CT-TAS v1.0 EN, §6.2.1, p. 48] |
| P3 Supprimer les tests manuels | Intention | Écart | L'automatisation « complète mais ne remplace pas » l'exploratoire et le manuel. Les tests exploratoires et ponctuels restent normalement manuels. Le manuel se concentre sur l'exploratoire et le retour utilisateur. L'ISTQB prévoit un transfert d'effort vers l'exploratoire, pas une suppression. | [CTAL-AT v2.0 EN, §6, p. 49] ; [CTAL-AT v2.0 EN, §6.1, p. 49] ; [CT-TAS v1.0 EN, §3.2.3, p. 26] |
| P4 Playwright | Intention | Hors ISTQB | Les syllabus lus ne prescrivent aucun outil. Le choix est neutre pour l'ISTQB. | Aucune |

Nuances sur P3 :
- Les tests manuels de régression peuvent être remplacés une fois que les tests automatisés les supplantent de façon adéquate, avec une période de double coût pendant la transition [CT-TAS v1.0 EN, §6.1.1, p. 45]. Supprimer le manuel de régression est donc défendable, mais pas tout le manuel.
- La régression exploratoire et la régression collaborative complètent l'automatisation [CTAL-AT v2.0 EN, §1.4, p. 17-18].

**Ce qui manque**
- **Sélection par le risque et la valeur.** Il n'y a ni critère de choix des tests à automatiser ni analyse de risque. [CTAL-AT v2.0 EN, §1.4, p. 17] ; [CTAL-AT v2.0 EN, §6.1, p. 49]
- **Pyramide de tests.** Il faut un équilibre composants / API / E2E soigneusement délimités. Playwright est surtout de l'UI ; viser 100 % en E2E va à l'encontre de cette pyramide. [CTAL-AT v2.0 EN, §6.1, p. 49] ; [CT-TAS v1.0 EN, §3.2.3, p. 26]
- **Découpage de la suite par déclencheur.** Smoke ou sous-ensemble à chaque commit, suite large séparée. [CT-TAS v1.0 EN, §3.2.3, p. 26] ; [CT-TAS v1.0 EN, §6.2.1, p. 48]
- **Suivi de la solution d'automatisation.** Heures de développement, heures de correction et gain par rapport au manuel. Signal d'alerte si la maintenance dépasse le temps du test manuel. [CT-TAS v1.0 EN, §6.2.1, p. 47]
- **Conception pour la maintenabilité.** Éviter le recouvrement fonctionnel (par exemple la séquence de connexion répétée), partager les données de test et gérer les interdépendances entre tests. [CT-TAS v1.0 EN, §6.1.1, p. 45]
- **Environnement isolé et configuration maîtrisée.** L'environnement doit être isolé des changements aléatoires, avec une gestion de configuration des suites. [CT-TAS v1.0 EN, §6.2.1, p. 48]
- **Place de l'exploratoire et traçabilité.** Il faut prévoir l'exploratoire et une traçabilité légère (par exemple des tags vers les user stories) pour repérer les trous de couverture. [CTAL-AT v2.0 EN, §1.4, p. 18]

**Niveau atteint : 1 — Initial · niveau visé : 2 — Discipliné**
- Justification : les trois pratiques sont des intentions. Aucune preuve de mise en place (document, pipeline, indicateur) n'est citée.
- Pour passer au niveau 2 :
  - rédiger une stratégie d'automatisation écrite ;
  - choisir les tests à automatiser selon le risque et la valeur ;
  - planifier la transition ;
  - superviser les résultats (taux d'échec, instabilité, coût de maintenance) ;
  - disposer d'un environnement de test stable.
- Les critères des niveaux 3 à 5 sont une adaptation du dépôt (grille du dépôt).

**Confiance : 78/100 (élevée)**
Calcul : base 80 × 0,6 = 48 ; 8 passages lus +20 ; 3 syllabus courants concordants +20 ; raisonnement sans source −10 → 78.
Les trois syllabus lus vont dans le même sens. Le jugement sur le « 100 % » en E2E avec Playwright relève en partie de mon raisonnement.

**Limites**
- Aucun syllabus de la bibliothèque ne couvre Playwright ni le choix d'un outil précis.
- L'ISO/IEC/IEEE 29119 n'est pas dans la bibliothèque, donc toute conformité ISO est non vérifiable.
- Aucun syllabus lu ne couvre un cadre réglementaire éventuel de ton domaine. Si un test manuel est exigé pour un audit, ce point est non vérifiable.
- Je n'ai pas lu CT-QDO en détail.

**Questions à choix**
1. Quel est ton contexte réglementaire ?
   1. Aucun
   2. Domaine réglementé (santé, finance, transport…)
   3. Je ne sais pas
2. Où en est l'automatisation aujourd'hui ?
   1. Rien d'automatisé
   2. Une partie déjà dans la CI
   3. Surtout de l'E2E UI

**Où creuser ensuite**
- À lire : CT-QDO v1.0 EN §3.3.2 (exploratoire dans le pipeline CI/CD).
- À lire : CTAL-TAE v2.0 EN (conception de la solution d'automatisation).
- À lire : CT-TAS v1.0 EN §3.3.1 (critères d'adéquation des tests à l'automatisation).
- Pour une recherche plus large sur Playwright, demander à Thomas.

**Traçabilité**
- Date de l'avis : 2026-10-30.
- Documents lus :
  - CTAL-AT-2.0-en, v2.0, publié le 2026-04-17 : §1.4 (p. 17-18), §6 et §6.1 (p. 49).
  - CT-TAS-1.0-en, v1.0, publié le 2024-05-03 : §3.2.2 et §3.2.3 (p. 26), §6.1.1 (p. 45), §6.2.1 (p. 47-48).
- Requêtes `chercher` :
  - « test automation regression continuous integration manual testing »
  - « test automation not everything can be automated manual testing exploratory »
- Grille lue : `referentiel/grille-maturite.md`.

Avis indicatif d'alignement sur les syllabus ISTQB locaux ; ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO.

## Commandes exécutées

- `Read {"file_path": "/tmp/claude-0/-home-user/da9346e2-ce5e-5882-830a-19be129b35c4/scratchpad/wt-campagne/referentiel/grille-m`
- `python qa.py chercher "test automation regression continuous integration manual testing" 2>&1 | head -80`
- `python qa.py section CTAL-AT-2.0-en 1.4 --max-caracteres 5000 2>&1; python qa.py section CT-TAS-1.0-en 6.2.1 --max-caracteres 4000 2>&1; python qa.py chercher "test automation not everything can be au`
- `python qa.py page CT-TAS-1.0-en 26 2>&1; python qa.py page CTAL-AT-2.0-en 49 2>&1; python qa.py page CT-TAS-1.0-en 45 2>&1`
- `python qa.py confiance --autorite 0 --base 80 --lus 8 --concordants 3 --ancien 0 --contradiction 0 --web 0 --raisonnement 1 --non-couvert 0 2>&1`
