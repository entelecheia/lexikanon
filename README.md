# Lexikanon

[![pypi-image]][pypi-url]
[![license-image]][license-url]

Korean and English tokenizers, text normalizers, and stopword lists. Lexikanon is a plain Python library; it also ships [HyFI 2.0](https://hyfi.entelecheia.ai) config groups, so the same tokenizers can be selected and run from HyFI workflows.

- [Documentation][docs-url]
- [Migrating from 0.x](https://lexikanon.entelecheia.ai/migration/)

Lexikanon 1.0 drops the HyFI 1.x API. Pin `lexikanon<1` to keep it.

## Install

```bash
uv add lexikanon          # or: pip install lexikanon
pip install 'lexikanon[datasets]'     # tokenize_dataset / extract_tokens on datasets.Dataset
pip install 'lexikanon[similarity]'   # find_similar_docs_by_clustering
```

Python 3.11 or newer. Korean morphological analysis uses MeCab through [eKoNLPy](https://github.com/entelecheia/eKoNLPy) (fugashi and mecab-ko-dic wheels). On Python 3.15, fugashi builds from source and needs the MeCab library (`apt-get install libmecab-dev` or `brew install mecab`).

## Use it as a library

```python
from lexikanon.normalizers import Normalizer
from lexikanon.tokenizers import MecabTokenizer

tokenizer = MecabTokenizer(noun_postags=["NNG", "NNP"])
tokenizer("금통위는 물가안정과 금리정책을 밝혔다.")
# ['금통위/NNG', '는/JX', '물가/NNG', '안정/NNG', '과/JC', ...]
tokenizer.nouns("금통위는 물가안정과 금리정책을 밝혔다.")

Normalizer(hanja2hangle=True)("今年에도 持續하고 있다")
# '금년에도 지속하고 있다'
```

Importing lexikanon never imports HyFI.

## Use it from HyFI

Installing lexikanon registers its config groups through the `hyfi.plugins` entry point:

| group | options |
|---|---|
| `tokenizer` | `default`, `simple`, `mecab`, `nltk`, `nltk_universal` |
| `normalizer` | `default`, `formal_ko`, `informal_ko`, `formal_en`, `formal_en_parantheses` |
| `stopwords` | `default` |
| `workflow` | `lexikanon_tokenize_text`, `lexikanon_tokenize_dataset`, `lexikanon_find_similar_docs` |

```bash
hyfi plugins
hyfi run workflow=lexikanon_tokenize_text tokenizer=mecab
```

```python
import hyfi

tokenizer = hyfi.instantiate(hyfi.compose_group("tokenizer", "mecab"))
```

See [Usage](https://lexikanon.entelecheia.ai/usage/) for workflow steps and presets.

## Citation

```tex
@software{lee_2023_lexikanon,
  author       = {Young Joon Lee},
  title        = {Lexikanon: A HyFI-based library for Tokenizers},
  year         = 2023,
  publisher    = {GitHub},
  url          = {https://github.com/entelecheia/lexikanon}
}
```

## License

[MIT][license-url]

[pypi-image]: https://img.shields.io/pypi/v/lexikanon
[pypi-url]: https://pypi.org/project/lexikanon
[license-image]: https://img.shields.io/github/license/entelecheia/lexikanon
[license-url]: https://github.com/entelecheia/lexikanon/blob/main/LICENSE
[docs-url]: https://lexikanon.entelecheia.ai
