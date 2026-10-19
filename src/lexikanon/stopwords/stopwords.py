import logging
from collections.abc import Callable
from pathlib import Path

from pydantic import PrivateAttr, field_validator

from lexikanon._base import Model

logger = logging.getLogger(__name__)


def _load_wordlist(filepath: str, lowercase: bool = False) -> list[str]:
    """First word of each non-empty line, without ``#`` comments, deduplicated and sorted.

    Same result as ``HyFI.load_wordlist`` in 1.x with its default arguments.
    """
    path = Path(filepath)
    if not path.is_file():
        logger.warning("File not found: %s", path)
        return []
    with path.open(encoding="utf-8") as f:
        words = [line.split()[0] for line in f if line.strip()]
    words = [w.lower() if lowercase else w for w in words if not w.startswith("#")]
    return sorted(set(words))


class Stopwords(Model):
    """
    name: stopwords
    lowercase: true
    stopwords_fn:
    stopwords_list:
    stopwords_path:
    nltk_stopwords_lang:
    verbose: False
    """

    name: str = "stopwords"
    lowercase: bool = False
    stopwords_fn: Callable[[str], bool] | None = None
    stopwords_list: list[str] | None = None
    stopwords_path: str | None = None
    nltk_stopwords_lang: str | None = None
    verbose: bool = False

    _loaded_: bool = False
    _stopwords_: list[str] = PrivateAttr(default_factory=list)

    @field_validator("stopwords_fn", mode="before")
    @classmethod
    def _no_source_strings(cls, value: object) -> object:
        # 0.x eval'd this string, which let a config run code outside HyFI's allowlist.
        if isinstance(value, str):
            raise ValueError(
                "stopwords_fn no longer evaluates Python source; pass a callable, or in a HyFI "
                "config use {_target_: mypkg.is_stopword, _partial_: true}"
            )
        return value

    @property
    def func(self) -> Callable | None:
        return self.stopwords_fn

    @property
    def stopwords(self) -> list[str]:
        if self._loaded_:
            return self._stopwords_
        self.load_stopwords()
        return self._stopwords_

    def load_stopwords(self):
        """Load stopwords from file or function"""
        if self.stopwords_path:
            self._stopwords_ = _load_wordlist(self.stopwords_path, lowercase=self.lowercase)
            if self.verbose:
                logger.info(
                    "Loaded %d stopwords from %s",
                    len(self._stopwords_),
                    self.stopwords_path,
                )
        else:
            self._stopwords_ = []

        if self.stopwords_list:
            if self.lowercase:
                self.stopwords_list = [w.lower() for w in self.stopwords_list]
            self._stopwords_ += self.stopwords_list

        if self.nltk_stopwords_lang:
            self._stopwords_ += self._load_nltk_stopwords(self.nltk_stopwords_lang)
        if self.verbose:
            logger.info("Loaded %d stopwords", len(self._stopwords_))
        self._loaded_ = True

    def __call__(self, word: str) -> bool:
        """Calling a stopwords instance like a function just calls the is_stopword method."""
        return self.is_stopword(word)

    def is_stopword(self, word: str) -> bool:
        """
        :type word: str
        :returns: bool
        """
        _word = word.lower() if self.lowercase else word
        if self.func:
            return self.func(_word) or (_word in self.stopwords)
        else:
            return _word in self.stopwords

    def _load_nltk_stopwords(self, language: str = "english") -> list[str]:
        """
        :type language: str
        :returns: list
        """
        import nltk
        from nltk.corpus import stopwords

        nltk.download("stopwords", quiet=True)
        if language in stopwords.fileids():
            if self.verbose:
                logger.info("Loaded NLTK stopwords for %s", language)
            return stopwords.words(language)

        logger.warning("No NLTK stopwords for %s", language)
        return []

    def __iter__(self):
        return iter(self.stopwords)

    def __len__(self):
        return len(self.stopwords)

    def __contains__(self, word):
        return self.is_stopword(word)

    def __getitem__(self, word):
        return self.is_stopword(word)

    def __repr__(self):
        return f"<Stopwords {len(self.stopwords)} stopwords>"

    def __str__(self):
        return f"<Stopwords {len(self.stopwords)} stopwords>"

    def __bool__(self):
        return bool(self.stopwords)

    def __eq__(self, other):
        if not isinstance(other, Stopwords):
            return NotImplemented
        return self.stopwords == other.stopwords

    def __ne__(self, other):
        if not isinstance(other, Stopwords):
            return NotImplemented
        return self.stopwords != other.stopwords

    def __lt__(self, other):
        return len(self.stopwords) < len(other.stopwords)

    def __le__(self, other):
        return len(self.stopwords) <= len(other.stopwords)

    def __gt__(self, other):
        return len(self.stopwords) > len(other.stopwords)

    def __ge__(self, other):
        return len(self.stopwords) >= len(other.stopwords)

    def __add__(self, other):
        return Stopwords(stopwords_list=self.stopwords + other.stopwords)

    def __sub__(self, other):
        return Stopwords(stopwords_list=[w for w in self.stopwords if w not in other.stopwords])

    def __and__(self, other):
        return Stopwords(stopwords_list=[w for w in self.stopwords if w in other.stopwords])

    def __or__(self, other):
        return Stopwords(
            stopwords_list=self.stopwords + [w for w in other.stopwords if w not in self.stopwords]
        )

    def __xor__(self, other):
        return Stopwords(
            stopwords_list=[w for w in self.stopwords if w not in other.stopwords]
            + [w for w in other.stopwords if w not in self.stopwords]
        )
