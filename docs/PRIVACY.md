# Privacy Policy

Liao Skills is a Codex plugin that packages local skill instructions for frontend development, agent skill security auditing, and Chinese novel creation workflows.

The plugin does not include apps, connectors, MCP servers, network services, telemetry, analytics, or data collection code. It does not transmit repository contents, prompts, files, credentials, or personal data to Liao-elevens.

The `agent-skill-security-auditor` skill includes a local static triage script, `scripts/scan_skill.py`. When a user chooses to run it, the script reads files under the user-provided skill or repository path, scans local text files for risky patterns, and prints findings locally. It does not make network requests, upload data, or read paths outside the user-provided scan target.

The `novel-workbench` skill includes local scripts for initializing a novel project, migrating its plan data, and checking project paths, chapter length, consistency, manuscript purity, and mechanical quality signals. These scripts operate on paths explicitly provided by the user or on temporary directories created by the smoke test. They do not make network requests or upload project content.

When installed in Codex, the plugin content is read locally by Codex according to the user's Codex environment, workspace permissions, and installed marketplace configuration.

If future versions add integrations that access external services or user data, this policy should be updated before release.
