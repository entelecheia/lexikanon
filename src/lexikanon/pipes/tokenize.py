"""Tokenize texts and ``datasets.Dataset`` columns; each function works as a HyFI workflow step.

In a workflow, pass the tokenizer as a config with ``_target_`` (or ``${tokenizer}`` from the
``tokenizer`` group); HyFI builds it before calling the step.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from lexikanon.tokenizers import SimpleTokenizer, Tokenizer

if TYPE_CHECKING:
    from datasets import Dataset

logger = logging.getLogger(__name__)


def _default_tokenizer() -> Tokenizer:
    # Same settings as the ``tokenizer=simple`` config, the 1.x default.
    return SimpleTokenizer(strip_pos=True)


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
        num_proc=num_workers,
        batched=batched,
        batch_size=batch_size,
        remove_columns=remove_columns,
        load_from_cache_file=load_from_cache_file,
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
        num_proc=num_workers,
        batched=batched,
        batch_size=batch_size,
        remove_columns=remove_columns,
        load_from_cache_file=load_from_cache_file,
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
