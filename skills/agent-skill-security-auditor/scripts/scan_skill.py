#!/usr/bin/env python3
"""Lightweight static triage for agent skill directories."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
}

TEXT_EXTENSIONS = {
    "",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".lock",
    ".env",
}

SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
IGNORE_MARKER = "skill-audit: ignore-line"


@dataclass
class Finding:
    severity: str
    category: str
    title: str
    path: str
    line: int
    evidence: str
    risk: str
    fix: str


PATTERNS: list[tuple[str, str, str, re.Pattern[str], str, str]] = [
    (
        "P0",
        "prompt-injection",
        "Instruction may bypass higher-priority safety or disclosure rules",  # skill-audit: ignore-line
        re.compile(
            r"\b(ignore|override|bypass|disregard)\b.{0,80}\b(system|developer|safety|policy|instruction)s?\b|"  # skill-audit: ignore-line
            r"\b(do not|don't)\b.{0,40}\b(tell|inform|mention|show)\b.{0,40}\b(user|developer)\b|"  # skill-audit: ignore-line
            r"\breveal\b.{0,40}\b(hidden|system|developer|prompt|instruction|chain of thought)\b",
            re.IGNORECASE,
        ),
        "The skill may instruct the agent to hide behavior or ignore higher-priority instructions.",  # skill-audit: ignore-line
        "Remove the bypass instruction and require normal platform permissions and user disclosure.",  # skill-audit: ignore-line
    ),
    (
        "P0",
        "remote-code-execution",
        "Remote installer pipeline executes downloaded code",
        re.compile(r"\b(curl|wget)\b[^|\n]{0,200}\|\s*(sh|bash|zsh|python|node)\b", re.IGNORECASE),  # skill-audit: ignore-line
        "Downloaded code can execute without review, pinning, or integrity checks.",
        "Avoid pipe-to-shell. Pin a version, verify a checksum, and show commands before execution.",
    ),
    (
        "P0",
        "secret-access",
        "Sensitive credential path or token is referenced",
        re.compile(
            r"(\.env(\.|$)|\.ssh/|id_rsa|id_ed25519|AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID|"  # skill-audit: ignore-line
            r"GOOGLE_APPLICATION_CREDENTIALS|GITHUB_TOKEN|GH_TOKEN|NPM_TOKEN|PYPI_TOKEN|"  # skill-audit: ignore-line
            r"STRIPE_SECRET|SLACK_BOT_TOKEN|VERCEL_TOKEN|CLOUDFLARE_API_TOKEN|cookie|cookies)",  # skill-audit: ignore-line
            re.IGNORECASE,
        ),
        "The skill may read or expose credentials, cookies, or private account tokens.",  # skill-audit: ignore-line
        "Require explicit user-provided paths or scoped tokens, and never scan home or credential stores by default.",
    ),
    (
        "P0",
        "destructive-command",
        "Potentially destructive command is present",
        re.compile(r"\brm\s+(-[A-Za-z]*r[A-Za-z]*f|-rf|-fr)\b|\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[fdx]+", re.IGNORECASE),
        "The command can irreversibly delete files or discard user work.",
        "Use dry-run, narrow explicit paths, backups, and explicit user confirmation.",
    ),
    (
        "P1",
        "dynamic-execution",
        "Dynamic code or subprocess execution is present",
        re.compile(
            r"\b(eval|exec)\s*\(|new\s+Function\s*\(|child_process|subprocess\.(run|Popen|call|check_output)|"  # skill-audit: ignore-line
            r"os\.system\s*\(|shell\s*=\s*True|python\s+-c|node\s+-e",
            re.IGNORECASE,
        ),
        "Dynamic execution can run attacker-controlled input or hide behavior from review.",
        "Avoid dynamic execution, validate inputs, avoid shell=True, and show commands before running them.",  # skill-audit: ignore-line
    ),
    (
        "P1",
        "network-access",
        "Network call or upload-capable tool is present",
        re.compile(
            r"\b(curl|wget|scp|rsync|ssh|nc)\b|requests\.(post|put|patch|get)\s*\(|"  # skill-audit: ignore-line
            r"\bfetch\s*\(|axios\.(post|put|patch|get)\s*\(|httpx\.(post|put|patch|get)\s*\(|urllib\.request",
            re.IGNORECASE,
        ),
        "The skill may send local data to an external destination or download executable content.",
        "Document the destination, payload, authentication, retention, and whether the network call is optional.",
    ),
    (
        "P1",
        "persistence",
        "Persistent environment or startup modification is present",
        re.compile(
            r"(\.bashrc|\.zshrc|\.profile|\.bash_profile|\.config/fish|git/hooks|crontab|launchctl|LaunchAgents|systemd)",  # skill-audit: ignore-line
            re.IGNORECASE,
        ),
        "Persistent modifications can affect future shells, git operations, or system startup.",
        "Avoid persistent changes by default and require explicit confirmation with exact file paths.",
    ),
    (
        "P2",
        "broad-filesystem",
        "Broad filesystem or home-directory access is referenced",
        re.compile(r"(/Users/|/home/|~[/\\]|\$HOME|Path\.home\(\)|os\.environ\.get\([\"']HOME)", re.IGNORECASE),  # skill-audit: ignore-line
        "Broad filesystem access can expose unrelated private files.",
        "Limit operations to user-provided paths or the current workspace.",
    ),
    (
        "P2",
        "obfuscation",
        "Long base64-like or opaque payload is present",
        re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{120,}={0,2}(?![A-Za-z0-9+/=])"),
        "Opaque payloads are difficult to review and may hide code or data.",
        "Replace opaque payloads with readable source or document their origin and verification method.",
    ),
]


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            path = Path(current_root) / filename
            if path.suffix.lower() in TEXT_EXTENSIONS:
                yield path


def read_lines(path: Path) -> list[str] | None:
    try:
        if path.stat().st_size > 1_000_000:
            return None
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None


def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def scan_patterns(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        lines = read_lines(path)
        if lines is None:
            continue
        relative = relpath(path, root)
        for line_number, line in enumerate(lines, start=1):
            if IGNORE_MARKER in line:
                continue
            for severity, category, title, pattern, risk, fix in PATTERNS:
                match = pattern.search(line)
                if match:
                    findings.append(
                        Finding(
                            severity=severity,
                            category=category,
                            title=title,
                            path=relative,
                            line=line_number,
                            evidence=line.strip()[:240],
                            risk=risk,
                            fix=fix,
                        )
                    )
    return findings


def scan_package_json(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("package.json"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        relative = relpath(path, root)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        scripts = data.get("scripts", {})
        if isinstance(scripts, dict):
            for name, command in scripts.items():
                if re.search(r"\b(preinstall|postinstall|prepare)\b", name, re.IGNORECASE):
                    findings.append(
                        Finding(
                            "P1",
                            "supply-chain",
                            "Install-time npm script is present",
                            relative,
                            1,
                            f"{name}: {command}",
                            "Install-time scripts can execute during dependency installation.",
                            "Remove install-time scripts or document why they are required and what they execute.",
                        )
                    )
        for section in ("dependencies", "devDependencies", "optionalDependencies"):
            deps = data.get(section, {})
            if not isinstance(deps, dict):
                continue
            for dep, version in deps.items():
                if isinstance(version, str) and re.search(r"(^\*|latest|^[~^]?>=|git\+|github:|http://|https://)", version):
                    findings.append(
                        Finding(
                            "P2",
                            "supply-chain",
                            "Unpinned or remote npm dependency is present",
                            relative,
                            1,
                            f"{section}.{dep}: {version}",
                            "Floating or remote dependency versions can change without review.",
                            "Pin exact versions or include a lockfile and justify remote dependencies.",
                        )
                    )
    return findings


def scan_requirements(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("requirements*.txt"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        lines = read_lines(path)
        if lines is None:
            continue
        relative = relpath(path, root)
        for line_number, raw in enumerate(lines, start=1):
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            if "://" in line or line.startswith("git+"):
                findings.append(
                    Finding(
                        "P2",
                        "supply-chain",
                        "Remote Python dependency is present",
                        relative,
                        line_number,
                        line,
                        "Remote dependencies can change or execute code during installation.",
                        "Use a pinned package version or a commit-pinned source with justification.",
                    )
                )
            elif "==" not in line:
                findings.append(
                    Finding(
                        "P2",
                        "supply-chain",
                        "Unpinned Python dependency is present",
                        relative,
                        line_number,
                        line,
                        "Unpinned dependencies can resolve to unreviewed versions.",
                        "Pin exact versions or provide a lockfile.",
                    )
                )
    return findings


def dedupe(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple[str, str, str, int, str]] = set()
    result: list[Finding] = []
    for finding in findings:
        key = (finding.severity, finding.category, finding.path, finding.line, finding.evidence)
        if key not in seen:
            seen.add(key)
            result.append(finding)
    return result


def sort_findings(findings: list[Finding]) -> list[Finding]:
    return sorted(findings, key=lambda f: (SEVERITY_ORDER.get(f.severity, 99), f.path, f.line, f.category))


def verdict(findings: list[Finding], policy: str) -> str:
    severities = {finding.severity for finding in findings}
    if "P0" in severities:
        return "Do not install"
    if "P1" in severities:
        return "Install with caution"
    if policy in {"enterprise", "marketplace"} and "P2" in severities:
        return "Install with caution"
    return "Install"


def render_markdown(findings: list[Finding], root: Path, policy: str) -> str:
    lines = [
        "## Verdict",
        verdict(findings, policy),
        "",
        f"Policy: {policy}",
        f"Scope reviewed: {root}",
        "",
        "## Findings",
    ]
    if not findings:
        lines.append("No blocking or high-risk findings were identified by static triage.")
    else:
        for finding in findings:
            lines.extend(
                [
                    f"- [{finding.severity}] {finding.title}",
                    f"  Evidence: {finding.path}:{finding.line} `{finding.evidence}`",
                    f"  Risk: {finding.risk}",
                    f"  Fix: {finding.fix}",
                ]
            )
    lines.extend(
        [
            "",
            "## Residual Risk",
            "This is static triage only. Manually review intent, metadata accuracy, dependency reputation, runtime behavior, and external service destinations before making a final trust decision.",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lightweight static scanner for agent skill security review.")
    parser.add_argument("path", help="Skill directory or repository root to scan.")
    parser.add_argument("--policy", choices=["personal", "team", "enterprise", "marketplace"], default="team")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--fail-on", choices=["P0", "P1", "P2", "P3"], help="Exit non-zero if this severity or higher is found.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        return 2
    findings = sort_findings(dedupe(scan_patterns(root) + scan_package_json(root) + scan_requirements(root)))

    if args.format == "json":
        payload = {
            "path": str(root),
            "policy": args.policy,
            "verdict": verdict(findings, args.policy),
            "findings": [asdict(finding) for finding in findings],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(findings, root, args.policy))

    if args.fail_on:
        threshold = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER.get(finding.severity, 99) <= threshold for finding in findings):
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
