from lexikanon.utils import CONTROL_RE


def test_control_re_keeps_bmp_text_and_drops_controls() -> None:
    # #122 pins the matched set: XML-disallowed controls, surrogates, U+FFFE/FFFF, and every
    # character above the BMP (emoji included) match; Hangul, ASCII, \t \n \r do not.
    text = "금통위는 IMF\t가\n推定\r(−)！"
    assert CONTROL_RE.findall(text) == []
    assert CONTROL_RE.sub("", "a\x00b\x0bc\x1fd￾e😀f\U0010ffff") == "abcdef"
