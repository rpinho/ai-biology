#!/bin/zsh
# Re-render the bio PR table from the GitHub API and push it if anything changed (merges, closes, replies).
# Run after every new PR (bio lane open_pr.sh) and daily by launchd (com.ricardo.ai-biology-prs).
set -e -o pipefail
cd "${0:A:h:h}"
GH=/Users/ricardo/dev/.bin/gh
export GITHUB_TOKEN=$($GH auth token)
git pull -q --ff-only https://github.com/rpinho/ai-biology.git main
python3 tools/render_bio_prs.py
if git diff --quiet -- README.md tools/bio_prs.tsv; then echo "$(date '+%F %T') no change"; exit 0; fi
git add README.md tools/bio_prs.tsv
git -c user.name="Ricardo Pinho" -c user.email="rpinho@users.noreply.github.com" commit -q -m "bio PRs: refresh status ($(grep -o '^[0-9]* PRs: [^.]*' README.md))"
git -c credential.helper= -c credential.helper='!/Users/ricardo/dev/.bin/gh auth git-credential' push -q https://github.com/rpinho/ai-biology.git HEAD:main
echo "$(date '+%F %T') pushed: $(grep -o '^[0-9]* PRs: [^.]*' README.md)"
