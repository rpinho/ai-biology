# B03: Incorrect NK nullcline, line35

Eq22 and Eq76 use hg+T, not hg+T^2. The extra square propagates through the CTL nullcline and tumor field. All other constants are held fixed in each before/after comparison.

Before at sigma=1000,k=1e-5,c=.001: T=0,17404.7359,19762510.0178 (two stable). After: only T=0 (stable). Full R/Python outputs also include residuals, folds and k=1e-4 image comparison.

Run `sh repro/B03/run.sh` from the workspace root. Saved evidence: [R](r_output.txt), [Python](python_output.txt), [R values](r_values.csv), [Python values](python_values.json), [minimal patch](patch.diff). [Preconditions and exact extraction patch](preconditions.md) explain which original expressions are executed and which unrelated demos are skipped.

The two implementations were written separately in this job by the same agent; this is not an independent referee. Full result scope and confidence are in ../../BUGS.md.
