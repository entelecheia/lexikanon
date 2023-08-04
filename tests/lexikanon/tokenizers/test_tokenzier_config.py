from lexikanon import HyFI


def test_tokenizer():
    tokenizer = HyFI.instantiate_config("tokenizer=mecab")
    # print(tokenizer)
    text = "금통위는 따라서 물가안정과 병행, 경기상황에 유의하는 금리정책을 펼쳐나가기로 했다고 밝혔다."
    tokens = tokenizer(text)
    print(tokens)
    # assert len(stop.stopwords_list) == 179


def test_nltk_tokenizer():
    tokenizer = HyFI.instantiate_config("tokenizer=nltk")
    # print(tokenizer)
    text = "Federal Reserve officials concluded their two-day policy meeting Wednesday by holding interest rates steady and signaling they expect to leave them unchanged for the foreseeable future."
    tokens = tokenizer(text)
    print(tokens)
    # assert len(stop.stopwords_list) == 179


if __name__ == "__main__":
    test_tokenizer()
    test_nltk_tokenizer()
