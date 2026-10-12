#!/usr/bin/env python3
"""Exercise publication-scope and reference failures in disposable fixtures."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).with_name("check_plugin.py")


class PluginChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plugin-check-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {
            "name": "sample", "version": "1.0.1", "skills": ["./skills/sample"],
            "interface": {"logo": "./assets/logo.png"},
        }
        self.market = {"plugins": [{
            "name": "sample", "source": {"source": "local", "path": "./"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Developer Tools",
        }]}
        self.write(".codex-plugin/plugin.json", json.dumps(self.manifest))
        self.write(".agents/plugins/marketplace.json", json.dumps(self.market))
        self.write("assets/logo.png", "fixture")
        self.write("README.md", "[Skill](skills/sample/SKILL.md#usage)\n")
        self.write("skills/sample/SKILL.md", "# Sample\n\n## Usage\n\nRead the sample.\n")
        self.write("skills/draft/SKILL.md", "[Unfinished](missing.md)\n")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_check(self, message=None):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(CHECKER), str(self.root)], capture_output=True, text=True)
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after, "The checker must not write to the fixture")
        self.assertEqual(result.returncode, 0 if message is None else 1, result.stderr)
        if message:
            self.assertIn(message, result.stderr)
        return result

    def test_only_declared_skills_are_checked(self):
        result = self.run_check()
        self.assertIn("Published skills (1): sample", result.stdout)

    def test_broad_directory_cannot_replace_allowlist(self):
        self.manifest["skills"] = "./skills/"
        self.write(".codex-plugin/plugin.json", json.dumps(self.manifest))
        self.run_check("explicit non-empty array")

    def test_stale_marketplace_entry_is_rejected(self):
        self.market["plugins"][0]["source"]["path"] = "./plugins/sample"
        self.write(".agents/plugins/marketplace.json", json.dumps(self.market))
        self.run_check("source must point at the repository root")

    def test_missing_resource_is_reported(self):
        (self.root / "assets/logo.png").unlink()
        self.run_check("Missing package path")

    def test_broken_reference_is_reported(self):
        self.write("skills/sample/SKILL.md", "# Sample\n\n## Usage\n\n[Rule](rules/missing.md)\n")
        self.run_check("Broken file reference")

    def test_missing_anchor_is_reported(self):
        self.write("README.md", "[Skill](skills/sample/SKILL.md#missing)\n")
        self.run_check("Missing heading")

    def test_portable_manifest_cannot_bypass_allowlist(self):
        self.write("plugin.json", '{"name":"sample"}\n')
        self.run_check("bypasses the compatibility skill allowlist")

    def test_duplicate_distribution_is_reported(self):
        self.write("plugins/liao-skills/skills/sample/SKILL.md", "duplicate\n")
        self.run_check("Duplicate distribution directory")

    def test_duplicate_skill_is_rejected(self):
        self.manifest["skills"].append("./skills/sample/")
        self.write(".codex-plugin/plugin.json", json.dumps(self.manifest))
        self.run_check("resolve to duplicate directories")

    def test_path_outside_repository_is_rejected(self):
        self.manifest["interface"]["logo"] = "./../outside.png"
        self.write(".codex-plugin/plugin.json", json.dumps(self.manifest))
        self.run_check("Path escapes the plugin root")

    def test_fenced_examples_are_not_treated_as_references(self):
        self.write("README.md", "```md\n[Example](missing.md)\n```\n[Skill](skills/sample/SKILL.md#usage)\n")
        self.run_check()


if __name__ == "__main__":
    unittest.main()
