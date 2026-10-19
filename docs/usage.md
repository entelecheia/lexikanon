# Usage

## Library

Every class is a Pydantic model; construct it with keyword arguments.

| class | module | what it does |
|---|---|---|
| `Tokenizer`, `SimpleTokenizer` | `lexikanon.tokenizers` | whitespace tokens |
| `MecabTokenizer` (+ `MecabTagger`) | `lexikanon.tokenizers` | Korean morphemes as `term/POS`, via eKoNLPy |
| `NLTKTokenizer` (+ `NLTKTagger`) | `lexikanon.tokenizers` | English tokens with Penn or universal tags, Porter stemming by default |
| `Normalizer` | `lexikanon.normalizers` | ftfy, quotes, hyphens, whitespace, optional hanja to hangul and emoticon folding |
| `Stopwords` | `lexikanon.stopwords` | a word list from a file, a list, NLTK, or a function |

A tokenizer holds a `normalizer` and `stopwords`. `tokenize()` normalizes and tags; `nouns()` and `tokens()` filter by `noun_postags`, `postags`, and `stop_postags`, then drop stopwords.

Class defaults are minimal: `MecabTokenizer()` has no POS filters, so `nouns()` keeps every token. The presets below (`tokenizer=mecab` and so on) carry the POS lists; copy them from `src/lexikanon/conf/` or compose them with HyFI.

The NLTK tagger downloads `punkt_tab`, `averaged_perceptron_tagger_eng`, `universal_tagset`, `wordnet`, and `omw-1.4` on construction. Set `NLTK_DATA` to choose where they go.

## Config groups

| option | what changes from `default` |
|---|---|
| `tokenizer=simple` | `SimpleTokenizer`, `strip_pos: true` |
| `tokenizer=mecab` | `MecabTokenizer`, Sejong POS lists for nouns, punctuation, and stop tags |
| `tokenizer=nltk` | `NLTKTokenizer`, Penn POS lists, `normalizer=formal_en` |
| `tokenizer=nltk_universal` | `nltk` with the universal tagset |
| `normalizer=formal_ko` | `hanja2hangle: true` |
| `normalizer=informal_ko` | `formal_ko` plus emoticon folding |
| `normalizer=formal_en` | `ftfy.unescape_html: auto` |
| `normalizer=formal_en_parantheses` | all brackets become `(` and `)` |

Every node has a `_target_`, so `hyfi.instantiate` builds the object:

```python
import hyfi

tok = hyfi.instantiate(hyfi.compose_group("tokenizer", "mecab", ["tokenizer.strip_pos=true"]))
```

## Workflow steps

The functions in `lexikanon.pipes` take their data as the first argument, so they chain as HyFI workflow steps:

- `lexikanon.pipes.tokenize.tokenize_texts(texts, tokenizer=None)`: a string or list of strings to lists of tokens.
- `lexikanon.pipes.tokenize.tokenize_dataset(data, tokenizer=None, text_col="text", token_col="tokens", ...)`: adds a token column to a `datasets.Dataset` (extra `datasets`).
- `lexikanon.pipes.tokenize.extract_tokens(data, tokenizer=None, token_col="tokens", extracted_col="extracted_tokens", nouns_only=False, ...)`: filters a token column by POS and stopwords.
- `lexikanon.pipes.similarity.find_similar_docs_by_clustering(data, ...)`: flags near-duplicate documents per time window in a pandas DataFrame (extra `similarity`).

`tokenizer=None` means `SimpleTokenizer(strip_pos=True)`, the same as `tokenizer=simple`. In a workflow, pass `${tokenizer}`; the example workflows pull `tokenizer: simple` into the root of the config, so `tokenizer=<option>` on the command line swaps it:

```yaml
# conf/workflow/my_corpus.yaml
defaults:
  - /tokenizer@_global_.tokenizer: mecab

name: my_corpus
steps:
  - run: datasets.load_dataset
    with: {path: csv, data_files: data/news.csv, split: train}
  - run: lexikanon.pipes.tokenize.tokenize_dataset
    with: {tokenizer: "${tokenizer}", text_col: body}
  - run: lexikanon.pipes.tokenize.extract_tokens
    with: {tokenizer: "${tokenizer}", nouns_only: true}
```

```bash
hyfi run workflow=my_corpus --allow 'lexikanon.*' --allow 'datasets.*' --allow 'nltk.*'
```

The NLTK presets build `nltk.stem.*` objects, so allow `nltk.*` when you pass `--allow`.
