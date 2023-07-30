from typing import List, Optional, Tuple

from hyfi.composer import BaseModel

from lexikanon import HyFI
from lexikanon.tokenizers.base import Tokenizer

logger = HyFI.getLogger(__name__)


class MecabTagger(BaseModel):
    """
    userdic_path:
    backend: ekonlpy
    verbose: false
    """

    _config_group_: str = "tokenizers/tagger"
    _config_name_: str = "mecab"

    userdic_path: Optional[str] = None
    backend: str = "ekonlpy"
    verbose: bool = False

    def _parse(self, text: str) -> List[Tuple[str, str]]:
        from ekonlpy import Mecab

        mecab = Mecab()
        return mecab.pos(text)


class MecabTokenizer(Tokenizer):
    tagger: MecabTagger = MecabTagger()
    flatten: bool = True

    def parse(self, text: str) -> List[Tuple[str, str]]:
        return self.tagger._parse(text)
