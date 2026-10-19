# Migrating from 0.x

Lexikanon 1.0 runs on HyFI 2.0 and no longer imports HyFI itself. To stay on the old API, pin `lexikanon<1` (which needs `hyfi<2` and Python below 3.13).

| 0.x | 1.0 |
|---|---|
| `from lexikanon import HyFI` | `import hyfi` (HyFI 2.0), only where you compose configs |
| `HyFI.compose_as_dict("tokenizer=mecab")` + `MecabTokenizer(**cfg)` | `hyfi.instantiate(hyfi.compose_group("tokenizer", "mecab"))` |
| `HyFI.instantiate_config("stopwords", overrides=[...])` | `hyfi.instantiate(hyfi.compose_group("stopwords", "default", [...]))` |
| option `__init__` (`stopwords=__init__`, `/normalizer@normalizer: __init__`) | option `default` |
| `Normalizer()` composed `normalizer/__init__.yaml` on construction | `Normalizer()` uses class defaults, which now match that file (`hanja2hangle=False`) |
| `NLTKTagger.generate_config()` and other HyFI model helpers | removed |
| `lexikanon` console command (`hyfi_main` wrapper) | the `hyfi` CLI |
| `run=tokenize_dataset`, `pipe=extract_tokens`, ... | `workflow=lexikanon_tokenize_dataset`, `workflow=lexikanon_find_similar_docs` |
| `tokenize_dataset(data, tokenizer="mecab")` (a config name) | `tokenize_dataset(data, tokenizer=MecabTokenizer(...))`, or `${tokenizer}` in a workflow |
| `about` group | removed |

Outputs did not change: the tests compare every tokenizer and normalizer preset against results recorded with lexikanon 0.6.5 (`tests/data/outputs_1x.json`).

Fixed along the way:

- The NLTK tagger downloads `punkt_tab` and `averaged_perceptron_tagger_eng`, which nltk 3.9+ needs; 0.6.5 failed on a clean machine.
- `find_similar_docs_by_clustering` works on scikit-learn 1.4+ (`metric=` instead of `affinity=`), with the default `distance_threshold=None`, and with ids that are not row positions.

## `stopwords_fn` no longer evaluates strings

0.x passed a string such as `"lambda w: len(w) < 2"` to `eval`, so any config could run arbitrary code, outside HyFI's execution allowlist. 1.0 rejects strings. Pass a callable from Python, or in a HyFI config point at a function and allow it:

```yaml
stopwords_fn:
  _target_: mypkg.text.is_short
  _partial_: true
```

```bash
hyfi run workflow=... --allow 'lexikanon.*' --allow mypkg.text.is_short
```

