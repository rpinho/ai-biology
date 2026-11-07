# Independent referee report

The declared theorem survives. See VERDICT.md for the decision and
AUDIT_PROOF.md for the independently reviewed count argument.
REFEREE_CERTIFICATE.json contains exact rational interval certificates;
referee_run.txt contains the original pod stdout, ending in PASS.
The scientific calculation took about 1.34 seconds on the shared ref pod.

Reproduction from this directory (all scientific work is on ref):

```sh
python3 stream_payload.py referee.py run_referee.sh
python3 pod_transport.py run_referee.sh 150 > referee_run.txt
python3 pod_transport.py source_inspect.sh 150 > source_inspect.txt
python3 stream_payload.py source_audit.py run_source_audit.sh
python3 pod_transport.py run_source_audit.sh 200 > source_audit.json
python3 pod_transport.py prior_followup.sh 150 > prior_followup.json
```

pod_transport.py executes the original supplied friends_podsh.py in memory,
changing only its temporary script creation into base64-to-bash streaming.
The normal helper failed with ENOSPC: the pod's 120 GB overlay was full.
Neither /tmp nor the permitted job directory could accept files. No pod
filesystem writes, package installation or background jobs were needed;
the short exact calculations ran from stdin. No Mini scientific computation,
claimant search/verifier imports, private uploads, contacts or pod changes.
Python packages on the pod: SymPy 1.13.3, SciPy 1.18.1 (SciPy was only
identified during source inspection, not used in the exact certificate).

Exact results: compact witness has 4 physical positive simple roots, 2 stable;
boundary eigenvalues are -1/10,-1,-1, giving 3 stable states overall. Stable
positive T values are 1.563147899242922 and 13.997093582532525. Other roots
have a3<0. Independent Table 3 witness roots are 257.9086426859718 (unstable)
and 9720.510428032612 (stable); boundary eigenvalues -43/500,-1,-2 give 2.
No positive-root poles occur in either witness. The exact general Schur
identity and the Table 3 all-positive-coupling coefficient proof both pass.
The universal crossing argument is a reviewed mathematical proof, not a
formal proof-assistant result. The code's decimal endpoints are summaries;
the exact rational endpoints, not those rounded decimals, certify the signs.

Primary source receipts, legacy code limitation, author identity and bounded
literature/public-code searches are in PRIOR_ART.md and source_audit.json.
The paper already gives the quintic, scalar alternation and numerical
bistability. Relative to that paper, this submission supplies an attained
three-state full-system capacity and the stricter Table 3 global bound.
No observational holdout exists; witness search is permissible for this
exact existence theorem. Broad parameter freedom explains why the witness
has an additional stable state; no gain at the paper's fixed constants is
established. NEXT BAR is an exact tristable witness inside independently
sourced physiological parameter bounds, should that interpretation be wanted.
