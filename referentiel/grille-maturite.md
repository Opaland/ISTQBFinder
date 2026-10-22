# Grille de maturité d'une démarche de test (utilisée par l'agent Sylvie)

**Ce que la grille mesure** : la maturité d'une *démarche décrite par l'utilisateur*
(ex. « mettre en place une stratégie de test basée sur les risques »), pas celle d'une
organisation. **Ce n'est pas une évaluation TMMi officielle** : une évaluation TMMi exige
un évaluateur accrédité et des preuves de terrain.

**Fondement** : les cinq niveaux reprennent ceux du modèle TMMi tels que décrits par
l'ISTQB — Initial, Managed, Defined, Management and measurement, Optimization —
[CTEL-ITP 2011 EN, §3.3.2, p. 26]. Les critères ci-dessous les adaptent à une démarche
unique ; chaque critère doit être rattaché par Sylvie à un passage de syllabus lu.

| Niveau | Nom | La démarche décrite… | Exemple (test basé sur les risques) |
|---|---|---|---|
| 1 | Initial | est une intention ou une pratique ponctuelle, dépendante des personnes, sans étapes définies | « on testera d'abord ce qui est risqué » |
| 2 | Géré | couvre les étapes que le syllabus décrit, au niveau d'un projet, avec des rôles, une planification et un suivi | risques identifiés avec les parties prenantes, évalués (probabilité × impact), traduits en priorité et profondeur de test, suivis pendant le projet |
| 3 | Défini | est standardisée pour l'organisation (stratégie / politique de test, modèles, formation, revues) et adaptée au cycle de vie | méthode RBT commune à toutes les équipes, intégrée à la stratégie de test organisationnelle, testeurs formés |
| 4 | Mesuré | est pilotée par des indicateurs quantitatifs définis à l'avance | métriques de succès du RBT suivies (ex. défauts résiduels par niveau de risque) et utilisées pour décider |
| 5 | Optimisé | s'améliore en continu à partir de ses mesures (analyse causale, prévention, rétrospectives) | le modèle de risques est recalibré à partir des défaillances en production et des rétrospectives |

Règles d'attribution :
- un niveau n'est atteint que si **tous** ses critères le sont (et ceux des niveaux inférieurs) ;
- un critère non mentionné par l'utilisateur est « non démontré », pas « acquis » ;
- donner le niveau atteint, puis ce qui manque pour le niveau suivant.

## Verdicts de conformité (par pratique)

| Verdict | Signification |
|---|---|
| Conforme | la pratique correspond à ce que décrit un syllabus (passage lu et cité) |
| Partiellement conforme | l'esprit y est, mais une étape ou une condition décrite par le syllabus manque |
| Écart | la pratique contredit ce que décrit le syllabus |
| Hors ISTQB | pratique non décrite par les syllabus (ni bonne ni mauvaise pour autant) |
| Non vérifiable | la référence nécessaire n'est pas dans la bibliothèque (ex. ISO/IEC/IEEE 29119) |

L'ISTQB n'est pas une norme : les syllabus décrivent des pratiques reconnues. « Conforme
ISTQB » signifie « alignée sur ces pratiques ». La série ISO/IEC/IEEE 29119 n'est pas
dans la bibliothèque : toute affirmation de conformité ISO est « non vérifiable ».
