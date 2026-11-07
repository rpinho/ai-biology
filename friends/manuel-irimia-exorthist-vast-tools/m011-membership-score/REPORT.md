Independent referee result: HOLDS WITH CAVEATS. The precise M011 species-selector witness and correction reproduce; neither orthology accuracy nor biological impact has been established. VERDICT.md is the requested short deliverable.

I read the primary publisher article and independently downloaded its Europe PMC XML, current source, historical source, official release archive and nf-test snapshot. Manuel Irimia is a listed author. The paper's membership score divides incoming matches, outgoing matches and reciprocal-neighbor count by twice the other-species exon count plus original gene-group size minus contributing same-species genes. That differs from the release's effective same-species gene count of one. The paper's >97% exon-recovery agreement with liftOver measures something else entirely.

The audit code is independent_audit.py. It parses the edge file and a supplied partition, reconstructs directed degrees and reciprocal neighbor sets without trusting the input reciprocity flags, counts species and genes directly, and evaluates rational scores with Fraction. All 2,144 edges are distinct, all reciprocal flags agree with actual reverse edges, each query has at most one target exon per target gene, and all 1,108 vertices occur exactly once. It checks every integer output component and tests score agreement within half a two-decimal unit. It imports no claimant search/verifier implementation. I did not inspect or execute the claimant's Python verifier or search code.

Fresh native execution of the official D2 source reconstructs the same partition. The unmodified official Perl formatter gives golden MD5 02479360ed2b8d659612fc60477ad355. The independently derived two-line patch in adversarial_replays.py is identical to the submitted R patch and yields corrected SHA256 5bc3a8a7494e9592a468e06d61c1a45ec816be7d9b565222ca586d456e8595c7. All 18 changes occur where multiple same-species genes contribute. Setting that count to one reproduces every original score. The other 1,090 scores, all integer graph fields, all final-table identities and all 377 clusters are unchanged.

I also ran the complete unmodified official pipeline from its public genome/GTF test inputs, in a fresh work directory without a prior Nextflow cache. It completed in 1m22s and reproduced the golden table byte-for-byte. Its generated edge graph SHA256 is 8345ecfff3b1f3fdeaaedd449f088b80aa9cb180c6c33706a514ffa1e77ecbe6, exactly the submitted graph. The claimed original gene input is byte-identical to the public test input. This establishes graph provenance independently of the claimant's intermediate outputs. The corrected path was executed as a fresh D2/formatter replay, not a second complete sequence-alignment pipeline.

The four-node witness was extracted independently from the newly reproduced partition and original edge file. It has eight directed edges and the full four-gene universe. Both R versions were rerun on it. Thirty-two fixed-seed edge-row shuffles were implemented afresh with Python Random and four concurrent R workers; every run preserved the canonical partition and exon-wise scores and had zero unclustered nodes. This supports only this bounded ordering claim.

There is no statistical hold-out. Public release-test reuse is appropriate to diagnose this deterministic software discrepancy but cannot estimate generalization or biological accuracy. Five material hashes in the supplied seal match fresh public-source reproduction; the seal has no independently authenticated timestamp. I therefore do not certify when the claimant first inspected outcomes.

Literal paper conformance is a separate limitation: 48 original scores and 30 species-corrected scores disagree with the paper's original-gene-group denominator. All corrected scores agree only with the alternative edge-observed gene universe. M011 expressly discloses this limitation and excludes the separate M021 repair, so it does not refute the narrow 18-row result. I have not independently refereed M021.

The public pinned environment was reinstalled under the audit's own pod directory: R4.1.3, igraph1.4.3, hashmap0.2.2, Nextflow24.10.0, Java17 and CLUSTALW2.1. MAFFT7.429 was fetched from the alternate official DDBJ host after the original host timed out; its archive SHA256 matches a939b153a5ebaa18a786ad0598ce11d177f4ccff698404a9f9686a38fc6ee67b. It was built with -fcommon, without algorithm changes. Runtime versions, compiler log, package URL/hash lock, download receipts, trace and logs are retained. This does not establish equivalence for all datasets or for the R4.4.2 container.

Exact command entrypoints executed, all on the shared ref pod under /workspace/ref_manuel_M011, at nice 10 with the long pipeline/order controls restricted to eight CPUs:

```sh
# After transferring this job's scripts/data through friends_podsh.py:
nohup nice -n 10 python3 fetch_public.py > fetch.log 2>&1 </dev/null &
# Public conda environment; setup_worker.sh records the original command.
MAMBA_ROOT_PREFIX="$PWD/mamba" bin/micromamba --no-rc create -y -p "$PWD/env" -f lock.txt
# Historical MAFFT fallback, build and full original pipeline:
python3 fetch_mafft_fallback.py
nohup nice -n 10 taskset -c "$CPUSET" bash build_and_run.sh > pipeline.log 2>&1 </dev/null &
# Independent arithmetic and native original/corrected graph replays:
nice -n 10 python3 independent_audit.py
nohup nice -n 10 bash pod_rerun.sh > rerun.log 2>&1 </dev/null &
# Independent patch, minimal witness, and all 32 row-order controls:
nohup nice -n 10 taskset -c "$CPUSET" python3 adversarial_replays.py > adversarial.log 2>&1 </dev/null &
nice -n 10 python3 pipeline_evidence.py
nice -n 10 python3 closing_audit.py
```

These are the executed fresh-directory commands. CPUSET was the first eight CPUs in sched_getaffinity(0). Use fresh replay/output directories for another execution: the original R script appends to files, and my control runner intentionally rejects existing score files. Shell/config entrypoints, public source URLs and small input/output files are in evidence/. Large public archives, genomes, environments and work directories remain only on the pod; retained evidence totals about 3.4 MB before compression.

PRIOR_ART.md records the searches. The closing recheck at 2026-11-02T12:05:20Z found latest release v2.0.0 and unchanged master plus all six prescribed AI indexes; the issue/PR list and recently updated repository search also remain unchanged. Both official branches and four public forks retain the selector mistake. No matching fix was found among 41 issue/PR records, seven PRs and 102 comments, or focused public literature/community searches. This bounded absence is not a global novelty claim. No accuracy leaderboard applies to this arithmetic regression audit.

Primary sources: https://doi.org/10.1186/s13059-021-02441-9 ; https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8379844/fullTextXML ; https://github.com/biocorecrg/ExOrthist ; https://github.com/biocorecrg/ExOrthist/releases/tag/v2.0.0 ; https://github.com/biocorecrg/ExOrthist/blob/v2.0.0/tests/workflows/main.nf.test.snap . Source snapshots, hashes and closing receipts are retained.

Next useful experiment: freeze one independently chosen public dataset and test whether a corrected literal-formula score changes a predeclared downstream decision. Present this result to the author as a small maintenance fix if contact is separately authorized; there is no basis here for a biological-discovery claim. No posting, messaging, credential transfer, pod lifecycle action or write outside this local claim directory was performed. The stalled download worker was stopped, every tracked pod worker subsequently exited, and ps-based cleanup evidence is in evidence/process_receipt.json.
