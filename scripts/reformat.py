"""
Auto-reformat markdown files:
  - Align table column widths
  - Normalize blank lines between sections
  - Ensure trailing --- separators
  - Normalize **HP:** / **Physical Damage:** spacing
"""

import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Table formatter
# ---------------------------------------------------------------------------

def format_table(rows: list[str]) -> list[str]:
    """Reformat a markdown table block so all columns are evenly padded."""
    parsed: list[list[str]] = []
    for row in rows:
        # Split on | and strip outer empties
        cells = [c.strip() for c in row.split("|")]
        if cells and cells[0] == "":
            cells = cells[1:]
        if cells and cells[-1] == "":
            cells = cells[:-1]
        parsed.append(cells)

    if not parsed:
        return rows

    # Determine column count from header row
    col_count = max(len(r) for r in parsed)

    # Pad all rows to same column count
    for r in parsed:
        while len(r) < col_count:
            r.append("")

    # Detect separator row (all dashes) and rebuild it after measuring widths
    sep_idx: int | None = None
    for i, r in enumerate(parsed):
        if all(re.match(r"^-+$", c.strip()) for c in r if c.strip()):
            sep_idx = i
            break

    # Compute column widths from non-separator rows
    widths = [0] * col_count
    for i, r in enumerate(parsed):
        if i == sep_idx:
            continue
        for j, cell in enumerate(r):
            widths[j] = max(widths[j], len(cell))

    # Minimum width 3 for separator dashes
    widths = [max(w, 3) for w in widths]

    result: list[str] = []
    for i, r in enumerate(parsed):
        if i == sep_idx:
            cells = ["-" * widths[j] for j in range(col_count)]
        else:
            cells = [r[j].ljust(widths[j]) for j in range(col_count)]
        result.append("| " + " | ".join(cells) + " |")

    return result


# ---------------------------------------------------------------------------
# Line-level normalizations
# ---------------------------------------------------------------------------

def normalize_line(line: str) -> str:
    # Normalize **HP:** — ensure single space after colon
    line = re.sub(r"\*\*HP:\*\*\s+", "**HP:** ", line)
    # Normalize **Physical Damage:** spacing
    line = re.sub(r"\*\*Physical Damage:\*\*\s+", "**Physical Damage:** ", line)
    # Normalize damage range spacing: "16-20" → "16 - 20", already "16 - 20" stays
    line = re.sub(r"(\d+)\s*-\s*(\d+)", r"\1 - \2", line)
    return line


# ---------------------------------------------------------------------------
# Block-level reformat
# ---------------------------------------------------------------------------

def reformat_text(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Collect table block
        if line.startswith("|"):
            table_lines: list[str] = []
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            for formatted in format_table(table_lines):
                output.append(formatted)
            continue

        output.append(normalize_line(line))
        i += 1

    text = "\n".join(output)

    # Collapse 3+ consecutive blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Ensure file ends with single newline
    text = text.rstrip("\n") + "\n"

    return text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    root = Path(__file__).parent.parent
    targets = [
        root / "monster-data_4.md",
        root / "resource_hp_data.md",
    ]

    changed: list[str] = []
    for path in targets:
        if not path.exists():
            print(f"⚠️  Skipping missing file: {path.name}")
            continue

        original = path.read_text(encoding="utf-8")
        reformatted = reformat_text(original)

        if reformatted != original:
            path.write_text(reformatted, encoding="utf-8")
            changed.append(path.name)
            print(f"✏️  Reformatted: {path.name}")
        else:
            print(f"✅ No changes needed: {path.name}")

    if changed:
        print(f"\nReformatted {len(changed)} file(s): {', '.join(changed)}")
        sys.exit(0)  # exit 0 — CI will detect git diff and commit


if __name__ == "__main__":
    main()
