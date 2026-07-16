---
name: novel-workbench
description: |
  中文小说创作工作台：用于需求访谈、故事圣经、分卷大纲、逐章写作、续写、审核、精修和终稿整理。
  支持短篇、中篇、多卷长篇、群像、悬疑、惊悚、科幻、奇幻、现实和复合题材。用户要求创作小说、续写章节、完成指定卷或章节、建立写作流程、检查连续性、精修或整理出版稿时使用。
---

# 小说创作工作台

本 Skill 负责“可持续完成一部小说”的流程，不保存任何具体作品的角色、世界观或隐藏真相。具体作品资料必须写入项目目录。

偏好也属于项目配置的一部分：不得在工作区最外层创建或读取全局偏好文件。新项目在标题确认后，将偏好与内容边界写入该项目的 `01-项目管理/创作配置-偏好与内容边界.json`；续写时只读取当前项目自己的配置文件。

## 先判断任务类型

- **新建项目**：读取 [项目初始化](references/workflows/workflow-01-项目初始化与断点恢复.md)、[需求访谈](references/workflows/workflow-02-需求访谈与标题确认.md)、[故事圣经与大纲](references/workflows/workflow-03-故事圣经与大纲锁定.md) 和 [范围与模式](references/workflows/workflow-04-写作范围与模式确认.md)。
- **继续写作**：先读取 [项目初始化与断点恢复](references/workflows/workflow-01-项目初始化与断点恢复.md)，根据项目状态恢复，不重新询问已确认内容。
- **指定卷或章节范围**：先读取 [范围与模式](references/workflows/workflow-04-写作范围与模式确认.md) 和 [分卷审核闭环](references/workflows/workflow-06-分卷审核与跨卷精修.md)，建立硬范围后才写作。
- **逐章串行创作**：读取 [逐章串行创作闭环](references/workflows/workflow-05-逐章串行创作闭环.md)。
- **审核、精修或出版整理**：读取 [分卷审核闭环](references/workflows/workflow-06-分卷审核与跨卷精修.md) 和 [出版级精修](references/workflows/workflow-07-出版级精修与终稿打包.md)。
- **发生中断、路径错误或批量修改风险**：读取 [中断恢复与安全回滚](references/workflows/workflow-08-中断恢复与安全回滚.md)。

在空工作区中，只有用户明确要求使用本 Skill 创作小说时才创建项目；Skill 被加载本身不会自动创建目录。

空白项目的完整触发链、示例提示词和预期目录见 [空白项目完整使用说明](references/usage/使用说明-空白项目完整流程.md)。

## 不可违反的规则

1. 只创作和修改用户明确授权的章节范围；范围结束后停止，不自动扩写下一卷。
2. 写作前必须读取当前章节规划、出场人物档案、上一章状态和真相边界。
3. `正文/` 只存纯正文；概要、审核、作者备注、隐藏真相和过程记录不得写入正文文件。
4. 已确认的大纲视为锁定计划。写作产生的偏差写入“实际完成记录”，不要悄悄改写原计划。
5. 每章必须产生可观察的变化：行动、关系、信息、代价或状态至少推进一项；节奏指标按题材调整，不使用机械配额代替文学判断。
6. 隐藏真相只用于一致性校验，不能用全知说明提前泄露；概念首次出现要给读者足够的局部解释。
7. 任何批量移动、重命名或正文清理前，先建立可恢复的检查点；不能用未经验证的全局正则替换改写正文。
8. 校验失败先定位原因，再局部修复；最多三轮仍失败时记录阻塞原因，不伪造“已通过”。
9. 不承诺自动切换模型。创作模型和审核模型可记录在项目元数据中，但模型切换由用户或运行环境完成。

## 标准项目结构

```text
项目名/
├── 项目索引.md
├── 01-项目管理/
├── 02-故事圣经/
├── 03-大纲与分卷/
├── 04-连续性与伏笔/
├── 05-写作过程/
├── 正文/
├── 06-出版与审校/
└── 99-归档/
```

目录、状态字段和计划文件结构见 [项目目录与状态规范](references/standards/standard-项目目录与状态规范.md) 与 [写作计划结构规范](references/schemas/写作计划结构规范.json)。

## 标准闭环

```text
需求访谈
  → 故事圣经与大纲锁定
  → 创建活动范围
  → 逐章写作与即时校验
  → 分卷机械审核与人工冷读
  → 跨卷连续性精修
  → 出版级正文清理与终稿校验
```

## 写作与审核规范导航

- 章节结构、节奏与开篇：[章节结构与节奏](references/standards/standard-章节结构与节奏.md)
- 人物、群像与一致性：[人物群像与一致性](references/standards/standard-人物群像与一致性.md)
- 对话、潜台词与人味：[对话潜台词与人味](references/standards/standard-对话潜台词与人味.md)
- 悬念、伏笔和真相边界：[悬念伏笔与真相边界](references/standards/standard-悬念伏笔与真相边界.md)
- 多线结构和分卷收束：[情节结构与多线收束](references/standards/standard-情节结构与多线收束.md)
- 去注水和场景扩写：[场景扩写与去注水](references/standards/standard-场景扩写与去注水.md)
- 标题与题材定位：[标题与定位](references/standards/standard-标题与定位.md)

## 输出模板导航

- 纯正文单章：[纯正文单章](references/templates/template-纯正文单章.md)
- 角色档案：[角色档案](references/templates/template-角色档案.md)
- 总纲与分卷规划：[总纲与分卷规划](references/templates/template-总纲与分卷规划.md)
- 项目索引：[项目索引](references/templates/template-项目索引.md)
- 审核报告：[审核报告](references/templates/template-审核报告.md)

## 脚本使用原则

- [`check_chapter_wordcount.py`](scripts/check_chapter_wordcount.py)：检查单章或嵌套 `正文/` 的汉字数。
- [`check_chapter_quality.py`](scripts/check_chapter_quality.py)：检查机械表达、直接引语和禁止提前出现的术语；机械表达默认只做人工复核提醒。
- [`check_project_paths.py`](scripts/check_project_paths.py)：检查计划文件中的章节路径、章节编号和卷目录。
- [`check_plan_consistency.py`](scripts/check_plan_consistency.py)：检查计划、大纲、正文文件和状态字段是否一致。
- [`check_pure_manuscript.py`](scripts/check_pure_manuscript.py)：检查正文中是否残留章节备注、作者说明、HTML 注释或内部真相。
- [`migrate_plan_v1_to_v2.py`](scripts/migrate_plan_v1_to_v2.py)：迁移旧版计划；默认只预览，原地写回必须显式使用 `--force`。
- [`init_novel_project.py`](scripts/init_novel_project.py)：在用户指定的项目库中安全创建空白小说项目。
- [`smoke_test.py`](scripts/smoke_test.py)：在临时目录中验证从项目初始化到首章校验的最小闭环。

脚本只能提供证据，不能代替人物声音、视角纪律、因果链、概念可读性和悬疑公平性的人工冷读。
