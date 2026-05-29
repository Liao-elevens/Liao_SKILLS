# Liao Skills

Reusable agent skills maintained by Liao-elevens. This repository is a multi-skill collection for `skills.sh`, Codex, Cursor, and other tools that can read `SKILL.md`.

Each skill lives under:

```text
skills/<skill-name>/SKILL.md
```

## Skills

### ai-frontend-dev-rules

Technology-neutral frontend architecture rules for AI-assisted development.

Use it when creating, extending, refactoring, or reviewing frontend features. It covers module splitting, shared boundaries, routing, type/schema placement, API integration, state/data ownership, data mapping, UI library usage, performance checks, and change reporting.

## Install

Install a specific skill with:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill ai-frontend-dev-rules
```

Codex users can target Codex explicitly:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill ai-frontend-dev-rules -a codex
```

Cursor users can target Cursor explicitly:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill ai-frontend-dev-rules -a cursor
```

For a global Cursor install:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill ai-frontend-dev-rules -a cursor -g
```

Claude Code users can target Claude Code explicitly:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill ai-frontend-dev-rules -a claude-code
```

Manual Claude Code install also works by placing this folder in a Claude skills directory:

```text
skills/ai-frontend-dev-rules/ -> ~/.claude/skills/ai-frontend-dev-rules/
```

For a project-local install, use:

```text
skills/ai-frontend-dev-rules/ -> .claude/skills/ai-frontend-dev-rules/
```

Codex users can also use this repository as a Codex plugin. The plugin manifest is:

```text
.codex-plugin/plugin.json
```

## Use

Example prompts:

```text
Use $ai-frontend-dev-rules to implement this dashboard and keep the entry file thin.
```

```text
Use $ai-frontend-dev-rules to review this frontend change for module boundaries, API usage, state ownership, and UI library compatibility.
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

Then install it with:

```bash
npx skills add https://github.com/Liao-elevens/Liao_SKILLS --skill <skill-name>
```

## License

MIT. See [LICENSE](LICENSE).
