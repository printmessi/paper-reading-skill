#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERN = re.compile(r"^(\d{3})-")


def scan_numbers(paths: list[Path]) -> list[int]:
    nums: list[int] = []
    for base in paths:
        if not base.exists():
            continue
        for p in base.glob("*.md"):
            m = PATTERN.match(p.name)
            if m:
                nums.append(int(m.group(1)))
    return nums


def main() -> int:
    ap = argparse.ArgumentParser(description="计算研究主题内下一个论文编号。只读。")
    ap.add_argument("paths", nargs="+", help="要扫描的 Papers/草稿目录")
    args = ap.parse_args()
    nums = scan_numbers([Path(x).expanduser().resolve() for x in args.paths])
    print(f"{(max(nums) + 1 if nums else 1):03d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
