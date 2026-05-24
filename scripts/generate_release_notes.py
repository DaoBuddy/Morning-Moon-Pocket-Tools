"""
Generate release notes for a monthly snapshot release.

Steps:
  1. Find the previous tag to get the diff range.
  2. Collect commits since that tag.
  3. Parse which monsters / resources were added or updated.
  4. List unique contributors.
  5. (Optional) Call Gemini API to write a human-readable summary.
  6. Print the full release body to stdout (captured by the workflow).

Usage:
  python scripts/generate_release_notes.py <new_tag> [--no-ai]

Environment:
  GEMINI_API_KEY  — if set, AI summary is generated (requires `pip install google-generativeai`)
"""

import os
import re
import subprocess
import sys
from pathlib import Path


DATA_FILES = ["monster-data_4.md", "resource_hp_data.md"]


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def previous_tag() -> str | None:
    tags = run(["git", "tag", "--sort=-creatordate"]).splitlines()
    return tags[0] if tags else None


def commits_since(tag: str | None) -> list[dict]:
    if tag:
        log_range = f"{tag}..HEAD"
    else:
        log_range = "HEAD"

    raw = run([
        "git", "log", log_range,
        "--pretty=format:%H|%an|%ae|%s",
        "--no-merges",
    ])
    commits = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash":    parts[0][:7],
                "author":  parts[1],
                "email":   parts[2],
                "subject": parts[3],
            })
    return commits


def diff_since(tag: str | None) -> str:
    if tag:
        return run(["git", "diff", tag, "HEAD", "--", *DATA_FILES])
    else:
        return run(["git", "show", "HEAD", "--", *DATA_FILES])


# ---------------------------------------------------------------------------
# Parse diff for added / updated entries
# ---------------------------------------------------------------------------

def parse_diff_entries(diff: str) -> dict:
    new_monsters:   list[str] = []
    new_resources:  list[str] = []
    upd_monsters:   list[str] = []
    upd_resources:  list[str] = []

    removed_sections: set[str] = set()

    for line in diff.splitlines():
        # Removed section header → update (not new)
        m = re.match(r"^-## (.+)", line)
        if m:
            removed_sections.add(m.group(1).strip())
        m = re.match(r"^-### (.+)", line)
        if m:
            removed_sections.add(m.group(1).strip())

    for line in diff.splitlines():
        m = re.match(r"^\+## (.+)", line)
        if m:
            name = m.group(1).strip()
            if name in removed_sections:
                upd_monsters.append(name)
            else:
                new_monsters.append(name)

        m = re.match(r"^\+### (.+)", line)
        if m:
            name = m.group(1).strip()
            if name in removed_sections:
                upd_resources.append(name)
            else:
                new_resources.append(name)

    return {
        "new_monsters":  new_monsters,
        "new_resources": new_resources,
        "upd_monsters":  upd_monsters,
        "upd_resources": upd_resources,
    }


# ---------------------------------------------------------------------------
# Contributor list
# ---------------------------------------------------------------------------

def contributors_since(tag: str | None) -> list[str]:
    if tag:
        log_range = f"{tag}..HEAD"
    else:
        log_range = "HEAD"

    raw = run(["git", "log", log_range, "--pretty=format:%an", "--no-merges"])
    seen: dict[str, int] = {}
    for name in raw.splitlines():
        name = name.strip()
        if name:
            seen[name] = seen.get(name, 0) + 1

    # Sort by commit count descending
    return [name for name, _ in sorted(seen.items(), key=lambda x: -x[1])]


# ---------------------------------------------------------------------------
# AI summary via Claude
# ---------------------------------------------------------------------------

def ai_summary(entries: dict, commits: list[dict], tag: str) -> str | None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        import google.generativeai as genai
    except ImportError:
        print("⚠️  google-generativeai package not installed — skipping AI summary", file=sys.stderr)
        return None

    commit_lines = "\n".join(f"- [{c['hash']}] {c['subject']} ({c['author']})" for c in commits[:40])

    new_m  = ", ".join(entries["new_monsters"])  or "none"
    new_r  = ", ".join(entries["new_resources"]) or "none"
    upd_m  = ", ".join(entries["upd_monsters"])  or "none"
    upd_r  = ", ".join(entries["upd_resources"]) or "none"

    prompt = f"""You are writing release notes for a community data repository for the game Morning Moon Pocket.
The repository collects monster stats and resource HP values contributed by players.

Release tag: {tag}

Changes this month:
- New monsters added: {new_m}
- New resources added: {new_r}
- Monsters updated: {upd_m}
- Resources updated: {upd_r}

Commits:
{commit_lines}

Write a short, friendly summary (3–5 sentences) in both Thai and English.
Thai first, then English. No headers, just the paragraphs.
Focus on what the community contributed and why it helps players."""

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


# ---------------------------------------------------------------------------
# Build release body
# ---------------------------------------------------------------------------

def build_release_body(
    tag: str,
    prev_tag: str | None,
    entries: dict,
    commits: list[dict],
    contribs: list[str],
    summary: str | None,
) -> str:
    lines: list[str] = []

    lines.append(f"# Release {tag}")
    lines.append("")

    # Summary
    if summary:
        lines.append("## Summary")
        lines.append("")
        lines.append(summary)
        lines.append("")
        lines.append("---")
        lines.append("")

    # What's new
    lines.append("## What's New")
    lines.append("")

    if entries["new_monsters"]:
        lines.append(f"**New Monsters ({len(entries['new_monsters'])}):**")
        for m in entries["new_monsters"]:
            lines.append(f"- {m}")
        lines.append("")

    if entries["new_resources"]:
        lines.append(f"**New Resources ({len(entries['new_resources'])}):**")
        for r in entries["new_resources"]:
            lines.append(f"- {r}")
        lines.append("")

    if entries["upd_monsters"]:
        lines.append(f"**Updated Monsters ({len(entries['upd_monsters'])}):**")
        for m in entries["upd_monsters"]:
            lines.append(f"- {m}")
        lines.append("")

    if entries["upd_resources"]:
        lines.append(f"**Updated Resources ({len(entries['upd_resources'])}):**")
        for r in entries["upd_resources"]:
            lines.append(f"- {r}")
        lines.append("")

    if not any(entries.values()):
        lines.append("_No data file changes this month._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Commit log
    lines.append("## Update Log")
    lines.append("")
    if commits:
        for c in commits:
            lines.append(f"- `{c['hash']}` {c['subject']} — _{c['author']}_")
    else:
        lines.append("_No commits this period._")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Contributors
    lines.append("## Contributors")
    lines.append("")
    if contribs:
        for name in contribs:
            lines.append(f"- {name}")
    else:
        lines.append("_No contributors this period._")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Footer
    range_str = f"`{prev_tag}...{tag}`" if prev_tag else f"initial → `{tag}`"
    lines.append(f"_Full diff: {range_str}_")
    lines.append("")
    lines.append("🌐 [xtools.daobuddy.xyz](https://xtools.daobuddy.xyz/)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: generate_release_notes.py <new_tag> [--no-ai]", file=sys.stderr)
        sys.exit(1)

    new_tag  = sys.argv[1]
    use_ai   = "--no-ai" not in sys.argv

    prev     = previous_tag()
    commits  = commits_since(prev)
    diff     = diff_since(prev)
    entries  = parse_diff_entries(diff)
    contribs = contributors_since(prev)
    summary  = ai_summary(entries, commits, new_tag) if use_ai else None

    body = build_release_body(new_tag, prev, entries, commits, contribs, summary)
    print(body)


if __name__ == "__main__":
    main()
