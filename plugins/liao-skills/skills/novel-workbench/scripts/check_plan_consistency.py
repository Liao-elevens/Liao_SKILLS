#!/usr/bin/env python3
"""检查计划中的状态、章节文件和字数字段是否一致。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def count_han(text: str) -> int:
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("#") and "章" in lines[0]:
        lines = lines[1:]
    return sum("\u4e00" <= char <= "\u9fff" for char in "\n".join(lines))


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python check_plan_consistency.py <项目目录>")
        return 2
    root = Path(sys.argv[1]).resolve()
    plan = root / "01-项目管理/章节写作计划-状态与范围.json"
    if not plan.exists():
        plan = root / "02-写作计划.json"
    if not plan.exists():
        print("❌ 找不到写作计划")
        return 1
    data = json.loads(plan.read_text(encoding="utf-8"))
    failures = 0
    for chapter in data.get("chapters", []):
        if chapter.get("status") != "completed":
            continue
        path_value = chapter.get("path", chapter.get("filePath", ""))
        path = root / path_value
        if not path.is_file():
            failures += 1
            print(f"❌ 缺失正文: 第{chapter.get('chapterNumber')}章")
            continue
        actual = count_han(path.read_text(encoding="utf-8"))
        recorded = chapter.get("actualChineseChars", chapter.get("wordCount"))
        if recorded is not None and actual != recorded:
            failures += 1
            print(f"❌ 字数不一致: 第{chapter.get('chapterNumber')}章 记录{recorded} / 实际{actual}")
    if failures:
        return 1
    print("✅ 计划与已完成正文一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
