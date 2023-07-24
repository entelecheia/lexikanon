# -*- coding: utf8 -*-


def separate(ch):
    """한글 자모 분리. 주어진 한글 한 글자의 초성, 중성 초성을 반환함."""
    uindex = ord(ch) - 0xAC00
    jongseong = uindex % 28
    # NOTE: Force integer-divisions
    joongseong = ((uindex - jongseong) // 28) % 21
    choseong = ((uindex - jongseong) // 28) // 21

    return (choseong, joongseong, jongseong)


def build(choseong, joongseong, jongseong):
    """초성, 중성, 종성을 조합하여 완성형 한 글자를 만듦. 'choseong',
    'joongseong', 'jongseong' are offsets. For example, 'ㄱ' is 0, 'ㄲ' is 1,
    'ㄴ' is 2, and so on and so fourth."""
    code = int(((((choseong) * 21) + joongseong) * 28) + jongseong + 0xAC00)
    return chr(code)


def dooeum(previous, current):
    """두음법칙을 적용하기 위한 함수."""
    p, c = separate(previous), separate(current)
    offset = 0

    current_head = build(c[0], c[1], 0)

    # 모음이나 ㄴ 받침 뒤에 이어지는 '렬, 률'은 '열, 율'로 발음한다.
    if previous.isalnum():
        if current in ("렬", "률") and is_hangul(previous) and p[2] in (0, 2):
            offset = 6
    # 한자음 '녀, 뇨, 뉴, 니', '랴, 려, 례, 료, 류, 리'가 단어 첫머리에 올 때
    # '여, 요, 유, 이', '야, 여, 예, 요, 유, 이'로 발음한다.
    elif current_head in ("녀", "뇨", "뉴", "니"):
        offset = 9
    elif current_head in ("랴", "려", "례", "료", "류", "리"):
        offset = 6
    # 한자음 '라, 래, 로, 뢰, 루, 르'가 단어 첫머리에 올 때 '나, 내, 노, 뇌,
    # 누, 느'로 발음한다.
    elif current_head in ("라", "래", "로", "뢰", "루", "르"):
        offset = -3

    return build(c[0] + offset, c[1], c[2])


def is_hangul(ch):
    return False if ch is None else ord(ch) >= 0xAC00 and ord(ch) <= 0xD7A3


def contains_hangul(text):
    if isinstance(text, str):
        # NOTE: Probably not an ideal solution in terms of performance
        tfs = map(lambda c: is_hangul(c), text)
        for tf in tfs:
            if tf:
                return True
    return False
