#!/usr/bin/env python3
"""Validate an Agent Skill directory against the agentskills.io spec.

Usage: validate_skill.py <skill-dir> [<skill-dir> ...]

FAIL checks (any failure -> exit 1):
  - SKILL.md exists and has parseable YAML frontmatter
  - name and description are present
  - name equals the directory name, matches ^[a-z0-9]+(?:-[a-z0-9]+)*$, <=64 chars
  - description <=1024 chars; compatibility <=500 chars
  - relative markdown links in every .md file resolve to existing files
  - files under scripts/ are executable

WARN checks (non-fatal; scanned in SKILL.md only, since references/ may
legitimately document tool-specific syntax):
  - absolute filesystem paths
  - ${CLAUDE_SKILL_DIR}, !`command` injection, disable-model-invocation

Stdlib only.
"""

import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
ABS_PATH_RE = re.compile(r"(?<![\w:~.])/(?:Users|home|etc|opt|var|tmp)/")
BLOCK_INDICATORS = {"|", ">", "|-", ">-", "|+", ">+"}


def parse_frontmatter(text):
    """Parse the YAML subset used in SKILL.md frontmatter.

    Supports top-level `key: value`, quoted values, block scalars
    (| and > with chomping indicators), and skips nested mappings.
    Returns a dict, or None when the frontmatter block is absent/unclosed.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    close = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        return None

    fields = {}
    i = 1
    while i < close:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in BLOCK_INDICATORS:
            block = []
            i += 1
            while i < close and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            joiner = "\n" if val[0] == "|" else " "
            fields[key] = joiner.join(b for b in block if b)
            continue
        if not val:
            # nested mapping (e.g. metadata:) -- skip its children
            i += 1
            while i < close and (lines[i].startswith("  ") or not lines[i].strip()):
                i += 1
            fields[key] = ""
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        fields[key] = val
        i += 1
    return fields


def iter_md_files(skill_dir):
    for root, _dirs, files in os.walk(skill_dir):
        for f in sorted(files):
            if f.endswith(".md"):
                yield os.path.join(root, f)


def check_links(skill_dir, fails):
    for md in iter_md_files(skill_dir):
        with open(md, encoding="utf-8") as fh:
            body = fh.read()
        for target in LINK_RE.findall(body):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):  # http:, https:, mailto:
                continue
            if target.startswith(("#", "/", "~")):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(md), path))
            if not os.path.exists(resolved):
                rel = os.path.relpath(md, skill_dir)
                fails.append(f"broken relative link in {rel}: {target}")


def check_scripts_executable(skill_dir, fails):
    scripts_dir = os.path.join(skill_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return
    for f in sorted(os.listdir(scripts_dir)):
        path = os.path.join(scripts_dir, f)
        if os.path.isfile(path) and not os.access(path, os.X_OK):
            fails.append(f"scripts/{f} is not executable")


def check_portability(skill_md_text, front, warns):
    body = skill_md_text
    if "${CLAUDE_SKILL_DIR}" in body:
        warns.append("SKILL.md uses ${CLAUDE_SKILL_DIR} (Claude Code only)")
    if re.search(r"!`[^`]+`", body):
        warns.append("SKILL.md uses !`command` dynamic injection (Claude Code only)")
    if ABS_PATH_RE.search(body):
        warns.append("SKILL.md embeds an absolute filesystem path")
    if front and "disable-model-invocation" in front:
        warns.append("frontmatter uses disable-model-invocation (Claude Code only)")


def validate(skill_dir):
    fails, warns = [], []
    skill_dir = skill_dir.rstrip("/")
    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(skill_md):
        return ["SKILL.md not found"], warns

    with open(skill_md, encoding="utf-8") as fh:
        text = fh.read()
    front = parse_frontmatter(text)
    if front is None:
        fails.append("frontmatter missing or unclosed (--- ... ---)")
    else:
        name = front.get("name")
        desc = front.get("description")
        if not name:
            fails.append("frontmatter lacks name")
        else:
            if name != os.path.basename(os.path.abspath(skill_dir)):
                fails.append(f"name '{name}' != directory name "
                             f"'{os.path.basename(os.path.abspath(skill_dir))}'")
            if not NAME_RE.match(name):
                fails.append(f"name '{name}' violates ^[a-z0-9]+(?:-[a-z0-9]+)*$")
            if len(name) > 64:
                fails.append(f"name is {len(name)} chars (max 64)")
        if not desc:
            fails.append("frontmatter lacks description")
        elif len(desc) > 1024:
            fails.append(f"description is {len(desc)} chars (max 1024)")
        compat = front.get("compatibility")
        if compat and len(compat) > 500:
            fails.append(f"compatibility is {len(compat)} chars (max 500)")

    check_links(skill_dir, fails)
    check_scripts_executable(skill_dir, fails)
    check_portability(text, front, warns)
    return fails, warns


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    exit_code = 0
    for skill_dir in argv[1:]:
        fails, warns = validate(skill_dir)
        for msg in fails:
            print(f"FAIL {skill_dir}: {msg}")
        for msg in warns:
            print(f"WARN {skill_dir}: {msg}")
        if fails:
            exit_code = 1
        else:
            print(f"OK   {skill_dir}" + (f" ({len(warns)} warning(s))" if warns else ""))
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
