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

Frontend architecture rules for AI-assisted coding.

## Long Description

Liao Skills packages reusable Codex skills for engineering workflows. `ai-frontend-dev-rules` guides frontend implementation and review across module splitting, shared boundaries, routing, type and schema placement, API integration, state and data ownership, value-label mapping, UI library usage, performance checks, and final change reporting. `agent-skill-security-auditor` reviews agent skills before installation, update, merge, or publication, using local static triage plus manual review guidance.

## Search Keywords

- ai-frontend-dev-rules
- agent-skill-security-auditor
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
- AI-assisted development

## Starter Prompts

```text
Use $ai-frontend-dev-rules to implement this page.
Review this frontend change with $ai-frontend-dev-rules.
Use $agent-skill-security-auditor to review this third-party skill before installation.
```

## Privacy Summary

The plugin packages local skill instructions and one local static triage script for skill security review. It does not include apps, connectors, MCP servers, network services, telemetry, analytics, or data collection code. The scanner reads only the user-provided scan target and prints results locally.

## Pre-Submission Checks

- `python3 <path-to-validate_plugin.py> .`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/ai-frontend-dev-rules --policy marketplace --format markdown`
- `python3 skills/agent-skill-security-auditor/scripts/scan_skill.py skills/agent-skill-security-auditor --policy marketplace --format markdown`
- Confirm `README.md` includes Codex install instructions.
- Confirm `docs/PRIVACY.md` and `docs/TERMS.md` are current.
- Confirm `assets/logo.png` renders correctly for both logo and composer icon.
- Confirm the GitHub repository is public and the latest release/tag is pushed.
- Confirm `plugin.json` version is bumped before submitting a material update.
