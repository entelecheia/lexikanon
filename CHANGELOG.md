<!--next-version-placeholder-->

## v1.0.1 (2026-10-19)

### Bug Fixes

- Compare and combine Stopwords through their loaded words
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Drop the malformed tail of CONTROL_RE's character class
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Keep one token list per row when tokenizing datasets unbatched
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Keep stopwords_fn and lowercase through Stopwords set operators
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Match similarity clusters to rows by position, not str(id)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Pick the earliest row per cluster without a temporary column
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Resolve follow-up issues (#120-#124, #126, #127)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Return find_similar_docs_by_clustering results in the input's shape
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Treat a Stopwords with only stopwords_fn as active
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

### Continuous Integration

- Always validate PRs beyond the files API limit (entelecheia/hyfi#479)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Count renamed paths and avoid grep -q in the docs-only check (entelecheia/hyfi#479)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Make releases retryable and keep ci-ok reported for docs-only PRs (entelecheia/hyfi#479)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Run full validation when the PR files API fails (entelecheia/hyfi#479)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- State that only tags from this release workflow can be republished (entelecheia/hyfi#479)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))

- Validate the tag before a republish (entelecheia/hyfi#479)
  ([#125](https://github.com/entelecheia/lexikanon/pull/125),
  [`f068453`](https://github.com/entelecheia/lexikanon/commit/f0684531b7ffef15da2b5e64e547ae4de73eb094))


## v1.0.0 (2026-10-19)

### Bug Fixes

- Build only nltk.stem targets inside NLTKTagger
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Include batched in the dataset cache key
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Include subclass fields of nested models in the dataset cache key
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Let datasets hash map functions instead of hand-made cache keys
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Reuse the dataset cache only when every setting is described exactly
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Run the dataset steps on Python 3.15 ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Stop evaluating stopwords_fn strings ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

### Build System

- Make the semantic-release build command fail fast
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Move to uv, hatchling, ruff, and python-semantic-release v10
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Update uv.lock in the semantic-release build command
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

### Chores

- Update poetry lock
  ([`b3d29b8`](https://github.com/entelecheia/lexikanon/commit/b3d29b837c06e8c966a7c050ea78b7f62cd840eb))

- Update poetry lock
  ([`66b5fde`](https://github.com/entelecheia/lexikanon/commit/66b5fde9c3b0498a5fa412bec82edf46cf675bc9))

- Update poetry lock
  ([`875e185`](https://github.com/entelecheia/lexikanon/commit/875e1852a86c21ccc829811a8db7a610a8cafc6a))

- Update poetry lock
  ([`05bd409`](https://github.com/entelecheia/lexikanon/commit/05bd409575d51e2f7efa101f01275bdadc86ad78))

- Update poetry lock
  ([`0b67b3f`](https://github.com/entelecheia/lexikanon/commit/0b67b3f57d38db7c5d13ee34e9bc5414fa0deeba))

- Update poetry lock
  ([`e8121c3`](https://github.com/entelecheia/lexikanon/commit/e8121c35cb1fdf6068a0ff63226ad1137ff3766d))

- **deps**: Bump codecov/codecov-action from 4 to 5
  ([`e3a10a0`](https://github.com/entelecheia/lexikanon/commit/e3a10a05d566da6f36daad7675e9c951db2eba64))

- **deps**: Bump ekonlpy from 2.0.4 to 2.0.5
  ([`628516e`](https://github.com/entelecheia/lexikanon/commit/628516eda9c05768fa9b7a05beecd2a4ec072083))

- **deps**: Bump ekonlpy from 2.0.5 to 2.0.6
  ([`c9b936f`](https://github.com/entelecheia/lexikanon/commit/c9b936fe4a9786ca7a876ef0b6c3805c5f5a4c9b))

- **deps**: Bump ftfy from 6.2.0 to 6.2.3
  ([`84f81d5`](https://github.com/entelecheia/lexikanon/commit/84f81d59048fb3130b425dce63e9fe3f5906045f))

- **deps**: Bump ftfy from 6.2.3 to 6.3.0
  ([`3e88ce0`](https://github.com/entelecheia/lexikanon/commit/3e88ce0d30ab6a74855a014e86442e3e7b86803d))

- **deps**: Bump ftfy from 6.3.0 to 6.3.1
  ([`2f82d8a`](https://github.com/entelecheia/lexikanon/commit/2f82d8a52aa49526d476e30053f251ae25b0b75c))

- **deps**: Bump hyfi from 1.36.3 to 1.36.4
  ([`8dd272c`](https://github.com/entelecheia/lexikanon/commit/8dd272c0a96fe7b54bb2811fd4f06cf4d2f8c640))

- **deps**: Bump hyfi from 1.36.4 to 1.37.0
  ([`bc6d048`](https://github.com/entelecheia/lexikanon/commit/bc6d04812a4c51d9e6b8a3b742659967853b0625))

- **deps**: Bump jupyter-book from 1.0.0 to 1.0.2
  ([`cb7ca32`](https://github.com/entelecheia/lexikanon/commit/cb7ca3250a70cc77e7d0cd20710554ef373a8222))

- **deps**: Bump jupyter-book from 1.0.2 to 1.0.3
  ([`ce1de2b`](https://github.com/entelecheia/lexikanon/commit/ce1de2b6225e40a937dc89d89c74c744a9550a6d))

- **deps**: Bump jupyter-book from 1.0.3 to 1.0.4
  ([`6cdfaf3`](https://github.com/entelecheia/lexikanon/commit/6cdfaf3adfe342c2e10457cc1ab70a624f4fe294))

- **deps**: Bump jupyter-book from 1.0.4 to 1.0.4.post1
  ([`c9090da`](https://github.com/entelecheia/lexikanon/commit/c9090da0473328bb5d42540f5c603f66d92dbe51))

- **deps**: Bump nltk from 3.8.1 to 3.8.2
  ([`e5013a1`](https://github.com/entelecheia/lexikanon/commit/e5013a121bd5975c353d5733ae1ab16776df7be9))

- **deps**: Bump nltk from 3.8.2 to 3.9
  ([`6415b54`](https://github.com/entelecheia/lexikanon/commit/6415b549bc696b267aa29d090f2a03be3e2103e4))

- **deps**: Bump nltk from 3.9 to 3.9.1
  ([`83500a2`](https://github.com/entelecheia/lexikanon/commit/83500a2f2db4d64dbdc084778fb771a9003f5fc6))

- **deps**: Bump peaceiris/actions-gh-pages from 3 to 4
  ([`f872ddd`](https://github.com/entelecheia/lexikanon/commit/f872dddcfafcc498634c8e65d4f655dc9caff20b))

- **deps**: Bump scikit-learn from 1.4.1.post1 to 1.4.2
  ([`c1ef0fb`](https://github.com/entelecheia/lexikanon/commit/c1ef0fb9280f49033f32ce5af34d3abf41decc7a))

- **deps**: Bump scikit-learn from 1.5.0 to 1.5.1
  ([`67b0722`](https://github.com/entelecheia/lexikanon/commit/67b072293ca3284a43672d4f3f121f35b0c866b9))

- **deps**: Bump scikit-learn from 1.5.1 to 1.5.2
  ([`0db67d2`](https://github.com/entelecheia/lexikanon/commit/0db67d22cd0c55d6bb1cae6c883ee71be94fb74c))

- **deps**: Bump scikit-learn from 1.5.2 to 1.6.1
  ([`0fbd08b`](https://github.com/entelecheia/lexikanon/commit/0fbd08b594854b4d4b07a6a2ab720a407744068b))

### Continuous Integration

- **workflows**: Upgrade Python version to 3.9
  ([`d9100e2`](https://github.com/entelecheia/lexikanon/commit/d9100e266c62cc9f590f6117e98b8d8ae1c54ff4))

### Documentation

- Drop the Zenodo badge and DOI citation ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Mkdocs site, migration guide, AGENTS.md and REVIEW.md
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

### Features

- Migrate to HyFI 2.0 (plain library + config groups)
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))

- Run on HyFI 2.0 as a plain library with config groups
  ([#119](https://github.com/entelecheia/lexikanon/pull/119),
  [`bd4e936`](https://github.com/entelecheia/lexikanon/commit/bd4e9368a3a44a29f798600847dc56e9e6a871fd))


## v0.6.5 (2024-03-27)

### Fix

* **dependencies:** Update python and hyfi versions ([`d55c830`](https://github.com/entelecheia/lexikanon/commit/d55c8302f0f33ab6ae25ebd457ee0262af9fa0e2))

## v0.6.4 (2023-08-24)

### Fix

* **tests:** Update HyFI method calls and behavior ([`c55189a`](https://github.com/entelecheia/lexikanon/commit/c55189ab1683fce33a26713c78a807833951371c))
* **Makefile:** Enable trust flag for copier command ([`1717647`](https://github.com/entelecheia/lexikanon/commit/1717647cad364b68ed19965f0e2833691d56fb89))

## v0.6.3 (2023-08-18)

### Fix

* **dependencies:** Upgrade hyfi to 1.29.8 ([`7747ddb`](https://github.com/entelecheia/lexikanon/commit/7747ddbcf22784d419f5be9e36719147521f9ab3))

## v0.6.2 (2023-08-15)

### Fix

* **book:** Update library description, add Zenodo link ([`b55f063`](https://github.com/entelecheia/lexikanon/commit/b55f06350c5a8264c126e3faf6e8a7437364b8bf))

### Documentation

* **readme:** Add Zenodo DOI badge and link, update library description ([`5513505`](https://github.com/entelecheia/lexikanon/commit/55135053650776ab352273201fb568d409ca7ec3))

## v0.6.1 (2023-08-13)

### Fix

* **tokenizers:** Add model validator after method ([`cfd8a06`](https://github.com/entelecheia/lexikanon/commit/cfd8a0685a6e0e3bc3f7266da536a3cd78d67446))
* **normalizer:** Change unescape_html type to Union[bool, str] ([`d7e024f`](https://github.com/entelecheia/lexikanon/commit/d7e024f54d5f0ba213c0536b89323f5550e16fb5))
* **tokenizer:** Add formal_en normalizer to nltk config ([`b65d01a`](https://github.com/entelecheia/lexikanon/commit/b65d01aa9d779a5c220e64354c9cacf4621efdbc))
* **stopwords:** Add verbose condition to logging ([`a7f168b`](https://github.com/entelecheia/lexikanon/commit/a7f168b1775df78d73e12ba4f6e2373304c4f9ec))
* **lexikanon:** Adjust NLTKTagger for tagsets and default tag ([`54ba18f`](https://github.com/entelecheia/lexikanon/commit/54ba18f94aa618ea3f78d85e4259a2358137545b))

## v0.6.0 (2023-08-13)

### Feature

* **tokenizer:** Add additional postags ([`fe95c3e`](https://github.com/entelecheia/lexikanon/commit/fe95c3ecbb8be03d2facc95bf9ccdbb2bb227c30))
* **tokenizer:** Add additional postags to nltk config ([`a35f684`](https://github.com/entelecheia/lexikanon/commit/a35f6849d884716c38f5697210d202b34542ba3c))
* **tokenizers/nltk:** Add language support, improve tagset flexibility, download universal_tagset ([`82e2514`](https://github.com/entelecheia/lexikanon/commit/82e2514eb91a66eaef838c92a9c9f6d6b2b54667))
* **lexikanon:** Add new nltk_universal configuration file ([`2c7880f`](https://github.com/entelecheia/lexikanon/commit/2c7880fc5facd1fbf18e58b81a605e8b47bc5481))
* **tokenizer:** Add nltk_universal configuration ([`e68c5e1`](https://github.com/entelecheia/lexikanon/commit/e68c5e1b2c8361e4bd8e75d5cd16f1687f90f0f7))
* **tokenizers:** Add MecabTagger and NLTKTagger ([`b766fb3`](https://github.com/entelecheia/lexikanon/commit/b766fb393e499eaf082968a9a96bd31007352fc8))
* **tokenizer/tagger:** Implement NLTKTagger ([`4f2d945`](https://github.com/entelecheia/lexikanon/commit/4f2d945240afa140063081391734788cdc5d923f))

### Fix

* **tokenizer:** Add punctuation postags to mecab.yaml ([`1624dbd`](https://github.com/entelecheia/lexikanon/commit/1624dbdb8466008eddf1f42fc34e75c0c6a9ada9))
* **tokenizers:** Adjust tokenizer base configurations ([`c96bfbf`](https://github.com/entelecheia/lexikanon/commit/c96bfbf7e8443f12d8839f96e514b4da6eeaadb9))
* **MecabTagger:** Correct config_group path ([`9b74064`](https://github.com/entelecheia/lexikanon/commit/9b74064eed4d97192c3b149b219fc11b73c03f83))

## v0.5.2 (2023-08-06)

### Fix

* **dependencies:** Upgrade hyfi to 1.20.0 ([`1b6c402`](https://github.com/entelecheia/lexikanon/commit/1b6c402dfb85ed81f2314d47f6d3823888caab3a))

## v0.5.1 (2023-08-05)

### Fix

* **stopwords:** Simplify loading and accessing stopwords ([`b4628f9`](https://github.com/entelecheia/lexikanon/commit/b4628f99ff24feda4002ece225ac42f7ea8194d7))

## v0.5.0 (2023-08-04)

### Feature

* **lexikanon:** Add find_similar_docs_by_clustering configuration ([`51ddf56`](https://github.com/entelecheia/lexikanon/commit/51ddf5692f05db3a8145b41f3ca18362d1644175))
* **lexikanon:** Add find_similar_docs_by_clustering configuration ([`e2122cf`](https://github.com/entelecheia/lexikanon/commit/e2122cfa1cf73c270d1657dfc9f01295ca8019a2))
* **lexikanon:** Add similarity.py for document similarity analysis ([`b1fc21b`](https://github.com/entelecheia/lexikanon/commit/b1fc21b12282211306fde4aab0d9df013cd9826f))
* **pyproject.toml:** Add scikit-learn dependency ([`7dd0014`](https://github.com/entelecheia/lexikanon/commit/7dd0014a9c80ef4986a943c4409379f4699c25ed))

## v0.4.3 (2023-08-04)

### Fix

* **tokenizers:** Add Tokenizer to lexikanon tokenizers ([`66712af`](https://github.com/entelecheia/lexikanon/commit/66712af95443085185cb3ac56c2e66f04ba38eec))
* **lexikanon:** Change tokenizer_config_name to tokenizer ([`dc014bc`](https://github.com/entelecheia/lexikanon/commit/dc014bcc2b07163581d57b259eff4a3c8d753ad6))
* **lexikanon/pipe/tokenize:** Enhance tokenizer function to support string or dict types ([`58e32f9`](https://github.com/entelecheia/lexikanon/commit/58e32f94e1b1da2a1c40254d347939cb74bfec20))

## v0.4.2 (2023-08-04)

### Fix

* **tokenizer:** Change target from corprep to lexikanon in nltk.yaml ([`27e6915`](https://github.com/entelecheia/lexikanon/commit/27e691528e0f7ed9e8c57cd644ad82c7b2235e9b))
* **.envrc:** Add new environment configuration file ([`13eeba2`](https://github.com/entelecheia/lexikanon/commit/13eeba255b13a914b5122dd746ff92c7e9c1e5ca))

## v0.4.1 (2023-08-03)

### Fix

* **lexikanon:** To bump version ([`b929758`](https://github.com/entelecheia/lexikanon/commit/b9297582d5b2e7a210358ec5921966c6bbde5221))

## v0.4.0 (2023-07-30)

### Feature

* **nltk:** Add config group and name to NLTKTagger ([`fd5ba82`](https://github.com/entelecheia/lexikanon/commit/fd5ba8297d37e57f148808cd63e2fda3b385aa28))
* **mecab:** Add _config_group_ and _config_name_ fields in MecabTagger ([`75937aa`](https://github.com/entelecheia/lexikanon/commit/75937aa60cd7190656fa6e528a359626bd1ad2d6))
* **lexikanon:** Add _config_group_ and _config_name_ to Tokenizer class ([`5ae39cb`](https://github.com/entelecheia/lexikanon/commit/5ae39cb0ed26359960722c5fdcb32fc7bd1c812e))
* **normalizer:** Add config group and config name attributes to classes ([`f55ea51`](https://github.com/entelecheia/lexikanon/commit/f55ea518a6c0a1fd9679069439b2c6327f373685))
* **tokenizer/tagger:** Add _config_group_ and _config_name_ in mecab.yaml and nltk.yaml ([`ed1be7c`](https://github.com/entelecheia/lexikanon/commit/ed1be7c987d013ac7dd6144f6d70a68caf56b2a7))
* **tokenizer:** Add _config_name_ in tokenizer configuration files ([`5a3d79b`](https://github.com/entelecheia/lexikanon/commit/5a3d79bde7bcb98269fe60f0b10c53eeb11a919c))
* **lexikanon:** Add _config_name_ in normalizer files ([`989d354`](https://github.com/entelecheia/lexikanon/commit/989d35405c368a638e3726f112b01392110bc2c1))

### Fix

* **dependencies:** Upgrade hyfi to 1.12.5 ([`0113560`](https://github.com/entelecheia/lexikanon/commit/01135605c20197ff7c7eb372b24638a7fa445011))

## v0.3.2 (2023-07-28)

### Fix

* To force bumping version ([`7c973d7`](https://github.com/entelecheia/lexikanon/commit/7c973d780668ec1a424757ee39a3ba50b4bc5db0))

## v0.3.1 (2023-07-26)

### Fix

* **lexikanon:** Simplify YAML configuration files ([`55def1f`](https://github.com/entelecheia/lexikanon/commit/55def1f4be3da40349017fbccb54464bf0d1ab52))
* **dependencies:** Upgrade hyfi to ^1.11.0 ([`1ea8090`](https://github.com/entelecheia/lexikanon/commit/1ea80909c640d871c2c5fc616683bc35de65087e))
* **lexikanon:** Add 'num_heads' and 'num_tails' options in 'dataset_extract_tokens.yaml', 'dataset_tokenize.yaml', 'tokenize.py' and 'extract_tokens' ([`07dec64`](https://github.com/entelecheia/lexikanon/commit/07dec647992eb14616be09c6d2edfb2d74ac2fa7))

## v0.3.0 (2023-07-26)

### Feature

* **lexikanon/pipe:** Add new tokenize module ([`307d2a7`](https://github.com/entelecheia/lexikanon/commit/307d2a7b6aeff3f8935d9173e6602590382b36ae))
* **lexikanon/pipe:** Add new __init__.py file ([`f824369`](https://github.com/entelecheia/lexikanon/commit/f824369d3ea13c6ecdd6eda86b91a5b53d4049ff))
* **lexikanon:** Add dataset_extract_nouns configuration ([`e175605`](https://github.com/entelecheia/lexikanon/commit/e1756050c378fbf020be8ae06c8e5b1d8e5e43c6))
* **lexikanon:** Add dataset_extract_tokens.yaml configuration ([`f024732`](https://github.com/entelecheia/lexikanon/commit/f02473250ef301025ea1cf4eeaaa9b43fd384413))
* **lexikanon:** Add new tokenizer configuration in the dataset_tokenize.yaml file ([`02f4044`](https://github.com/entelecheia/lexikanon/commit/02f4044a06aa9f20ce71405252e67827657ba74d))

### Fix

* **lexikanon:** Update logging and data display in tokenize functions ([`27b22e7`](https://github.com/entelecheia/lexikanon/commit/27b22e7db54f15987e8100ed21666285b641cab9))

## v0.2.4 (2023-07-25)

### Fix

* **stopwords:** Add special methods for Stopwords ([`e1b8871`](https://github.com/entelecheia/lexikanon/commit/e1b88711a5764cd638f52f8110dcb1411795fcc0))
* **stopwords:** Separate stopwords function and list, enhance logging control ([`fe2cf32`](https://github.com/entelecheia/lexikanon/commit/fe2cf323e514fce0f25068a1aaa25d58d2f90a8a))
* **stopwords:** Rename configuration variables ([`084f679`](https://github.com/entelecheia/lexikanon/commit/084f679737d38b625051fb6e081bf28ddda101c5))
* **dependencies:** Upgrade hyfi to 1.9.4 ([`7a0bc54`](https://github.com/entelecheia/lexikanon/commit/7a0bc5445d80fb8ec71c1c12dc7d3f2a8972786d))

## v0.2.3 (2023-07-25)
### Fix
* **lexikanon:** Change __package_name__ to __package_path__ in HyFI.initialize_global_hyfi args ([`0b93f1a`](https://github.com/entelecheia/lexikanon/commit/0b93f1a426d8ac29ca9248bff10fd06a7864fa65))
* **dependencies:** Upgrade hyfi to 1.9.3 ([`beb09bb`](https://github.com/entelecheia/lexikanon/commit/beb09bb185d09e2213605ffd4ad0113ae074be11))
* **dependencies:** Upgrade ekonlpy to 2.0.2 ([`4215068`](https://github.com/entelecheia/lexikanon/commit/4215068b4ec5e46d7ac32249e30a4326e4c0f34e))

## v0.2.2 (2023-07-24)
### Fix
* **tokenizer:** Change SimpleTokenizer path in config ([`13d4ea0`](https://github.com/entelecheia/lexikanon/commit/13d4ea0ec4aba20801d5b9687de14dda78a36a91))
* **tokenizer:** Change MecabTokenizer import path ([`edc6e8d`](https://github.com/entelecheia/lexikanon/commit/edc6e8d0ac6f53c26c88e56401d5b4515ac0d7ac))
* **stopwords:** Update target path ([`da93a48`](https://github.com/entelecheia/lexikanon/commit/da93a48e8e9112fc2c10f1a9636b8a298c1f99fb))
* **normalizer:** Update target to lexikanon.normalizers.Normalizer ([`c33e060`](https://github.com/entelecheia/lexikanon/commit/c33e0605b992afdbc3558d1e6f9eeac535a5fd7e))

## v0.2.1 (2023-07-24)
### Fix
* **dependencies:** Upgrade hyfi to 1.9.0 ([`e91bf8d`](https://github.com/entelecheia/lexikanon/commit/e91bf8d67b5fa8a621ce2edb4dddf156cb93b13f))

## v0.2.0 (2023-07-24)
### Feature
* **tests:** Add stopwords test in lexikanon module ([`32be6ae`](https://github.com/entelecheia/lexikanon/commit/32be6ae7c37b5eaefb605c03f729cd1f0e098991))
* **tests:** Add new test cases in test_tokenizer.py ([`f4f6eb8`](https://github.com/entelecheia/lexikanon/commit/f4f6eb8762fd690ac7b5b63835d856483ca6d567))
* **tests:** Add normalizer test case in lexikanon ([`ef1d8c9`](https://github.com/entelecheia/lexikanon/commit/ef1d8c950644ba321e793bc23421e50b3785a4fc))
* **lexikanon/utils/hanja:** Add table loading functionality ([`e3f14ee`](https://github.com/entelecheia/lexikanon/commit/e3f14ee7ec89cd5bf5b5fea66b0b974b8cb0e5e5))
* **lexikanon:** Add hanja translation support ([`36df26b`](https://github.com/entelecheia/lexikanon/commit/36df26bdc20ed06d8390eaa63729a047acf4d178))
* **hangul:** Add support for Hangul character operations ([`130c699`](https://github.com/entelecheia/lexikanon/commit/130c69945a0b55304c480783121a44bdd7109092))
* **lexikanon/utils/hanja:** Add new translation functionality ([`d35534b`](https://github.com/entelecheia/lexikanon/commit/d35534b0bac6f692d8527d8962978466f0102281))
* **lexikanon/utils:** Add hangle utilities to handle korean language ([`dba4474`](https://github.com/entelecheia/lexikanon/commit/dba44740d86693c0082ae7e8cf5d5ddaefe9dfb1))
* **lexikanon/utils:** Add new util file with various text processing functions ([`6fd05ec`](https://github.com/entelecheia/lexikanon/commit/6fd05ec13eb4395994f30a8ded08b68a6f5fd775))
* **tokenizers:** Add SimpleTokenizer, MecabTokenizer, NLTKTokenizer ([`6154fa0`](https://github.com/entelecheia/lexikanon/commit/6154fa0dfb8108bd9ce8bf93ea333a9fae6111d6))
* **tokenizers:** Add NLTKTokenizer and NLTKTagger classes ([`44aacd0`](https://github.com/entelecheia/lexikanon/commit/44aacd02f57e1d7666af081d4a47325f0dbacf95))
* **tokenizers:** Add MecabTokenizer and MecabTagger classes ([`23dec65`](https://github.com/entelecheia/lexikanon/commit/23dec65492a5cc72b1309b56fbfab305067c8116))
* **lexikanon/tokenizers:** Add base tokenizer methods ([`dc826d1`](https://github.com/entelecheia/lexikanon/commit/dc826d1a6de95b806e4d39c22fa0a0d9c2686170))
* **stopwords:** Add Stopwords class ([`3ae64af`](https://github.com/entelecheia/lexikanon/commit/3ae64af937b0196fce8f392a3d884b81b6fe32ad))
* **lexikanon/resources/dictionaries/mecab:** Add new ekon_v1 dictionary file ([`5a0cb8a`](https://github.com/entelecheia/lexikanon/commit/5a0cb8a4847bf6365958c6c0688768092996c24b))
* **lexikanon/normalizers:** Add new file normalizer.py with Normalizer class and associated configurations ([`94fda7f`](https://github.com/entelecheia/lexikanon/commit/94fda7fcc236ce591da6138af08cdd7fc9b25284))
* **lexikanon/normalizers:** Add Normalizer ([`342b781`](https://github.com/entelecheia/lexikanon/commit/342b781c5e896ec047d345bc8bd12d15f3533b8d))
* **lexikanon:** Add new tokenizer configuration ([`2c3ce80`](https://github.com/entelecheia/lexikanon/commit/2c3ce80147e88095dd8e44339d6332d3858ef216))
* **tokenizer:** Add nltk configuration files for tokenization and tagging ([`e700d9b`](https://github.com/entelecheia/lexikanon/commit/e700d9bb76f66bf90b43f3b80b512c9ec384541c))
* **tokenizer:** Add configuration for mecab tokenizer ([`05caee4`](https://github.com/entelecheia/lexikanon/commit/05caee47a9e8e82baeb92ee8738366d229286446))
* **tokenizer:** Add new tokenizer configuration file ([`ad9c0c2`](https://github.com/entelecheia/lexikanon/commit/ad9c0c2b150f1a895d947bf49fb93b07cb2306b8))
* **stopwords:** Add new stopwords configuration file ([`d403295`](https://github.com/entelecheia/lexikanon/commit/d403295b2810f0413d203a44db49001dcf056e3f))
* **normalizer:** Add new files for various character settings ([`2568cdd`](https://github.com/entelecheia/lexikanon/commit/2568cdda9cc17643f9ce1157192d44006fa93d9c))
* **dependencies:** Add ftfy, nltk and ekonlpy ([`6b68952`](https://github.com/entelecheia/lexikanon/commit/6b68952e7cd83f15735350518a84285c80466d87))

## v0.1.4 (2023-07-24)
### Fix
* **pyproject.toml:** Update package version and dependency versions ([`0f40b84`](https://github.com/entelecheia/lexikanon/commit/0f40b84db260930f8c862b44fbce9fc68b5c5f1a))

## v0.1.3 (2023-04-26)
### Fix
* Apply updated template ([`37a9567`](https://github.com/entelecheia/lexikanon/commit/37a956785ae2f2daca3168c9fba6a27abeb010b4))

## v0.1.2 (2023-04-21)
### Fix
* **version:** Disable scm-version ([`c929957`](https://github.com/entelecheia/lexikanon/commit/c9299570acf5ca49c365a2d24338560a8b667fa8))

## v0.1.1 (2023-04-21)
### Fix
* **version:** Add pre-commit command to make scm-version ([`fd61706`](https://github.com/entelecheia/lexikanon/commit/fd61706cd9a84f76bc8a5a071159060f5cb0e9c0))

## v0.1.0 (2023-04-21)
### Feature
* Initial version ([`eb58046`](https://github.com/entelecheia/lexikanon/commit/eb58046ad5e623f4b32b8f773527366494d0b6ae))
