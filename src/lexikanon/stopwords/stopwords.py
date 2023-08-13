import logging
from typing import Callable, List, Optional, Union

from hyfi.composer import BaseModel

from lexikanon import HyFI

logger = logging.getLogger(__name__)


class Stopwords(BaseModel):
    """
    name: stopwords
    lowercase: true
    stopwords_fn:
    stopwords_list:
    stopwords_path:
    nltk_stopwords_lang:
    verbose: False
    """

    _config_group_: str = "/stopwords"
    _config_name_: str = "__init__"

    name: str = "stopwords"
    lowercase: bool = False
    stopwords_fn: Optional[Union[str, Callable[[str], bool]]] = None
    stopwords_list: Optional[List[str]] = None
    stopwords_path: Optional[str] = None
    nltk_stopwords_lang: Optional[str] = None
    verbose: bool = False

    _loaded_: bool = False
    _stopwords_: List[str] = []

    @property
    def func(self) -> Optional[Callable]:
        if callable(self.stopwords_fn):
            return self.stopwords_fn
        elif isinstance(self.stopwords_fn, str):
            return eval(self.stopwords_fn)

    @property
    def stopwords(self) -> List[str]:
        if self._loaded_:
            return self._stopwords_
        self.load_stopwords()
        return self._stopwords_

    def load_stopwords(self):
        """Load stopwords from file or function"""
        if self.stopwords_path:
            self._stopwords_ = HyFI.load_wordlist(
                self.stopwords_path, lowercase=self.lowercase, verbose=self.verbose
            )
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

    def _load_nltk_stopwords(self, language: str = "english") -> List[str]:
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
        return self.stopwords == other._stopwords_list

    def __ne__(self, other):
        return self.stopwords != other._stopwords_list

    def __lt__(self, other):
        return len(self.stopwords) < len(other._stopwords_list)

    def __le__(self, other):
        return len(self.stopwords) <= len(other._stopwords_list)

    def __gt__(self, other):
        return len(self.stopwords) > len(other._stopwords_list)

    def __ge__(self, other):
        return len(self.stopwords) >= len(other._stopwords_list)

    def __add__(self, other):
        return Stopwords(stopwords_list=self.stopwords + other._stopwords_list)

    def __sub__(self, other):
        return Stopwords(
            stopwords_list=[w for w in self.stopwords if w not in other._stopwords_list]
        )

    def __and__(self, other):
        return Stopwords(
            stopwords_list=[w for w in self.stopwords if w in other._stopwords_list]
        )

    def __or__(self, other):
        return Stopwords(
            stopwords_list=self.stopwords
            + [w for w in other._stopwords_list if w not in self.stopwords]
        )

    def __xor__(self, other):
        return Stopwords(
            stopwords_list=[w for w in self.stopwords if w not in other._stopwords_list]
            + [w for w in other._stopwords_list if w not in self.stopwords]
        )
