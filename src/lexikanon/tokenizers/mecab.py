import logging

from lexikanon._base import Model
from lexikanon.tokenizers.base import Tokenizer

logger = logging.getLogger(__name__)


class MecabTagger(Model):
    """
    userdic_path:
    backend: ekonlpy
    verbose: false
    """

    userdic_path: str | None = None
    backend: str = "ekonlpy"
    verbose: bool = False

    def _parse(self, text: str) -> list[tuple[str, str]]:
        from ekonlpy import Mecab

        mecab = Mecab()
        return mecab.pos(text)


class MecabTokenizer(Tokenizer):
    tagger: MecabTagger = MecabTagger()
    flatten: bool = True

    def parse(self, text: str) -> list[tuple[str, str]]:
        return self.tagger._parse(text)
