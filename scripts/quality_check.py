#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_DEEP = [
    "论文核心问题",
    "方法",
    "关键理论与公式",
    "实验",
    "创新",
    "局限",
    "主动回忆",
]

DANGEROUS_PATTERNS = [
    r"PDF p\.\?",
    r"Paper p\.\?",
    r"Eq\. \(\?\)",
]


def check_md(path: Path) -> dict:
    if not path.exists():
        return {"ok": False, "error": "文件不存在", "path": str(path)}
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [x for x in REQUIRED_DEEP if x not in text]
    placeholders = [p for p in DANGEROUS_PATTERNS if re.search(p, text)]
    evidence_labels = [
        "【原文明确】",
        "【根据原文分析】",
        "【外部证据】",
        "【AI 分析】",
        "【待核验】",
        "【暂无】",
    ]
    return {
        "ok": not missing,
        "path": str(path),
        "missing_sections_or_terms": missing,
        "unresolved_locator_placeholders": placeholders,
        "evidence_labels_present": [x for x in evidence_labels if x in text],
        "warnings": [
            "出现 ? 定位占位符时，正式写入前必须改为准确定位或明确标注待核验。"
        ] if placeholders else [],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="轻量检查深度精读稿的结构与未解决定位。")
    ap.add_argument("md_file")
    args = ap.parse_args()
    report = check_md(Path(args.md_file).expanduser().resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
