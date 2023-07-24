# -*- encoding:utf8 -*-
import re
from typing import Dict, List, Tuple, Union

import numpy as np

kor_begin: int = 44032
kor_end: int = 55203
chosung_base: int = 588
jungsung_base: int = 28
jaum_begin: int = 12593
jaum_end: int = 12622
moum_begin: int = 12623
moum_end: int = 12643

chosung_list = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

jungsung_list = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

jongsung_list = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

jaum_list = [
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

moum_list = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

doublespace_pattern = re.compile(r"\s+")
repeatchars_pattern = re.compile(r"(\w)\\1{3,}")


class ConvolutionHangleEncoder:
    """초/중/종성을 구성하는 자음/모음과 띄어쓰기만 인코딩
    one hot vector [ㄱ, ㄴ, ㄷ, ... ㅎ, ㅏ, ㅐ, .. ㅢ, ㅣ,"  ", ㄱ, ㄲ, ... ㅍ, ㅎ,"  ", 0, 1, 2, .. 9]
    """

    def __init__(self):
        self.jung_begin: int = 19  # len(chosung_list)
        self.jong_begin: int = 40  # self.jung_begin + len(jungsung_list)
        self.number_begin: int = 68  # self.jong_begin + len(jongsung_list)
        self.space: int = (
            78  # len(chosung_list) + len(jungsung_list) + len(jongsung_list) + 10
        )
        self.unk: int = 79
        self.dim: int = 80
        num = [str(i) for i in range(10)]
        space = " "
        unk = "<unk>"
        idx_to_char = (
            chosung_list + jungsung_list + jongsung_list + num + [space] + [unk]
        )
        self.idx_to_char: Dict[int, str] = dict(enumerate(idx_to_char))
        self.jamo_to_idx: Dict[str, int] = {
            "ㄱ": 0,
            "ㄲ": 1,
            "ㄴ": 2,
            "ㄷ": 3,
            "ㄸ": 4,
            "ㄹ": 5,
            "ㅁ": 6,
            "ㅂ": 7,
            "ㅃ": 8,
            "ㅅ": 9,
            "ㅆ": 10,
            "ㅇ": 11,
            "ㅈ": 12,
            "ㅉ": 13,
            "ㅊ": 14,
            "ㅋ": 15,
            "ㅌ": 16,
            "ㅍ": 17,
            "ㅎ": 18,
            "ㅏ": 19,
            "ㅐ": 20,
            "ㅑ": 21,
            "ㅒ": 22,
            "ㅓ": 23,
            "ㅔ": 24,
            "ㅕ": 25,
            "ㅖ": 26,
            "ㅗ": 27,
            "ㅘ": 28,
            "ㅙ": 29,
            "ㅚ": 30,
            "ㅛ": 31,
            "ㅜ": 32,
            "ㅝ": 33,
            "ㅞ": 34,
            "ㅟ": 35,
            "ㅠ": 36,
            "ㅡ": 37,
            "ㅢ": 38,
            "ㅣ": 39,
            " ": 40,
            "ㄳ": 43,
            "ㄵ": 45,
            "ㄶ": 46,
            "ㄺ": 49,
            "ㄻ": 50,
            "ㄼ": 51,
            "ㄽ": 52,
            "ㄾ": 53,
            "ㄿ": 54,
            "ㅀ": 55,
            "ㅄ": 58,
        }

    def encode(self, sent: str) -> np.ndarray:
        onehot = self.sent_to_onehot(sent)
        x = np.zeros((len(onehot), self.dim))
        for i, xi in enumerate(onehot):
            for j in xi:
                if j >= 0:
                    x[i, j] = 1
        return x

    def sent_to_onehot(self, sent: str) -> List[Tuple[int, int, int]]:
        chars = self._normalize(sent)
        ords = [ord(c) for c in chars]
        onehot = []
        for char, idx in zip(chars, ords):
            if idx == 32:
                onehot.append((self.space, -1, -1))
            elif 48 <= idx <= 57:
                onehot.append((idx - 48 + self.number_begin, -1, -1))
            else:
                onehot.append(self._decompose(char, idx))
        return onehot

    def onehot_to_sent(self, encoded_sent: List[Tuple[int, int, int]]) -> str:
        def check_cjj(char: Tuple[int, int, int]):
            cho, jung, jong = char
            if not (0 <= cho < self.jung_begin):
                raise ValueError("Chosung %d is out of index" % cho)
            if not (self.jung_begin <= jung < self.jong_begin):
                raise ValueError("Jungsung %d is out of index" % jung)
            if not (self.jong_begin <= jong < self.number_begin):
                raise ValueError("Jongsung %d is out of index" % jong)

        chars = []
        for char in encoded_sent:
            if char[1] < 0 or char[2] < 0:
                if not 0 <= char[0] < self.dim:
                    raise ValueError(
                        "character index %d is out of index [0, %d]"
                        % (char[0], self.dim)
                    )
                chars.append(self.idx_to_char[char[0]])
            else:
                check_cjj(char)
                cho, jung, jong = tuple(self.idx_to_char[ci] for ci in char)
                chars.append(compose(cho, jung, jong))
        return "".join(chars)

    def _normalize(self, sent: str) -> str:
        import re

        regex = re.compile("[^ㄱ-ㅎㅏ-ㅣ가-힣 0-9]")
        sent = regex.sub(" ", sent)
        sent = doublespace_pattern.sub(" ", sent).strip()
        return sent

    def _compose(
        self,
        cho: int,
        jung: int,
        jong: int,
    ) -> str:
        return chr(kor_begin + chosung_base * cho + jungsung_base * jung + jong)

    def _decompose(self, char: str, i: int) -> Tuple[int, int, int]:
        if not kor_begin <= i <= kor_end:
            return (self.jamo_to_idx.get(char, self.unk), -1, -1)
        i -= kor_begin
        cho = i // chosung_base
        jung = (i - cho * chosung_base) // jungsung_base
        jong = i - cho * chosung_base - jung * jungsung_base
        return (cho, self.jung_begin + jung, self.jong_begin + jong)


def compose(chosung: str, jungsung: str, jongsung: str) -> str:
    return chr(
        kor_begin
        + chosung_base * chosung_list.index(chosung)
        + jungsung_base * jungsung_list.index(jungsung)
        + jongsung_list.index(jongsung)
    )


def decompose(char: str) -> Tuple[str, str, str]:
    if not is_korean(char):
        return (char, " ", " ")
    i = to_base(char)
    if jaum_begin <= i <= jaum_end:
        return (char, " ", " ")
    if moum_begin <= i <= moum_end:
        return (" ", char, " ")
    i -= kor_begin
    cho = i // chosung_base
    jung = (i - cho * chosung_base) // jungsung_base
    jong = i - cho * chosung_base - jung * jungsung_base
    return (chosung_list[cho], jungsung_list[jung], jongsung_list[jong])


def is_korean(char: str):
    i = to_base(char)
    return (
        (kor_begin <= i <= kor_end)
        or (jaum_begin <= i <= jaum_end)
        or (moum_begin <= i <= moum_end)
    )


def is_complete_korean(char: str):
    return kor_begin <= to_base(char) <= kor_end


def is_jaum(char: str):
    return jaum_begin <= to_base(char) <= jaum_end


def is_moum(char: str):
    return moum_begin <= to_base(char) <= moum_end


def to_base(char: Union[str, int]):
    if type(char) in [str, int]:
        return ord(str(char))
    else:
        raise TypeError


def is_number(char: str):
    i = to_base(char)
    return i >= 48 and i <= 57


def is_english(char: str):
    i = to_base(char)
    return (i >= 97 and i <= 122) or (i >= 65 and i <= 90)


def is_punctuation(char: str):
    i = to_base(char)
    return i in [33, 34, 39, 44, 46, 63, 96]
