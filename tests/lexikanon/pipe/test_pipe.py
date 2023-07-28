from lexikanon.pipe.tokenize import tokenize_dataset, extract_tokens
from lexikanon import HyFI


def test_pipes():
    name = HyFI.save_hyfi_pipe_config(tokenize_dataset)
    assert name == "tokenize_dataset"
    name = HyFI.save_hyfi_pipe_config(extract_tokens)
    assert name == "extract_tokens"


if __name__ == "__main__":
    test_pipes()
