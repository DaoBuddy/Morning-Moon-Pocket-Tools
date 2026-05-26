"""
Classify PR changes as 'new' or 'update'.

  new    — only additive changes: new sections or new observation rows added.
           No existing content was removed or modified.
  update — at least one existing line was deleted or modified.

Rule: data must only grow. Any reduction → manual review required.

Usage:
  python scripts/classify_changes.py <path-to-diff-file>

Outputs:
  Sets GitHub Actions output  change_type=new|update
  Exits 0 always (classification itself is not a failure).
"""

import os
import re
import sys
from pathlib import Path


DATA_FILES = {"monster-data_4.md", "resource_hp_data.md"}

ADDED_LINE_RE   = re.compile(r"^\+(?!\+\+)")  # + but not +++
REMOVED_LINE_RE = re.compile(r"^-(?!--)")     # - but not --- separator

# Lines that are purely structural/derived — changes allowed without review
DERIVED_LINE_RE = re.compile(
    r"^\*\*Estimated HP:\*\*"   # recalculated summary line
)


def set_output(key: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")
    print(f"::set-output name={key}::{value}")


def classify_diff(diff_text: str) -> tuple[str, dict]:
    """
    Returns ('new'|'update', stats_dict).

    A change is 'new' only when:
    - No existing content lines are removed (ignoring whitespace-only diffs
      which are already filtered by --ignore-all-space in git diff).
    - Removed section headers count as deletions.
    - Removed observation rows (table data rows) count as deletions.
    - Changes to **Estimated HP:** lines are allowed only when they accompany
      new observation rows (recalculation), not standalone removals.
    """
    in_data_file = False
    new_sections: list[str] = []
    deleted_lines: list[str] = []
    new_obs_rows = 0   # added | D ... | rows

    for line in diff_text.splitlines():
        if line.startswith("diff --git"):
            in_data_file = any(f in line for f in DATA_FILES)
            continue

        if not in_data_file:
            continue

        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            continue

        if REMOVED_LINE_RE.match(line):
            content = line[1:].strip()

            # Ignore blank lines removed (reformat sometimes removes trailing blanks)
            if not content:
                continue

            # Derived lines: allow if accompanied by new obs rows (handled below)
            if DERIVED_LINE_RE.match(content):
                # Mark as pending — resolved after full parse
                deleted_lines.append(("derived", content))
                continue

            deleted_lines.append(("data", content))

        elif ADDED_LINE_RE.match(line):
            content = line[1:].strip()

            if line.startswith("+## ") or line.startswith("+### "):
                new_sections.append(content)

            # Observation row: starts with | and contains a digit in first cell
            if re.match(r"^\+\|\s*\d", line):
                new_obs_rows += 1

    # Resolve derived-line deletions:
    # If **Estimated HP** was removed alongside new observation rows being added,
    # it's a legitimate recalculation → not a deletion.
    real_deletions = []
    for kind, content in deleted_lines:
        if kind == "derived" and new_obs_rows > 0:
            continue  # recalculation — OK
        real_deletions.append(content)

    change_type = "update" if real_deletions else "new"

    stats = {
        "new_sections": new_sections,
        "new_obs_rows": new_obs_rows,
        "deleted_lines": real_deletions,
    }
    return change_type, stats


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: classify_changes.py <diff-file>", file=sys.stderr)
        sys.exit(1)

    diff_path = Path(sys.argv[1])
    if not diff_path.exists():
        print(f"Diff file not found: {diff_path}", file=sys.stderr)
        set_output("change_type", "update")
        sys.exit(0)

    diff_text = diff_path.read_text(encoding="utf-8-sig")  # strip BOM if present
    change_type, stats = classify_diff(diff_text)

    print(f"\n📊 Change Classification: {change_type.upper()}")
    if stats["new_sections"]:
        print(f"  New sections ({len(stats['new_sections'])}):")
        for s in stats["new_sections"]:
            print(f"    + {s}")
    if stats["new_obs_rows"]:
        print(f"  New observation rows added: {stats['new_obs_rows']}")
    if stats["deleted_lines"]:
        print(f"  Deleted/modified lines ({len(stats['deleted_lines'])}) — REVIEW REQUIRED:")
        for s in stats["deleted_lines"][:20]:
            print(f"    - {s}")

    if change_type == "new":
        print("\n✅ Additive-only changes — eligible for auto-merge.")
    else:
        print("\n⚠️  Existing data was removed or modified — manual review required.")

    set_output("change_type", change_type)


if __name__ == "__main__":
    main()
