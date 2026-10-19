import importlib
import logging
from typing import Any

from pydantic import Field, model_validator

from lexikanon._base import Model
from lexikanon.tokenizers.base import Tokenizer

logger = logging.getLogger(__name__)

# word_tokenize and pos_tag need the *_tab / *_eng resources on nltk>=3.9.
NLTK_RESOURCES = [
    "punkt_tab",
    "averaged_perceptron_tagger_eng",
    "universal_tagset",
    "wordnet",
    "omw-1.4",
]


def _build(spec: Any) -> Any:
    """Call the ``_target_`` of a ``{"_target_": "pkg.Class", **kwargs}`` dict.

    Anything else is returned as is: HyFI/Hydra configs arrive already instantiated.
    """
    if not (isinstance(spec, dict) and isinstance(spec.get("_target_"), str)):
        return spec
    kwargs = {k: v for k, v in spec.items() if k != "_target_"}
    module, _, name = spec["_target_"].rpartition(".")
    logger.debug("instantiating %s...", spec["_target_"])
    return getattr(importlib.import_module(module), name)(**kwargs)


class NLTKTagger(Model):
    """
    lemmatize: false
    stem: true
    lemmatizer:
        _target_: nltk.stem.WordNetLemmatizer
    stemmer:
        _target_: nltk.stem.PorterStemmer
    """

    tagset: str | None = Field(
        None, description="the tagset to be used, e.g. universal, wsj, brown"
    )
    language: str = Field(
        "english",
        description="the language to be used, e.g. 'english' for English, 'russian' for Russian",
    )
    lemmatize: bool = False
    stem: bool = True
    # A {"_target_": ...} spec or an already built object (HyFI instantiates nested targets).
    lemmatizer: Any | None = Field(
        default_factory=lambda: {"_target_": "nltk.stem.WordNetLemmatizer"}
    )
    stemmer: Any | None = Field(default_factory=lambda: {"_target_": "nltk.stem.PorterStemmer"})
    verbose: bool = False

    _lemmatizer: Any = None
    _stemmer: Any = None

    @model_validator(mode="after")
    def validate_nltk(self) -> "NLTKTagger":
        import nltk as NLTK

        for resource in NLTK_RESOURCES:
            NLTK.download(resource, quiet=True)

        if self.lemmatizer:
            self._lemmatizer = _build(self.lemmatizer)
        if self.stemmer:
            self._stemmer = _build(self.stemmer)
        self.lemmatize = self.lemmatize and self._lemmatizer is not None
        self.stem = self.stem and self._stemmer is not None

        return self

    def _parse(self, text: str) -> list[tuple[str, str]]:
        import nltk

        tokens: list[tuple] = nltk.pos_tag(
            nltk.word_tokenize(text, language=self.language),
            tagset=self.tagset,
            lang=self.language[:3],
        )
        return tokens

    def _lemmatize(self, token_pos: tuple[str, str]) -> tuple[str, str]:
        if self._lemmatizer is None:
            return token_pos
        return (
            self._lemmatizer.lemmatize(
                token_pos[0], self._get_wordnet_pos(token_pos[1], tagset=self.tagset)
            ),
            token_pos[1],
        )

    def _stem(self, token_pos: tuple[str, str]) -> tuple[str, str]:
        if self.stemmer is None:
            return token_pos
        return (self._stemmer.stem(token_pos[0]), token_pos[1])

    @staticmethod
    def _get_wordnet_pos(
        tag: str,
        tagset: str | None = None,
    ) -> str:
        from nltk.corpus import wordnet

        """Map POS tag to first character lemmatize() accepts"""
        if tagset == "universal":
            tag_dict = {
                "ADJ": wordnet.ADJ,
                "NOUN": wordnet.NOUN,
                "VERB": wordnet.VERB,
                "ADV": wordnet.ADV,
            }
        else:
            tag = tag[0].upper()
            tag_dict = {
                "J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV,
            }
        # if there is no match, default to noun (otherwise lemmatize returns None)
        return tag_dict.get(tag, wordnet.NOUN)


class NLTKTokenizer(Tokenizer):
    tagger: NLTKTagger = NLTKTagger()

    def parse(self, text: str) -> list[tuple[str, str]]:
        token_tuples = self.tagger._parse(text)
        tokens = []
        for token_tuple in token_tuples:
            if self.tagger.lemmatize:
                token_tuple = self.tagger._lemmatize(token_tuple)
            if self.tagger.stem:
                token_tuple = self.tagger._stem(token_tuple)
            tokens.append(self.to_token(token_tuple))
        # "term/POS" strings, not tuples; Tokenizer.to_token passes strings through.
        return tokens  # type: ignore[return-value]
