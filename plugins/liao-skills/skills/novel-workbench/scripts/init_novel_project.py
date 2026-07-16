#!/usr/bin/env python3
"""在指定小说项目库中安全创建一个空白小说项目。"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


PROJECT_DIRS = (
    "01-项目管理",
    "02-故事圣经",
    "03-大纲与分卷/分卷锁定",
    "04-连续性与伏笔",
    "05-写作过程/分卷审核",
    "05-写作过程/跨卷精修",
    "正文",
    "06-出版与审校",
    "99-归档",
)


def sanitize_title(title: str) -> str:
    """把用户标题转换为安全、可读的目录名。"""
    cleaned = title.strip().replace("《", "").replace("》", "")
    cleaned = re.sub(r"[\\/:*?\"<>|]", "-", cleaned)
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-+", "-", cleaned).strip("-.")
    return cleaned[:80] or "未命名小说"


def relative_project_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def initialize_project(
    projects_root: Path,
    title: str,
    timestamp: str | None = None,
    force: bool = False,
) -> Path:
    if not title.strip():
        raise ValueError("标题不能为空；请先完成标题确认")
    safe_title = sanitize_title(title)
    stamp = timestamp or datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    if not re.fullmatch(r"\d{8}-\d{6}", stamp):
        raise ValueError("timestamp 必须是 YYYYMMDD-HHmmss 格式")

    project_root = projects_root / f"{stamp}-{safe_title}"
    if project_root.exists() and not project_root.is_dir():
        raise FileExistsError(f"项目路径不是目录: {project_root}")
    if project_root.exists():
        if not force or any(project_root.iterdir()):
            raise FileExistsError(
                f"项目目录已存在且不为空: {project_root}；请更换时间戳或标题"
            )
    project_root.mkdir(parents=True, exist_ok=True)
    for directory in PROJECT_DIRS:
        (project_root / directory).mkdir(parents=True, exist_ok=True)

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    project_path = relative_project_path(project_root)
    index = f"""# 《{title.strip() or safe_title}》项目索引

## 当前状态

- 项目状态：`planning`
- 当前活动范围：尚未确认
- 下一步动作：完成需求访谈、标题确认和故事大纲

## 项目位置

- 项目目录：`{project_path}/`
- 正文目录：`正文/`
- 配置目录：`01-项目管理/`

## 目录职责

- `01-项目管理/`：项目元数据、创作配置和章节状态。
- `02-故事圣经/`：人物、世界观、概念、群像和作者真相。
- `03-大纲与分卷/`：锁定的大纲。
- `04-连续性与伏笔/`：连续性台账和伏笔矩阵。
- `05-写作过程/`：实际完成记录、审核和精修报告。
- `正文/`：只存纯正文。
- `06-出版与审校/`：出版级精修和终稿检查。
- `99-归档/`：旧版本和迁移备份。
"""
    (project_root / "项目索引.md").write_text(index, encoding="utf-8")
    (project_root / "正文/正文目录.md").write_text(
        f"# 《{title.strip() or safe_title}》正文目录\n\n项目规划完成后，在此记录卷目录和章节范围。\n",
        encoding="utf-8",
    )

    write_json(
        project_root / "01-项目管理/项目元数据-标题与规格.json",
        {
            "novelName": title.strip() or safe_title,
            "format": "待确认",
            "totalChapters": 0,
            "volumeCount": 0,
            "defaultMode": "serial",
            "chapterSpec": {
                "minChineseChars": 3000,
                "targetChineseChars": 4000,
                "maxChineseChars": 5000,
            },
            "contentScale": "待确认",
            "generationModel": None,
            "reviewModel": None,
            "createdAt": now,
        },
    )
    write_json(
        project_root / "01-项目管理/创作配置-偏好与内容边界.json",
        {
            "schemaVersion": 1,
            "updatedAt": now,
            "preferences": {
                "favoriteGenres": [],
                "preferredProtagonist": "",
                "preferredPerspective": "",
                "preferredTone": "",
                "typicalChapterCount": None,
                "styleReferences": [],
                "dislikes": [],
                "creationHistory": [],
            },
            "projectOverrides": {
                "novelName": title.strip() or safe_title,
                "contentBoundaries": [],
                "hardConstraints": [],
            },
        },
    )
    write_json(
        project_root / "01-项目管理/章节写作计划-状态与范围.json",
        {
            "schemaVersion": 2,
            "novelName": title.strip() or safe_title,
            "projectRoot": project_path,
            "totalChapters": 0,
            "chapterSpec": {
                "minChineseChars": 3000,
                "targetChineseChars": 4000,
                "maxChineseChars": 5000,
            },
            "createdAt": now,
            "updatedAt": now,
            "projectStatus": "planning",
            "mode": "serial",
            "activeScope": {
                "type": "full_novel",
                "startChapter": 1,
                "endChapter": 0,
                "stopAfterScope": True,
                "status": "pending",
            },
            "scopeHistory": [],
            "chapters": [],
        },
    )
    return project_root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="已确认的小说标题")
    parser.add_argument(
        "--projects-root",
        type=Path,
        default=Path("novel-projects"),
        help="小说项目库目录，默认 novel-projects",
    )
    parser.add_argument("--timestamp", help="测试或迁移时使用 YYYYMMDD-HHmmss")
    parser.add_argument("--force", action="store_true", help="仅允许复用空目录")
    args = parser.parse_args()
    try:
        project = initialize_project(
            args.projects_root,
            args.title,
            timestamp=args.timestamp,
            force=args.force,
        )
    except (FileExistsError, ValueError) as exc:
        print(f"❌ 创建失败: {exc}")
        return 1
    print(f"✅ 项目已创建: {project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
