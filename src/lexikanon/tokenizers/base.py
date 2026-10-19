import codecs
import logging
from collections.abc import Callable

from lexikanon._base import Model
from lexikanon.normalizers import Normalizer
from lexikanon.stopwords import Stopwords

logger = logging.getLogger(__name__)


class Tokenizer(Model):
    stopwords: Stopwords = Stopwords()
    normalizer: Normalizer = Normalizer()

    lowercase: bool = False
    strip_pos: bool = False
    postag_delim: str = "/"
    postag_length: int | None = None
    include_whitespace_token: bool = True
    tokenize_each_word: bool = False
    sentence_separator: str = "\\n"
    wordpieces_prefix: str | None = "##"
    postags: list[str] | None = None
    noun_postags: list[str] | None = None
    punct_postags: list[str] | None = None
    stop_postags: list[str] | None = None
    verbose: bool = False

    @property
    def sentence_separator_unicode(self) -> str:
        return codecs.decode(self.sentence_separator, "unicode_escape")

    def __call__(self, text: str) -> list[str]:
        """Calling a tokenize config instance like a function just calls the tokenize method."""
        return self.tokenize(text)

    def tokenize(self, text: str) -> list[str]:
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

    def parse(self, text: str) -> list[tuple[str, str]]:
        return [(token, "") for token in text.split()]

    def to_token(self, term_pos: str | tuple) -> str:
        if isinstance(term_pos, tuple):
            return _tuple_to_token(
                term_pos,
                self.strip_pos,
                self.postag_delim,
                self.postag_length,
            )
        return term_pos

    def tokenize_word(self, word: str) -> list[str]:
        self.punct_postags = self.punct_postags or []
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

    def pos(self, text: str) -> list[tuple[str, str]]:
        return self.parse(text)

    def tokenize_article(
        self,
        article: str | None,
    ) -> list[list[str]]:
        if article is None:
            return []

        tokenized_article = []
        for sent in article.split(self.sentence_separator):
            sent = sent.strip()
            tokens = self.tokenize(sent)
            tokenized_article.append(tokens)
        return tokenized_article

    def nouns(self, text: str) -> list[str]:
        tokens = self.tokenize(text)
        return self.extract(tokens, nouns_only=True)

    def tokens(self, text: str) -> list[str]:
        tokens = self.tokenize(text)
        return self.extract(tokens, nouns_only=False)

    def morphs(self, text: str) -> list[str]:
        return self.tokens(text)

    def extract(
        self,
        text: str | list[str],
        nouns_only: bool = False,
        postags: list[str] | None = None,
        stop_postags: list[str] | None = None,
        strip_pos: bool | None = None,
        postag_delim: str | None = None,
        postag_length: int | None = None,
    ) -> list[str]:
        if strip_pos is None:
            strip_pos = self.strip_pos
        if stop_postags is None:
            stop_postags = self.stop_postags or []
        if postags is None:
            postags = self.noun_postags if nouns_only else self.postags or []
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
        article: str | None,
        nouns_only: bool = False,
    ) -> list[list[str]]:
        if article is None:
            return []

        tokens_article = []
        for sent in article.split(self.sentence_separator_unicode):
            sent = sent.strip()
            tokens = self.extract(sent, nouns_only=nouns_only)
            tokens_article.append(tokens)
        return tokens_article

    def extract_tokens(self, article: str | None) -> list[list[str]]:
        return self.extract_article(article, nouns_only=False)

    def extract_nouns(self, article: str | None) -> list[list[str]]:
        return self.extract_article(article, nouns_only=True)

    def filter_stopwords(
        self,
        text_or_tokens: str | list[str] | None,
    ) -> list[str]:
        if text_or_tokens is None:
            return []

        if isinstance(text_or_tokens, list):
            tokens = text_or_tokens
        else:
            tokens = self.tokenize(text_or_tokens)

        if self.stopwords and callable(self.stopwords):
            tokens = [token for token in tokens if not self.stopwords(token)]

        return tokens

    def filter_article_stopwords(self, article: str | None) -> list[list[str]]:
        if article is None:
            return []

        return [
            self.filter_stopwords(sent) for sent in article.split(self.sentence_separator_unicode)
        ]


class SimpleTokenizer(Tokenizer):
    def parse(self, text: str) -> list[tuple[str, str]]:
        return [(token, "") for token in text.split()]


def _match_tags(
    token: tuple,
    tags: list[str],
) -> bool:
    return any(token[1].startswith(tag) for tag in tags)


def _extract_tokens(
    tokenized_text: str | list[str],
    postags: list[str] | None = None,
    stop_postags: list[str] | None = None,
    stopwords: Callable[[str], bool] | None = None,
    strip_pos: bool = True,
    postag_delim: str = "/",
    postag_length: int | None = None,
    **kwargs,
) -> list[str]:
    if postags is None:
        postags = []
    if stop_postags is None:
        stop_postags = ["SP"]
    tokens = tokenized_text.split() if isinstance(tokenized_text, str) else tokenized_text
    _token_pos_tuples = [
        _token_to_tuple(token, postag_delim=postag_delim, postag_length=postag_length)
        for token in tokens
    ]
    postags = [
        postag[:postag_length] if postag_length else postag
        for postag in postags
        if postag not in stop_postags
    ]
    stop_postags = [postag[:postag_length] if postag_length else postag for postag in stop_postags]
    _tokens = []
    if postags:
        _tokens = [
            token_pos
            for token_pos in _token_pos_tuples
            if len(token_pos) == 1
            or (not _match_tags(token_pos, stop_postags) and _match_tags(token_pos, postags))
        ]
    else:
        _tokens = [
            token_pos
            for token_pos in _token_pos_tuples
            if len(token_pos) == 1 or not _match_tags(token_pos, stop_postags)
        ]
    if stopwords is not None:
        _tokens = [token_pos for token_pos in _tokens if not stopwords(token_pos[0])]

    return [
        _tuple_to_token(
            token_pos,
            strip_pos=strip_pos,
            postag_delim=postag_delim,
            postag_length=postag_length,
        )
        for token_pos in _tokens
    ]


def _tuple_to_token(
    token_pos: tuple,
    strip_pos: bool = True,
    postag_delim: str = "/",
    postag_length: int | None = None,
) -> str:
    if strip_pos or len(token_pos) == 1:
        return token_pos[0]
    return (
        token_pos[0].strip()
        + postag_delim
        + (token_pos[1][:postag_length] if postag_length else token_pos[1])
    )


def _token_to_tuple(
    _token: str | tuple,
    postag_delim: str = "/",
    postag_length: int | None = None,
) -> tuple[str, str] | tuple[str]:
    if isinstance(_token, str):
        token_pos = _token.split(postag_delim)
        if len(token_pos) == 2:
            return (
                token_pos[0],
                token_pos[1][:postag_length] if postag_length else token_pos[1],
            )
        return (token_pos[0],)
    return _token
