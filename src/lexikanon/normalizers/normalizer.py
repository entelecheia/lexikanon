import re
from typing import Optional

from ftfy import TextFixerConfig, fix_text
from hyfi.composer.base import BaseConfig
from pydantic import BaseModel

from lexikanon import HyFI
from lexikanon.utils import (
    ACCENTS,
    APOSTROPHES,
    CONTROLS,
    DOUBLE_QUOTES,
    HYPHENS,
    LEFT_PARENTHESES,
    MINUSES,
    QUOTES,
    RIGHT_PARENTHESES,
    SINGLE_QUOTES,
    SLASHES,
    TILDES,
    emoticon_normalize,
    hanja_to_hangle,
)

logger = HyFI.getLogger(__name__)


class FyfyConfig(BaseModel):
    """
    unescape_html: true
    remove_terminal_escapes: true
    fix_encoding: true
    restore_byte_a0: true
    replace_lossy_sequences: true
    decode_inconsistent_utf8: true
    fix_c1_controls: true
    fix_latin_ligatures: true
    fix_character_width: true
    uncurl_quotes: true
    fix_line_breaks: true
    fix_surrogates: true
    remove_control_chars: true
    normalization: NFKC
    max_decode_length: 1000000
    """

    unescape_html: bool = True
    remove_terminal_escapes: bool = True
    fix_encoding: bool = True
    restore_byte_a0: bool = True
    replace_lossy_sequences: bool = True
    decode_inconsistent_utf8: bool = True
    fix_c1_controls: bool = True
    fix_latin_ligatures: bool = True
    fix_character_width: bool = True
    uncurl_quotes: bool = True
    fix_line_breaks: bool = True
    fix_surrogates: bool = True
    remove_control_chars: bool = True
    normalization: str = "NFKC"
    max_decode_length: int = 1000000


class SpacesConfig(BaseModel):
    """
    strip: true
    fix_whitespaces: true
    collapse_whitespaces: true
    replace_tabs: true
    num_spaces_for_tab: 4
    """

    strip: bool = True
    fix_whitespaces: bool = True
    collapse_whitespaces: bool = True
    replace_tabs: bool = True
    num_spaces_for_tab: int = 4


class SpecialCharactersConfig(BaseModel):
    """
    fix_hyphens: true
    fix_ellipsis: true
    fix_slashes: true
    fix_tildes: true
    fix_emoticons: false
    single_quotes_only: false
    regular_parentheses_only: false
    """

    fix_hyphens: bool = True
    fix_ellipsis: bool = True
    fix_slashes: bool = True
    fix_tildes: bool = True
    fix_emoticons: bool = False
    single_quotes_only: bool = False
    regular_parentheses_only: bool = False


class Normalizer(BaseConfig):
    """Main Normalizer class for generic text.
    Normalize unicode, hyphens, quotes, whitespace.
    By default, the normal form NFKC is used for unicode normalization.
    This applies a compatibility decomposition,
    under which equivalent characters are unified, followed by a canonical composition.
    See Python docs for information
    on normal forms: http://docs.python.org/2/library/unicodedata.html#unicodedata.normalize
    """

    ftfy: FyfyConfig = FyfyConfig()
    spaces: SpacesConfig = SpacesConfig()
    special_characters: SpecialCharactersConfig = SpecialCharactersConfig()
    hanja2hangle: bool = True
    num_repeats: int = 2

    _ftfy_cfg: Optional[TextFixerConfig] = None

    def __call__(self, text: Optional[str]) -> str:
        """Calling a normalizer instance like a function just calls the normalize method."""
        return self.normalize(text)

    def normalize(self, text: Optional[str]) -> str:
        """Run the Normalizer on a string.
        :param text: The string to normalize.
        """
        if text is None:
            return ""
        text = self._fix_text(text)

        # Normalize to canonical unicode (using NFKC by default)
        # if self.form is not None:
        #     text = unicodedata.normalize(self.form, text)

        if self.ftfy.remove_control_chars:
            text = self._remove_control_chars(text)

        # if self.fix_line_breaks:
        #     text = text.replace('\u2028', '\n').replace('\u2029', '\n').replace('\r\n', '\n').replace('\r', '\n')

        if self.special_characters.fix_hyphens:
            text = self._fix_hyphens(text)

        if self.ftfy.uncurl_quotes:
            text = self._uncurl_quotes(text)

        if self.special_characters.fix_ellipsis:
            text = self._fix_ellipsis(text)

        if self.special_characters.fix_slashes:
            text = self._fix_slashes(text)

        if self.special_characters.fix_tildes:
            text = self._fix_tildes(text)

        if self.spaces.replace_tabs:
            repacement_spaces = " " * self.spaces.num_spaces_for_tab
            text = self._replace_tabs(text, replacement_spaces=repacement_spaces)

        if self.spaces.fix_whitespaces:
            text = self._fix_whitespaces(text)

        if self.spaces.collapse_whitespaces:
            text = self._collapse_whitespaces(text)

        if self.spaces.strip and text is not None:
            text = text.strip()

        if self.special_characters.single_quotes_only:
            text = self._single_quotes_only(text)

        if self.special_characters.regular_parentheses_only:
            text = self._regular_parentheses_only(text)

        if self.hanja2hangle:
            text = self._hanja_to_hangle(text)

        if self.special_characters.fix_emoticons and text is not None:
            text = emoticon_normalize(text, num_repeats=self.num_repeats)

        return text or ""

    def _fix_text(self, text: Optional[str]) -> Optional[str]:
        if self._ftfy_cfg is None:
            self._ftfy_cfg = TextFixerConfig(**self.ftfy.model_dump())
        return None if text is None else fix_text(str(text), self._ftfy_cfg)

    def _remove_control_chars(self, text: Optional[str]) -> Optional[str]:
        """
        Strip out any control characters (they occasionally creep in somehow)
        """
        return self._replace_special_characters(text, CONTROLS, "")

    def _fix_hyphens(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize all hyphens, minuses and dashes to ascii hyphen-minus and remove soft hyphen entirely
        """
        # TODO: Better normalization of em/en dashes to '--' if surrounded by spaces or start/end?
        if text is None:
            return None
        for hyphen in HYPHENS | MINUSES:
            text = text.replace(hyphen, "-")
        text = text.replace("\u00ad", "")
        return text

    def _uncurl_quotes(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize all quotes and primes to ascii apostrophe and quotation mark
        """
        if text is None:
            return None
        for double_quote in DOUBLE_QUOTES:
            text = text.replace(double_quote, '"')  # \u0022
        for single_quote in SINGLE_QUOTES | APOSTROPHES | ACCENTS:
            text = text.replace(single_quote, "'")  # \u0027
        text = text.replace("′", "'")  # \u2032 prime
        text = text.replace("‵", "'")  # \u2035 reversed prime
        text = text.replace("″", "''")  # \u2033 double prime
        text = text.replace("‶", "''")  # \u2036 reversed double prime
        text = text.replace("‴", "'''")  # \u2034 triple prime
        text = text.replace("‷", "'''")  # \u2037 reversed triple prime
        text = text.replace("⁗", "''''")  # \u2057 quadruple prime
        return text

    def _fix_ellipsis(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize ellipses to three full stops
        """
        if text is None:
            return None
        text = text.replace("…", "...").replace(" . . . ", " ... ")  # \u2026
        return text

    def _fix_slashes(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize slash characters to ascii slash
        """
        return self._replace_special_characters(text, SLASHES, "/")

    def _fix_tildes(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize tilde characters to ascii tilde
        """
        return self._replace_special_characters(text, TILDES, "~")

    def _replace_tabs(
        self, text: Optional[str], replacement_spaces=" " * 4
    ) -> Optional[str]:
        """
        Replace tabs with spaces
        """
        if text is None:
            return None
        text = text.replace("\t", replacement_spaces)
        return text

    def _fix_whitespaces(self, text: Optional[str]) -> Optional[str]:
        """
        Normalize unusual whitespace not caught by unicodedata
        """
        if text is None:
            return None
        text = text.replace("\u000b", " ").replace("\u000c", " ").replace("\u0085", " ")
        return text

    def _collapse_whitespaces(self, text: Optional[str]) -> Optional[str]:
        """
        Collapse all whitespace to a single space
        """
        if text is None:
            return None

        text = re.sub(r" +", " ", text)
        return text

    def _single_quotes_only(self, text: Optional[str]) -> Optional[str]:
        """
        Replace all double quotes with single quotes
        """
        return self._replace_special_characters(text, QUOTES, "'")

    def _replace_special_characters(
        self, text: Optional[str], special_chars, replacement
    ) -> Optional[str]:
        if text is None:
            return None
        for control in special_chars:
            text = text.replace(control, replacement)
        return text

    # Convert all brackets to regular parentheses
    def _regular_parentheses_only(self, text: Optional[str]) -> Optional[str]:
        """
        Replace all curly brackets with regular parentheses
        """
        if text is None:
            return None
        for ob in LEFT_PARENTHESES:
            text = text.replace(ob, "(")
        for cb in RIGHT_PARENTHESES:
            text = text.replace(cb, ")")
        return text

    def _hanja_to_hangle(self, text: Optional[str]) -> Optional[str]:
        """
        Convert all hanja to hangle
        """
        if text is None:
            return None
        text = hanja_to_hangle(text)
        return text

    def _fix_emoticons(self, text: Optional[str], num_repeats=2) -> Optional[str]:
        """
        Replace emoticons with their text equivalents
        """
        if text is None:
            return None
        text = emoticon_normalize(text, num_repeats=num_repeats)
        return text
