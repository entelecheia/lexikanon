import logging
from typing import Any, Dict, List, Optional, Union

from datasets import Dataset

from lexikanon import HyFI

logger = logging.getLogger(__name__)


def tokenize_dataset(
    data: Dataset,
    tokenizer: Union[str, Dict[str, Any]] = "simple",
    num_workers: int = 1,
    batched: bool = True,
    batch_size: int = 1000,
    text_col: str = "text",
    token_col: str = "tokens",
    remove_columns: Optional[Union[List[str], str]] = None,
    load_from_cache_file: bool = True,
    num_heads: Optional[int] = 1,
    num_tails: Optional[int] = 1,
    verbose: bool = False,
) -> Dataset:
    def pos_tagging(batch):
        if isinstance(tokenizer, str):
            _tokenizer_ = HyFI.instantiate_config(
                f"tokenizer={tokenizer}",
            )
        else:
            _tokenizer_ = HyFI.instantiate(
                tokenizer,
            )
        batch_tokens = []
        for text in batch[text_col]:
            sentences = text.split("\n")
            tokens = []
            for sentence in sentences:
                tokens.extend(_tokenizer_(sentence))
            batch_tokens.append(tokens)
        return {token_col: batch_tokens}

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
    tokenizer: Union[str, Dict[str, Any]] = "simple",
    num_workers: int = 1,
    batched: bool = True,
    batch_size: int = 1000,
    token_col: str = "tokens",
    extracted_col: str = "extracted_tokens",
    nouns_only: bool = False,
    postags: Optional[List[str]] = None,
    stop_postags: Optional[List[str]] = None,
    strip_pos: Optional[bool] = None,
    postag_delim: Optional[str] = None,
    postag_length: Optional[int] = None,
    remove_columns: Optional[Union[List[str], str]] = None,
    load_from_cache_file: bool = True,
    num_heads: Optional[int] = 1,
    num_tails: Optional[int] = 1,
    verbose: bool = False,
) -> Dataset:
    def pos_tagging(batch):
        if isinstance(tokenizer, str):
            _tokenizer_ = HyFI.instantiate_config(
                f"tokenizer={tokenizer}",
            )
        else:
            _tokenizer_ = HyFI.instantiate(
                tokenizer,
            )
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
