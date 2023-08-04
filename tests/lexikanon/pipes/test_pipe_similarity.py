from lexikanon.pipes.similarity import find_similar_docs_by_clustering
from lexikanon import HyFI
from hyfi.composer import PipeTargetTypes

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal


@pytest.fixture
def sample_data():
    data = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"]
            ),
            "tokens": [
                ["apple", "banana", "cherry"],
                ["apple", "banana", "date"],
                ["apple", "banana", "elderberry"],
                ["apple", "banana", "fig"],
                ["apple", "banana", "grape"],
            ],
            "id": [1, 2, 3, 4, 5],
        }
    )
    return data


def test_find_similar_docs_by_clustering(sample_data):
    # Arrange
    expected_result = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"]
            ),
            "tokens": [
                ["apple", "banana", "cherry"],
                ["apple", "banana", "date"],
                ["apple", "banana", "elderberry"],
                ["apple", "banana", "fig"],
                ["apple", "banana", "grape"],
            ],
            "id": [1, 2, 3, 4, 5],
            "cluster": [None, None, None, None, None],
            "duplicate": [False, False, False, False, False],
            "dist_fig": [None, None, None, None, None],
        }
    )

    # Act
    result = find_similar_docs_by_clustering(sample_data)

    # Assert
    result.set_index("id", inplace=True)
    expected_result.set_index("id", inplace=True)
    assert_frame_equal(result, expected_result)


def test_pipes():
    HyFI.generate_pipe_config(
        find_similar_docs_by_clustering,
        pipe_target_type=PipeTargetTypes.GENERAL_EXTERNAL_FUNCS,
    )


if __name__ == "__main__":
    test_pipes()
