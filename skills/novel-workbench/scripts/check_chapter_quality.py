#!/usr/bin/env python3
"""检查中文小说章节的直接引语比例与常见机械表达。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


AI_TERMS = (
    "此外",
    "然而",
    "值得注意的是",
    "需要强调的是",
    "不可忽视",
    "彰显",
    "诠释",
    "赋能",
    "映射",
    "折射",
    "不禁",
    "油然而生",
    "心潮澎湃",
)

HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
DIALOGUE_RE = re.compile(r"“(.*?)”", re.S)


def read_main_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = COMMENT_RE.sub("", text)
    lines = text.splitlines()
    if lines and lines[0].lstrip().startswith("#") and "章" in lines[0]:
        lines = lines[1:]
    return "\n".join(lines)


def count_han(text: str) -> int:
    return len(HAN_RE.findall(text))


def inspect(
    path: Path,
    minimum_dialogue: float,
    forbidden: list[str],
    fail_on_style: bool,
) -> dict:
    text = read_main_text(path)
    total = count_han(text)
    dialogue = sum(count_han(match) for match in DIALOGUE_RE.findall(text))
    ratio = dialogue / total if total else 0.0
    ai_hits = [term for term in AI_TERMS if term in text]
    forbidden_hits = [term for term in forbidden if term and term in text]
    passed = (
        total > 0
        and ratio >= minimum_dialogue
        and not forbidden_hits
        and (not fail_on_style or not ai_hits)
    )
    return {
        "path": path,
        "total": total,
        "dialogue": dialogue,
        "ratio": ratio,
        "ai_hits": ai_hits,
        "forbidden_hits": forbidden_hits,
        "passed": passed,
    }


def collect_paths(
    target: Path,
    all_files: bool,
    start_chapter: int | None,
    end_chapter: int | None,
) -> list[Path]:
    if all_files:
        paths = sorted(target.rglob("第*.md"))
        if start_chapter is None and end_chapter is None:
            return paths

        scoped_paths = []
        for path in paths:
            match = re.match(r"第(\d+)章", path.name)
            if not match:
                continue
            chapter = int(match.group(1))
            if start_chapter is not None and chapter < start_chapter:
                continue
            if end_chapter is not None and chapter > end_chapter:
                continue
            scoped_paths.append(path)
        return scoped_paths
    return [target]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="章节文件或章节目录")
    parser.add_argument("--all", action="store_true", help="检查目录内所有第*.md章节")
    parser.add_argument("--start-chapter", type=int, help="--all 时只检查起始章及以后")
    parser.add_argument("--end-chapter", type=int, help="--all 时只检查结束章及以前")
    parser.add_argument("--min-dialogue", type=float, default=0.30, help="最低直接引语比例，默认0.30")
    parser.add_argument("--forbid", action="append", default=[], help="禁止出现的术语，可重复使用")
    parser.add_argument(
        "--fail-on-style",
        action="store_true",
        help="把常见机械表达从人工复核提醒升级为不通过",
    )
    args = parser.parse_args()

    if not args.all and (args.start_chapter is not None or args.end_chapter is not None):
        parser.error("--start-chapter/--end-chapter 只能与 --all 一起使用")
    if (
        args.start_chapter is not None
        and args.end_chapter is not None
        and args.start_chapter > args.end_chapter
    ):
        parser.error("起始章不能大于结束章")

    paths = collect_paths(
        args.target,
        args.all,
        args.start_chapter,
        args.end_chapter,
    )
    if not paths:
        print("没有找到章节文件", file=sys.stderr)
        return 2

    failures = 0
    for path in paths:
        if not path.is_file():
            print(f"❌ {path}: 文件不存在")
            failures += 1
            continue
        result = inspect(path, args.min_dialogue, args.forbid, args.fail_on_style)
        icon = "✅" if result["passed"] else "❌"
        print(
            f"{icon} {path.name}: 直接引语 {result['ratio']:.1%} "
            f"({result['dialogue']}/{result['total']})"
        )
        if result["ai_hits"]:
            label = "机械表达（不通过）" if args.fail_on_style else "机械表达（人工复核）"
            print(f"   {label}: " + "、".join(result["ai_hits"]))
        if result["forbidden_hits"]:
            print("   禁止术语: " + "、".join(result["forbidden_hits"]))
        if result["ratio"] < args.min_dialogue:
            print(f"   低于要求: {args.min_dialogue:.1%}")
        failures += 0 if result["passed"] else 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
