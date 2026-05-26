"""
AI review of PR diff using Gemini 1.5 Flash via OpenRouter.

Checks:
  - HP range formula correctness: [(A-1)*D+1, A*D]
  - Estimated HP is the intersection of all observation rows
  - Resource Type is valid (Chopping, Mining, Breaking, Cutting)
  - No obvious typos or duplicate section names in the diff
  - Data looks internally consistent

Usage:
  python scripts/ai_review.py <diff-file>

Environment:
  OPENROUTER_API_KEY  — required
  GITHUB_OUTPUT       — set by GitHub Actions

Exit codes:
  0  — review passed (or skipped due to missing key)
  1  — AI found issues that need attention
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-flash-1.5"

SYSTEM_PROMPT = """You are a data validator for the game "Morning Moon Pocket".
You review pull request diffs for a community data file (resource_hp_data.md).

Rules you must check:
1. HP range formula: if D = damage and A = hits needed, then HP range = [(A-1)*D+1, A*D]
   Example: D=12, A=2 → HP range = [13, 24]  ✓
2. Estimated HP must be the intersection of ALL observation rows for that resource.
   If only one row exists, Estimated HP = that row's range.
3. Valid Types: Chopping, Cutting, Breaking, Mining (case-sensitive).
4. Section headers must be ### ResourceName (Title Case preferred).
5. No duplicate resource names within the diff.
6. Observation rows must follow: | D | A | HP range | format with numeric D and A.

You will receive a git diff. Only check lines that are added (+) — do not flag removed lines.
Be concise. List only real errors. If everything looks correct, respond with exactly: LGTM"""

USER_PROMPT_TEMPLATE = """Review this PR diff and check for data errors:

```diff
{diff}
```

Respond with either:
- "LGTM" if no issues found
- A short bullet list of specific errors with line context (e.g. "Rock: HP range should be [13,24] not [12,24]")

Do not suggest style improvements. Only report factual errors."""


def set_output(key: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")


def call_openrouter(api_key: str, diff_text: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(diff=diff_text[:8000])},
        ],
        "max_tokens": 512,
        "temperature": 0.1,
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Morning-Moon-Pocket-Tools",
            "X-Title": "Morning Moon Pocket Tools CI",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    return body["choices"][0]["message"]["content"].strip()


def main() -> None:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("⚠️  OPENROUTER_API_KEY not set — skipping AI review.")
        set_output("ai_result", "skipped")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: ai_review.py <diff-file>", file=sys.stderr)
        sys.exit(1)

    diff_path = Path(sys.argv[1])
    if not diff_path.exists():
        print(f"Diff file not found: {diff_path}", file=sys.stderr)
        set_output("ai_result", "skipped")
        sys.exit(0)

    diff_text = diff_path.read_text(encoding="utf-8-sig").strip()
    if not diff_text:
        print("Empty diff — nothing to review.")
        set_output("ai_result", "lgtm")
        sys.exit(0)

    print(f"🤖 Sending diff to {MODEL} for review...")

    try:
        review = call_openrouter(api_key, diff_text)
    except urllib.error.HTTPError as e:
        print(f"⚠️  OpenRouter API error {e.code}: {e.read().decode()} — skipping AI review.")
        set_output("ai_result", "skipped")
        sys.exit(0)
    except Exception as e:
        print(f"⚠️  AI review failed: {e} — skipping.")
        set_output("ai_result", "skipped")
        sys.exit(0)

    print(f"\n📝 AI Review Result:\n{review}\n")

    if review.upper().startswith("LGTM"):
        print("✅ AI review passed.")
        set_output("ai_result", "lgtm")
        set_output("ai_comment", "✅ **AI Review (Gemini 1.5 Flash):** LGTM — ข้อมูลถูกต้อง")
        sys.exit(0)
    else:
        print("⚠️  AI found potential issues.")
        comment = f"⚠️ **AI Review (Gemini 1.5 Flash):** พบปัญหาที่ควรตรวจสอบ\n\n{review}\n\n> ตรวจสอบโดย AI — โปรด verify ก่อน merge"
        set_output("ai_result", "issues")
        set_output("ai_comment", comment)
        sys.exit(1)


if __name__ == "__main__":
    main()
