<!--next-version-placeholder-->

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
