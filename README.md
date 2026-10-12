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
| [`ai-frontend-dev-rules`](skills/ai-frontend-dev-rules/SKILL.md) | Framework-neutral rules for readable frontend code and practical module boundaries. | Creating, refactoring, or reviewing frontend features. |
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

Codex users can also use this repository as a Codex plugin marketplace. The repository root is the plugin root. The marketplace entry in [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) uses `source.path: "./"`, and the single plugin manifest is:

```text
.codex-plugin/plugin.json
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

The manifest explicitly lists the four skills shown above. Other directories under `skills/` are not automatically exposed by the Codex plugin. This loading allowlist does not hide files committed to the Git repository from other installers or repository readers.

This layout requires a client that supports both a marketplace entry at `./` and an array of skill paths. Discovery and loading were verified with the desktop-bundled Codex `0.162.0-alpha.17.2`. Codex CLI `0.132.0` does not support this combination and may show no plugin; use a compatible client before installation. These checks do not constitute a fresh installation or update of a user's installed plugin.

This repository uses Git-backed marketplace distribution. Submission to the public plugin directory is a separate release process; see [OpenAI's submission documentation](https://developers.openai.com/plugins/deploy/submission).

## Use

Example prompts:

```text
Use $ai-frontend-dev-rules to implement this dashboard with concise code, grouped helpers, and appropriate module boundaries.
```

```text
Use $ai-frontend-dev-rules to review this frontend change for naming, control flow, helper grouping, state ownership, and framework compatibility.
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

- `skills/` is the only maintained skill source directory. There is no duplicate distribution tree to synchronize.
- `.codex-plugin/plugin.json` is the single plugin manifest; its `skills` array is the explicit publication/loading list.
- Platform-specific folders such as `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, or `~/.codex/skills/` are installation targets created by local tooling.
- This repository intentionally avoids duplicating rules into platform-specific formats unless a future platform requires a separate adapter.

## Validate Changes

Run these checks from the repository root:

```bash
python3 scripts/check_plugin.py
python3 scripts/test_check_plugin.py
```

The first command is read-only and checks the root marketplace entry, explicit skill paths, assets, and local Markdown links in published skills and repository documentation. It does not scan unlisted skills, install the plugin, access the network, or modify user configuration. The second command exercises failure cases in temporary fixtures.

Before releasing a packaging change, also verify discovery and the exposed skill list with a compatible Codex client. Increment the single manifest version for a release and update the installed plugin through the normal client workflow; editing source files alone does not update every existing installation.

## Add A Skill

Add each new skill as a separate folder:

```text
skills/<skill-name>/SKILL.md
```

An existing skill needs edits only in this location. To include a new skill in the Codex plugin, explicitly add its directory to the manifest's `skills` array and update the published skill list above after it is ready. `glassmorphism-ui-style` and `learn-assessment` remain outside the current plugin list.

## License

MIT. See [LICENSE](LICENSE).
