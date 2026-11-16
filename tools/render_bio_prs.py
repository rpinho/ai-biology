"""Render the contributions table in README.md from tools/bio_prs.tsv and the GitHub API.

Run: python3 tools/render_bio_prs.py   (set GITHUB_TOKEN: 3 API calls per PR exceed the unauthenticated limit)\nbio_prs.tsv columns: repo, PR number, one-line description, optional type (bug fix | speedup | tests/CI | tool; default bug fix).\nDaily refresh + push: tools/update_bio_prs.sh (launch agent com.ricardo.ai-biology-prs).
Rewrites only the text between <!-- auto:bio-prs --> and <!-- /auto -->.
With --stdout it prints the table instead, for readme-blocks (readme-blocks.json).
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- auto:bio-prs -->", "<!-- /auto -->"


BOTS = re.compile(r"bot|copilot|reviewer|github-actions|^claude$|^rpinho$", re.I)
TYPES = ("bug fix", "speedup", "tests/CI", "tool")


def api(path: str):
    req = urllib.request.Request(f"https://api.github.com/{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def pr_status(repo: str, number: str) -> str:
    pr = api(f"repos/{repo}/pulls/{number}")
    if pr.get("merged_at"):
        return f"merged {pr['merged_at'][:10]}"
    if pr["state"] == "closed":
        return "closed"
    # Human replies only: maintainers' comments and reviews, not bots or our own pings.
    people = [c["user"]["login"] for c in api(f"repos/{repo}/issues/{number}/comments?per_page=100")]
    people += [r["user"]["login"] for r in api(f"repos/{repo}/pulls/{number}/reviews?per_page=100") if r.get("user")]
    replies = sum(1 for login in people if not BOTS.search(login))
    return f"open, {replies} repl{'y' if replies == 1 else 'ies'}" if replies else "open"


def render() -> str:
    rows, statuses = [], []
    for line in (ROOT / "tools/bio_prs.tsv").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        repo, number, fix, *rest = line.split("\t")
        kind = rest[0] if rest else "bug fix"
        if kind not in TYPES:
            raise SystemExit(f"bio_prs.tsv: unknown type {kind!r} for {repo}#{number}; use one of {TYPES}")
        url = f"https://github.com/{repo}/pull/{number}"
        status = pr_status(repo, number)
        statuses.append(status.split()[0].rstrip(","))
        rows.append(f"| [{repo}](https://github.com/{repo}) | [#{number}]({url}) | {kind} | {fix} | {status} |")
    merged, opened, closed = (statuses.count(k) for k in ("merged", "open", "closed"))
    table = "\n".join(
        [
            f"{len(rows)} PRs: {merged} merged, {opened} open, {closed} closed.",
            "",
            "| Repo | PR | Type | What it does | Status |",
            "| --- | --- | --- | --- | --- |",
            *rows,
        ]
    )
    return table


def main() -> None:
    table = render()
    if "--stdout" in sys.argv[1:]:
        print(table)
        return
    readme = ROOT / "README.md"
    text = readme.read_text()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), f"{START}\n{table}\n{END}", text, flags=re.S)
    readme.write_text(new)


if __name__ == "__main__":
    main()
