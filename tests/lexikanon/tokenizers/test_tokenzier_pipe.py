import pandas as pd
from lexikanon import HyFI
from lexikanon.tokenizers import MecabTokenizer
from datasets.arrow_dataset import Dataset


def test_tokenizer():
    cfg = HyFI.compose("run=tokenize_dataset")
    cfg.text_col = "text"
    cfg.verbose = True
    print(cfg)
    func = HyFI.partial(cfg)
    text = "금통위는 따라서 물가안정과 병행, 경기상황에 유의하는 금리정책을 펼쳐나가기로 했다고 밝혔다."
    df = pd.DataFrame({"text": [text]})
    data = Dataset.from_pandas(df)
    func(data)


def test_nltk_tokenizer():
    nltk_cfg = HyFI.compose_as_dict("tokenizer=nltk")
    cfg = HyFI.compose("run=tokenize_dataset")
    cfg.tokenizer = nltk_cfg
    cfg.text_col = "text"
    cfg.verbose = True
    print(cfg)
    func = HyFI.partial(cfg)
    text = "Federal Reserve officials concluded their two-day policy meeting Wednesday by holding interest rates steady and signaling they expect to leave them unchanged for the foreseeable future."
    df = pd.DataFrame({"text": [text]})
    data = Dataset.from_pandas(df)
    func(data)


if __name__ == "__main__":
    test_tokenizer()
    test_nltk_tokenizer()
