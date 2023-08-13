import logging
from typing import Any, Dict, List, Optional, Tuple

from hyfi.composer import BaseModel, Field, model_validator

from lexikanon import HyFI
from lexikanon.tokenizers.base import Tokenizer

logger = logging.getLogger(__name__)


class NLTKTagger(BaseModel):
    """
    lemmatize: false
    stem: true
    lemmatizer:
        _target_: nltk.stem.WordNetLemmatizer
    stemmer:
        _target_: nltk.stem.PorterStemmer
    """

    _config_group_: str = "/tokenizer/tagger"
    _config_name_: str = "nltk"

    tagset: Optional[str] = Field(
        None, description="the tagset to be used, e.g. universal, wsj, brown"
    )
    language: str = Field(
        "english",
        description="the language to be used, e.g. 'english' for English, 'russian' for Russian",
    )
    lemmatize: bool = False
    stem: bool = True
    lemmatizer: Optional[Dict] = {"_target_": "nltk.stem.WordNetLemmatizer"}
    stemmer: Optional[Dict] = {"_target_": "nltk.stem.PorterStemmer"}
    verbose: bool = False

    _lemmatizer: Any = None
    _stemmer: Any = None

    @model_validator(mode="after")
    def validate_nltk(self) -> "NLTKTagger":
        import nltk as NLTK

        NLTK.download("punkt", quiet=True)
        NLTK.download("averaged_perceptron_tagger", quiet=True)
        NLTK.download("universal_tagset", quiet=True)
        NLTK.download("wordnet", quiet=True)
        NLTK.download("omw-1.4", quiet=True)

        if self.lemmatizer and HyFI.is_instantiatable(self.lemmatizer):
            logger.debug("instantiating %s...", self.lemmatizer["_target_"])
            self._lemmatizer = HyFI.instantiate(self.lemmatizer)
        if self.stemmer and HyFI.is_instantiatable(self.stemmer):
            logger.debug("instantiating %s...", self.stemmer["_target_"])
            self._stemmer = HyFI.instantiate(self.stemmer)
        self.lemmatize = self.lemmatize and self._lemmatizer is not None
        self.stem = self.stem and self._stemmer is not None

        return self

    def _parse(self, text: str) -> List[Tuple[str, str]]:
        import nltk

        tokens: List[tuple] = nltk.pos_tag(
            nltk.word_tokenize(text, language=self.language),
            tagset=self.tagset,
            lang=self.language[:3],
        )
        return tokens

    def _lemmatize(self, token_pos: Tuple[str, str]) -> Tuple[str, str]:
        if self._lemmatizer is None:
            return token_pos
        return (
            self._lemmatizer.lemmatize(
                token_pos[0], self._get_wordnet_pos(token_pos[1], tagset=self.tagset)
            ),
            token_pos[1],
        )

    def _stem(self, token_pos: Tuple[str, str]) -> Tuple[str, str]:
        if self.stemmer is None:
            return token_pos
        return (self._stemmer.stem(token_pos[0]), token_pos[1])

    @staticmethod
    def _get_wordnet_pos(
        tag: str,
        tagset: Optional[str] = None,
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

    def parse(self, text: str) -> List[Tuple[str, str]]:
        token_tuples = self.tagger._parse(text)
        tokens = []
        for token_tuple in token_tuples:
            if self.tagger.lemmatize:
                token_tuple = self.tagger._lemmatize(token_tuple)
            if self.tagger.stem:
                token_tuple = self.tagger._stem(token_tuple)
            tokens.append(self.to_token(token_tuple))
        return tokens
