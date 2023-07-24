from lexikanon import HyFI
from lexikanon.normalizers import Normalizer


def test_normalizer():
    print(HyFI.get_caller_module_name())
    cfg = HyFI.compose_as_dict("normalizer=formal_ko")
    norm = Normalizer(**cfg)
    text = "IMF가 推定한 우리나라의 GDP갭률은 今年에도 소폭의 마이너스(−)를 持續하고 있다."
    print(norm(text))
    normalized_text = "IMF가 추정한 우리나라의 GDP갭률은 금년에도 소폭의 마이너스(-)를 지속하고 있다."
    assert norm(text) == normalized_text


if __name__ == "__main__":
    test_normalizer()
