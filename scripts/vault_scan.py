#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def scan(root: Path, terms: list[str]) -> list[dict]:
    results = []
    lowered = [t.lower() for t in terms if t.strip()]
    for p in root.rglob("*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        low = text.lower()
        hits = [t for t in lowered if t in low or t in p.stem.lower()]
        if not lowered or hits:
            results.append({
                "path": str(p),
                "title": p.stem,
                "matched_terms": hits,
                "wikilinks": sorted(set(WIKILINK.findall(text)))[:50],
            })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="只扫描指定 Obsidian 主题目录，不扫描整个 Vault。")
    ap.add_argument("--topic-dir", required=True)
    ap.add_argument("--term", action="append", default=[])
    args = ap.parse_args()
    root = Path(args.topic_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(json.dumps({"error": "topic-dir 不存在", "path": str(root)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(scan(root, args.term), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
