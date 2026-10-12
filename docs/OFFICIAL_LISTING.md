# Official Listing Draft

This file keeps public-directory listing copy and release checks ready for a future official Codex Plugin Directory submission.

## Plugin

- Name: `liao-skills`
- Display name: `Liao Skills`
- Category: `Developer Tools`
- Publisher: `Liao-elevens`
- Repository: `https://github.com/Liao-elevens/Liao_SKILLS`
- Website: `https://github.com/Liao-elevens/Liao_SKILLS`
- License: `MIT`

## Short Description

Reliable task execution, coding, security, and Chinese novel writing workflows.

## Long Description

Liao Skills packages reusable Codex skills for reliable task execution, coding, security review, and creative writing. `reliable-task-execution` aligns execution authorization, planning depth, impact analysis, validation, real user-path testing, and completion evidence with task risk. `ai-frontend-dev-rules` guides frontend implementation and review across module splitting, shared boundaries, routing, type and schema placement, API integration, state and data ownership, value-label mapping, UI library usage, performance checks, and final change reporting. `agent-skill-security-auditor` reviews agent skills before installation, update, merge, or publication, using local static triage plus manual review guidance. `novel-workbench` provides an end-to-end Chinese novel workflow for requirements interviews, story bibles, outlines, serial chapter drafting, continuity review, polishing, and final manuscript packaging.

## Search Keywords

- ai-frontend-dev-rules
- agent-skill-security-auditor
- novel-workbench
- reliable-task-execution
- task reliability
- execution authorization
- change validation
- codex skills
- codex plugin
- frontend architecture
- frontend development
- module splitting
- code review
- state management
- API integration
- UI library
- performance
- skill security
- prompt injection
- supply chain
- novel writing
- creative writing
- Chinese fiction
- AI-assisted development

## Starter Prompts

```text
Use $ai-frontend-dev-rules to implement this page.
Review this frontend change with $ai-frontend-dev-rules.
Use $agent-skill-security-auditor to review this third-party skill before installation.
Use $novel-workbench to plan and write a Chinese novel.
Use $reliable-task-execution to align this change and verify the result.
```

## Privacy Summary

The plugin packages local skill instructions, one local static triage script for skill security review, and local project initialization and validation utilities for novel writing. It does not include apps, connectors, MCP servers, network services, telemetry, analytics, or data collection code. The utilities operate only on user-provided local paths or temporary test directories and do not upload data.

## Pre-Submission Checks

- Run checks from the repository root, which is also the plugin root. Maintain only `.codex-plugin/plugin.json` and the skill sources under `skills/`; do not recreate a duplicate distribution directory.
- `python3 scripts/check_plugin.py`
- `python3 scripts/test_check_plugin.py`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/ai-frontend-dev-rules --policy marketplace --format markdown`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/agent-skill-security-auditor --policy marketplace --format markdown`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/novel-workbench --policy marketplace --format markdown`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/reliable-task-execution --policy marketplace --format markdown`
- `python3 skills/novel-workbench/scripts/smoke_test.py`
- Confirm `README.md` includes Codex install instructions.
- Confirm `docs/PRIVACY.md` and `docs/TERMS.md` are current.
- Confirm `assets/logo.png` renders correctly for both logo and composer icon.
- Confirm the explicit `skills` array exposes only the four approved skills. Unlisted local skills must not be added as an incidental packaging change.
- Verify root-entry discovery and skill loading with a compatible client. Desktop-bundled Codex `0.162.0-alpha.17.2` passed these checks; CLI `0.132.0` did not. Static checks alone do not verify a fresh installation.
- Confirm the GitHub repository is public and the latest release/tag is pushed.
- Confirm `plugin.json` version is bumped before submitting a material update.
