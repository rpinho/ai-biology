"""Render the contributions table in README.md from tools/bio_prs.tsv and the GitHub API.

Run: python3 tools/render_bio_prs.py   (uses GITHUB_TOKEN if set; 10-ish unauthenticated calls are fine)
Rewrites only the text between <!-- auto:bio-prs --> and <!-- /auto:bio-prs -->.
"""
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- auto:bio-prs -->", "<!-- /auto:bio-prs -->"


def pr_status(repo: str, number: str) -> str:
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/pulls/{number}")
    req.add_header("Accept", "application/vnd.github+json")
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        pr = json.load(resp)
    if pr.get("merged_at"):
        return f"merged {pr['merged_at'][:10]}"
    return "closed" if pr["state"] == "closed" else "open"


def main() -> None:
    rows, statuses = [], []
    for line in (ROOT / "tools/bio_prs.tsv").read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        repo, number, fix = line.split("\t")
        url = f"https://github.com/{repo}/pull/{number}"
        status = pr_status(repo, number)
        statuses.append(status.split()[0])
        rows.append(f"| [{repo}](https://github.com/{repo}) | [#{number}]({url}) | {fix} | {status} |")
    merged, opened, closed = (statuses.count(k) for k in ("merged", "open", "closed"))
    table = "\n".join(
        [
            f"{len(rows)} PRs: {merged} merged, {opened} open, {closed} closed.",
            "",
            "| Repo | PR | Fix | Status |",
            "| --- | --- | --- | --- |",
            *rows,
        ]
    )
    readme = ROOT / "README.md"
    text = readme.read_text()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), f"{START}\n{table}\n{END}", text, flags=re.S)
    readme.write_text(new)


if __name__ == "__main__":
    main()
