#!/usr/bin/env python3
"""检查 v2 写作计划中的章节路径、编号和文件存在性。"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python check_project_paths.py <项目目录>")
        return 2
    root = Path(sys.argv[1]).resolve()
    candidates = [
        root / "01-项目管理/章节写作计划-状态与范围.json",
        root / "01-项目管理/章节写作计划.json",
        root / "02-写作计划.json",
    ]
    plan = next((path for path in candidates if path.exists()), None)
    if plan is None:
        print("❌ 找不到写作计划 JSON")
        return 1
    try:
        data = json.loads(plan.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"❌ JSON 无法解析: {exc}")
        return 1

    chapters = data.get("chapters", [])
    failures = 0
    numbers = []
    project_root = root.resolve()
    manuscript_root = (root / "正文").resolve()
    for chapter in chapters:
        number = chapter.get("chapterNumber")
        path_value = chapter.get("path", chapter.get("filePath", ""))
        numbers.append(number)
        if not isinstance(path_value, str) or not path_value:
            print(f"❌ 第{number}章没有有效路径")
            failures += 1
            continue
        target = (root / path_value).resolve()
        try:
            target.relative_to(project_root)
            target.relative_to(manuscript_root)
        except ValueError:
            print(f"❌ 第{number}章路径必须位于项目正文目录内: {path_value}")
            failures += 1
            continue
        if not target.is_file():
            print(f"❌ 第{number}章路径不存在: {path_value}")
            failures += 1
    if any(not isinstance(number, int) for number in numbers):
        print("❌ 章节编号必须是整数")
        failures += 1
    elif numbers != sorted(numbers) or len(numbers) != len(set(numbers)):
        print("❌ 章节编号不是递增且唯一")
        failures += 1
    total = data.get("totalChapters")
    if isinstance(total, int) and total != len(chapters):
        print(f"❌ totalChapters={total} 与章节记录数={len(chapters)} 不一致")
        failures += 1
    if not (root / "正文").is_dir():
        print("❌ 缺少正文目录")
        failures += 1
    if failures:
        return 1
    print(f"✅ 路径通过: {len(chapters)} 章")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
