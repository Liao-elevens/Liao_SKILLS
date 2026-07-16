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

Reusable coding, security, and Chinese novel writing workflows.

## Long Description

Liao Skills packages reusable Codex skills for coding, security review, and creative writing. `ai-frontend-dev-rules` guides frontend implementation and review across module splitting, shared boundaries, routing, type and schema placement, API integration, state and data ownership, value-label mapping, UI library usage, performance checks, and final change reporting. `agent-skill-security-auditor` reviews agent skills before installation, update, merge, or publication, using local static triage plus manual review guidance. `novel-workbench` provides an end-to-end Chinese novel workflow for requirements interviews, story bibles, outlines, serial chapter drafting, continuity review, polishing, and final manuscript packaging.

## Search Keywords

- ai-frontend-dev-rules
- agent-skill-security-auditor
- novel-workbench
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
```

## Privacy Summary

The plugin packages local skill instructions, one local static triage script for skill security review, and local project initialization and validation utilities for novel writing. It does not include apps, connectors, MCP servers, network services, telemetry, analytics, or data collection code. The utilities operate only on user-provided local paths or temporary test directories and do not upload data.

## Pre-Submission Checks

- `python3 <path-to-validate_plugin.py> .`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/ai-frontend-dev-rules --policy marketplace --format markdown`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/agent-skill-security-auditor --policy marketplace --format markdown`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/novel-workbench --policy marketplace --format markdown`
- `python3 skills/novel-workbench/scripts/smoke_test.py`
- Confirm `README.md` includes Codex install instructions.
- Confirm `docs/PRIVACY.md` and `docs/TERMS.md` are current.
- Confirm `assets/logo.png` renders correctly for both logo and composer icon.
- Confirm the GitHub repository is public and the latest release/tag is pushed.
- Confirm `plugin.json` version is bumped before submitting a material update.
