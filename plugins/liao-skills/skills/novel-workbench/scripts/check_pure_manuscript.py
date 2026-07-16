#!/usr/bin/env python3
"""检查正文目录是否残留内部元数据或作者说明。"""

from __future__ import annotations

import sys
from pathlib import Path


FORBIDDEN = (
    "章节备注",
    "本章概要",
    "作者说明",
    "写作说明",
    "<!--",
    "作者内部真相",
)


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python check_pure_manuscript.py <正文目录>")
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"❌ 正文目录不存在: {root}")
        return 1
    files = sorted(root.rglob("第*.md"))
    if not files:
        print("❌ 正文目录中没有章节文件")
        return 1
    failures = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        hits = [item for item in FORBIDDEN if item in text]
        if hits:
            print(f"❌ {path}: " + "、".join(hits))
            failures += 1
    if failures:
        return 1
    print(f"✅ 正文纯净检查通过: {len(files)} 章")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
