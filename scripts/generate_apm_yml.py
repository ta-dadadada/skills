#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""Generate apm.yml files for apm (Agent Package Manager) from SKILL.md frontmatter.

Walks the repository (respecting git tracking / .gitignore), finds every
SKILL.md, parses its YAML frontmatter, and writes a sibling apm.yml derived
from the `name`, `description`, and `license` fields. SKILL.md itself is
never modified.

Also writes a root apm.yml that aggregates every skill as an APM dependency
(`<owner>/<repo>/<skill-path>`), so `apm install <owner>/<repo>` installs the
whole collection in one command. The repo slug is derived from `git remote
get-url origin`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FIELDS = ("name", "description", "license")


def find_skill_files(repo_root: Path) -> list[Path]:
    """Return git-tracked SKILL.md paths (case-insensitive), excluding .git etc.

    Uses `git ls-files` so untracked and .gitignore'd files are naturally
    excluded, matching the repository's own notion of "real" content.
    """
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    paths = []
    for line in result.stdout.splitlines():
        if Path(line).name.lower() == "skill.md":
            paths.append(repo_root / line)
    return sorted(paths)


def parse_frontmatter(text: str) -> dict | None:
    """Extract and parse the leading YAML frontmatter block (--- ... ---)."""
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
    if end_index is None:
        return None
    frontmatter_text = "\n".join(lines[1:end_index])
    data = yaml.safe_load(frontmatter_text)
    if not isinstance(data, dict):
        return None
    return data


class QuotedString(str):
    """Marker type forcing single-quoted scalar style on dump (e.g. version)."""


def _represent_quoted_string(dumper: yaml.Dumper, data: "QuotedString") -> yaml.Node:
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="'")


yaml.add_representer(QuotedString, _represent_quoted_string, Dumper=yaml.Dumper)


def build_apm_yml(frontmatter: dict) -> str:
    ordered = {
        "name": frontmatter["name"],
        "description": frontmatter["description"],
        "license": frontmatter["license"],
        "type": "skill",
        "version": QuotedString("0.1.0"),
    }
    return yaml.dump(
        ordered,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )


def repo_slug(repo_root: Path) -> str:
    """Derive `owner/repo` from the origin remote URL (SSH or HTTPS)."""
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    url = result.stdout.strip()
    # git@github.com:owner/repo.git / https://github.com/owner/repo(.git)
    tail = url.split(":", 1)[-1] if url.startswith("git@") else "/".join(url.split("/")[-2:])
    return tail.removesuffix(".git")


def build_root_apm_yml(slug: str, skill_paths: list[Path], repo_root: Path) -> str:
    ordered = {
        "name": slug.split("/")[-1],
        "description": "Agent skill collection; installing this package installs every skill below as a dependency.",
        "license": "MIT",
        "version": QuotedString("0.1.0"),
        "dependencies": {
            "apm": [
                f"{slug}/{skill.parent.relative_to(repo_root).as_posix()}"
                for skill in skill_paths
            ]
        },
    }
    return yaml.dump(
        ordered,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=120,
    )


def main() -> int:
    skill_files = find_skill_files(REPO_ROOT)

    generated = 0
    skipped = 0

    for skill_path in skill_files:
        try:
            text = skill_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: failed to read {skill_path}: {exc}", file=sys.stderr)
            skipped += 1
            continue

        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            print(f"ERROR: no valid YAML frontmatter found in {skill_path}", file=sys.stderr)
            skipped += 1
            continue

        missing = [field for field in REQUIRED_FIELDS if field not in frontmatter or frontmatter[field] in (None, "")]
        if missing:
            print(
                f"ERROR: {skill_path} is missing required frontmatter field(s): {', '.join(missing)}",
                file=sys.stderr,
            )
            skipped += 1
            continue

        apm_yml_content = build_apm_yml(frontmatter)
        apm_yml_path = skill_path.parent / "apm.yml"
        apm_yml_path.write_text(apm_yml_content, encoding="utf-8")
        generated += 1

    total = generated + skipped
    print(f"Processed {total} SKILL.md file(s): {generated} apm.yml generated, {skipped} skipped.")

    if skipped == 0 and skill_files:
        slug = repo_slug(REPO_ROOT)
        root_path = REPO_ROOT / "apm.yml"
        root_path.write_text(build_root_apm_yml(slug, skill_files, REPO_ROOT), encoding="utf-8")
        print(f"Root apm.yml generated with {len(skill_files)} skill dependencies ({slug}).")
    elif skipped:
        print("Root apm.yml not regenerated because some SKILL.md files were skipped.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
