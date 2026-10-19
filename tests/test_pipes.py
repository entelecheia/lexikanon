from typing import Any

import pandas as pd
from datasets import Dataset

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


def test_dataset_fingerprint_tracks_settings() -> None:
    # tokenize_dataset passes its own fingerprint so datasets never dill-hashes the map
    # function (fails on Python 3.15); different settings must not share a cache entry.
    data = Dataset.from_dict({"text": [KO]})
    a = tokenize_dataset(data, tokenizer=MecabTokenizer())
    b = tokenize_dataset(data, tokenizer=MecabTokenizer(strip_pos=True))
    c = tokenize_dataset(data, tokenizer=MecabTokenizer())
    assert a._fingerprint == c._fingerprint != b._fingerprint
    assert b["tokens"][0][:2] == ["금통위", "는"]


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
