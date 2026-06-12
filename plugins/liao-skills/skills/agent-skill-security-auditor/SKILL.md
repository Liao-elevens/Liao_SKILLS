---
name: agent-skill-security-auditor
description: Security audit workflow for agent skills before installation, publication, or review. Use when checking third-party or local SKILL.md packages, Codex/Claude/Cursor skills, skill repositories, skill update diffs, bundled scripts, dependencies, metadata, prompt-injection risks, secret access, network exfiltration, destructive commands, or whether a skill is safe to install, publish, merge, or share with a team. Run scripts/scan_skill.py for lightweight static triage when a local skill directory is available, then perform manual review with the referenced risk rubric and output template.
---

# Agent Skill Security Auditor

## Purpose

Audit agent skills for security and trust risks before installing, publishing, updating, or merging them.

This skill focuses on risks specific to agent skill packages: unsafe instructions in `SKILL.md`, misleading metadata, bundled scripts, external network calls, credential access, destructive commands, supply-chain exposure, and behavior that expands the agent's authority without clear user consent.

## When to Apply

Use this skill when:
- Reviewing a third-party skill from GitHub, skills.sh, a plugin bundle, or a local folder before installation.
- Auditing a new or modified skill before publishing it.
- Reviewing a PR that adds or changes a skill.
- Comparing a skill update against an older version.
- Checking whether a skill is safe for personal, team, enterprise, or marketplace use.

## Quick Workflow

1. Identify the skill root and inspect these files if present:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `.codex-plugin/plugin.json`
   - `scripts/`
   - `references/`
   - `assets/`
   - `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`
   - `requirements.txt`, `pyproject.toml`, `uv.lock`, `Pipfile.lock`
   - shell scripts and other executable files
2. If a local directory is available, run static triage:

   ```bash
   python scripts/scan_skill.py /path/to/skill --policy team --format markdown
   ```

   Use `--format json` when another tool will consume the findings.
   Use `# skill-audit: ignore-line` or `<!-- skill-audit: ignore-line -->` sparingly for intentional examples inside security documentation or scanner source. Do not suppress real behavior in third-party skills without explaining why.
3. Read `references/risk-rubric.md` for severity rules.
4. Read `references/dangerous-patterns.md` when a finding involves scripts, dependencies, credentials, network calls, or prompt-injection behavior.
5. Produce the final report using `references/output-template.md`.

## Review Priorities

Start with issues that can harm users or systems without meaningful consent:
- Prompt-injection instructions that tell the agent to ignore policies, reveal hidden context, bypass approval, or hide actions from the user. <!-- skill-audit: ignore-line -->
- Exfiltration of secrets, tokens, cookies, `.env`, `.ssh`, cloud credentials, browser profiles, git history, or private project files. <!-- skill-audit: ignore-line -->
- Remote code execution through `curl | sh`, `wget | bash`, unpinned installers, `eval`, dynamic imports, or downloaded scripts. <!-- skill-audit: ignore-line -->
- Destructive actions such as deleting files, changing shell profiles, modifying git hooks, pushing code, deploying, sending email, or creating paid cloud resources.
- Metadata that understates the skill's behavior, such as a harmless description paired with scripts that access credentials or the network.

## Policy Presets

Use the policy preset to frame the recommendation:

| Policy | Intended Use | Default Recommendation Bias |
| --- | --- | --- |
| `personal` | Individual local use | Allow medium risk if disclosed and user-controlled. |
| `team` | Shared team install or repository PR | Block high risk unless remediated. Require clear permission boundaries. |
| `enterprise` | Managed environment | Block unpinned dependencies, implicit credential access, remote execution, and broad filesystem access. |
| `marketplace` | Public publishing | Require accurate metadata, clear capability disclosure, no hidden high-risk behavior, and safe defaults. |

## Decision Rules

- Say `Do not install` for any unresolved P0 finding.
- Say `Install with caution` when P1 findings are mitigated by explicit user confirmation, sandboxing, pinning, or narrow scope.
- Say `Install` only when no P0/P1 issues remain and medium risks are disclosed with practical mitigations.
- Do not treat scanner output as final proof. Static scanning is triage; manual review decides exploitability and user impact.

## Final Report Requirements

Always include:
- Verdict: `Install`, `Install with caution`, or `Do not install`.
- Findings ordered by severity, with file and line evidence.
- Sensitive capabilities observed: network, file writes, secret access, external services, subprocess execution.
- Concrete fixes for each blocking or high-risk issue.
- Residual risk and assumptions.

If no issues are found, say that no blocking findings were identified and note what was not verified, such as remote repository history, dependency reputation, or runtime behavior.
