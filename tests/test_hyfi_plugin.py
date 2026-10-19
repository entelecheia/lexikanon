"""AC2: HyFI 2.0 discovers the lexikanon config groups and runs the workflow examples."""

import json
from pathlib import Path
from typing import Any

import hyfi
import pytest
from hyfi.workflow import Workflow, execute

from .conftest import KO, hyfi_cli
from .test_outputs import GOLDEN

WORKFLOWS = sorted(
    p.stem for p in (Path(__file__).parents[1] / "src/lexikanon/conf/workflow").glob("*.yaml")
)


def run_example(name: str, *overrides: str) -> Any:
    cfg = hyfi.to_dict(hyfi.compose([f"workflow={name}", *overrides]))
    workflow = Workflow.model_validate(cfg["workflow"])
    workflow.steps = [s for s in workflow.steps if s.run != "builtins.print"]
    result, records = execute(workflow)
    assert [r.status for r in records] == ["ok"] * len(records)
    return result


def test_plugins_lists_lexikanon(workdir: Path) -> None:
    r = hyfi_cli("plugins", "--json", cwd=workdir)
    assert r.returncode == 0, r.stderr
    row = {"name": "lexikanon", "module": "lexikanon.conf", "distribution": "lexikanon"}
    assert {**row, "available": True} in json.loads(r.stdout)


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [([], "'금통위는', '따라서'"), (["tokenizer=mecab"], "'금통위/NNG', '는/JX'")],
)
def test_hyfi_run_tokenizes_sample_text(workdir: Path, overrides: list[str], expected: str) -> None:
    r = hyfi_cli("run", "workflow=lexikanon_tokenize_text", *overrides, cwd=workdir)
    assert r.returncode == 0, r.stderr
    assert expected in r.stdout
    assert len(list(workdir.glob(".hyfi/runs/*/manifest.json"))) == 1


@pytest.mark.parametrize("name", WORKFLOWS)
def test_workflow_examples_resolve(workdir: Path, name: str) -> None:
    r = hyfi_cli("run", f"workflow={name}", "--dry-run", "--json", cwd=workdir)
    assert r.returncode == 0, r.stdout + r.stderr
    assert all(step["ok"] for step in json.loads(r.stdout)["steps"])


def test_tokenize_text_example(workdir: Path) -> None:
    assert run_example("lexikanon_tokenize_text", "tokenizer=mecab")[0][:2] == [
        "금통위/NNG",
        "는/JX",
    ]


def test_tokenize_dataset_example(workdir: Path) -> None:
    data = run_example("lexikanon_tokenize_dataset", "tokenizer=mecab")
    assert data["text"][0] == KO
    assert data["nouns"][0] == GOLDEN["tokenizer/mecab/nouns"]
    assert len(data["nouns"]) == 2


def test_find_similar_docs_example(workdir: Path) -> None:
    data = run_example("lexikanon_find_similar_docs")
    assert data["duplicate"].tolist() == [False, True, False, True]


@pytest.mark.parametrize(
    ("group", "name", "cls"),
    [
        ("tokenizer", "nltk_universal", "NLTKTokenizer"),
        ("normalizer", "informal_ko", "Normalizer"),
        ("stopwords", "default", "Stopwords"),
    ],
)
def test_groups_instantiate(group: str, name: str, cls: str) -> None:
    obj = hyfi.instantiate(hyfi.compose_group(group, name), allow=["lexikanon.*", "nltk.*"])
    assert type(obj).__name__ == cls
