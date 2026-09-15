#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import ensure_dir, load_json, now_iso, topic_slug, write_json_atomic


def main() -> int:
    ap = argparse.ArgumentParser(description="创建研究主题。默认先预览，--apply 后才写入。")
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--obsidian-vault", default="")
    ap.add_argument("--research-root", default="Research")
    ap.add_argument("--create-obsidian-dirs", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    slug = topic_slug(args.topic)
    topic_dir = workspace / "topics" / slug
    state_dir = workspace / "state" / slug

    print("准备创建研究主题：")
    print(f"- 主题：{args.topic}")
    print(f"- 工作区目录：{topic_dir}")
    print(f"- 状态目录：{state_dir}")

    obsidian_topic = None
    if args.create_obsidian_dirs:
        if not args.obsidian_vault:
            print("--create-obsidian-dirs 需要 --obsidian-vault。未做修改。")
            return 2
        obsidian_topic = Path(args.obsidian_vault).expanduser().resolve() / args.research_root / args.topic
        print(f"- Obsidian 主题目录：{obsidian_topic}")
        print("  将创建 Papers / Concepts / Methods；MOC 仍由后续提案决定。")

    if not args.apply:
        print("\n这是预览。确认无误后加 --apply。")
        return 0

    ensure_dir(topic_dir)
    ensure_dir(state_dir)
    ensure_dir(topic_dir / "cache")
    ensure_dir(topic_dir / "drafts")

    meta = {
        "topic": args.topic,
        "slug": slug,
        "created_at": now_iso(),
        "next_number": 1,
        "obsidian_topic_dir": str(obsidian_topic) if obsidian_topic else "",
    }
    write_json_atomic(topic_dir / "topic.json", meta)

    if obsidian_topic:
        for d in ["Papers", "Concepts", "Methods"]:
            ensure_dir(obsidian_topic / d)

    print("创建完成。建议下一步：在 Zotero 中建立同名 Collection，并将论文加入后执行‘筛选论文’。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
