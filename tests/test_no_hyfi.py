"""AC1: the library imports and works without hyfi (or Hydra/OmegaConf) installed."""

import re
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).parents[1] / "src" / "lexikanon"

BLOCKED_SCRIPT = """
import sys

BLOCKED = {"hyfi", "hydra", "omegaconf"}


class Block:
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] in BLOCKED:
            raise ImportError(f"blocked for this test: {name}")


sys.meta_path.insert(0, Block())

import lexikanon
import lexikanon.normalizers
import lexikanon.pipes.similarity
import lexikanon.pipes.tokenize
import lexikanon.stopwords
import lexikanon.tokenizers
import lexikanon.utils
from lexikanon.normalizers import Normalizer
from lexikanon.pipes.tokenize import tokenize_texts
from lexikanon.tokenizers import MecabTokenizer

assert tokenize_texts("a b") == [["a", "b"]]
assert MecabTokenizer().tokenize("물가안정")[:2] == ["물가/NNG", "안정/NNG"]
assert Normalizer(hanja2hangle=True)("今年") == "금년"
loaded = sorted(m for m in sys.modules if m.split(".")[0] in BLOCKED)
assert not loaded, loaded
print("ok")
"""


def test_imports_without_hyfi() -> None:
    r = subprocess.run([sys.executable, "-c", BLOCKED_SCRIPT], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "ok"


def test_no_hyfi_import_in_library_code() -> None:
    pattern = re.compile(r"^\s*(import|from)\s+(hyfi|hydra|omegaconf)\b", re.M)
    offenders = [
        str(p.relative_to(SRC))
        for p in SRC.rglob("*.py")
        if pattern.search(p.read_text(encoding="utf-8"))
    ]
    assert offenders == []
