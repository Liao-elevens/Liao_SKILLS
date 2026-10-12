#!/usr/bin/env python3
"""Read-only checks for this repository's root plugin and explicit skill list."""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


class CheckError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckError(message)


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise CheckError(f"Cannot read {path}: {error}") from error


def local_path(root, value):
    require(isinstance(value, str) and value.startswith("./"),
            f"Expected a ./-prefixed package path: {value!r}")
    path = (root / value).resolve()
    require(path.is_relative_to(root), f"Path escapes the plugin root: {value}")
    require(path.exists(), f"Missing package path: {value}")
    return path


def prose(text):
    """Exclude fenced examples from link and heading checks."""
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker, suffix = match.groups()
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not suffix.strip():
                fence = None
        elif fence is None:
            lines.append(line)
    return "\n".join(lines)


def anchors(text):
    ids = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    counts = Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", prose(text), re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")
        suffix = f"-{counts[slug]}" if counts[slug] else ""
        ids.add(slug + suffix)
        counts[slug] += 1
    return ids


def check_links(root, documents):
    count = 0
    issues = []
    pattern = re.compile(r'!?\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)(?:\s+"[^"\n]*")?\)')
    for document in sorted(documents):
        text = prose(document.read_text(encoding="utf-8"))
        for match in pattern.finditer(text):
            target = match.group(1).strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            count += 1
            path = (document.parent / unquote(url.path)).resolve() if url.path else document
            location = f"{document.relative_to(root)} -> {target}"
            if not path.is_relative_to(root):
                issues.append(f"Link leaves repository: {location}")
            elif not path.exists():
                issues.append(f"Broken file reference: {location}")
            elif url.fragment and path.suffix.lower() == ".md" and path.is_file():
                if unquote(url.fragment) not in anchors(path.read_text(encoding="utf-8")):
                    issues.append(f"Missing heading: {location}")
    require(not issues, "\n".join(issues))
    return count


def check(root):
    require(not (root / "plugin.json").exists(),
            "A portable root plugin.json bypasses the compatibility skill allowlist; review publication scope first.")
    require(not (root / "plugins/liao-skills").exists(),
            "Duplicate distribution directory found; maintain skills only at the repository root.")
    market = read_json(root / ".agents/plugins/marketplace.json")
    manifest = read_json(root / ".codex-plugin/plugin.json")
    require(isinstance(market, dict) and isinstance(manifest, dict), "Manifests must be JSON objects.")
    name = manifest.get("name")
    require(isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name),
            "Invalid plugin name.")
    require(isinstance(manifest.get("version"), str) and
            re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", manifest["version"]),
            "Expected an explicit semantic version.")
    entries = market.get("plugins", [])
    require(isinstance(entries, list), "Marketplace plugins must be an array.")
    matches = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == name]
    require(len(matches) == 1, "Expected one marketplace entry matching the plugin name.")
    entry = matches[0]
    require(entry.get("source") == {"source": "local", "path": "./"},
            "Marketplace source must point at the repository root: ./")
    require(entry.get("category") and entry.get("policy", {}).get("installation") and
            entry.get("policy", {}).get("authentication"), "Missing marketplace policy/category.")
    skills = manifest.get("skills")
    require(isinstance(skills, list) and skills, "skills must be an explicit non-empty array, not ./skills/.")
    require(all(isinstance(path, str) for path in skills), "Every skill path must be a string.")
    require(len(skills) == len(set(skills)), "Duplicate skill paths.")
    roots = []
    for value in skills:
        require(re.fullmatch(r"\./skills/[a-z0-9]+(?:-[a-z0-9]+)*/?", value),
                f"Declare an individual root skill directory: {value}")
        path = local_path(root, value)
        require((path / "SKILL.md").is_file(), f"Missing SKILL.md: {value}")
        roots.append(path)
    require(len(roots) == len(set(roots)), "Skill paths resolve to duplicate directories.")
    interface = manifest.get("interface", {})
    require(isinstance(interface, dict), "interface must be an object.")
    for key in ["composerIcon", "logo"]:
        if interface.get(key):
            require(local_path(root, interface[key]).is_file(), f"Invalid {key} file.")
    for value in interface.get("screenshots", []):
        require(local_path(root, value).is_file(), f"Invalid screenshot: {value}")
    documents = {root / "README.md"}
    documents.update((root / "docs").glob("*.md"))
    for path in roots:
        documents.update(path.rglob("*.md"))
    require(all(path.is_file() for path in documents), "Missing README or Markdown document.")
    references = check_links(root, documents)
    print(f"OK: {name} {manifest['version']}; marketplace source ./")
    print(f"Published skills ({len(roots)}): {', '.join(path.name for path in roots)}")
    print(f"Checked {len(documents)} Markdown files and {references} local links; unlisted skills were not scanned.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        check(args.root.resolve())
    except (CheckError, OSError) as error:
        print(f"Plugin check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
