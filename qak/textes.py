"""Normalisation de texte partagée : recherche, déduplication, taxonomie."""
import json
import re
import unicodedata
from functools import lru_cache

from . import chemins

MOTS_VIDES = set("""
a au aux avec ce ces cet cette dans de des du elle en est et etre il ils je la le les leur leurs lui ma mais me meme
mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur ta te tes toi ton tu un une vos votre
vous y d l j m n s t c qu quel quelle quels quelles comment pourquoi quoi dont ou est-ce peut peuvent permet ai
permettent pourrait pourraient faire fait sont ont avoir plus moins tres tout tous toute toutes autre autres
entre sans sous chez ainsi aussi donc alors comme si non oui afin cela ceci celui celle ceux nos via
pendant lors durant selon notre nos leurs avant apres depuis vers deja encore ici bien tres trop peu
quand quoi lequel laquelle lesquels lesquelles doit doivent faut existe existent quel donne donner
the of and or to in on for with by an is are be as at from that this these those it its can could should would
which what how why when where who into than then there their them they not no do does using use used about
""".split())

# Mots trop généraux dans un corpus de syllabus pour peser dans une requête.
MOTS_GENERIQUES = {"istqb", "syllabus", "idee", "idees", "pratique", "pratiques",
                   "recherche", "cherche", "trouve", "retrouve", "quelles", "ameliorer", "amelioration",
                   "difference", "differences"}


def sans_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def normaliser(s: str) -> str:
    """Minuscules, sans accents, apostrophes et ponctuation → espaces."""
    s = sans_accents((s or "").lower()).replace("’", " ").replace("'", " ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def motif_sous_sections(numero: str) -> str:
    """Motif LIKE des sous-sections de `numero` (« 4.2 » → « 4.2.% »), jokers % et _
    échappés : à employer avec `LIKE ? ESCAPE '\\'`. Sans échappement, une section « % »
    désignait tout le document."""
    n = numero.rstrip(".").replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return n + ".%"


def racine(mot: str) -> str:
    """Racinisation minimale FR/EN (pluriels) : suffisante pour comparer des titres."""
    for suf in ("ies", "es", "s", "x"):
        if len(mot) > 4 and mot.endswith(suf):
            return mot[: -len(suf)] + ("y" if suf == "ies" else "")
    return mot


def mots(s: str, garder_generiques: bool = True) -> list[str]:
    out = [m for m in normaliser(s).split() if m not in MOTS_VIDES and (len(m) > 1 or m.isdigit())]
    return out if garder_generiques else [m for m in out if m not in MOTS_GENERIQUES]


@lru_cache(maxsize=4)
def _thesaurus(chemin: str) -> tuple:
    data = json.loads(open(chemin, encoding="utf-8").read())
    concepts, motifs = [], []
    for c in data["concepts"]:
        termes = tuple(t for t in c["termes"] if normaliser(t))
        concepts.append((c["id"], termes))
        majuscules = {normaliser(t) for t in c.get("majuscules", [])}
        for t in termes:
            cible = tuple(racine(m) for m in normaliser(t).split())
            motifs.append((cible, c["id"], termes, sigle_court(cible) or normaliser(t) in majuscules))
    motifs.sort(key=lambda m: -len(m[0]))  # expressions les plus longues d'abord
    return tuple(concepts), tuple(motifs)


def thesaurus() -> tuple:
    """Tuple de (id_concept, termes)."""
    return _thesaurus(str(chemins.thesaurus()))[0]


def _en_majuscules(texte: str, origine: list[str]) -> list[bool]:
    """Pour chaque mot normalisé de `texte`, vrai s'il était écrit en MAJUSCULES."""
    bruts = re.sub(r"[^A-Za-z0-9]+", " ", sans_accents((texte or "").replace("’", " "))).split()
    if [b.lower() for b in bruts] != origine:  # découpage différent (caractère exotique) : prudence
        return [False] * len(origine)
    return [b.isupper() for b in bruts]


def sigle_court(cible: tuple) -> bool:
    """Terme d'un seul mot de 2 lettres (ai, ia, ml, ux) : ce sont aussi des mots ordinaires
    (« j'ai »), reconnus seulement écrits en MAJUSCULES dans la question (issue #42). Un
    concept peut soumettre d'autres termes à la même règle (clé « majuscules » : IDEAL)."""
    return len(cible) == 1 and len(cible[0]) <= 2 and cible[0].isalpha()


def termes_thesaurus() -> frozenset:
    """Tous les termes du thésaurus, normalisés (« tmmi », « api », « partition d equivalence »)."""
    return _termes_thesaurus(str(chemins.thesaurus()))


@lru_cache(maxsize=4)
def _termes_thesaurus(chemin: str) -> frozenset:
    return frozenset(normaliser(t) for _, termes in _thesaurus(chemin)[0] for t in termes)


def reperer_concepts(texte: str) -> tuple[list[tuple[str, tuple]], list[str]]:
    """Repère les concepts du thésaurus dans `texte` (pluriels tolérés, expressions
    longues prioritaires ; sigles de 2 lettres seulement en MAJUSCULES). Renvoie
    [(id_concept, termes)] et les mots non couverts."""
    origine = normaliser(texte).split()
    majuscules = _en_majuscules(texte, origine)
    toks: list = [racine(m) for m in origine]
    trouves, vus = [], set()
    for cible, cid, termes, en_majuscules in _thesaurus(str(chemins.thesaurus()))[1]:
        k = len(cible)
        for i in range(len(toks) - k + 1):
            if tuple(toks[i:i + k]) == cible and (not en_majuscules or all(majuscules[i:i + k])):
                toks[i:i + k] = [None] * k  # consommé : ne sert plus à un concept plus court
                if cid not in vus:
                    trouves.append((cid, termes))
                    vus.add(cid)
    reste = [o for o, t in zip(origine, toks) if t is not None and o not in MOTS_VIDES]
    return trouves, reste


def signature(texte: str) -> set[str]:
    """Ensemble comparable : concepts du thésaurus + racines des mots restants.
    « Partitions d'équivalence » et « equivalence partitioning » ont la même signature."""
    concepts, reste = reperer_concepts(texte)
    sig = {f"#{cid}" for cid, _ in concepts}
    sig |= {racine(m) for m in reste if m not in MOTS_GENERIQUES and len(m) > 2}
    return sig


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def recouvrement(a: set, b: set) -> float:
    """Part du plus petit ensemble contenue dans l'autre (titre court inclus dans un long)."""
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0
