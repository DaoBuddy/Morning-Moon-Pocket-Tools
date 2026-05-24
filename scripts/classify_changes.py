"""
Classify PR changes as 'new' or 'update'.

  new    — only new sections (## Monster or ### Resource) were added,
           no existing lines were modified or deleted.
  update — at least one existing line was changed or removed.

Usage:
  python scripts/classify_changes.py <path-to-diff-file>

Outputs:
  Sets GitHub Actions output  change_type=new|update
  Prints a human-readable summary.
  Exits 0 always (classification itself is not a failure).
"""

import os
import re
import sys
from pathlib import Path


DATA_FILES = {"monster-data_4.md", "resource_hp_data.md"}

# Patterns that mark the start of a new entry
NEW_MONSTER_RE = re.compile(r"^\+## .+")
NEW_RESOURCE_RE = re.compile(r"^\+### .+")
ADDED_LINE_RE = re.compile(r"^\+(?!\+\+)")   # + but not +++
REMOVED_LINE_RE = re.compile(r"^-(?!--)")    # - but not ---


def set_output(key: str, value: str) -> None:
    """Write to GITHUB_OUTPUT if available, otherwise print."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")
    print(f"::set-output name={key}::{value}")


def classify_diff(diff_text: str) -> tuple[str, dict]:
    """
    Returns ('new'|'update', stats_dict).

    Strategy:
    - Track whether we are inside a hunk that belongs to a data file.
    - When we see a removed line (-) that is not a section header → 'update'.
    - When we see an added section header without any preceding removed section
      header → genuinely new section.
    """
    in_data_file = False
    removed_lines: list[str] = []
    added_section_headers: list[str] = []
    modified_content_lines: list[str] = []

    for line in diff_text.splitlines():
        # File header
        if line.startswith("diff --git"):
            # Check if this diff is for one of our data files
            in_data_file = any(f in line for f in DATA_FILES)
            continue

        if not in_data_file:
            continue

        # Skip diff metadata lines
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue

        if REMOVED_LINE_RE.match(line):
            content = line[1:]
            # A removed section header means a section was renamed/deleted → update
            if content.startswith("## ") or content.startswith("### "):
                modified_content_lines.append(f"Removed section: {content.strip()}")
            else:
                modified_content_lines.append(f"Removed: {content.strip()}")

        elif ADDED_LINE_RE.match(line):
            content = line[1:]
            if NEW_MONSTER_RE.match(line) or NEW_RESOURCE_RE.match(line):
                added_section_headers.append(content.strip())

    # Determine type
    # If any non-section lines were removed → update
    has_removals = bool(modified_content_lines)

    stats = {
        "new_sections": added_section_headers,
        "removed_or_modified": modified_content_lines,
    }

    change_type = "update" if has_removals else "new"
    return change_type, stats


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: classify_changes.py <diff-file>", file=sys.stderr)
        sys.exit(1)

    diff_path = Path(sys.argv[1])
    if not diff_path.exists():
        print(f"Diff file not found: {diff_path}", file=sys.stderr)
        # Default to 'update' (safer — requires manual review)
        set_output("change_type", "update")
        sys.exit(0)

    diff_text = diff_path.read_text(encoding="utf-8")
    change_type, stats = classify_diff(diff_text)

    print(f"\n📊 Change Classification: {change_type.upper()}")
    if stats["new_sections"]:
        print(f"  New sections added ({len(stats['new_sections'])}):")
        for s in stats["new_sections"]:
            print(f"    + {s}")
    if stats["removed_or_modified"]:
        print(f"  Modified/removed lines ({len(stats['removed_or_modified'])}):")
        for s in stats["removed_or_modified"][:20]:  # cap output
            print(f"    - {s}")

    if change_type == "new":
        print("\n✅ Only new data detected — eligible for auto-merge.")
    else:
        print("\n⚠️  Existing data was modified — manual review required.")

    set_output("change_type", change_type)


if __name__ == "__main__":
    main()
