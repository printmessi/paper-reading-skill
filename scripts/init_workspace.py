#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

from common import command_exists, ensure_dir, now_iso, run_git, write_json_atomic

RUNTIME_DIRS = [
    "topics",
    "papers",
    "deep-reading",
    "drafts",
    "state",
    "cache",
    "no-records",
    "logs",
]


def detect_default_apps() -> dict:
    home = Path.home()
    candidates = {
        "zotero": [],
        "obsidian": [],
    }
    if os.name == "nt":
        candidates["zotero"] = [
            Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Zotero" / "zotero.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Zotero" / "zotero.exe",
        ]
        candidates["obsidian"] = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Obsidian" / "Obsidian.exe",
        ]
    elif sys.platform == "darwin":
        candidates["zotero"] = [Path("/Applications/Zotero.app")]
        candidates["obsidian"] = [Path("/Applications/Obsidian.app")]
    else:
        candidates["zotero"] = [home / ".local/share/applications/zotero.desktop"]
        candidates["obsidian"] = [home / ".local/share/applications/obsidian.desktop"]

    return {
        name: [str(p) for p in paths if str(p) and p.exists()]
        for name, paths in candidates.items()
    }


def check_environment() -> dict:
    return {
        "python": {
            "ok": sys.version_info >= (3, 10),
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "git": {"ok": command_exists("git")},
        "apps_detected": detect_default_apps(),
        "platform": platform.platform(),
        "note": "检查不会安装软件或修改系统设置。",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="安全初始化论文阅读工作区。不会自动安装软件或修改系统设置。")
    ap.add_argument("--workspace", help="工作区路径")
    ap.add_argument("--obsidian-vault", default="", help="Obsidian Vault 路径（仅记录，不修改）")
    ap.add_argument("--research-root", default="Research", help="Vault 内研究根目录")
    ap.add_argument("--check-only", action="store_true", help="只做环境检查")
    ap.add_argument("--apply", action="store_true", help="实际创建工作区文件")
    ap.add_argument("--init-git", action="store_true", help="在工作区初始化 Git（需要 --apply）")
    args = ap.parse_args()

    report = check_environment()
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.check_only:
        return 0

    if not args.workspace:
        print("\n缺少 --workspace。未做任何修改。")
        return 2

    workspace = Path(args.workspace).expanduser().resolve()
    print("\n准备执行：")
    print(f"- 工作区：{workspace}")
    print(f"- 创建目录：{', '.join(RUNTIME_DIRS)}")
    print(f"- Obsidian Vault（仅记录）：{args.obsidian_vault or '未设置'}")
    print(f"- Research 根目录：{args.research_root}")
    print(f"- 初始化 Git：{'是' if args.init_git else '否'}")

    if not args.apply:
        print("\n这是预览。添加 --apply 后才会真正创建。")
        return 0

    ensure_dir(workspace)
    for d in RUNTIME_DIRS:
        ensure_dir(workspace / d)

    config = {
        "schema_version": 1,
        "created_at": now_iso(),
        "platform": sys.platform,
        "workspace": str(workspace),
        "obsidian_vault": str(Path(args.obsidian_vault).expanduser().resolve()) if args.obsidian_vault else "",
        "obsidian_research_root": args.research_root,
        "zotero": {
            "local_api": "http://127.0.0.1:23119/api",
            "library_prefix": "users/0",
            "bbt_json_rpc": "http://127.0.0.1:23119/better-bibtex/json-rpc",
            "never_write_sqlite": True,
        },
        "safety": {
            "proposal_then_confirm": True,
            "topic_only_obsidian_scan": True,
            "primary_paper_requires_user_pdf": True,
        },
    }
    write_json_atomic(workspace / "runtime-config.json", config)

    gitignore = workspace / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(
            "# Research workspace\n*.pdf\ncache/\nlogs/\n*.tmp\n.env\n.DS_Store\nThumbs.db\n",
            encoding="utf-8",
        )

    if args.init_git:
        code, out = run_git(["init"], workspace)
        print(f"Git init: code={code} {out}")

    print("\n初始化完成。下一步建议：创建研究主题。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
