"""AC3: outputs for the 1.x test inputs are unchanged.

``data/outputs_1x.json`` was recorded with lexikanon 0.6.5 on hyfi 1.37.0, ekonlpy 2.0.6, and
nltk 3.9.1 (its poetry.lock). ``data/composed_1x.json`` holds the configs 1.x composed for each
group option, without the 1.x ``_config_name_`` / ``_config_group_`` keys.

Not carried over: the 1.x test asserted 179 NLTK English stopwords; the count comes from the
NLTK stopwords corpus (198 when recorded), not from lexikanon, so it is checked loosely in
test_stopwords.py.
"""

import json
from pathlib import Path
from typing import Any

import hyfi
import pytest

from lexikanon.normalizers import Normalizer
from lexikanon.stopwords import Stopwords
from lexikanon.tokenizers import MecabTokenizer, NLTKTokenizer, SimpleTokenizer, Tokenizer

from .conftest import EN, KO, KO_HANJA

DATA = Path(__file__).parent / "data"
GOLDEN: dict[str, Any] = json.loads((DATA / "outputs_1x.json").read_text(encoding="utf-8"))
COMPOSED: dict[str, Any] = json.loads((DATA / "composed_1x.json").read_text(encoding="utf-8"))
NORM_TEXT = KO_HANJA + " ㅋㅋㅋㅋ 　“quoted”\t…"


def build(group: str, name: str) -> Any:
    return hyfi.instantiate(hyfi.compose_group(group, name))


@pytest.fixture(scope="module")
def outputs() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name in ["default", "formal_ko", "informal_ko", "formal_en", "formal_en_parantheses"]:
        key = "__init__" if name == "default" else name
        out[f"normalizer/{key}"] = build("normalizer", name)(NORM_TEXT)
    for name in ["mecab", "simple", "nltk", "nltk_universal"]:
        text = KO if name in ("mecab", "simple") else EN
        tok = build("tokenizer", name)
        out[f"tokenizer/{name}/tokenize"] = tok(text)
        out[f"tokenizer/{name}/nouns"] = tok.nouns(text)
        out[f"tokenizer/{name}/tokens"] = tok.tokens(text)
        if name.startswith("nltk"):
            tok.strip_pos = False
            tok.stopwords.nltk_stopwords_lang = "english"
            out[f"tokenizer/{name}/stopwords_en/tokenize"] = tok(text)
            out[f"tokenizer/{name}/stopwords_en/nouns"] = tok.nouns(text)
            out[f"tokenizer/{name}/stopwords_en/tokens"] = tok.tokens(text)
    each_word = build("tokenizer", "mecab")
    each_word.tokenize_each_word = True
    out["tokenizer/mecab/tokenize_each_word"] = each_word(KO)
    out["instantiate/tokenizer=mecab"] = build("tokenizer", "mecab")(KO)

    # Direct construction, without HyFI.
    out["direct/Normalizer()"] = Normalizer()(NORM_TEXT)
    for name, cls, text in [
        ("Tokenizer", Tokenizer, KO),
        ("SimpleTokenizer", SimpleTokenizer, KO),
        ("MecabTokenizer", MecabTokenizer, KO),
        ("NLTKTokenizer", NLTKTokenizer, EN),
    ]:
        tok = cls()
        out[f"direct/{name}()/tokenize"] = tok(text)
        out[f"direct/{name}()/nouns"] = tok.nouns(text)
        out[f"direct/{name}()/tokens"] = tok.tokens(text)
    stop = Stopwords(stopwords_list=["The", "of"], lowercase=True)
    out["direct/Stopwords"] = [stop("the"), stop("THE"), stop("x"), len(stop)]
    return out


@pytest.mark.parametrize("key", sorted(GOLDEN))
def test_output_matches_1x(outputs: dict[str, Any], key: str) -> None:
    assert outputs[key] == GOLDEN[key]


def test_formal_ko_normalizer() -> None:
    expected = "IMF가 추정한 우리나라의 GDP갭률은 금년에도 소폭의 마이너스(-)를 지속하고 있다."
    assert build("normalizer", "formal_ko")(KO_HANJA) == expected


@pytest.mark.parametrize("key", sorted(COMPOSED))
def test_config_matches_1x(key: str) -> None:
    group, _, name = key.partition("=")
    assert hyfi.to_dict(hyfi.compose_group(group, name or "default")) == COMPOSED[key]


def test_sentence_separator() -> None:
    tok = build("tokenizer", "mecab")
    assert tok.sentence_separator == "\\n"
    assert tok.sentence_separator_unicode == "\n"
