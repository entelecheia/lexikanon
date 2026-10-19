# lexikanon

Korean and English tokenizers, normalizers, and stopwords as a plain Pydantic library (`src/lexikanon/`), plus HyFI 2.0 config groups in `src/lexikanon/conf/` registered through the `hyfi.plugins` entry point.

Design and decisions: issue #118 (the spec). Change the spec before the code when they disagree.

## Commands

- Install: `make install` (uv sync with all dependency groups)
- Lint: `make lint` (`uv lock --locked`, ruff check, ruff format --check, mypy on `src/lexikanon`)
- Test: `make test` (pytest with coverage, fails under the floor in `pyproject.toml`)
- Docs: `make docs-test` (strict mkdocs build)

## Verifying your work

```bash
make verify
```

Healthy output ends with `Required test coverage of 55.0% reached` and `N passed`. Run it before reporting any change complete and paste the tail. Fix the code when a test fails, never the test or the threshold. Tests download NLTK data; set `NLTK_DATA` to a scratch directory to keep it out of your home.

## Conventions

- Python `>=3.11`; ruff targets py311, line length 100. Development pins 3.13 (`.python-version`).
- Library modules never import `hyfi`, `hydra`, or `omegaconf`; HyFI wiring lives only in `conf/*.yaml`. Enforced by `tests/test_no_hyfi.py`.
- `tests/data/outputs_1x.json` and `composed_1x.json` are recorded 0.6.5 results. Never regenerate them to make a test pass; an intended output change gets its own test and a stated reason.
- Workflow examples in `conf/workflow/` are prefixed `lexikanon_` so they do not collide with other plugins.
- Conventional commits; python-semantic-release versions from tags on the `release` branch. Never hand-edit `src/lexikanon/_version.py` or the version in `pyproject.toml`.
- `uv.lock` is committed; re-run `uv lock` after editing dependencies or `make lint` fails.

## Things the agent gets wrong

- 2026-10-19, config defaults vs class defaults: 0.x `Normalizer` composed `normalizer/default.yaml` on construction, so its class defaults must equal that file. Change both together. Revisit if `Normalizer` gets a second preset source.
- 2026-10-19, fugashi has no cp315 wheel: Python 3.15 builds it from source and needs `libmecab-dev` (CI installs it). Do not drop 3.15 from the matrix because a local build fails. Revisit when fugashi ships cp315 wheels.

---

Contract and update rule for this file: `_meta/rules/development-lifecycle.md` §6 in the workspace repo. When the same mistake appears twice, add the correction here in the same PR.
