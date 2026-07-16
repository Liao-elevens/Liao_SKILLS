#!/usr/bin/env python3
"""在临时目录中验证空白项目初始化到首章校验的最小闭环。"""

from __future__ import annotations

import json
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

from check_chapter_quality import main as quality_main
from check_chapter_wordcount import main as wordcount_main
from check_plan_consistency import main as consistency_main
from check_project_paths import main as paths_main
from check_pure_manuscript import main as pure_main
from init_novel_project import initialize_project


@contextmanager
def argv(*args: str):
    previous = sys.argv
    sys.argv = [previous[0], *args]
    try:
        yield
    finally:
        sys.argv = previous


def run(main, *args: str) -> None:
    with argv(*args):
        result = main()
    if result != 0:
        raise RuntimeError(f"测试步骤失败: {main.__module__} {args}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="novel-workbench-smoke-") as temporary:
        root = Path(temporary)
        project = initialize_project(
            root / "novel-projects",
            "《测试小说》",
            timestamp="20260101-010203",
        )
        assert project.name == "20260101-010203-测试小说"
        chapter = project / "正文/第一卷-测试/第01章-测试.md"
        chapter.parent.mkdir(parents=True)
        chapter.write_text("# 第01章：测试\n" + "字" * 3000 + "\n", encoding="utf-8")

        plan_path = project / "01-项目管理/章节写作计划-状态与范围.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["totalChapters"] = 1
        plan["projectStatus"] = "completed"
        plan["activeScope"].update({"endChapter": 1, "status": "completed"})
        plan["chapters"] = [
            {
                "chapterNumber": 1,
                "title": "测试",
                "path": "正文/第一卷-测试/第01章-测试.md",
                "status": "completed",
                "actualChineseChars": 3000,
                "checks": {"wordcount": True, "quality": True},
            }
        ]
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

        run(paths_main, str(project))
        run(consistency_main, str(project))
        run(pure_main, str(project / "正文"))
        run(wordcount_main, "--all", str(project / "正文"))
        run(quality_main, str(project / "正文"), "--all", "--min-dialogue", "0")

    print("✅ 空白项目端到端冒烟测试通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
