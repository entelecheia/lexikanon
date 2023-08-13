from lexikanon import HyFI
from lexikanon.tokenizers import MecabTokenizer, NLTKTokenizer

HyFI.setLogger("INFO")


def test_tokenizer():
    cfg = HyFI.compose_as_dict("tokenizer=mecab")
    tokenizer = MecabTokenizer(**cfg)
    print(tokenizer.sentence_separator, tokenizer.sentence_separator_unicode)
    assert tokenizer.sentence_separator == "\\n"
    assert tokenizer.sentence_separator_unicode == "\n"
    # print(tokenizer)
    text = "금통위는 따라서 물가안정과 병행, 경기상황에 유의하는 금리정책을 펼쳐나가기로 했다고 밝혔다."
    tokens = tokenizer(text)
    print(tokens)
    # assert len(stop.stopwords_list) == 179


def test_nltk_tokenizer():
    cfg = HyFI.compose_as_dict("tokenizer=nltk")
    tokenizer = NLTKTokenizer(**cfg)
    tokenizer.strip_pos = False
    tokenizer.stopwords.nltk_stopwords_lang = "english"
    tokenizer.stopwords.verbose = True
    tokenizer.verbose = True

    # print(tokenizer)
    text = "Federal Reserve officials concluded their two-day policy meeting Wednesday by holding interest rates steady and signaling they expect to leave them unchanged for the foreseeable future."
    tokens = tokenizer(text)
    print(tokens)
    tokens = tokenizer.nouns(text)
    print(tokens)
    tokens = tokenizer.tokens(text)
    print(tokens)


def test_nltk_tokenizer_univ():
    cfg = HyFI.compose_as_dict("tokenizer=nltk_universal")
    tokenizer = NLTKTokenizer(**cfg)
    tokenizer.strip_pos = False
    tokenizer.stopwords.nltk_stopwords_lang = "english"
    tokenizer.stopwords.verbose = True
    tokenizer.verbose = True

    # print(tokenizer)
    text = "Federal Reserve officials concluded their two-day policy meeting Wednesday by holding interest rates steady and signaling they expect to leave them unchanged for the foreseeable future."
    tokens = tokenizer(text)
    print(tokens)
    tokens = tokenizer.nouns(text)
    print(tokens)
    tokens = tokenizer.tokens(text)
    print(tokens)
    # assert len(stop.stopwords_list) == 179


if __name__ == "__main__":
    test_tokenizer()
    test_nltk_tokenizer()
    test_nltk_tokenizer_univ()
