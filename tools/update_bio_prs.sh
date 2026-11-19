#!/bin/zsh
# The PR table moved to rpinho/fixing-research-software (11-19): one table for all fields, rendered from
# fixing-research-software/tools/prs.tsv. This wrapper keeps the daily launch agent (com.ricardo.ai-biology-prs)
# and existing callers working; it re-renders all three READMEs, including this repo's biology rows.
exec ~/dev/fixing-research-software/tools/update_prs.sh "$@"
