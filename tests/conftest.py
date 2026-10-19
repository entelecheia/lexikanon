import os
import subprocess
import sys
from pathlib import Path

import pytest

KO = "금통위는 따라서 물가안정과 병행, 경기상황에 유의하는 금리정책을 펼쳐나가기로 했다고 밝혔다."
KO_HANJA = "IMF가 推定한 우리나라의 GDP갭률은 今年에도 소폭의 마이너스(−)를 持續하고 있다."
EN = (
    "Federal Reserve officials concluded their two-day policy meeting Wednesday by holding "
    "interest rates steady and signaling they expect to leave them unchanged for the "
    "foreseeable future."
)


@pytest.fixture
def workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty cwd without HYFI_* env, so ./conf and .hyfi/runs never touch the checkout."""
    monkeypatch.chdir(tmp_path)
    for key in list(os.environ):
        if key.startswith("HYFI_"):
            monkeypatch.delenv(key)
    return tmp_path


def hyfi_cli(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "hyfi", *args], cwd=cwd, capture_output=True, text=True
    )
