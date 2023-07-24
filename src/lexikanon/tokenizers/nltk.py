from typing import Any, List, Optional, Tuple

from pydantic import BaseModel, model_validator

from lexikanon import HyFI
from lexikanon.tokenizers.base import Tokenizer

logger = HyFI.getLogger(__name__)


class NLTKTagger(BaseModel):
    """
    lemmatize: false
    stem: true
    lemmatizer:
        _target_: nltk.stem.WordNetLemmatizer
    stemmer:
        _target_: nltk.stem.PorterStemmer
    """

    lemmatize: bool = False
    stem: bool = True
    lemmatizer: Optional[dict] = None
    stemmer: Optional[dict] = None
    verbose: bool = False

    _lemmatizer: Any = None
    _stemmer: Any = None

    @model_validator(mode="after")
    def validate_nltk(self) -> "NLTKTagger":
        import nltk as NLTK

        NLTK.download("punkt", quiet=True)
        NLTK.download("averaged_perceptron_tagger", quiet=True)
        NLTK.download("wordnet", quiet=True)
        NLTK.download("omw-1.4", quiet=True)

        if self.lemmatizer and HyFI.is_instantiatable(self.lemmatizer):
            logger.info("instantiating %s...", self.lemmatizer["_target_"])
            self._lemmatizer = HyFI.instantiate(self.lemmatizer)
        if self.stemmer and HyFI.is_instantiatable(self.stemmer):
            logger.info("instantiating %s...", self.stemmer["_target_"])
            self._stemmer = HyFI.instantiate(self.stemmer)
        self.lemmatize = self.lemmatize and self._lemmatizer is not None
        self.stem = self.stem and self._stemmer is not None

        return self

    def _parse(self, text: str) -> List[Tuple[str, str]]:
        import nltk

        tokens: List[tuple] = nltk.pos_tag(nltk.word_tokenize(text))
        return tokens

    def _lemmatize(self, token_pos: Tuple[str, str]) -> Tuple[str, str]:
        if self._lemmatizer is None:
            return token_pos
        return (
            self._lemmatizer.lemmatize(
                token_pos[0], self._get_wordnet_pos(token_pos[1])
            ),
            token_pos[1],
        )

    def _stem(self, token_pos: Tuple[str, str]) -> Tuple[str, str]:
        if self.stemmer is None:
            return token_pos
        return (self._stemmer.stem(token_pos[0]), token_pos[1])

    @staticmethod
    def _get_wordnet_pos(tag: str) -> str:
        from nltk.corpus import wordnet

        """Map POS tag to first character lemmatize() accepts"""
        tag = tag[0].upper()
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }

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
