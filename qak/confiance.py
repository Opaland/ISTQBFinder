"""Score de confiance d'une RÉPONSE, calculé de façon déterministe (issue #18).

L'agent fournit des faits vérifiables (couverture lexicale de la requête principale,
passages réellement lus, syllabus concordants…) ; la grille ci-dessous, et elle seule,
donne le score. Deux agents qui ont fait la même recherche obtiennent le même nombre.
La couverture lexicale de `chercher` ne mesure que la présence des notions : elle ne
compte que pour 60 % ; le reste se gagne en lisant les passages.
La grille est recopiée dans .claude/skills/qa-knowledge/SKILL.md (test de cohérence)."""
from .recherche import libelle

PART_BASE = 0.6
BONUS_LUS = {0: 0, 1: 10}           # 2 passages lus ou plus : 20
BONUS_LUS_MAX = 20
BONUS_CONCORDANTS = {0: 0, 1: 0, 2: 10}  # 3 syllabus concordants ou plus : 20
BONUS_CONCORDANTS_MAX = 20
MALUS = {
    "ancien": (15, "seul un syllabus ancien (avant 2017) ou une version remplacée couvre le sujet"),
    "contradiction": (15, "syllabus contradictoires non arbitrés"),
    "web": (10, "une partie de la réponse repose sur le Web"),
    "raisonnement": (10, "une partie repose sur un raisonnement sans source"),
}
PLAFOND_NON_COUVERT = 60  # une notion de la question n'est couverte ni par un passage lu ni par le Web
# #226 : la section qui fait autorité sur LA notion de la question (syllabus dédié, titre
# qui la nomme), lue en entier, vaut une lecture complète et une concordance suffisante :
# une question de cours n'a pas besoin de trois syllabus. Les questions larges ne sont pas
# concernées (rien ne change sans --autorite 1).


def calculer(base: int, lus: int, concordants: int, ancien: bool = False, contradiction: bool = False,
             web: bool = False, raisonnement: bool = False, non_couvert: bool = False,
             autorite: bool = False) -> dict:
    """Renvoie {score, libelle, calcul:[lignes]}. Lève ValueError sur une entrée incohérente."""
    if not 0 <= base <= 100:
        raise ValueError(f"--base : couverture lexicale entre 0 et 100 attendue (reçu : {base}).")
    if lus < 0 or concordants < 0:
        raise ValueError("--lus et --concordants : nombres positifs ou nuls attendus.")
    if concordants > lus:
        raise ValueError(f"--concordants ({concordants}) ne peut dépasser --lus ({lus}) : un syllabus ne compte "
                         "comme concordant que si un de ses passages a été lu.")
    if autorite and not concordants:
        raise ValueError("--autorite 1 exige d'avoir lu la section qui fait autorité (--lus et --concordants ≥ 1).")
    calcul = []
    score = round(PART_BASE * base)
    calcul.append((f"base : couverture lexicale {base} × {PART_BASE}", score))
    b = BONUS_LUS.get(lus, BONUS_LUS_MAX)
    c = BONUS_CONCORDANTS.get(concordants, BONUS_CONCORDANTS_MAX)
    if autorite:
        b, c = BONUS_LUS_MAX, BONUS_CONCORDANTS_MAX
    autorite_txt = " ; section de référence lue" if autorite else ""
    calcul.append((f"passages lus (lire/section/page) : {lus}{autorite_txt}", b))
    calcul.append((f"syllabus courants concordants, passages lus : {concordants}{autorite_txt}", c))
    score += b + c
    actifs = {"ancien": ancien, "contradiction": contradiction, "web": web, "raisonnement": raisonnement}
    for cle, (malus, texte) in MALUS.items():
        if actifs[cle]:
            calcul.append((texte, -malus))
            score -= malus
    score = max(0, min(100, score))
    lignes = [f"{texte:62} {v:+4d}" if i else f"{texte:62} {v:4d}" for i, (texte, v) in enumerate(calcul)]
    lignes.append(f"{'total borné entre 0 et 100':62} = {score:3d}")
    if non_couvert and score > PLAFOND_NON_COUVERT:
        score = PLAFOND_NON_COUVERT
        lignes.append(f"{'plafond : une notion de la question non couverte (ni lu, ni Web)':62} → {score:3d}")
    return {"score": score, "libelle": libelle(score), "calcul": lignes}
