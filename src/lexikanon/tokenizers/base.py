import codecs
from typing import Callable, List, Optional, Tuple, Union

from pydantic import BaseModel

from lexikanon import HyFI
from lexikanon.normalizers import Normalizer
from lexikanon.stopwords import Stopwords

logger = HyFI.getLogger(__name__)


class Tokenizer(BaseModel):
    stopwords: Stopwords = Stopwords()
    normalizer: Normalizer = Normalizer()

    lowercase: bool = False
    strip_pos: bool = False
    postag_delim: str = "/"
    postag_length: Optional[int] = None
    include_whitespace_token: bool = True
    tokenize_each_word: bool = False
    sentence_separator: str = "\n"
    userdic_path: Optional[str] = None
    wordpieces_prefix: Optional[str] = "##"
    postags: Optional[List[str]] = None
    noun_postags: Optional[List[str]] = None
    punct_postags: List[str] = ["SF", "SP", "SSO", "SSC", "SY"]
    stop_postags: Optional[List[str]] = None
    verbose: bool = False

    @property
    def sentence_separator_unicode(self) -> str:
        return codecs.decode(self.sentence_separator, "unicode_escape")

    def __call__(self, text: str) -> List[str]:
        """Calling a tokenize config instance like a function just calls the tokenize method."""
        return self.tokenize(text)

    def tokenize(self, text: str) -> List[str]:
        if self.lowercase:
            text = text.lower()
        if self.normalizer and callable(self.normalizer):
            text = self.normalizer(text)
        if len(text) > 0:
            if self.tokenize_each_word:
                term_pos = []
                for word in text.split():
                    term_pos += self.tokenize_word(word)
            else:
                text = " ".join(text.split())
                term_pos = [self.to_token(token) for token in self.parse(text)]
        else:
            term_pos = []
        return term_pos

    def parse(self, text: str) -> List[Tuple[str, str]]:
        return [(token, "") for token in text.split()]

    def to_token(self, term_pos: Union[str, tuple]) -> str:
        if isinstance(term_pos, tuple):
            return _tuple_to_token(
                term_pos,
                self.strip_pos,
                self.postag_delim,
                self.postag_length,
            )
        return term_pos

    def tokenize_word(self, word: str) -> List[str]:
        tokens = self.parse(word)
        tokenized = []
        for i, token_pos in enumerate(tokens):
            term = self.to_token(token_pos)
            if i == 0 or not self.include_whitespace_token:
                tokenized.append(term)
                continue
            pos = token_pos[1]
            prv_pos = tokens[i - 1][1]
            if (
                self.wordpieces_prefix
                and pos not in self.punct_postags
                and prv_pos not in self.punct_postags
            ):
                term = f"{self.wordpieces_prefix}{term}"
            tokenized.append(term)
        return tokenized

    def pos(self, text: str) -> List[Tuple[str, str]]:
        return self.parse(text)

    def tokenize_article(
        self,
        article: Optional[str],
    ) -> List[List[str]]:
        if article is None:
            return []

        tokenized_article = []
        for sent in article.split(self.sentence_separator):
            sent = sent.strip()
            tokens = self.tokenize(sent)
            tokenized_article.append(tokens)
        return tokenized_article

    def nouns(self, text: str) -> List[str]:
        tokens = self.tokenize(text)
        return self.extract(tokens, nouns_only=True)

    def tokens(self, text: str) -> List[str]:
        tokens = self.tokenize(text)
        return self.extract(tokens, nouns_only=False)

    def morphs(self, text: str) -> List[str]:
        return self.tokens(text)

    def extract(
        self,
        text: Union[str, List[str]],
        nouns_only: bool = False,
        postags: Optional[List[str]] = None,
        stop_postags: Optional[List[str]] = None,
        strip_pos: Optional[bool] = None,
        postag_delim: Optional[str] = None,
        postag_length: Optional[int] = None,
    ) -> List[str]:
        if strip_pos is None:
            strip_pos = self.strip_pos
        if stop_postags is None:
            stop_postags = self.stop_postags
        if postags is None:
            postags = self.noun_postags if nouns_only else self.postags
        if postag_delim is None:
            postag_delim = self.postag_delim
        if postag_length is None:
            postag_length = self.postag_length

        return _extract_tokens(
            text,
            postags=postags,
            stop_postags=stop_postags,
            stopwords=self.stopwords,
            strip_pos=strip_pos,
            postag_delim=postag_delim,
            postag_length=postag_length,
        )

    def extract_article(
        self,
        article: Optional[str],
        nouns_only: bool = False,
    ) -> List[List[str]]:
        if article is None:
            return []

        tokens_article = []
        for sent in article.split(self.sentence_separator_unicode):
            sent = sent.strip()
            tokens = self.extract(sent, nouns_only=nouns_only)
            tokens_article.append(tokens)
        return tokens_article

    def extract_tokens(self, article: Optional[str]) -> List[List[str]]:
        return self.extract_article(article, nouns_only=False)

    def extract_nouns(self, article: Optional[str]) -> List[List[str]]:
        return self.extract_article(article, nouns_only=True)

    def filter_stopwords(
        self,
        text_or_tokens: Union[str, List[str], None],
    ) -> List[str]:
        if text_or_tokens is None:
            return []

        if isinstance(text_or_tokens, list):
            tokens = text_or_tokens
        else:
            tokens = self.tokenize(text_or_tokens)

        if self.stopwords and callable(self.stopwords):
            tokens = [token for token in tokens if not self.stopwords(token)]

        return tokens

    def filter_article_stopwords(self, article: Optional[str]) -> List[List[str]]:
        if article is None:
            return []

        return [
            self.filter_stopwords(sent)
            for sent in article.split(self.sentence_separator_unicode)
        ]


class SimpleTokenizer(Tokenizer):
    def parse(self, text: str) -> List[Tuple[str, str]]:
        return [(token, "") for token in text.split()]


def _match_tags(
    token: tuple,
    tags: List[str],
) -> bool:
    return any(token[1].startswith(tag) for tag in tags)


def _extract_tokens(
    tokenized_text: Union[str, List[str]],
    postags: Optional[List[str]] = None,
    stop_postags: Optional[List[str]] = None,
    stopwords: Optional[Callable[[str], bool]] = None,
    strip_pos: bool = True,
    postag_delim: str = "/",
    postag_length: Optional[int] = None,
    **kwargs,
) -> List[str]:
    if postags is None:
        postags = []
    if stop_postags is None:
        stop_postags = ["SP"]
    if isinstance(tokenized_text, str):
        tokens = tokenized_text.split()
    else:
        tokens = tokenized_text
    _token_pos_tuples = [
        _token_to_tuple(token, postag_delim=postag_delim, postag_length=postag_length)
        for token in tokens
    ]
    postags = [
        postag[:postag_length] if postag_length else postag
        for postag in postags
        if postag not in stop_postags
    ]
    stop_postags = [
        postag[:postag_length] if postag_length else postag for postag in stop_postags
    ]
    _tokens = []
    if postags:
        _tokens = [
            token_pos
            for token_pos in _token_pos_tuples
            if len(token_pos) == 1
            or (
                not _match_tags(token_pos, stop_postags)
                and _match_tags(token_pos, postags)
            )
        ]
    else:
        _tokens = [
            token_pos
            for token_pos in _token_pos_tuples
            if len(token_pos) == 1 or not _match_tags(token_pos, stop_postags)
        ]
    if stopwords is not None:
        _tokens = [token_pos for token_pos in _tokens if not stopwords(token_pos[0])]

    _tokens = [
        _tuple_to_token(
            token_pos,
            strip_pos=strip_pos,
            postag_delim=postag_delim,
            postag_length=postag_length,
        )
        for token_pos in _tokens
    ]
    return _tokens


def _tuple_to_token(
    token_pos: tuple,
    strip_pos: bool = True,
    postag_delim: str = "/",
    postag_length: Optional[int] = None,
) -> str:
    if strip_pos or len(token_pos) == 1:
        return token_pos[0]
    return (
        token_pos[0].strip()
        + postag_delim
        + (token_pos[1][:postag_length] if postag_length else token_pos[1])
    )


def _token_to_tuple(
    _token: Union[str, tuple],
    postag_delim: str = "/",
    postag_length: Optional[int] = None,
) -> Union[Tuple[str, str], Tuple[str]]:
    if isinstance(_token, str):
        token_pos = _token.split(postag_delim)
        if len(token_pos) == 2:
            return (
                token_pos[0],
                token_pos[1][:postag_length] if postag_length else token_pos[1],
            )
        return (token_pos[0],)
    return _token
