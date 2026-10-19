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
    assert not ab <= bc and ab <= (ab | bc) and ab < (ab | bc) and (ab | bc) > ab
    assert ab != ["a", "b"]


def test_function_only_stopwords_filter_tokens() -> None:
    # #124: a Stopwords with only stopwords_fn was falsy, so filter_stopwords skipped it.
    from lexikanon.tokenizers import SimpleTokenizer

    tok = SimpleTokenizer(stopwords=Stopwords(stopwords_fn=lambda w: w == "a"))
    assert tok.filter_stopwords(["a", "b"]) == ["b"]
    assert not Stopwords()


def test_stopwords_operators_keep_functions_and_case() -> None:
    # #126: the operators returned a plain word list, dropping stopwords_fn and lowercase.
    short = Stopwords(stopwords_fn=lambda w: len(w) == 1, stopwords_list=["the"], lowercase=True)
    ab = Stopwords(stopwords_list=["A", "bb"], lowercase=True)
    for result in (short | ab, short + ab, ab | short):
        assert result.lowercase
        assert all(result(w) for w in ("X", "THE", "bb")) and not result("cc")
    assert list(short & ab) == ["a"] and (short & ab)("A") and not (short & ab)("bb")
    diff = short - ab
    assert diff("x") and diff("the") and not diff("a") and not diff("bb")
    rev = ab - short
    assert list(rev) == ["bb"] and not rev("a")
    sym = short ^ ab
    assert sym("x") and sym("bb") and not sym("a") and not sym("cc")
    with pytest.raises(ValueError, match="lowercase"):
        short | Stopwords(stopwords_list=["a"])
    with pytest.raises(ValueError, match="stopwords_fn"):
        short & Stopwords(stopwords_fn=str.isdigit, lowercase=True)


def test_comparisons_include_the_function() -> None:
    # #129: ==, < and <= compared only the word lists (and < / <= only their lengths).
    def is_short(w: str) -> bool:
        return len(w) == 1

    plain = Stopwords(stopwords_list=["the"])
    short = Stopwords(stopwords_list=["the"], stopwords_fn=is_short)
    assert plain != short
    assert short == Stopwords(stopwords_list=["the"], stopwords_fn=is_short)
    assert Stopwords(stopwords_list=["a", "b"]) == Stopwords(stopwords_list=["b", "a"])
    assert plain <= short and plain < short and short >= plain
    assert Stopwords(stopwords_list=["x"]) <= short  # matched by the function
    assert short <= short and not short < short
    with pytest.raises(TypeError, match="stopwords_fn"):
        _ = short <= plain


def test_falsy_callable_is_still_a_function() -> None:
    # #130: is_stopword used `if self.func`, ignoring a callable whose bool() is False.
    class Falsy:
        def __bool__(self) -> bool:
            return False

        def __call__(self, w: str) -> bool:
            return w == "a"

    stop = Stopwords(stopwords_fn=Falsy())
    assert stop and stop.is_stopword("a") and not stop.is_stopword("b")
    assert (stop | Stopwords(stopwords_list=["b"]))("a")
    assert (stop - Stopwords(stopwords_list=["b"]))("a")
