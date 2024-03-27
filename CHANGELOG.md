<!--next-version-placeholder-->

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
