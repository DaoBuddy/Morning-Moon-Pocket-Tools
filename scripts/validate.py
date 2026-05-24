"""
Validate markdown format for monster-data and resource_hp_data files.
Exits with code 1 if any validation error is found.
"""

import re
import sys
from pathlib import Path

ERRORS: list[str] = []


def err(file: str, line: int, msg: str) -> None:
    ERRORS.append(f"{file}:{line}: {msg}")


# ---------------------------------------------------------------------------
# Monster file validation
# ---------------------------------------------------------------------------

def validate_monster_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    name = path.name

    in_monster = False
    monster_name = ""
    monster_start = 0
    has_hp = False
    has_phys = False
    has_item_drop = False
    has_table = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # New monster section
        if line.startswith("## ") and not line.startswith("## How"):
            # Close previous
            if in_monster:
                if not has_hp:
                    err(name, monster_start, f"Monster '{monster_name}' missing **HP:**")
                if not has_phys:
                    err(name, monster_start, f"Monster '{monster_name}' missing **Physical Damage:**")
                if not has_item_drop:
                    err(name, monster_start, f"Monster '{monster_name}' missing ### Item Drop")
                if not has_table:
                    err(name, monster_start, f"Monster '{monster_name}' missing item drop table")

            in_monster = True
            monster_name = line[3:].strip()
            monster_start = i + 1
            has_hp = has_phys = has_item_drop = has_table = False

        elif in_monster:
            if re.match(r"\*\*HP:\*\*\s+\d+", line):
                has_hp = True
            if re.match(r"\*\*Physical Damage:\*\*\s+\d+\s*-\s*\d+", line):
                has_phys = True
            if line.strip() == "### Item Drop":
                has_item_drop = True
            if line.startswith("| Item Name"):
                has_table = True

        i += 1

    # Close last monster
    if in_monster:
        if not has_hp:
            err(name, monster_start, f"Monster '{monster_name}' missing **HP:**")
        if not has_phys:
            err(name, monster_start, f"Monster '{monster_name}' missing **Physical Damage:**")
        if not has_item_drop:
            err(name, monster_start, f"Monster '{monster_name}' missing ### Item Drop")
        if not has_table:
            err(name, monster_start, f"Monster '{monster_name}' missing item drop table")


# ---------------------------------------------------------------------------
# Resource file validation
# ---------------------------------------------------------------------------

def validate_resource_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    name = path.name

    in_resource = False
    resource_name = ""
    resource_start = 0
    has_type = False
    table_header_seen = False
    table_sep_seen = False

    SKIP_SECTIONS = {"Resources", "How HP is calculated", "Contribution template"}

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("### "):
            # Close previous
            if in_resource and resource_name not in SKIP_SECTIONS:
                if not has_type:
                    err(name, resource_start, f"Resource '{resource_name}' missing - **Type:**")
                if table_header_seen and not table_sep_seen:
                    err(name, resource_start, f"Resource '{resource_name}' table missing separator row")

            resource_name = line[4:].strip()
            resource_start = i + 1
            in_resource = True
            has_type = False
            table_header_seen = False
            table_sep_seen = False

        elif in_resource:
            if re.match(r"-\s+\*\*Type:\*\*", line):
                has_type = True
            if line.startswith("| D (your damage)"):
                table_header_seen = True
            if table_header_seen and re.match(r"\|[-| ]+\|", line):
                table_sep_seen = True

        i += 1

    # Close last resource
    if in_resource and resource_name not in SKIP_SECTIONS:
        if not has_type:
            err(name, resource_start, f"Resource '{resource_name}' missing - **Type:**")
        if table_header_seen and not table_sep_seen:
            err(name, resource_start, f"Resource '{resource_name}' table missing separator row")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    root = Path(__file__).parent.parent

    monster_file = root / "monster-data_4.md"
    resource_file = root / "resource_hp_data.md"

    if monster_file.exists():
        validate_monster_file(monster_file)
    else:
        ERRORS.append(f"Missing file: {monster_file.name}")

    if resource_file.exists():
        validate_resource_file(resource_file)
    else:
        ERRORS.append(f"Missing file: {resource_file.name}")

    if ERRORS:
        print("❌ Validation failed:")
        for e in ERRORS:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("✅ All files passed validation.")


if __name__ == "__main__":
    main()
