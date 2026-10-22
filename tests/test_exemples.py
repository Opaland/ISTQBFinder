"""Issue #47 : citations de docs/exemples-conversations.md relues avec la CLI
(`section CTAL-TAE-2.0-fr 3.1.3`, `page CTAL-TA-4.0-en 25`)."""
import re

from conftest import RACINE_CODE

EXEMPLES = (RACINE_CODE / "docs" / "exemples-conversations.md").read_text(encoding="utf-8")


def test_couches_citees_au_paragraphe_3_1_3():
    # La superposition en couches du TAF est au §3.1.3 (p. 26 FR / p. 24 EN), pas aux §4.3 / §3.1.5.
    for m in re.finditer(r"couches[^\[]{0,120}\[([^\]]+)\]", EXEMPLES):
        assert "§3.1.3" in m.group(1), m.group(0)
    assert "§3.1.3, p. 26 ; EN p. 24" in EXEMPLES


def test_passage_ta_en_p25_indexe_sous_l_introduction():
    assert "EN §2.1, p. 25" not in EXEMPLES
    assert "EN §2 (introduction du chapitre), p. 25" in EXEMPLES
