# Review instructions

Read by the required OCR delegation reviewer (Claude Code, Codex, or Kimi Code), additional `/codex:review` or `/code-review` passes, and human reviewers alike.

## Passes

Run these passes and tag every finding with its pass:

- Bugs: logic errors, broken edge cases, regressions.
- Security: HyFI configs choose which Python callables run. Look for config values that reach `eval`, `importlib`, or shell calls without going through `hyfi.instantiate` and its allowlist.
- Compliance: the change matches issue #118 (spec and decision table). Workflow changes (`.github/workflows/`) are checked against the workspace CI standard: every job has `timeout-minutes`, PR runs cancel in progress, docs-only changes skip the test matrix but still run the docs build, actions are pinned by SHA.
- Instruction prose (AGENTS.md, REVIEW.md): does each directive name the failure it prevents? Nits unless runtime behavior changes.

## Repo focus

- Tokenizer and normalizer output is the product. Any change to `tests/data/*_1x.json`, or to code that alters tokens for those inputs without a new pinned test and a stated reason, is Important.
- `ekonlpy>=2.2` (was `==2.0.6`): a change to that floor, a new upper cap, or a lock bump of ekonlpy, fugashi, mecab-ko-dic, or nltk must keep `tests/test_outputs.py` passing unchanged; flag any change that edits that test instead.
- No `hyfi`, `hydra`, or `omegaconf` import under `src/lexikanon/` (`tests/test_no_hyfi.py`).
- Every config node that builds an object has a `_target_` under `lexikanon.*` or `nltk.stem.*`; a new target outside those needs a line in the docs' allowlist note (`docs/usage.md`).
- `Stopwords.stopwords_fn` takes callables only; strings are rejected (0.x eval'd them, bypassing the allowlist). Reintroducing any `eval`/`exec` of config values is Important.

## Findings

Each finding carries its pass, severity, evidence (`file:line` or a reproduction), and provenance: introduced by this change, pre-existing, or indeterminate. Pre-existing findings go to a follow-up issue instead of widening the change. Report what was reviewed and what was not reached.

## Re-review

Hand the reviewer the diff, the spec, and this file, and let it read the rest of the repo (AGENTS.md included). Do not hand it fix-status claims, earlier dispositions, or do-not-reflag notes.

## Cap the nits

Report at most 5 nits per review; summarize the rest as a count.

## Do not report

- Generated paths: `uv.lock` (style only), `CHANGELOG.md`, `src/lexikanon/_version.py`.
- Vendored helpers under `src/lexikanon/utils/hanja/` and `utils/hangle.py`, unless the change touches them.
- Anything CI already enforces: `uv lock --locked`, ruff check and format, mypy, pytest with the coverage floor, strict mkdocs build.
