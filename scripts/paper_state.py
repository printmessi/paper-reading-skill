#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import VALID_STATUSES, load_json, normalize_status, now_iso, topic_slug, write_json_atomic


def state_path(workspace: Path, topic: str, citekey: str) -> Path:
    return workspace / "state" / topic_slug(topic) / f"{citekey}.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="管理单篇论文跨会话状态。")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("create")
    p.add_argument("--workspace", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--citekey", required=True)
    p.add_argument("--zotero-item-key", default="")
    p.add_argument("--title", default="")

    p = sub.add_parser("show")
    p.add_argument("--workspace", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--citekey", required=True)

    p = sub.add_parser("set")
    p.add_argument("--workspace", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--citekey", required=True)
    p.add_argument("--field", required=True)
    p.add_argument("--value", required=True)

    args = ap.parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    path = state_path(workspace, args.topic, args.citekey)

    if args.cmd == "create":
        if path.exists():
            print(path.read_text(encoding="utf-8"))
            return 0
        data = {
            "citekey": args.citekey,
            "zotero_item_key": args.zotero_item_key,
            "title": args.title,
            "topic": topic_slug(args.topic),
            "paper_type": [],
            "status": "状态/待读",
            "screening": "pending",
            "deep_reading": "pending",
            "knowledge_integration": "pending",
            "obsidian_note": None,
            "zotero_status_suggestion": "状态/待读",
            "updated_at": now_iso(),
        }
        write_json_atomic(path, data)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    data = load_json(path)
    if data is None:
        print(f"状态文件不存在：{path}")
        return 2

    if args.cmd == "show":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if args.field == "status":
        value = normalize_status(args.value)
        if value not in VALID_STATUSES:
            print(f"非法状态：{value}")
            return 2
    else:
        value = args.value
    data[args.field] = value
    data["updated_at"] = now_iso()
    write_json_atomic(path, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
