# Échelle de capacité d'une démarche de test, inspirée du TMMi (utilisée par l'agent Sylvie)

> **Avis indicatif** d'alignement sur les syllabus ISTQB locaux ; ni attestation de
> conformité, ni évaluation ISTQB / TMMi / ISO.

**Ce que l'échelle mesure** : la capacité d'une *démarche décrite par l'utilisateur*
(ex. « mettre en place une stratégie de test basée sur les risques »), pas la maturité
d'une organisation. Ce n'est **pas** une évaluation TMMi : une évaluation TMMi exige un
évaluateur accrédité et des preuves de terrain.

## Fondement (passages lus avec la CLI)

- Le TMMi a une architecture **étagée** : l'*organisation* passe par des niveaux de
  maturité, chacun associé à un ensemble de domaines de processus
  [CTEL-ITP 2011 EN, §3.1.2, p. 23 ; §3.3.2, p. 26]. Noter **une démarche isolée**
  relève plutôt d'une représentation **continue**, qui attribue un niveau de capacité à
  un domaine (ex. le domaine clé « Test Strategy » de TPI NEXT)
  [CTEL-ITP 2011 EN, §3.1.2, p. 23]. D'où une échelle *inspirée* du TMMi, qui n'en
  reprend ni la méthode ni la notation.
- L'amélioration fondée sur un modèle peut s'appliquer au niveau d'un projet, en se
  concentrant sur les domaines liés au projet (planification, conception) ou en adaptant
  au projet les pratiques de niveau organisation (politique de test, organisation)
  [CTAL-TM v3.0 EN, §1.5.2, p. 39].
- Libellés des cinq niveaux TMMi : EN « Initial, Managed, Defined, Management and
  measurement, Optimization » [CTEL-ITP 2011 EN, §3.3.2, p. 26] ; FR (traduction CFTL)
  « Initial, Discipliné, Ajusté, Géré quantitativement, En optimisation »
  [CTEL-ITP 2011 FR, §3.3.2, pp. 28-29]. (La même traduction appelle aussi le niveau 2
  « Géré » à la p. 29.)
- Domaines de processus du **niveau 2** : politique et stratégie de test, planification
  de test, supervision et contrôle du test, conception et exécution des tests,
  environnement de test [CTEL-ITP 2011 EN, §3.3.2, p. 26 ; FR p. 29]. La **politique et
  la stratégie de test relèvent donc du niveau 2**, pas du niveau 3.

Les critères des niveaux 3 à 5 ci-dessous sont une **adaptation du dépôt** (les
syllabus lus ne détaillent pas leurs domaines de processus) : Sylvie les présente comme
tels et rattache chaque critère qu'elle applique à un passage de syllabus lu.

## Niveaux

| N | Libellé FR (CFTL) · EN | La démarche… | Exemple (test basé sur les risques) |
|---|---|---|---|
| 1 | Initial · Initial | est une intention ou une pratique ponctuelle, dépendante des personnes, sans étapes définies | « on testera d'abord ce qui est risqué » |
| 2 | Discipliné · Managed | est rattachée à une politique / stratégie de test écrite, planifiée, conçue et exécutée selon les étapes que le syllabus décrit, supervisée et contrôlée pendant le projet, avec l'environnement de test nécessaire | stratégie RBT écrite ; risques identifiés avec les parties prenantes, évalués (probabilité × impact), traduits en priorité et profondeur de test ; suivi des risques et des tests pendant le projet |
| 3 | Ajusté · Defined | *(adaptation du dépôt)* est standardisée pour toute l'organisation (processus commun, modèles, formation, revues) et adaptée à chaque cycle de vie | méthode RBT commune à toutes les équipes, testeurs formés, adaptation agile / séquentiel documentée |
| 4 | Géré quantitativement · Management and measurement | *(adaptation du dépôt)* est pilotée par des indicateurs quantitatifs définis à l'avance et utilisés pour décider | défauts résiduels par niveau de risque suivis et utilisés pour arbitrer |
| 5 | En optimisation · Optimization | *(adaptation du dépôt)* s'améliore en continu à partir de ses mesures (analyse causale, prévention, rétrospectives) | modèle de risques recalibré à partir des défaillances en production |

## Intention ou en place

Chaque pratique est marquée **« intention »** (prévue, « je veux mettre en place… ») ou
**« en place (preuve : …) »** (déjà appliquée, avec l'élément qui le montre : document,
outil, réunion, indicateur cité par l'utilisateur).

Règles d'attribution :
- seules les pratiques **en place** comptent pour le niveau atteint ; une intention bien
  décrite compte pour le **niveau visé** ;
- tant qu'**aucune** pratique n'est en place, le niveau est **plafonné à 1** et la
  réponse donne « Niveau atteint : 1 — Initial · niveau visé : N » ;
- un niveau n'est atteint que si **tous** ses critères le sont (et ceux des niveaux
  inférieurs) ; un critère non mentionné est « non démontré », pas « acquis » ;
- donner le niveau atteint, le niveau visé s'il diffère, puis ce qui manque pour le
  niveau suivant ;
- le titre « Niveau atteint : N » porte **toujours le niveau retenu** : un niveau dont un
  critère n'est pas démontré n'y figure jamais, même qualifié de « provisoire » ou de
  « non démontré » ; il va dans « niveau visé ».

## Verdicts d'alignement (par pratique)

| Verdict | Signification |
|---|---|
| Aligné | la pratique correspond à ce que décrit un syllabus (passage lu et cité) |
| Partiellement aligné | l'esprit y est, mais une étape ou une condition décrite par le syllabus manque |
| Écart | la pratique contredit ce que décrit le syllabus |
| Hors ISTQB | pratique non décrite par les syllabus (ni bonne ni mauvaise pour autant) |
| Non vérifiable | la référence nécessaire n'est pas dans la bibliothèque (ex. ISO/IEC/IEEE 29119) |

L'ISTQB n'est pas une norme : les syllabus décrivent des pratiques reconnues. On parle
d'**alignement**, jamais de conformité. La série ISO/IEC/IEEE 29119 n'est pas dans la
bibliothèque : toute affirmation de conformité ISO est « non vérifiable ».

## Mentions obligatoires de la réponse

- **En tête et en pied** : « Avis indicatif d'alignement sur les syllabus ISTQB locaux ;
  ni attestation de conformité, ni évaluation ISTQB/TMMi/ISO. »
- **Bloc de traçabilité final** : date de l'avis ; pour chaque document lu, `doc_id`,
  version et date de publication ; sections et pages lues ; requêtes `chercher` lancées.
