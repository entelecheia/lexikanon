import itertools
import re
import unicodedata
from typing import Optional, Set

from lexikanon import HyFI

from .hangle import compose, decompose
from .hanja import translate as hanja2hangle

logger = HyFI.getLogger(__name__)


doublespace_pattern = re.compile(r"\s+")
repeatchars_pattern = re.compile(r"(\w)\\1{2,}")
number_pattern = re.compile(r"[0-9]")
punctuation_pattern = re.compile(r"[,\.\?\!]")
symbol_pattern = re.compile(r"[()\[\]\{\}`]")
hangle_pattern = re.compile(r"[ㄱ-ㅎㅏ-ㅣ가-힣]")
alphabet_pattern = re.compile(r"[a-zA-Z]")

hangle_filter = re.compile(r"[^ㄱ-ㅎㅏ-ㅣ가-힣]")
hangle_number_filter = re.compile(r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9]")
text_filter = re.compile(r"[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9,\.\?\!&·\"'\(\)\[\]\{\}+\-\\\/\*×%]")
# text_filter = re.compile(r'[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9,\.\?\!&·\"\'-()\[\]\{\}]')
text_filter_for_lrgraph = re.compile(r"[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9,\.\?\!&\"'-()\[\]\{\}]")


#: Control characters.
CONTROLS = {
    "\u0001",
    "\u0002",
    "\u0003",
    "\u0004",
    "\u0005",
    "\u0006",
    "\u0007",
    "\u0008",
    "\u000e",
    "\u000f",
    "\u0011",
    "\u0012",
    "\u0013",
    "\u0014",
    "\u0015",
    "\u0016",
    "\u0017",
    "\u0018",
    "\u0019",
    "\u001a",
    "\u001b",
}
# There are further control characters, but they are instead replaced with a space by unicode normalization
# '\u0009', '\u000a', '\u000b', '\u000c', '\u000d', '\u001c',  '\u001d', '\u001e', '\u001f'


#: Hyphen and dash characters.
HYPHENS = {
    "-",  # \u002d Hyphen-minus
    "‐",  # \u2010 Hyphen
    "‑",  # \u2011 Non-breaking hyphen
    "⁃",  # \u2043 Hyphen bullet
    "‒",  # \u2012 figure dash
    "–",  # \u2013 en dash
    "—",  # \u2014 em dash
    "―",  # \u2015 horizontal bar
}

#: Minus characters.
MINUSES = {
    "-",  # \u002d Hyphen-minus
    "−",  # \u2212 Minus
    "－",  # \uff0d Full-width Hyphen-minus
    "⁻",  # \u207b Superscript minus
}

#: Plus characters.
PLUSES = {
    "+",  # \u002b Plus
    "＋",  # \uff0b Full-width Plus
    "⁺",  # \u207a Superscript plus
}

#: Slash characters.
SLASHES = {
    "/",  # \u002f Solidus
    "⁄",  # \u2044 Fraction slash
    "∕",  # \u2215 Division slash
}

#: Tilde characters.
TILDES = {
    "~",  # \u007e Tilde
    "˜",  # \u02dc Small tilde
    "⁓",  # \u2053 Swung dash
    "∼",  # \u223c Tilde operator
    "∽",  # \u223d Reversed tilde
    "∿",  # \u223f Sine wave
    "〜",  # \u301c Wave dash
    "～",  # \uff5e Full-width tilde
}

#: Apostrophe characters.
APOSTROPHES = {
    "'",  # \u0027
    "’",  # \u2019
    "՚",  # \u055a
    "Ꞌ",  # \ua78b
    "ꞌ",  # \ua78c
    "＇",  # \uff07
}

#: Single quote characters.
SINGLE_QUOTES = {
    "'",  # \u0027
    "‘",  # \u2018
    "’",  # \u2019
    "‚",  # \u201a
    "‛",  # \u201b
}

#: Double quote characters.
DOUBLE_QUOTES = {
    '"',  # \u0022
    "“",  # \u201c
    "”",  # \u201d
    "„",  # \u201e
    "‟",  # \u201f
}

#: Accent characters.
ACCENTS = {
    "`",  # \u0060
    "´",  # \u00b4
}

#: Prime characters.
PRIMES = {
    "′",  # \u2032
    "″",  # \u2033
    "‴",  # \u2034
    "‵",  # \u2035
    "‶",  # \u2036
    "‷",  # \u2037
    "⁗",  # \u2057
}

#: Quote characters, including apostrophes, single quotes, double quotes, accents and primes.
QUOTES = APOSTROPHES | SINGLE_QUOTES | DOUBLE_QUOTES | ACCENTS | PRIMES

#: Uppercase and lowercase greek letters.
GREEK = {
    "Α",  # \u0391
    "Β",  # \u0392
    "Γ",  # \u0393
    "Δ",  # \u0394
    "Ε",  # \u0395
    "Ζ",  # \u0396
    "Η",  # \u0397
    "Θ",  # \u0398
    "Ι",  # \u0399
    "Κ",  # \u039a
    "Λ",  # \u039b
    "Μ",  # \u039c
    "Ν",  # \u039d
    "Ξ",  # \u039e
    "Ο",  # \u039f
    "Π",  # \u03a0
    "Ρ",  # \u03a1
    "Σ",  # \u03a3
    "Τ",  # \u03a4
    "Υ",  # \u03a5
    "Φ",  # \u03a6
    "Χ",  # \u03a7
    "Ψ",  # \u03a8
    "Ω",  # \u03a9
    "α",  # \u03b1
    "β",  # \u03b2
    "γ",  # \u03b3
    "δ",  # \u03b4
    "ε",  # \u03b5
    "ζ",  # \u03b6
    "η",  # \u03b7
    "θ",  # \u03b8
    "ι",  # \u03b9
    "κ",  # \u03ba
    "λ",  # \u03bb
    "μ",  # \u03bc
    "ν",  # \u03bd
    "ξ",  # \u03be
    "ο",  # \u03bf
    "π",  # \u03c0
    "ρ",  # \u03c1
    "σ",  # \u03c3
    "τ",  # \u03c4
    "υ",  # \u03c5
    "φ",  # \u03c6
    "χ",  # \u03c7
    "ψ",  # \u03c8
    "ω",  # \u03c9
}

#: Names of greek letters spelled out as words.
GREEK_WORDS = {
    "Alpha",
    "Beta",
    "Gamma",
    "Delta",
    "Epsilon",
    "Zeta",
    "Eta",
    "Theta",
    "Iota",
    "Kappa",
    "Lambda",
    "Mu",
    "Nu",
    "Xi",
    "Omicron",
    "Pi",
    "Rho",
    "Sigma",
    "Tau",
    "Upsilon",
    "Phi",
    "Chi",
    "Psi",
    "Omega",
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "eta",
    "theta",
    "iota",
    "kappa",
    "lamda",
    "mu",
    "nu",
    "xi",
    "omicron",
    "pi",
    "rho",
    "sigma",
    "tau",
    "upsilon",
    "phi",
    "chi",
    "psi",
    "omega",
}

#: Words that should not be capitalized in titles.
SMALL = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "but",
    "by",
    "en",
    "for",
    "if",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "v",
    "via",
    "vs",
}

#: Words that should not be capitalized in names.
NAME_SMALL = {
    "abu",
    "bon",
    "bin",
    "da",
    "dal",
    "del",
    "der",
    "de",
    "di",
    "dí",
    "ibn",
    "la",
    "le",
    "san",
    "st",
    "ste",
    "van",
    "vel",
    "von",
    "y",
}

# This isn't every possible TLD, just the most common, to avoid false positives.
TLDS = {
    "aero",
    "asia",
    "biz",
    "cat",
    "com",
    "coop",
    "edu",
    "eu",
    "gov",
    "info",
    "int",
    "jobs",
    "mil",
    "mobi",
    "museum",
    "name",
    "net",
    "org",
    "pro",
    "tel",
    "travel",
    "xxx",
    "ad",
    "as",
    "ar",
    "au",
    "br",
    "bz",
    "ca",
    "cc",
    "cd",
    "co",
    "ch",
    "cn",
    "de",
    "dj",
    "es",
    "fr",
    "fm",
    "it",
    "io",
    "jp",
    "la",
    "ly",
    "me",
    "ms",
    "nl",
    "no",
    "nu",
    "ru",
    "sc",
    "se",
    "sr",
    "su",
    "tk",
    "tv",
    "uk",
    "us",
    "ws",
}

#: A variety of numbers, spelled out as words.
NUMBERS = {
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
    "hundred",
    "thousand",
    "million",
    "billion",
    "trillion",
}
LEFT_PARENTHESES = {"(", "[", "{", "&lt;"}
RIGHT_PARENTHESES = {")", "]", "}", "&gt;"}
#: Regular expression that matches email addresses.
EMAIL_RE = re.compile(r"([\w\-\.\+%]+@(\w[\w\-]+\.)+[\w\-]+)", re.I | re.U)
#: Regular expression that matches DOIs.
DOI_RE = re.compile(r"^10\.\d{4,9}/[-\._;()/:A-Z0-9]+$", re.U)
#: Regular expression that matches ISSNs.
ISSN_RE = re.compile(r"^\d{4}-\d{3}[\dX]$", re.U)
#: Regular expression that matches control characters not allowed in XML.
CONTROL_RE = re.compile(
    "[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+"
)


def levenshtein(s1: str, s2: str, allow_substring: bool = False) -> int:
    """Return the Levenshtein distance between two strings.
    The Levenshtein distance (a.k.a "edit difference") is the number of characters that need to be substituted,
    inserted or deleted to transform s1 into s2.
    Setting the `allow_substring` parameter to True allows s1 to be a
    substring of s2, so that, for example, "hello" and "hello there" would have a distance of zero.
    :param string s1: The first string
    :param string s2: The second string
    :param bool allow_substring: Whether to allow s1 to be a substring of s2
    :returns: Levenshtein distance.
    :rtype int
    """
    len1, len2 = len(s1), len(s2)
    lev = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        lev[i][0] = i
    for j in range(len2 + 1):
        lev[0][j] = 0 if allow_substring else j
    for i, j in itertools.product(range(len1), range(len2)):
        lev[i + 1][j + 1] = min(
            lev[i][j + 1] + 1, lev[i + 1][j] + 1, lev[i][j] + (s1[i] != s2[j])
        )
    return min(lev[len1]) if allow_substring else lev[len1][len2]


def bracket_level(
    text: str, _open: Optional[Set[str]] = None, _close: Optional[Set[str]] = None
) -> int:
    """Return 0 if string contains balanced brackets or no brackets."""
    if _open is None:
        _open = {"(", "[", "{"}
    if _close is None:
        _close = {")", "]", "}"}
    level = 0
    for c in text:
        if c in _open:
            level += 1
        elif c in _close:
            level -= 1
    return level


def is_punct(text: str) -> bool:
    return all(unicodedata.category(char).startswith("P") for char in text)


def is_ascii(text: str) -> bool:
    return all(ord(char) < 128 for char in text)


def like_url(text: str) -> bool:
    if not text:
        return False
    if text.startswith("http://"):
        return True
    elif text.startswith("www.") and len(text) >= 5:
        return True
    if len(text) < 2 or text[0] == "." or text[-1] == "." or "." not in text:
        return False
    tld = text.rsplit(".", 1)[1].split(":", 1)[0]
    return True if tld.endswith("/") else bool(tld.isalpha() and tld in TLDS)


def like_number(text: str) -> bool:
    text = text.replace(",", "").replace(".", "")
    if text.isdigit():
        return True
    if text.count("/") == 1:
        num, denom = text.split("/")
        if like_number(num) and like_number(denom):
            return True
    return text in NUMBERS


def word_shape(text: str) -> str:
    prev_m = ""
    seq = 0
    shape = []
    for c in text:
        if c.isdigit():
            m = "d"  # Digits
        elif c in GREEK:
            m = "g"  # Greek letters
        elif c.isalpha():
            m = "X" if c.isupper() else "x"  # Uppercase or lowercase alphabetical
        elif c in QUOTES:
            m = "'"  # Quotes and apostrophes
        elif c in {":", ";"}:
            m = ":"  # Colons and semicolons
        elif c in {"!", "?", "."}:
            m = "."  # Sentence ends
        elif c in {"(", "[", "{", ")", "]", "}"}:
            m = "b"  # Brackets
        elif c in {"°", "%"}:
            m = "u"  # units
        elif c in {"■", "◼", "●", "▲", "○", "◆", "▼", "⧫", "△", "◇", "▽", "⬚", "□"}:
            m = "l"  # list markers
        elif c in {",", "$", "&", "-"}:
            m = c  # Stay the same
        else:
            m = "*"
            # Everything else, symbols etc:
            # {'=', '+', '*', '_', '|', '@', '×', '÷', '±', '<', '≤', '>', '≥', '≦', '≡', '≅', '≈', '≃', '≲',
            # '→', '←', '⇄', '≪', '≫', '↔', '≠', '∝', '∈', '⇌', '⇋', '⋯', '~', '·', '•', '√', '⊃', '∑', '∏',
            # '®', '∞', '∂', '∫', '∇', '∧', '⟨', '⟩'}
        if m == prev_m:
            seq += 1
        else:
            seq = 0
            prev_m = m
        if seq < 3:
            shape.append(m)
    return "".join(shape)


def remove_doublespace(sent: str) -> str:
    return doublespace_pattern.sub(" ", sent)


def repeat_normalize(sent: str, num_repeats: int = 2) -> str:
    if num_repeats > 0:
        sent = repeatchars_pattern.sub("\\1" * num_repeats, sent)
    sent = doublespace_pattern.sub(" ", sent)
    return sent.strip()


def emoticon_normalize(sent: str, num_repeats: int = 2) -> str:
    if not sent:
        return sent

    # Pattern matching ㅋ쿠ㅜ
    def pattern(idx):
        # Jaum: 0, Moum: 1, Complete: 2, else -1
        if 12593 <= idx <= 12622:
            return 0
        elif 12623 <= idx <= 12643:
            return 1
        elif 44032 <= idx <= 55203:
            return 2
        else:
            return -1

    idxs = [pattern(ord(c)) for c in sent]
    sent_ = []
    last_idx = len(idxs) - 1
    for i, (idx, c) in enumerate(zip(idxs, sent)):
        if (i > 0 and i < last_idx) and (
            idxs[i - 1] == 0 and idx == 2 and idxs[i + 1] == 1
        ):
            cho, jung, jong = decompose(c)
            if (cho == sent[i - 1]) and (jung == sent[i + 1]) and (jong == " "):
                sent_.append(cho)
                sent_.append(jung)
            else:
                sent_.append(c)
        elif (i < last_idx) and (idx == 2) and (idxs[i + 1] == 0):
            cho, jung, jong = decompose(c)
            if jong == sent[i + 1]:
                sent_.append(compose(cho, jung, " "))
                sent_.append(jong)
        elif (i > 0) and (idx == 2 and idxs[i - 1] == 0):
            cho, jung, jong = decompose(c)
            if cho == sent[i - 1]:
                sent_.append(cho)
                sent_.append(jung)
        else:
            sent_.append(c)
    return repeat_normalize("".join(sent_), num_repeats)


def hanja_to_hangle(sent: str) -> str:
    return hanja2hangle(sent, "substitution")


def only_hangle(sent: str) -> str:
    sent = hanja_to_hangle(sent)
    return doublespace_pattern.sub(" ", hangle_filter.sub(" ", sent)).strip()


def only_hangle_number(sent: str) -> str:
    sent = hanja_to_hangle(sent)
    return doublespace_pattern.sub(" ", hangle_number_filter.sub(" ", sent)).strip()


def only_text(sent: str) -> str:
    sent = hanja_to_hangle(sent)
    return doublespace_pattern.sub(" ", text_filter.sub(" ", sent)).strip()


def remain_hangle_on_last(eojeol: str) -> str:
    matchs = list(hangle_pattern.finditer(eojeol))
    if not matchs:
        return ""
    last_index = matchs[-1].span()[1]
    return eojeol[:last_index].strip()


def normalize_sent_for_lrgraph(sent: str) -> str:
    sent = hanja_to_hangle(sent)
    sent = text_filter_for_lrgraph.sub(" ", sent)
    sent = symbol_pattern.sub(" ", sent)
    sent_ = [remain_hangle_on_last(eojeol) for eojeol in sent.split()]
    sent_ = [eojeol for eojeol in sent_ if eojeol]
    return " ".join(sent_) if sent_ else ""
