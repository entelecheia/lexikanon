from pathlib import Path

import pytest

from lexikanon.stopwords import Stopwords


def test_stopwords_path(tmp_path: Path) -> None:
    path = tmp_path / "stop.txt"
    path.write_text("The 1\nof\n\n# comment\nthe\nAnd extra\n", encoding="utf-8")
    stop = Stopwords(stopwords_path=str(path), lowercase=True, stopwords_list=["X"])
    assert list(stop) == ["and", "of", "the", "x"]
    assert stop("THE") and not stop("comment")


def test_missing_stopwords_path(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    assert len(Stopwords(stopwords_path=str(tmp_path / "missing.txt"))) == 0
    assert "File not found" in caplog.text


def test_nltk_stopwords() -> None:
    stop = Stopwords(nltk_stopwords_lang="english", lowercase=True)
    # The count depends on the NLTK stopwords corpus version (179 in 2023, 198 in 2026).
    assert len(stop) > 150
    assert stop("The") and not stop("rate")


def test_stopwords_fn() -> None:
    stop = Stopwords(stopwords_fn=lambda w: len(w) < 2)
    assert stop("a") and not stop("ab")


def test_stopwords_fn_rejects_source_strings() -> None:
    # A config string used to be eval'd, bypassing HyFI's execution allowlist.
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError, match="no longer evaluates"):
        Stopwords(stopwords_fn="lambda w: len(w) < 2")


def is_short(word: str) -> bool:
    return len(word) < 2


def test_stopwords_fn_from_hyfi_target_respects_allowlist() -> None:
    import pytest
    from hyfi import instantiate
    from hyfi.config import TargetNotAllowed

    target = f"{__name__}.is_short"
    cfg = {
        "_target_": "lexikanon.stopwords.Stopwords",
        "stopwords_fn": {"_target_": target, "_partial_": True},
    }
    stop = instantiate(cfg, allow=["lexikanon.*", target])
    assert stop.is_stopword("a") and not stop.is_stopword("bb")
    with pytest.raises(TargetNotAllowed, match=r"is_short"):
        instantiate(cfg, allow=["lexikanon.*"])


def test_stopwords_operators_use_loaded_words() -> None:
    # #123: the operators read a missing other._stopwords_list attribute.
    ab, bc = Stopwords(stopwords_list=["a", "b"]), Stopwords(stopwords_list=["b", "c"])
    assert ab == Stopwords(stopwords_list=["a", "b"]) and ab != bc
    assert list(ab | bc) == ["a", "b", "c"]
    assert list(ab & bc) == ["b"]
    assert list(ab - bc) == ["a"]
    assert list(ab ^ bc) == ["a", "c"]
    assert list(ab + bc) == ["a", "b", "b", "c"]
    assert ab <= bc and not ab < bc
    assert ab != ["a", "b"]


def test_function_only_stopwords_filter_tokens() -> None:
    # #124: a Stopwords with only stopwords_fn was falsy, so filter_stopwords skipped it.
    from lexikanon.tokenizers import SimpleTokenizer

    tok = SimpleTokenizer(stopwords=Stopwords(stopwords_fn=lambda w: w == "a"))
    assert tok.filter_stopwords(["a", "b"]) == ["b"]
    assert not Stopwords()
