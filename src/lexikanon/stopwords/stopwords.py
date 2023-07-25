from typing import Callable, List, Optional, Union

from pydantic import BaseModel, model_validator

from lexikanon import HyFI

logger = HyFI.getLogger(__name__)


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

    name: str = "stopwords"
    lowercase: bool = False
    stopwords_fn: Optional[Union[str, Callable[[str], bool]]] = None
    stopwords_list: Optional[List[str]] = None
    stopwords_path: Optional[str] = None
    nltk_stopwords_lang: Optional[str] = None
    verbose: bool = False

    _stopwords_fn: Optional[Callable] = None

    @model_validator(mode="after")
    def validate_stopwords(self) -> "Stopwords":
        if self.stopwords_path:
            self._stopwords_list = HyFI.load_wordlist(
                self.stopwords_path, lowercase=self.lowercase, verbose=self.verbose
            )
            if self.verbose:
                logger.info(
                    "Loaded %d stopwords from %s",
                    len(self._stopwords_list),
                    self.stopwords_path,
                )
        else:
            self._stopwords_list = []

        if callable(self.stopwords_fn):
            self._stopwords_fn = self.stopwords_fn
        elif isinstance(self.stopwords_fn, str):
            self._stopwords_fn = eval(self.stopwords_fn)

        if self.verbose:
            logger.info("Using custom stopwords function %s", self._stopwords_fn)

        if self.stopwords_list:
            if self.lowercase:
                self.stopwords_list = [w.lower() for w in self.stopwords_list]
            self._stopwords_list += self.stopwords_list

        if self.nltk_stopwords_lang:
            self._stopwords_list += self._load_nltk_stopwords(self.nltk_stopwords_lang)
        if self.verbose:
            logger.info("Loaded %d stopwords", len(self._stopwords_list))
        return self

    def __call__(self, word: str) -> bool:
        """Calling a stopwords instance like a function just calls the is_stopword method."""
        return self.is_stopword(word)

    def is_stopword(self, word: str) -> bool:
        """
        :type word: str
        :returns: bool
        """
        _word = word.lower() if self.lowercase else word
        if self._stopwords_fn:
            return self._stopwords_fn(_word) or (_word in self._stopwords_list)
        else:
            return _word in self._stopwords_list

    def _load_nltk_stopwords(self, language: str = "english") -> List[str]:
        """
        :type language: str
        :returns: list
        """
        import nltk
        from nltk.corpus import stopwords

        nltk.download("stopwords", quiet=True)
        if language in stopwords.fileids():
            logger.info("Loaded NLTK stopwords for %s", language)
            return stopwords.words(language)

        logger.warning("No NLTK stopwords for %s", language)
        return []

    def __iter__(self):
        return iter(self._stopwords_list)

    def __len__(self):
        return len(self._stopwords_list)

    def __contains__(self, word):
        return self.is_stopword(word)

    def __getitem__(self, word):
        return self.is_stopword(word)

    def __repr__(self):
        return f"<Stopwords {len(self._stopwords_list)} stopwords>"

    def __str__(self):
        return f"<Stopwords {len(self._stopwords_list)} stopwords>"

    def __bool__(self):
        return bool(self._stopwords_list)

    def __eq__(self, other):
        return self._stopwords_list == other._stopwords_list

    def __ne__(self, other):
        return self._stopwords_list != other._stopwords_list

    def __lt__(self, other):
        return len(self._stopwords_list) < len(other._stopwords_list)

    def __le__(self, other):
        return len(self._stopwords_list) <= len(other._stopwords_list)

    def __gt__(self, other):
        return len(self._stopwords_list) > len(other._stopwords_list)

    def __ge__(self, other):
        return len(self._stopwords_list) >= len(other._stopwords_list)

    def __add__(self, other):
        return Stopwords(stopwords_list=self._stopwords_list + other._stopwords_list)

    def __sub__(self, other):
        return Stopwords(
            stopwords_list=[
                w for w in self._stopwords_list if w not in other._stopwords_list
            ]
        )

    def __and__(self, other):
        return Stopwords(
            stopwords_list=[
                w for w in self._stopwords_list if w in other._stopwords_list
            ]
        )

    def __or__(self, other):
        return Stopwords(
            stopwords_list=self._stopwords_list
            + [w for w in other._stopwords_list if w not in self._stopwords_list]
        )

    def __xor__(self, other):
        return Stopwords(
            stopwords_list=[
                w for w in self._stopwords_list if w not in other._stopwords_list
            ]
            + [w for w in other._stopwords_list if w not in self._stopwords_list]
        )
