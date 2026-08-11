# Liao Skills

[![skills.sh](https://skills.sh/b/Liao-elevens/Liao_SKILLS)](https://skills.sh/Liao-elevens/Liao_SKILLS)

Reusable agent skills maintained by Liao-elevens. This repository is a multi-skill collection for `skills.sh`, Codex, Cursor, and other tools that can read `SKILL.md`.

Each skill lives under:

```text
skills/<skill-name>/SKILL.md
```

## Skills

| Skill | Purpose | Use when |
| --- | --- | --- |
| [`ai-frontend-dev-rules`](skills/ai-frontend-dev-rules/SKILL.md) | Technology-neutral frontend architecture rules. | Creating, refactoring, or reviewing frontend features. |
| [`agent-skill-security-auditor`](skills/agent-skill-security-auditor/SKILL.md) | Lightweight V2 security auditor for agent skills. | Reviewing skills before installation, publication, update, or merge. |
| [`novel-workbench`](skills/novel-workbench/references/usage/使用说明-空白项目完整流程.md) | End-to-end Chinese novel creation workbench. | Planning, drafting, continuing, reviewing, polishing, or packaging Chinese fiction. |
| [`reliable-task-execution`](skills/reliable-task-execution/references/usage/使用说明.md) | Reliability workflow for requirement refinement, planning, authorization, execution, and validation. | Making project changes or handling complex, ambiguous, multi-step, or high-impact tasks. |

## Install

Install a specific skill with:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill <skill-name>
```

For example, install `novel-workbench` with:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill novel-workbench
```

Codex users can target Codex explicitly:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill <skill-name> -a codex
```

Cursor and Claude Code users can target their agent explicitly:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill <skill-name> -a cursor
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill <skill-name> -a claude-code
```

Use `-g` for a global install:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill <skill-name> -a <agent> -g
```

Manual Claude Code install also works by placing this folder in a Claude skills directory:

```text
skills/<skill-name>/ -> ~/.claude/skills/<skill-name>/
```

For a project-local install, use:

```text
skills/<skill-name>/ -> .claude/skills/<skill-name>/
```

Codex users can also use this repository as a Codex plugin marketplace. The marketplace entry points to the self-contained plugin package:

```text
plugins/liao-skills/.codex-plugin/plugin.json
```

Add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add Liao-elevens/Liao_SKILLS --ref main
```

Then install the `Liao Skills` plugin from the Codex plugin directory. After installation, use:

```text
$ai-frontend-dev-rules
$agent-skill-security-auditor
$novel-workbench
$reliable-task-execution
```

OpenAI's official public Plugin Directory does not currently support self-serve third-party publishing. This repository is prepared for Git-backed marketplace distribution and future official review by including Codex plugin metadata, marketplace metadata, privacy terms, display assets, and install instructions.

## Use

Example prompts:

```text
Use $ai-frontend-dev-rules to implement this dashboard and keep the entry file thin.
```

```text
Use $ai-frontend-dev-rules to review this frontend change for module boundaries, API usage, state ownership, and UI library compatibility.
```

```text
Use $agent-skill-security-auditor to review this third-party skill before I install it.
```

```text
Use $agent-skill-security-auditor to audit the skill I am about to publish and suggest fixes for any security findings.
```

```text
Use $novel-workbench to plan and write a Chinese novel from the initial interview through final manuscript packaging.
```

```text
Use $reliable-task-execution to align this change, obtain execution authorization, and verify the result.
```

```text
Use $reliable-task-execution to brainstorm this rough feature idea and turn it into an actionable design.
```

```text
Use $reliable-task-execution to grill this architecture proposal, expose weak assumptions, and then red-team the resulting plan.
```

## Notes

- `skills/` is the source directory in this repository.
- Platform-specific folders such as `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, or `~/.codex/skills/` are installation targets created by local tooling.
- This repository intentionally avoids duplicating rules into platform-specific formats unless a future platform requires a separate adapter.

## Add A Skill

Add each new skill as a separate folder:

```text
skills/<skill-name>/SKILL.md
```

## License

MIT. See [LICENSE](LICENSE).
