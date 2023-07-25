from lexikanon import HyFI
from lexikanon.stopwords import Stopwords


def test_stopwords():
    print(HyFI.get_caller_module_name())
    cfg = HyFI.compose_as_dict("stopwords")
    cfg["nltk_stopwords_lang"] = "english"
    stop = Stopwords(**cfg)
    print(stop)
    print(list(stop))
    assert len(stop) == 179


if __name__ == "__main__":
    test_stopwords()
