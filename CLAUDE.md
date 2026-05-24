# CLAUDE.md — AI Contributor Guide

This file tells AI assistants (Claude Code, GitHub Copilot, OpenAI Codex, etc.)
everything they need to know to contribute to this repository correctly.

---

## Project Purpose

This is a **community data repository** for the game **Morning Moon Pocket**.
It stores monster stats and wild resource HP values as Markdown files.
The data feeds the tool website at https://xtools.daobuddy.xyz/

There is **no application code** to run. The entire codebase is Markdown data + CI scripts.

---

## Repository Layout

```
monster-data_4.md        Monster database (HP, damage, debuffs, item drops)
resource_hp_data.md      Wild resource HP observations (trees, rocks, etc.)
scripts/
  validate.py            Format validator — run before submitting a PR
  reformat.py            Auto-formatter — normalizes tables & spacing
  classify_changes.py    Detects new vs updated entries (used by CI)
  generate_release_notes.py  Monthly release notes generator
.github/workflows/
  pr-check.yml           CI: reformat → validate → classify → auto-merge or review
  monthly-release.yml    Cron: monthly snapshot release with AI summary
VERSION                  Current snapshot version (vYYYY.MM)
```

---

## Data Format Rules

### Monster File (`monster-data_4.md`)

Each monster is a `##` section followed by bold stat lines and an item drop table:

```markdown
## Monster Name
**HP:** 123
**Physical Damage:** 50 - 80
**Debuff:** Blind (5%) 1 Duration   ← optional

### Item Drop
| Item Name    | Chance | Amount  |
|--------------|--------|---------|
| Item A       | 100%   | 10 - 15 |
| Item B       | 20%    | 1       |

---
```

Rules:
- `**HP:**` must be a single integer.
- `**Physical Damage:**` must be `N - N` format with spaces around `-`.
- `### Item Drop` and its table are required.
- Sections are separated by `---`.

### Resource File (`resource_hp_data.md`)

Each resource is a `###` section:

```markdown
### Resource Name
- **Type:** Chopping | Breaking | Cutting
- **Reward:** N ItemName   ← optional

| D (your damage) | A (hits needed) | HP range         |
|-----------------|-----------------|------------------|
| 12              | 4               | 37 – 48          |
| 5               | 9               | 41 – 45          |

**Estimated HP:** 41–45 _(intersection of both ranges)_

---
```

HP range formula:
```
HP range = [ (A-1)×D + 1 , A×D ]
Estimated HP = intersection of all ranges
```

---

## AI Tasks — What You Can Help With

### 1. Add a New Monster

When a user says "add monster X with HP Y, damage A-B, drops C at Z%":

```markdown
## X
**HP:** Y
**Physical Damage:** A - B

### Item Drop
| Item Name | Chance | Amount |
|-----------|--------|--------|
| C         | Z%     | 1      |

---
```

Then run:
```bash
python scripts/reformat.py
python scripts/validate.py
```

### 2. Add a Resource Observation

When a user says "I hit [Resource] with damage D and needed A hits":

Calculate: HP range = `[(A-1)×D + 1, A×D]`

Add a row to the resource's table and recalculate **Estimated HP** as the intersection.

Then run:
```bash
python scripts/reformat.py
python scripts/validate.py
```

### 3. Validate & Reformat

```bash
python scripts/validate.py      # check for format errors
python scripts/reformat.py      # auto-fix table alignment and spacing
```

### 4. Check What Type of Change This Is

```bash
git diff main -- monster-data_4.md resource_hp_data.md > /tmp/pr.diff
python scripts/classify_changes.py /tmp/pr.diff
# Output: change_type=new  OR  change_type=update
```

### 5. Generate Release Notes Locally

```bash
# With AI summary (requires GEMINI_API_KEY — free tier available at aistudio.google.com)
GEMINI_API_KEY=AIza... python scripts/generate_release_notes.py v2026.06

# Without AI summary
python scripts/generate_release_notes.py v2026.06 --no-ai
```

---

## CI Behavior (for AI to understand)

When a PR is opened against `main`:

1. **Reformat** — tables are auto-aligned and committed back to the PR branch.
2. **Validate** — format rules are checked; PR fails if invalid.
3. **Classify** — determines `new` or `update`:
   - `new` → only new `## Monster` or `### Resource` sections added → **auto-merged**.
   - `update` → existing lines changed/removed → **requires manual approval**.

---

## Contribution Rules for AI

- Never modify the `## How HP is calculated` or `## Contribution template` sections.
- Always place a new monster in alphabetical order (or at the end if unsure).
- Always end a section with `---` on its own line.
- Do not add columns to existing tables — only add rows.
- Do not change `**Estimated HP:**` lines for resources unless you have recalculated the intersection from all observation rows.
- Keep damage ranges as `N - N` (spaces around the dash).

---

## What AI Should NOT Do

- Do not invent HP or damage values — only add data provided by the user.
- Do not delete existing monster or resource sections.
- Do not modify `scripts/` or `.github/workflows/` unless explicitly asked.
- Do not push directly to `main` — always use a PR.
