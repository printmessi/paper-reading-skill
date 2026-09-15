from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_dir(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_json(path: str | Path, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json_atomic(path: str | Path, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=str(p.parent))
    os.close(fd)
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, p)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def run_git(args: list[str], cwd: str | Path) -> tuple[int, str]:
    if not command_exists("git"):
        return 127, "git not found"
    cp = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    out = (cp.stdout + cp.stderr).strip()
    return cp.returncode, out


def safe_filename(text: str, max_len: int = 100) -> str:
    text = re.sub(r"[<>:\\|?*\"/]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    if not text:
        return "Untitled"
    return text[:max_len].rstrip(" .")


def topic_slug(topic: str) -> str:
    # Keep Unicode so Chinese topic names remain readable on Windows/macOS.
    s = safe_filename(topic, 80)
    return re.sub(r"\s+", "-", s)


def normalize_status(status: str) -> str:
    mapping = {
        "待读": "状态/待读",
        "No": "状态/No",
        "no": "状态/No",
        "精读": "状态/精读",
        "整理": "状态/整理",
        "已读": "状态/已读",
    }
    return mapping.get(status, status)


VALID_STATUSES = {
    "状态/待读",
    "状态/No",
    "状态/精读",
    "状态/整理",
    "状态/已读",
}
