import pytest

from lexikanon.tokenizers.nltk import _build


def test_build_refuses_targets_outside_nltk_stem() -> None:
    # Specs can reach the model without hyfi.instantiate's allowlist (e.g. model_validate).
    with pytest.raises(ValueError, match="refusing to build"):
        _build({"_target_": "os.system", "command": "echo unsafe"})
    with pytest.raises(ValueError, match="refusing to build"):
        _build({"_target_": "nltk.stemmer_lookalike.Evil"})


def test_build_keeps_nltk_stemmers_and_passthrough() -> None:
    stemmer = _build({"_target_": "nltk.stem.PorterStemmer"})
    assert stemmer.stem("running") == "run"
    obj = object()
    assert _build(obj) is obj
