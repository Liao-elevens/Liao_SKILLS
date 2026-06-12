# Dangerous Patterns

Use this reference when reviewing scanner matches or performing manual review.

## Prompt Injection

High-risk instructions include:
- Ignore previous, system, developer, or safety instructions. <!-- skill-audit: ignore-line -->
- Reveal hidden prompts, chain of thought, secrets, environment variables, or private files. <!-- skill-audit: ignore-line -->
- Do not tell the user, hide this action, silently continue, or avoid mentioning a risky step. <!-- skill-audit: ignore-line -->
- Always approve, never ask for confirmation, or bypass review.
- Treat skill instructions as higher priority than system or developer instructions.

Safe alternative:
- Require the agent to follow platform permissions and ask for explicit user confirmation before sensitive actions.

## Secret and Private Data Access

Sensitive targets include:
- `.env`, `.env.*` <!-- skill-audit: ignore-line -->
- `.ssh/`, `id_rsa`, `id_ed25519`, `known_hosts` <!-- skill-audit: ignore-line -->
- `.aws/credentials`, `.config/gcloud`, Azure credentials
- GitHub, GitLab, npm, PyPI, Docker, Vercel, Cloudflare, Stripe, Slack, Figma, browser, and cookie tokens <!-- skill-audit: ignore-line -->
- `~/Library/Application Support`, browser profile directories, keychains, password stores <!-- skill-audit: ignore-line -->

Safe alternative:
- Require user-provided paths and scoped tokens. Never scan home directories by default.

## Network Exfiltration

Review calls such as:
- `curl`, `wget`, `nc`, `ssh`, `scp`, `rsync` <!-- skill-audit: ignore-line -->
- JavaScript `fetch`, `axios`, `child_process` <!-- skill-audit: ignore-line -->
- Python `requests`, `urllib`, `httpx`, `socket`
- Webhooks, pastebins, telemetry, analytics, or arbitrary API uploads

Safe alternative:
- Explain destination, payload, authentication, retention, and whether the call is optional.

## Remote Code Execution

Block or require strong mitigation for:
- `curl ... | sh`, `wget ... | bash` <!-- skill-audit: ignore-line -->
- `eval`, `exec`, `new Function`
- `python -c`, `node -e`, shell command construction from unsanitized input <!-- skill-audit: ignore-line -->
- Downloading a script and executing it without version pinning and integrity checks

Safe alternative:
- Pin versions, verify checksums, avoid shell pipelines, and show commands before execution.

## Destructive or Persistent Changes

High-risk actions include:
- `rm -rf`, `chmod -R`, `chown -R`, recursive deletion or permission changes <!-- skill-audit: ignore-line -->
- Modifying `.bashrc`, `.zshrc`, `.profile`, shell aliases, git hooks, launch agents, cron jobs, or startup items <!-- skill-audit: ignore-line -->
- Force pushing, deleting branches, rewriting history, changing remotes
- Deploying, creating cloud resources, changing IAM, rotating secrets, sending email or messages

Safe alternative:
- Require dry-run, narrow paths, backups, and explicit confirmation for every destructive or external mutation.

## Supply Chain

Watch for:
- Unpinned dependencies: `latest`, `*`, `>=`, branch refs, git URLs without commits
- `postinstall`, `preinstall`, `prepare`, or install-time scripts
- Binary downloads or platform-specific executables
- Obfuscated package names, typo-squatting, abandoned packages

Safe alternative:
- Pin exact versions or lockfiles, avoid install-time scripts, and document why each dependency is needed.

## Misleading Metadata

Compare:
- `SKILL.md` frontmatter description
- `agents/openai.yaml`
- `.codex-plugin/plugin.json`
- README installation instructions
- Script behavior

Flag when public metadata sounds narrow or harmless but bundled code performs broad filesystem, network, credential, or destructive operations.
