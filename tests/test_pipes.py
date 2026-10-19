import sys
from typing import Any

import pandas as pd
import pytest
from datasets import Dataset

from lexikanon.normalizers import Normalizer
from lexikanon.pipes.similarity import find_similar_docs_by_clustering
from lexikanon.pipes.tokenize import extract_tokens, tokenize_dataset, tokenize_texts
from lexikanon.tokenizers import MecabTokenizer

from .conftest import KO


def test_tokenize_texts_default_is_simple() -> None:
    assert tokenize_texts(["a b\nc", "d"]) == [["a", "b", "c"], ["d"]]


def test_tokenize_and_extract_dataset() -> None:
    tok = MecabTokenizer(noun_postags=["NNG"])
    data = Dataset.from_dict({"text": [KO]})
    data = tokenize_dataset(data, tokenizer=tok, verbose=True)
    data = extract_tokens(data, tokenizer=tok, nouns_only=True, strip_pos=True)
    assert data["tokens"][0][:2] == ["금통위/NNG", "는/JX"]
    assert data["extracted_tokens"][0][:3] == ["금통위", "물가", "안정"]


def test_unbatched_map_stores_one_token_list_per_row() -> None:
    # #120: the map callbacks always returned a batch, so batched=False nested one level deeper.
    data = Dataset.from_dict({"text": ["a b\nc", "d"]})
    for batched in (True, False):
        tokens = tokenize_dataset(data, batched=batched)
        assert tokens["tokens"] == [["a", "b", "c"], ["d"]]
        extracted = extract_tokens(tokens, batched=batched)
        assert extracted["extracted_tokens"] == [["a", "b", "c"], ["d"]]


DILL_HASHING = sys.version_info < (3, 15)


class CaseNormalizer(Normalizer):  # module level, so dill can hash it
    upper: bool = False


@pytest.mark.skipif(not DILL_HASHING, reason="datasets hashes map functions with dill below 3.15")
def test_dataset_cache_key_tracks_every_setting() -> None:
    # Review of #119 found four settings a hand-made key missed; datasets' own dill hash of
    # the map function and its arguments captures them all, including private state.
    from nltk.stem import PorterStemmer

    from lexikanon.tokenizers import NLTKTagger, NLTKTokenizer, SimpleTokenizer

    data = Dataset.from_dict({"text": [KO]})

    def fp(**kw: Any) -> str:
        return tokenize_dataset(data, **kw)._fingerprint

    mecab = MecabTokenizer()
    assert fp(tokenizer=mecab) == fp(tokenizer=MecabTokenizer())  # identical settings reuse
    assert fp(tokenizer=mecab) != fp(tokenizer=MecabTokenizer(strip_pos=True))
    assert fp(batched=True) != fp(batched=False)
    lower = SimpleTokenizer(normalizer=CaseNormalizer(upper=False))
    upper = SimpleTokenizer(normalizer=CaseNormalizer(upper=True))
    assert fp(tokenizer=lower) != fp(tokenizer=upper)

    def nltk(mode: str) -> NLTKTokenizer:
        return NLTKTokenizer(tagger=NLTKTagger(stemmer=PorterStemmer(mode=mode)))

    assert fp(tokenizer=nltk("ORIGINAL_ALGORITHM")) != fp(tokenizer=nltk("NLTK_EXTENSIONS"))

    tokens = tokenize_dataset(data, tokenizer=mecab)
    a, b = MecabTokenizer(), MecabTokenizer()
    b.stopwords.stopwords.append("물가")  # same public settings, different loaded list
    assert extract_tokens(tokens, tokenizer=a)._fingerprint != (
        extract_tokens(tokens, tokenizer=b)._fingerprint
    )


@pytest.mark.skipif(DILL_HASHING, reason="only Python 3.15+ falls back to random keys")
def test_dataset_cache_is_not_reused_without_dill() -> None:
    data = Dataset.from_dict({"text": ["a b"]})
    assert tokenize_dataset(data)._fingerprint != tokenize_dataset(data)._fingerprint


def _docs(ids: list[Any], days: list[str], tokens: list[list[str]]) -> pd.DataFrame:
    return pd.DataFrame({"timestamp": pd.to_datetime(days), "tokens": tokens, "id": ids})


def test_small_batches_are_skipped() -> None:
    days = ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"]
    tokens = [["apple", "banana", x] for x in ["cherry", "date", "elderberry", "fig", "grape"]]
    result = find_similar_docs_by_clustering(_docs([1, 2, 3, 4, 5], days, tokens))
    assert result["id"].tolist() == [1, 2, 3, 4, 5]
    assert result["cluster"].isna().all()
    assert not result["duplicate"].any()


def test_duplicates_are_flagged(tmp_path: Any) -> None:
    # Before 1.0 the cluster table was built from index-misaligned Series, so this raised
    # unless ids equalled row positions, and the default distance_threshold=None hit a
    # NameError while plotting. Integer and string ids both go through the id handling.
    days = ["2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06"]
    tokens = [["rate", "steady"], ["rate", "steady"], ["apple", "banana"], ["rate", "hold"]]
    for ids in ([10, 11, 12, 13], ["a", "b", "c", "d"]):
        result = find_similar_docs_by_clustering(
            _docs(ids, days, tokens),
            num_workers=1,
            min_num_docs=2,
            output_dir=str(tmp_path),
            save_fig=True,
        )
        assert result["id"].tolist() == ids
        assert result["duplicate"].tolist() == [False, True, False, False]
    assert list(tmp_path.glob("similarity_dist_*.png"))


def test_duplicates_keep_typed_ids_apart(tmp_path: Any) -> None:
    # #121: the earliest document was matched by str(id), so the later "1" counted as the
    # earliest of its cluster because the int 1 was.
    days = ["2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06"]
    tokens = [["rate", "steady"], ["rate", "steady"], ["apple", "banana"], ["apple", "banana"]]
    result = find_similar_docs_by_clustering(
        _docs([1, 2, 3, "1"], days, tokens),
        num_workers=1,
        min_num_docs=2,
        output_dir=str(tmp_path),
    )
    assert result["id"].tolist() == [1, 2, 3, "1"]
    assert result["duplicate"].tolist() == [False, True, False, True]


def test_similar_docs_keep_input_columns_and_index(tmp_path: Any) -> None:
    # #127: the timestamp became the index and then a leading column, the input index was
    # replaced by per-batch positions, and the caller's frame was modified in place.
    days = ["2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", "2022-01-12"]
    tokens = [["rate", "steady"], ["rate", "steady"], ["apple"], ["rate", "hold"], ["x"]]
    data = pd.DataFrame(
        {"id": [10, 11, 12, 13, 14], "tokens": tokens, "timestamp": days},
        index=pd.Index(list("vwxyz"), name="key"),
    )
    before = data.copy()
    result = find_similar_docs_by_clustering(
        data, num_workers=1, min_num_docs=2, output_dir=str(tmp_path)
    )
    pd.testing.assert_frame_equal(data, before)
    assert result.columns.tolist() == [
        "id",
        "tokens",
        "timestamp",
        "cluster",
        "duplicate",
        "dist_fig",
    ]
    assert result.index.equals(before.index)
    assert result["duplicate"].tolist() == [False, True, False, False, False]


def test_similar_docs_column_names_do_not_collide(tmp_path: Any) -> None:
    # Review of #125: an internal "order" key column overwrote cluster_col="order".
    days = ["2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06"]
    tokens = [["rate", "steady"], ["rate", "steady"], ["apple", "banana"], ["rate", "hold"]]
    data = pd.DataFrame({"index": days, "tokens": tokens, "level_0": [1, 2, 3, 4]})
    result = find_similar_docs_by_clustering(
        data,
        num_workers=1,
        min_num_docs=2,
        timestamp_col="index",
        id_col="level_0",
        cluster_col="order",
        duplicate_col="keys",
        output_dir=str(tmp_path),
    )
    assert result["keys"].tolist() == [False, True, False, False]
    assert result["order"].iloc[0] == result["order"].iloc[1]


def test_similar_docs_empty_input_and_missing_timestamps(tmp_path: Any) -> None:
    # #128: an empty frame raised in pd.concat, and NaT rows were dropped from the result.
    cols = ["id", "tokens", "timestamp", "cluster", "duplicate", "dist_fig"]
    empty = pd.DataFrame({"id": [], "tokens": [], "timestamp": []})
    result = find_similar_docs_by_clustering(empty, num_workers=1, output_dir=str(tmp_path))
    assert result.columns.tolist() == cols and len(result) == 0

    days = ["2022-01-03", None, "2022-01-04", "2022-01-05"]
    tokens = [["rate", "steady"], ["rate", "steady"], ["rate", "steady"], ["apple"]]
    data = pd.DataFrame(
        {"id": [1, 2, 3, 4], "tokens": tokens, "timestamp": days}, index=list("abcd")
    )
    result = find_similar_docs_by_clustering(
        data, num_workers=1, min_num_docs=2, output_dir=str(tmp_path)
    )
    assert result.index.tolist() == list("abcd")
    assert result["duplicate"].tolist() == [False, False, True, False]
    assert result.loc["b", "cluster"] is None

    no_times = data.assign(timestamp=None)
    result = find_similar_docs_by_clustering(no_times, num_workers=1, output_dir=str(tmp_path))
    assert result.index.tolist() == list("abcd") and not result["duplicate"].any()
