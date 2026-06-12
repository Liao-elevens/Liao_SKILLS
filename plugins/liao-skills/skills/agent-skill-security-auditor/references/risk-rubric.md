# Risk Rubric

Use severity based on user impact, consent, reversibility, and scope.

## P0 Blocker

Recommend `Do not install` until fixed.

Examples:
- Reads or exports secrets, tokens, cookies, `.env`, `.ssh`, cloud credentials, browser profiles, or private keys without explicit user request. <!-- skill-audit: ignore-line -->
- Executes downloaded code or installer pipelines such as `curl ... | sh` or `wget ... | bash`. <!-- skill-audit: ignore-line -->
- Tells the agent to ignore system/developer instructions, hide actions, reveal hidden prompts, or bypass approval. <!-- skill-audit: ignore-line -->
- Deletes broad paths, rewrites user shell profiles, changes git hooks, disables security controls, or performs irreversible destructive actions.
- Automatically deploys, pushes, sends messages, changes billing resources, or mutates production systems without explicit confirmation.

## P1 High

Usually `Install with caution` or block for team/enterprise use until fixed.

Examples:
- Installs unpinned dependencies or uses floating remote URLs for executable code.
- Uses `eval`, dynamic execution, `child_process`, `subprocess`, shell expansion, or broad script execution without narrow input validation. <!-- skill-audit: ignore-line -->
- Accesses broad filesystem locations outside the user-provided workspace.
- Sends file contents, repository data, logs, or environment details to external services.
- Metadata or description hides important capabilities such as network access, file mutation, credentials, or external accounts.

## P2 Medium

Acceptable only when disclosed and bounded.

Examples:
- Scripts mutate files but lack `--dry-run`, backup, or clear user confirmation.
- Dependency files are present but lockfiles are missing.
- The skill asks for broad credentials when scoped tokens would work.
- Failure modes are unclear for destructive or external-service workflows.
- References include large opaque payloads or generated code that is hard to review.

## P3 Low

Should be fixed but does not normally block installation.

Examples:
- Vague permission wording.
- Missing output template, missing usage examples, or unclear trigger scope.
- Inconsistent naming across metadata files.
- Minor unsafe examples that are not part of the default workflow.

## Evidence Rules

Every finding should include:
- File path and line number when available.
- The risky behavior in plain language.
- Why it matters for an agent skill.
- A concrete remediation.

Avoid unsupported claims about author intent. Describe observable behavior and likely impact.
