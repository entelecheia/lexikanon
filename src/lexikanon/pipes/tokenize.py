"""Tokenize texts and ``datasets.Dataset`` columns; each function works as a HyFI workflow step.

In a workflow, pass the tokenizer as a config with ``_target_`` (or ``${tokenizer}`` from the
``tokenizer`` group); HyFI builds it before calling the step.
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from lexikanon._version import __version__
from lexikanon.tokenizers import SimpleTokenizer, Tokenizer

if TYPE_CHECKING:
    from datasets import Dataset

logger = logging.getLogger(__name__)


def _default_tokenizer() -> Tokenizer:
    # Same settings as the ``tokenizer=simple`` config, the 1.x default.
    return SimpleTokenizer(strip_pos=True)


class _Unrepresentable(Exception):
    """A setting the cache key cannot capture exactly."""


_SCALARS = (str, int, float, bool, type(None))


def _describe(value: Any) -> Any:
    """Exact JSON description of a settings tree: pydantic models (by actual type and fields),
    containers, and JSON scalars. Anything else raises ``_Unrepresentable``.

    ``model_dump()`` would serialize a nested field by its declared type (dropping subclass
    fields), and ``repr()`` cannot tell apart objects such as two configured stemmers.
    """
    if isinstance(value, BaseModel):
        cls = type(value)
        fields = {name: _describe(getattr(value, name)) for name in cls.model_fields}
        fields.update({str(k): _describe(v) for k, v in (value.model_extra or {}).items()})
        return {"__type__": f"{cls.__module__}.{cls.__qualname__}", **fields}
    if isinstance(value, dict):
        if not all(isinstance(k, _SCALARS) for k in value):
            raise _Unrepresentable("dict key")
        return {str(k): _describe(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_describe(v) for v in value]
    if isinstance(value, set | frozenset):
        return sorted((_describe(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    if isinstance(value, _SCALARS):
        return value
    raise _Unrepresentable(f"{type(value).__module__}.{type(value).__qualname__}")


def _fingerprint(data: Any, step: str, tokenizer: Tokenizer, **params: Any) -> str:
    """Cache key for ``Dataset.map``: input fingerprint, step, tokenizer settings, parameters.

    Passed as ``new_fingerprint`` so datasets does not hash the map function with dill,
    which fails on Python 3.15 (dill 0.4.1). The cache is reused only when every setting is
    captured exactly; otherwise a random key forces recomputation instead of a wrong reuse.
    """
    try:
        key = [getattr(data, "_fingerprint", None), step, __version__, _describe(tokenizer)]
        key.append(_describe(params))
        payload = json.dumps(key, sort_keys=True)
    except _Unrepresentable as e:
        logger.debug("dataset cache disabled for %s: cannot describe %s", step, e)
        return uuid.uuid4().hex[:16]
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _num_proc(num_workers: int) -> int | None:
    # datasets 5 starts a worker pool even for num_proc=1; None keeps one worker in-process.
    return num_workers if num_workers > 1 else None


def tokenize_texts(
    texts: str | list[str],
    tokenizer: Tokenizer | None = None,
) -> list[list[str]]:
    """Tokenize each text (a single string counts as one text), line by line."""
    tokenizer = tokenizer or _default_tokenizer()
    if isinstance(texts, str):
        texts = [texts]
    return [[tok for line in text.split("\n") for tok in tokenizer(line)] for text in texts]


def tokenize_dataset(
    data: Dataset,
    tokenizer: Tokenizer | None = None,
    num_workers: int = 1,
    batched: bool = True,
    batch_size: int = 1000,
    text_col: str = "text",
    token_col: str = "tokens",
    remove_columns: list[str] | str | None = None,
    load_from_cache_file: bool = True,
    num_heads: int | None = 1,
    num_tails: int | None = 1,
    verbose: bool = False,
) -> Dataset:
    _tokenizer_ = tokenizer or _default_tokenizer()

    def pos_tagging(batch: dict[str, Any]) -> dict[str, Any]:
        return {token_col: tokenize_texts(batch[text_col], _tokenizer_)}

    data = data.map(
        pos_tagging,
        num_proc=_num_proc(num_workers),
        batched=batched,
        batch_size=batch_size,
        remove_columns=remove_columns,
        load_from_cache_file=load_from_cache_file,
        new_fingerprint=_fingerprint(
            data,
            "tokenize_dataset",
            _tokenizer_,
            batched=batched,  # changes the result shape, so it must change the key
            text_col=text_col,
            token_col=token_col,
            remove_columns=remove_columns,
        ),
    )
    logger.info("POS tagging done. See column '%s'.", token_col)
    if verbose:
        if num_heads:
            num_heads = min(num_heads, len(data))
            print(data[:num_heads][token_col])
        if num_tails:
            num_tails = min(num_tails, len(data))
            print(data[-num_tails:][token_col])
    return data


def extract_tokens(
    data: Dataset,
    tokenizer: Tokenizer | None = None,
    num_workers: int = 1,
    batched: bool = True,
    batch_size: int = 1000,
    token_col: str = "tokens",
    extracted_col: str = "extracted_tokens",
    nouns_only: bool = False,
    postags: list[str] | None = None,
    stop_postags: list[str] | None = None,
    strip_pos: bool | None = None,
    postag_delim: str | None = None,
    postag_length: int | None = None,
    remove_columns: list[str] | str | None = None,
    load_from_cache_file: bool = True,
    num_heads: int | None = 1,
    num_tails: int | None = 1,
    verbose: bool = False,
) -> Dataset:
    _tokenizer_ = tokenizer or _default_tokenizer()

    def pos_tagging(batch: dict[str, Any]) -> dict[str, Any]:
        batch_tokens = []
        for tokens in batch[token_col]:
            batch_tokens.append(
                _tokenizer_.extract(
                    tokens,
                    nouns_only=nouns_only,
                    postags=postags,
                    stop_postags=stop_postags,
                    strip_pos=strip_pos,
                    postag_delim=postag_delim,
                    postag_length=postag_length,
                )
            )
        return {extracted_col: batch_tokens}

    data = data.map(
        pos_tagging,
        num_proc=_num_proc(num_workers),
        batched=batched,
        batch_size=batch_size,
        remove_columns=remove_columns,
        load_from_cache_file=load_from_cache_file,
        new_fingerprint=_fingerprint(
            data,
            "extract_tokens",
            _tokenizer_,
            batched=batched,  # changes the result shape, so it must change the key
            token_col=token_col,
            extracted_col=extracted_col,
            nouns_only=nouns_only,
            postags=postags,
            stop_postags=stop_postags,
            strip_pos=strip_pos,
            postag_delim=postag_delim,
            postag_length=postag_length,
            remove_columns=remove_columns,
        ),
    )
    logger.info("Extracting tokens done, see column '%s'.", extracted_col)
    if verbose:
        if num_heads:
            num_heads = min(num_heads, len(data))
            print(data[:num_heads][extracted_col])
        if num_tails:
            num_tails = min(num_tails, len(data))
            print(data[-num_tails:][extracted_col])
    return data
