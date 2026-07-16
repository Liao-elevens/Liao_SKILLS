#!/usr/bin/env python3
"""把旧版写作计划迁移为 schemaVersion 2；默认只预览，--force 才会原地写回。"""

from __future__ import annotations

import json
import argparse
import shutil
import sys
from pathlib import Path


def migrate(path: Path, *, dry_run: bool = False, force: bool = False) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schemaVersion") == 2:
        return path
    if not dry_run and not force:
        raise ValueError("原地迁移需要显式指定 --force；只预览请使用 --dry-run")
    backup = path.with_suffix(path.suffix + ".v1")
    if not dry_run and not backup.exists():
        shutil.copy2(path, backup)
    old_scope = data.get("writingScope", {})
    mode = data.get("writingMode", "serial")
    if mode in {"subagent-parallel", "agent-teams"}:
        mode = "parallel"
    chapters = []
    for item in data.get("chapters", []):
        chapters.append(
            {
                "chapterNumber": item.get("chapterNumber"),
                "title": item.get("title", ""),
                "path": item.get("path", item.get("filePath", "")),
                "status": item.get("status", "pending"),
                "actualChineseChars": item.get("actualChineseChars", item.get("wordCount")),
                "checks": {
                    "wordcount": item.get("wordCountPass"),
                    "quality": item.get("qualityPass"),
                    "continuity": item.get("continuityPass"),
                    "pureManuscript": item.get("pureManuscriptPass"),
                },
                "retryCount": item.get("retryCount", 0),
                "viewpoint": item.get("viewpoint"),
                "updatedAt": data.get("updatedAt", ""),
            }
        )
    new = {
        "schemaVersion": 2,
        "novelName": data.get("novelName", ""),
        "projectRoot": data.get("projectRoot", data.get("projectPath", "")),
        "totalChapters": data.get("totalChapters", len(chapters)),
        "chapterSpec": {
            "minChineseChars": data.get("minWordsPerChapter", 3000),
            "targetChineseChars": data.get("targetWordsPerChapter", 4000),
            "maxChineseChars": data.get("maxWordsPerChapter", 5000),
        },
        "createdAt": data.get("createdAt", ""),
        "updatedAt": data.get("updatedAt", ""),
        "projectStatus": data.get("projectStatus", data.get("status", "planning")),
        "mode": data.get("mode", mode),
        "activeScope": {
            "type": old_scope.get("type", "full_novel"),
            "startChapter": old_scope.get("startChapter", 1),
            "endChapter": old_scope.get("endChapter", data.get("totalChapters", len(chapters))),
            "stopAfterScope": old_scope.get("stopAfterScope", True),
            "status": old_scope.get("status", "pending"),
        },
        "scopeHistory": [old_scope] if old_scope else [],
        "chapters": chapters,
    }
    if dry_run:
        print(f"预览：{path} 将迁移 {len(chapters)} 章，原文件不会修改")
        return path
    path.write_text(json.dumps(new, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="旧版写作计划 JSON")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不修改文件")
    parser.add_argument("--force", action="store_true", help="确认原地写回并创建 .v1 备份")
    args = parser.parse_args()
    try:
        print(f"✅ 已迁移: {migrate(args.plan, dry_run=args.dry_run, force=args.force)}")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"❌ 迁移失败: {exc}", file=sys.stderr)
        raise SystemExit(1)
