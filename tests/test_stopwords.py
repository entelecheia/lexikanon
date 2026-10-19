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
