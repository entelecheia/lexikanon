from lexikanon.pipe.tokenize import tokenize_dataset, extract_tokens
from lexikanon import HyFI


def test_pipes():
    name = HyFI.generate_config(tokenize_dataset, use_first_arg_as_pipe_obj=True)
    assert name == "tokenize_dataset"
    name = HyFI.generate_config(extract_tokens, use_first_arg_as_pipe_obj=True)
    assert name == "extract_tokens"


if __name__ == "__main__":
    test_pipes()
