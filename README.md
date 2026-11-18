![Biology with AI agents: Anthropic x Adaptyv, Arc Virtual Cell Challenge, Virtual Embryo Challenge](assets/banner.png)

# ai-biology

**AI for Biology & Drug Discovery.**

Everything I've run on biology with AI agents, in one place. Three sponsored challenges, two tools, and bug reports for scientists' published software. Each section links to the code and results, says how it was checked, and says where a result is still a candidate.

My PhD was on the evolution of gene regulatory networks, in Marcus Feldman's lab at Stanford: evolutionary biology and population genetics. I came back to it in 2026 with AI agents. Biology has been the hardest of the three fields I've worked in this year, after math and physics. Why, in the [field retro](RETRO.md).

Every result in one file, with its claim or bug report, checks and verdict copied from the result folders: [PAPER.md](PAPER.md).

Sister hubs: [math](https://github.com/rpinho/math-certificates) · [physics](https://github.com/rpinho/ai-physics) · [astronomy](https://github.com/rpinho/planet-hunt)

## Why it's laid out like this

Brian Armstrong wrote on November 7 that publicly funded science should work like open source: every experiment as a repo anyone can fork, rerun and fix, with replication rewarded like new papers ([post](https://x.com/brian_armstrong/status/2119150702446420027)). His point about AI matches what I keep hitting. Agents make finding things cheaper, so the bottleneck moves to checking them, and in biology checking usually means a wet lab.

So each result here ships with what you need to rerun it and a separate referee's verdict. A referee here is a different agent that rebuilds the claim from the primary source on a fresh clone, without the finder's code. Only CONFIRMED, HOLDS and HOLDS WITH CAVEATS results are listed, and the caveats stay attached.

## Challenges

| Challenge | What I entered | Status | Code |
|---|---|---|---|
| **Anthropic × Adaptyv Protein Design Competition** ([competition](https://proteinbase.com/competitions/anthropic-adaptyv-2026)) | Entries for Challenges 3, 4 and 5. The competition measures submitted entries in an automated lab and publishes every measurement, failures included. | Submitted; lab results not out at the time of writing | [adaptyv-challenges](https://github.com/rpinho/adaptyv-challenges) |
| **Arc Institute Virtual Cell Challenge 2026** ([site](https://virtualcellchallenge.org/)) | Predicting CRISPRi knockdown effects in an unseen cell type. Best official validation 0.16438, about rank 463 of 1,580 when recorded. The final phase closed November 5 and its scores are hidden. | Closed; [retro](https://github.com/rpinho/virtual-cell-challenge/blob/main/RETRO.md) published | [virtual-cell-challenge](https://github.com/rpinho/virtual-cell-challenge) |
| **Virtual Embryo Challenge** ([site](https://virtualembryo.ai/challenge)) | Community tools and an Agent Team entry: stage-window checks against public atlases, and synthetic tutorials on choosing what to submit and on building local proxy boards. No challenge data or results are published here. | Scoring closed; results December 11 | [virtual-embryo-community](https://github.com/rpinho/virtual-embryo-community) |

## Tools and older work

| Repo | What it is |
|---|---|
| [louis](https://github.com/rpinho/louis) | Pick an autoimmune disease, get trust-ranked candidate CD4+ T-cell targets, built on the Marson/Pritchard genome-scale T-cell Perturb-seq. MCP server, skill or Slack bot. Hypothesis generation, not a clinical claim. |
| [autoregulation](https://github.com/rpinho/autoregulation) | My PhD code: stability of Boolean gene regulatory networks depends on the sign of self-regulation. Python 2, kept as a record. Published (PLoS Comput Biol 2014; PLoS ONE 2012, 2015). |

## Friends' software: what was asked, what we found, how it was checked

Scientists I know publish code with their papers. I asked each of them whether a bug hunt would be useful, ran one on the public repository at a pinned commit, had a separate referee reproduce every finding from scratch, and sent them the report. Everything below has been sent to the person named. Their replies stay private; only what went out is here.

### Manuel Irimia — ExOrthist and vast-tools

- **Who:** [Manuel Irimia](https://www.crg.eu/en/programmes-groups/irimia-lab), ICREA at CRG and UPF, Barcelona. [ExOrthist](https://github.com/biocorecrg/ExOrthist) (Márquez et al., *Genome Biology* 2021, [doi:10.1186/s13059-021-02441-9](https://doi.org/10.1186/s13059-021-02441-9)) infers exon orthologies; [vast-tools](https://github.com/vastgroup/vast-tools) quantifies alternative splicing.
- **Asked:** he said yes to a report, so the hunt ran on public master, pinned at `83185dc` (ExOrthist) and `5598e1f` (vast-tools).
- **Found:** 32 bugs in ExOrthist (23 plus 9 minor) and 6 in vast-tools (4 plus 2 minor). Examples: a transcript-first GTF writes transcript IDs into gene slots; minus-strand CDS records in ascending order change the translated protein and reverse exon numbering; exon end positions include one residue of the next exon. Each has a `git apply` patch and a before/after repro. One candidate was judged intended behaviour and dropped.
- **Checked:** a separate referee reproduced all of them independently on pristine pinned clones — [ExOrthist A/B](friends/manuel-irimia-exorthist-vast-tools/referee/exorthist-a-b/VERDICTS.md), [ExOrthist C/D](friends/manuel-irimia-exorthist-vast-tools/referee/exorthist-c-d/VERDICTS.md), [vast-tools](friends/manuel-irimia-exorthist-vast-tools/referee/vast-tools/VERDICTS.md).
- **Separately, M011:** the released ExOrthist membership score disagrees with the formula printed in the paper's Methods on 18 of 1,108 rows of the official test (0.86 where the formula gives exactly 1). HOLDS WITH CAVEATS — the caveat is that a second, disclosed defect in the gene universe means the literal paper formula still fails on 30 rows after the fix. [Claim, report and verdict](friends/manuel-irimia-exorthist-vast-tools/m011-membership-score/).
- **Code and results:** [report, patches and repros](friends/manuel-irimia-exorthist-vast-tools/).

### Hugo Fernandes — pyglmnet

- **Who:** [Hugo L. Fernandes](https://scholar.google.com/citations?user=0Yy0dJkAAAAJ), computational neuroscience. [pyglmnet](https://github.com/glm-tools/pyglmnet) is the elastic-net GLM package he contributed to.
- **Asked:** he said that if we found things there, we could open PRs.
- **Found and upstreamed:** three fixes, each with a test that fails on master and passes with the fix — [PR #399](https://github.com/glm-tools/pyglmnet/pull/399) (Bernoulli log-likelihood is NaN at probabilities 0 and 1, and overflows for large logits), [PR #400](https://github.com/glm-tools/pyglmnet/pull/400) (gamma deviance and pseudo-R² omit the saturated log-likelihood; the fixed value matches statsmodels to 1e-15), [PR #401](https://github.com/glm-tools/pyglmnet/pull/401) (`simulate_glm(sample=True)` returns `exp(mu)` instead of gamma draws). [#399](https://github.com/glm-tools/pyglmnet/pull/399) and [#401](https://github.com/glm-tools/pyglmnet/pull/401) were merged on 2026-11-08; #400 is still open.
- **Checked:** a separate referee's [verdicts](friends/hugo-fernandes-pyglmnet/referee/VERDICTS.md), plus a full-suite [verification log](friends/hugo-fernandes-pyglmnet/VERIFY.txt) and [a review](friends/hugo-fernandes-pyglmnet/REVIEW.md) that sent the first draft back three times. Two further findings were left out because an existing open PR already covers one and the other is intended behaviour.
- **Code:** [PR texts, patches and the verification script](friends/hugo-fernandes-pyglmnet/).
- Hugo's optimization results are in the [math hub](https://github.com/rpinho/math-certificates), because they are exact optima rather than biology.

### Kris Sankaran — R packages

- **Who:** [Kris Sankaran](https://krisrs1128.github.io/LSLab/), statistics, UW-Madison. Packages: [multimedia](https://cran.r-project.org/package=multimedia), [structSSI](https://cran.r-project.org/package=structSSI), [miniLNM](https://github.com/krisrs1128/miniLNM).
- **Found:** 7 bugs (6 plus 1 minor). The top three: `multimedia`'s Gaussian glmnet and random-forest samplers pass a variance where `rnorm` expects a standard deviation, so simulated noise is squared; `structSSI`'s GBH gives every result the name of the first sorted hypothesis; `miniLNM` filters the design matrix by variable name and silently drops the intercept.
- **Checked:** separate referee, CONFIRMED, on pinned source and the installed CRAN versions. Verdicts and repros stay in the bug report sent to him; this hub links the summary rather than republishing his packages' sources.
- **Sent:** November 6, with patches and before/after output.

### Gavin Sherlock — GO::TermFinder

- **Who:** [Gavin Sherlock](https://sherlocklab.stanford.edu/), Stanford Genetics. [GO::TermFinder](https://metacpan.org/dist/GO-TermFinder) 0.86 (Boyle et al., *Bioinformatics* 2004, [doi:10.1093/bioinformatics/bth456](https://doi.org/10.1093/bioinformatics/bth456)).
- **Found:** 6 bugs (4 plus 2 minor). The top one: NOT-qualified GAF annotations are counted as positive evidence, which inflates enrichment for exactly the genes an annotator said the term does not apply to. Three further findings are already fixed in the Princeton fork and are named but not counted.
- **Checked:** separate referee on a fresh CPAN build.
- **Sent:** November 7, first contact, with an all-fixes patch.

### Marcel Salathé — COVID-Twitter-BERT and lab repos

- **Who:** [Marcel Salathé](https://people.epfl.ch/marcel.salathe), EPFL Digital Epidemiology. [COVID-Twitter-BERT](https://github.com/digitalepidemiologylab/covid-twitter-bert) ([arXiv:2005.07503](https://arxiv.org/abs/2005.07503)) and two other lab repositories.
- **Found:** 5 bugs (3 plus 2 minor). The top one: a single over-length line makes the whole `run_predict.py` batch fail, so an ordinary mixed text file cannot be scored. Numeric TSV labels crash fine-tuning data generation before any record is written. One further finding is inherited from upstream and is named but not counted.
- **Checked:** separate referee on independently downloaded pinned source, [verdicts](friends/salathe-covid-twitter-bert/VERDICTS.md).
- **Sent:** November 7, first contact.

### Victor Garcia — the NK-CTL model and a codon-rate preprint

- **Who:** Victor Garcia, mathematical modelling of immune responses and evolution, Switzerland. Garcia, Bonhoeffer and Fu, *J. Theor. Biol.* 2020, [doi:10.1016/j.jtbi.2020.110185](https://doi.org/10.1016/j.jtbi.2020.110185), with its R script on Figshare; the 2025 codon-rate preprint, [doi:10.1101/2025.06.03.657573](https://doi.org/10.1101/2025.06.03.657573).
- **Found:**
  - **The model (HOLDS, three separate referees):** global convergence and the exact bistability region of the NK-CTL model. [Note, checker and verdicts](friends/victor-garcia-nk-ctl/nk-ctl-note/).
  - **The script (CONFIRMED WITH CAVEATS):** line 35 of the released R script uses `hg + T²` where equations 22 and 76 use `hg + T`. At σ = 1000, k = 10⁻⁵, c = 0.001 that change creates a stable tumor state the printed model doesn't have. The caveat: the paper doesn't pin σ and k for Fig. A2, and the corrected model can still be bistable elsewhere. [Bug, repro and verdict](friends/victor-garcia-nk-ctl/script-line-35/).
  - **The preprint (HOLDS):** NMDS stress drops from 34.8 to 16.97 for Fig 2B and from 23.4 to 13.48 for Fig 2C, on the same data and the same objective. [Fig 2B](friends/victor-garcia-nk-ctl/nmds-fig2b/) · [Fig 2C](friends/victor-garcia-nk-ctl/nmds-fig2c/).
  - **A later-data test of the Danish forecast (HOLDS WITH CAVEATS).** [Claim and verdict](friends/victor-garcia-nk-ctl/danish-forecast/).
- **Sent:** November 2, 5 and 6.

### Not in this hub

- Aires Ferreira (KITE) is condensed-matter physics and sits in the [physics hub](https://github.com/rpinho/ai-physics); Hugo's optimization work, José Bento's optimization results, Oliveira e Silva's analysis and Marco Sampaio's benchmark are in the [math hub](https://github.com/rpinho/math-certificates).
- Results that were never sent to the person they concern are not here, in any field.

## Contributions to AI-bio companies and open-source tools

Pull requests to AI-for-biology companies' public code: bug fixes, plus speedups with identical outputs, tests/CI and small tools as they land. Each bug was found by one model and confirmed by a referee from a different model family, with a failing test before the fix. The table is rendered from the GitHub API by `tools/render_bio_prs.py` and refreshed daily; "replies" counts maintainers' comments and reviews, not bots.

<!-- auto:bio-prs -->
144 PRs: 8 merged, 130 open, 6 closed.

| Repo | PR | Type | What it does | Status |
| --- | --- | --- | --- | --- |
| [synthesizebio/pysynthbio](https://github.com/synthesizebio/pysynthbio) | [#77](https://github.com/synthesizebio/pysynthbio/pull/77) | bug fix | `predict_query` no longer writes its options into the caller's query dict | open |
| [EdisonScientific/labbench2](https://github.com/EdisonScientific/labbench2) | [#45](https://github.com/EdisonScientific/labbench2/pull/45) | bug fix | Leading-decimal answers like `.701` keep their value when graded | merged 2026-11-16 |
| [EdisonScientific/labbench2](https://github.com/EdisonScientific/labbench2) | [#46](https://github.com/EdisonScientific/labbench2/pull/46) | bug fix | Report summaries keep metrics whose scores are all 0 | merged 2026-11-16 |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | [#372](https://github.com/snap-stanford/Biomni/pull/372) | bug fix | FDA adverse-event summaries count deaths and hospitalizations from the report-level flags | merged 2026-11-16 |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | [#373](https://github.com/snap-stanford/Biomni/pull/373) | bug fix | `query_openfda` sends its search, sort, count and skip parameters | merged 2026-11-16 |
| [latchbio/latch](https://github.com/latchbio/latch) | [#624](https://github.com/latchbio/latch/pull/624) | bug fix | Glob patterns match the whole file name (`*.fq` no longer matches `a.fq.gz`) | open |
| [latchbio/latch](https://github.com/latchbio/latch) | [#625](https://github.com/latchbio/latch/pull/625) | bug fix | `generate-metadata` handles nf-core schema patterns that crashed it (55 to 124 of 146 pipelines) | open |
| [robocurve/inspect-robots](https://github.com/robocurve/inspect-robots) | [#617](https://github.com/robocurve/inspect-robots/pull/617) | bug fix | Rollouts record a copy of each executed action, so a reused policy buffer can't change scores | open |
| [robocurve/inspect-robots](https://github.com/robocurve/inspect-robots) | [#618](https://github.com/robocurve/inspect-robots/pull/618) | bug fix | Trial artifacts stay separate for scene IDs that differ only in case | open |
| [rowansci/rowan-python](https://github.com/rowansci/rowan-python) | [#19](https://github.com/rowansci/rowan-python/pull/19) | bug fix | Scan energy positions, explicit empty pKa element lists, and folder lookup past the first page | closed |
| [seqeralabs/nf-metro](https://github.com/seqeralabs/nf-metro) | [#2172](https://github.com/seqeralabs/nf-metro/pull/2172) | bug fix | Converted metro maps keep edges into dead-end processes in other sections | open |
| [seqeralabs/nf-metro](https://github.com/seqeralabs/nf-metro) | [#2173](https://github.com/seqeralabs/nf-metro/pull/2173) | bug fix | Subworkflows with the same short name get separate sections instead of overwriting each other | open |
| [Arcadia-Science/agentic-pymol](https://github.com/Arcadia-Science/agentic-pymol) | [#18](https://github.com/Arcadia-Science/agentic-pymol/pull/18) | bug fix | get_model works against real PyMOL (Indexed was imported from the wrong module) | merged 2026-11-16 |
| [Arcadia-Science/agentic-pymol](https://github.com/Arcadia-Science/agentic-pymol) | [#19](https://github.com/Arcadia-Science/agentic-pymol/pull/19) | bug fix | Relative file paths are resolved by PyMOL, as documented, not by the MCP server | open |
| [chaidiscovery/chai-lab](https://github.com/chaidiscovery/chai-lab) | [#437](https://github.com/chaidiscovery/chai-lab/pull/437) | bug fix | Merging A3M files from the same database keeps every file's hits | open |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | [#10](https://github.com/adaptyvbio/protein-design-skills/pull/10) | bug fix | The UniProt skill's PDB helper puts the chains, not the resolution, in its chains field | open |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | [#11](https://github.com/adaptyvbio/protein-design-skills/pull/11) | bug fix | The setup check uses modal token info, since modal token show does not exist | open |
| [rowansci/openconf](https://github.com/rowansci/openconf) | [#19](https://github.com/rowansci/openconf/pull/19) | bug fix | Heavy-atom RMSD searches symmetry mappings, so symmetric conformers compare as identical | open |
| [rowansci/openconf](https://github.com/rowansci/openconf) | [#20](https://github.com/rowansci/openconf/pull/20) | bug fix | random_seed=0 gives reproducible conformers instead of an unseeded run | open |
| [rowansci/steamroll](https://github.com/rowansci/steamroll) | [#8](https://github.com/rowansci/steamroll/pull/8) | bug fix | Transition-metal conversions keep input atom order and supplied coordinates | open |
| [chaidiscovery/chai-lab](https://github.com/chaidiscovery/chai-lab) | [#438](https://github.com/chaidiscovery/chai-lab/pull/438) | bug fix | Template lookup keeps chain names like 001 or NA as strings | open |
| [nf-core/tools](https://github.com/nf-core/tools) | [#4619](https://github.com/nf-core/tools/pull/4619) | bug fix | create-params-file includes parameters defined at the schema's top level | open, 6 replies |
| [nf-core/tools](https://github.com/nf-core/tools) | [#4620](https://github.com/nf-core/tools/pull/4620) | bug fix | Schema build keeps 0 and 0.0 defaults from the pipeline config | merged 2026-11-18 |
| [Future-House/aviary](https://github.com/Future-House/aviary) | [#393](https://github.com/Future-House/aviary/pull/393) | bug fix | Tool servers build for tools with list parameters (JSON Schema "array") | open |
| [Arcadia-Science/glass-box-umap](https://github.com/Arcadia-Science/glass-box-umap) | [#34](https://github.com/Arcadia-Science/glass-box-umap/pull/34) | bug fix | Float64 Tensor input works in transform and compute_contributions, like NumPy input | open |
| [MultiQC/MultiQC](https://github.com/MultiQC/MultiQC) | [#3736](https://github.com/MultiQC/MultiQC/pull/3736) | bug fix | A module set only in top_modules no longer runs a second time on all logs | open |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | [#1373](https://github.com/Future-House/paper-qa/pull/1373) | bug fix | Text parsing compares page_size_limit with each line's length, not the line count | open |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | [#1374](https://github.com/Future-House/paper-qa/pull/1374) | bug fix | Rebuilding an index with use_absolute_paper_directory keeps unchanged documents | open |
| [latchbio/scbench](https://github.com/latchbio/scbench) | [#8](https://github.com/latchbio/scbench/pull/8) | bug fix | scbench batch skips evals/manifest.json instead of counting it as a failed eval | open |
| [Arcadia-Science/glass-box-umap](https://github.com/Arcadia-Science/glass-box-umap) | [#35](https://github.com/Arcadia-Science/glass-box-umap/pull/35) | tool | py.typed marker so type checkers use the package's annotations (issue #18) | open |
| [Future-House/aviary](https://github.com/Future-House/aviary) | [#394](https://github.com/Future-House/aviary/pull/394) | bug fix | Tool servers pass a parameter's declared default when the request leaves it out | open |
| [ArcInstitute/state](https://github.com/ArcInstitute/state) | [#283](https://github.com/ArcInstitute/state/pull/283) | bug fix | Gene mapping uses the detected gene-name column, so genes named only there aren't dropped | open |
| [ArcInstitute/cell-eval](https://github.com/ArcInstitute/cell-eval) | [#248](https://github.com/ArcInstitute/cell-eval/pull/248) | bug fix | score_agg_metrics works when one normalization group is empty | open |
| [ArcInstitute/cell-eval](https://github.com/ArcInstitute/cell-eval) | [#249](https://github.com/ArcInstitute/cell-eval/pull/249) | bug fix | Pipeline metric settings no longer leak into other pipelines' defaults | open |
| [ArcInstitute/evo2](https://github.com/ArcInstitute/evo2) | [#236](https://github.com/ArcInstitute/evo2/pull/236) | bug fix | An interrupted shard merge no longer leaves a truncated checkpoint that later loads accept | open |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | [#376](https://github.com/snap-stanford/Biomni/pull/376) | bug fix | Drug recall search applies the requested classification filter | open |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | [#377](https://github.com/snap-stanford/Biomni/pull/377) | bug fix | Adverse-event search reports FDA API errors instead of 'no adverse events found' | open |
| [NVIDIA-BioNeMo/bionemo-recipes](https://github.com/NVIDIA-BioNeMo/bionemo-recipes) | [#1802](https://github.com/NVIDIA-BioNeMo/bionemo-recipes/pull/1802) | bug fix | ESM-2 PEFT validation packing uses val_micro_batch_size | open |
| [EdisonScientific/labbench2](https://github.com/EdisonScientific/labbench2) | [#48](https://github.com/EdisonScientific/labbench2/pull/48) | bug fix | custom runner outputs crash after generation (OSError) | merged 2026-11-17 |
| [EdisonScientific/labbench2](https://github.com/EdisonScientific/labbench2) | [#49](https://github.com/EdisonScientific/labbench2/pull/49) | bug fix | --retry-from ignores the original agent/mode; merges mix configurations | merged 2026-11-17 |
| [ArcInstitute/cell-eval](https://github.com/ArcInstitute/cell-eval) | [#250](https://github.com/ArcInstitute/cell-eval/pull/250) | speedup | sparse pseudobulk and centroids without densifying (3x faster, 4.8x less memory) | open |
| [robocurve/inspect-robots](https://github.com/robocurve/inspect-robots) | [#622](https://github.com/robocurve/inspect-robots/pull/622) | speedup | HTML report scans the frame directory once (16x faster, byte-identical) | open |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | [#378](https://github.com/snap-stanford/Biomni/pull/378) | bug fix | database REST helper: timeouts and bounded GET retries | open |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | [#1375](https://github.com/Future-House/paper-qa/pull/1375) | speedup | reuse NumpyVectorStore matrix and norms across retrievals (70x warm, bit-identical) | open |
| [sunpy/sunpy](https://github.com/sunpy/sunpy) | [#8919](https://github.com/sunpy/sunpy/pull/8919) | bug fix | Fixes CROTA fallback for EUI maps | closed |
| [scverse/scanpy](https://github.com/scverse/scanpy) | [#4531](https://github.com/scverse/scanpy/pull/4531) | bug fix | fix: match expression layers before reusing marker statistics | open |
| [scverse/scanpy](https://github.com/scverse/scanpy) | [#4532](https://github.com/scverse/scanpy/pull/4532) | bug fix | fix: keep legacy graph metrics usable without anndata.acc | open, 1 reply |
| [scverse/scanpy](https://github.com/scverse/scanpy) | [#4533](https://github.com/scverse/scanpy/pull/4533) | bug fix | fix: derive PCA defaults from the selected representation | open, 1 reply |
| [scverse/scanpy](https://github.com/scverse/scanpy) | [#4534](https://github.com/scverse/scanpy/pull/4534) | bug fix | fix: preserve gene pool alignment in score_genes | open |
| [latchbio/latch](https://github.com/latchbio/latch) | [#626](https://github.com/latchbio/latch/pull/626) | bug fix | launch: send false Nextflow flags and pick the File/Dir union variant by type | open |
| [latchbio/latch](https://github.com/latchbio/latch) | [#627](https://github.com/latchbio/latch/pull/627) | bug fix | file_glob: put a slash between remote_directory and the file name | open |
| [rowansci/openconf](https://github.com/rowansci/openconf) | [#21](https://github.com/rowansci/openconf/pull/21) | bug fix | hybrid: pick low-mode source seeds from the pool after seed insertion | open |
| [rowansci/openconf](https://github.com/rowansci/openconf) | [#22](https://github.com/rowansci/openconf/pull/22) | bug fix | pool: apply energy_window_kcal to the final selection | open |
| [rowansci/steamroll](https://github.com/rowansci/steamroll) | [#9](https://github.com/rowansci/steamroll/pull/9) | bug fix | to_rdkit: check transition-metal results against the supplied SMILES | open |
| [Arcadia-Science/agentic-pymol](https://github.com/Arcadia-Science/agentic-pymol) | [#21](https://github.com/Arcadia-Science/agentic-pymol/pull/21) | bug fix | types: drop slots from tool result dataclasses so FastMCP publishes output schemas | open |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4787](https://github.com/materialsproject/pymatgen/pull/4787) | speedup | ZSLGenerator: cache super-lattice reductions, vectorize match check (3.3-4.8x, byte-identical) | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4788](https://github.com/materialsproject/pymatgen/pull/4788) | bug fix | Fix GibbsComputedStructureEntry.from_dict for entries with a correction | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4789](https://github.com/materialsproject/pymatgen/pull/4789) | bug fix | Fix QuasiRRHO free-rotor interpolation using vibrational temperatures instead of wavenumbers | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4790](https://github.com/materialsproject/pymatgen/pull/4790) | bug fix | Fix MagneticStructureEnumerator crash when the ferromagnetic strategy is not used | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4791](https://github.com/materialsproject/pymatgen/pull/4791) | bug fix | Fix get_plot and plot_structures with two_theta_range=None | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4792](https://github.com/materialsproject/pymatgen/pull/4792) | bug fix | Fix XAS.stitch in XAFS mode when called on the EXAFS spectrum | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4793](https://github.com/materialsproject/pymatgen/pull/4793) | bug fix | Normalize data["volume"] per formula unit in InsertionVoltagePair | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4794](https://github.com/materialsproject/pymatgen/pull/4794) | bug fix | Fix get_dimensionality_cheon modifying the input structure when standardize=False | open, 1 reply |
| [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | [#4795](https://github.com/materialsproject/pymatgen/pull/4795) | bug fix | Return "intercalated ion" from get_dimensionality_cheon with larger_cell=True | open, 1 reply |
| [astropy/astropy](https://github.com/astropy/astropy) | [#20894](https://github.com/astropy/astropy/pull/20894) | bug fix | Fix sigma_clip rejection masks for Quantity input | closed |
| [astropy/astropy](https://github.com/astropy/astropy) | [#20895](https://github.com/astropy/astropy/pull/20895) | bug fix | Honor zero sigma bounds in SigmaClip | closed |
| [astropy/astropy](https://github.com/astropy/astropy) | [#20896](https://github.com/astropy/astropy/pull/20896) | bug fix | Fix array indexing of scalar Distribution | closed |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#802](https://github.com/Quandela/Perceval/pull/802) | bug fix | Make BSDistribution(bsd) copy the source distribution | open |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#803](https://github.com/Quandela/Perceval/pull/803) | bug fix | Validate each iteration of a ComputationIterator | open, 1 reply |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#804](https://github.com/Quandela/Perceval/pull/804) | bug fix | Set ERROR status when execute_sync fails with allow_partial_results | open, 1 reply |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#805](https://github.com/Quandela/Perceval/pull/805) | bug fix | Reset the Processor source when its noise model is changed | open, 2 replies |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#806](https://github.com/Quandela/Perceval/pull/806) | bug fix | Fix result insertion for a ComputationIterator without iteration | open |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#807](https://github.com/Quandela/Perceval/pull/807) | bug fix | Fix serialization of detectors without a name | closed |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#808](https://github.com/Quandela/Perceval/pull/808) | bug fix | Keep min_detected_photons_filter(0) through experiment serialization | open, 1 reply |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#809](https://github.com/Quandela/Perceval/pull/809) | speedup | Do not copy the experiment in use_phase_noise when there is no phase noise | open, 2 replies |
| [Quandela/Perceval](https://github.com/Quandela/Perceval) | [#810](https://github.com/Quandela/Perceval/pull/810) | speedup | Compute numeric circuit unitaries by updating row blocks | open, 1 reply |
| [scikit-bio/scikit-bio](https://github.com/scikit-bio/scikit-bio) | [#2676](https://github.com/scikit-bio/scikit-bio/pull/2676) | speedup | PERF: slice positions from stacked bytes in TabularMSA.iter_positions | open |
| [lightkurve/lightkurve](https://github.com/lightkurve/lightkurve) | [#1595](https://github.com/lightkurve/lightkurve/pull/1595) | bug fix | Fixed local FITS time units for reordered columns | open |
| [biotite-dev/biotite](https://github.com/biotite-dev/biotite) | [#1037](https://github.com/biotite-dev/biotite/pull/1037) | bug fix | Fix `check_in_box()` returning atoms inside the box | open |
| [scikit-bio/scikit-bio](https://github.com/scikit-bio/scikit-bio) | [#2677](https://github.com/scikit-bio/scikit-bio/pull/2677) | bug fix | BUG: accept a sparse basis in ilr and ilr_inv | open |
| [lightkurve/lightkurve](https://github.com/lightkurve/lightkurve) | [#1596](https://github.com/lightkurve/lightkurve/pull/1596) | bug fix | Fixed stitching light curves with different time formats | open |
| [biotite-dev/biotite](https://github.com/biotite-dev/biotite) | [#1038](https://github.com/biotite-dev/biotite/pull/1038) | bug fix | Reject GRO stacks with unequal model lengths | open |
| [dfm/emcee](https://github.com/dfm/emcee) | [#588](https://github.com/dfm/emcee/pull/588) | bug fix | fix: keep autocorrelation error estimates in original steps | open |
| [healpy/healpy](https://github.com/healpy/healpy) | [#1152](https://github.com/healpy/healpy/pull/1152) | bug fix | Fix mmax handling in harmonic_ud_grade | open |
| [joshspeagle/dynesty](https://github.com/joshspeagle/dynesty) | [#529](https://github.com/joshspeagle/dynesty/pull/529) | bug fix | fix iteration count for stopped merged runs | open |
| [healpy/healpy](https://github.com/healpy/healpy) | [#1153](https://github.com/healpy/healpy/pull/1153) | bug fix | Fix string column names in write_map | open |
| [joshspeagle/dynesty](https://github.com/joshspeagle/dynesty) | [#530](https://github.com/joshspeagle/dynesty/pull/530) | bug fix | fix information for zero reweighting factors | open |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | [#8643](https://github.com/pymc-devs/pymc/pull/8643) | bug fix | Fix MultiTrace slicing counts and negative strides | open |
| [lmfit/lmfit-py](https://github.com/lmfit/lmfit-py) | [#1068](https://github.com/lmfit/lmfit-py/pull/1068) | bug fix | FIX: use component prefixes in eval_uncertainty | open |
| [pybamm-team/PyBaMM](https://github.com/pybamm-team/PyBaMM) | [#6070](https://github.com/pybamm-team/PyBaMM/pull/6070) | bug fix | fix: preserve skip_ok on repeated experiment steps | open |
| [phonopy/phonopy](https://github.com/phonopy/phonopy) | [#1118](https://github.com/phonopy/phonopy/pull/1118) | bug fix | Fix empty arguments in deprecated option name handling | open, 1 reply |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | [#8644](https://github.com/pymc-devs/pymc/pull/8644) | bug fix | Initialize variational groups in their variable order | open |
| [lmfit/lmfit-py](https://github.com/lmfit/lmfit-py) | [#1069](https://github.com/lmfit/lmfit-py/pull/1069) | bug fix | FIX: handle sequence inputs with nan_policy='omit' | open |
| [biotite-dev/biotite](https://github.com/biotite-dev/biotite) | [#1039](https://github.com/biotite-dev/biotite/pull/1039) | bug fix | Fix GFF annotation grouping for discontinuous features | open |
| [biotite-dev/biotite](https://github.com/biotite-dev/biotite) | [#1040](https://github.com/biotite-dev/biotite/pull/1040) | bug fix | Fix `to_sequence()` chain selection for atom array stacks | open |
| [scikit-bio/scikit-bio](https://github.com/scikit-bio/scikit-bio) | [#2678](https://github.com/scikit-bio/scikit-bio/pull/2678) | bug fix | BUG: drop gap columns across all sequences in AlignPath.to_indices | open |
| [scikit-bio/scikit-bio](https://github.com/scikit-bio/scikit-bio) | [#2679](https://github.com/scikit-bio/scikit-bio/pull/2679) | bug fix | BUG: update stored IDs in OrdinationResults.rename | open |
| [scikit-bio/scikit-bio](https://github.com/scikit-bio/scikit-bio) | [#2680](https://github.com/scikit-bio/scikit-bio/pull/2680) | bug fix | BUG: treat missing lengths as zero while climbing in root_at_midpoint | open |
| [healpy/healpy](https://github.com/healpy/healpy) | [#1154](https://github.com/healpy/healpy/pull/1154) | bug fix | Fix ud_grade averaging with non-finite pixels | open |
| [joshspeagle/dynesty](https://github.com/joshspeagle/dynesty) | [#531](https://github.com/joshspeagle/dynesty/pull/531) | bug fix | fix strand IDs when merging independent runs | open |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | [#8645](https://github.com/pymc-devs/pymc/pull/8645) | bug fix | Preserve dimension names in ZarrTrace without coordinate labels | open |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | [#8646](https://github.com/pymc-devs/pymc/pull/8646) | bug fix | Flatten start_sigma arrays when initializing ADVI | open |
| [lmfit/lmfit-py](https://github.com/lmfit/lmfit-py) | [#1070](https://github.com/lmfit/lmfit-py/pull/1070) | bug fix | FIX: preserve directories when loading saved models from Paths | open |
| [phonopy/phonopy](https://github.com/phonopy/phonopy) | [#1119](https://github.com/phonopy/phonopy/pull/1119) | bug fix | Fix loading YAML with a NumPy primitive matrix | open |
| [phonopy/phonopy](https://github.com/phonopy/phonopy) | [#1120](https://github.com/phonopy/phonopy/pull/1120) | bug fix | Preserve symbol distinction when replicating Phonopy | open |
| [phonopy/phonopy](https://github.com/phonopy/phonopy) | [#1121](https://github.com/phonopy/phonopy/pull/1121) | speedup | Speed up thermal displacements by batching mode populations | open |
| [pybamm-team/PyBaMM](https://github.com/pybamm-team/PyBaMM) | [#6072](https://github.com/pybamm-team/PyBaMM/pull/6072) | bug fix | fix: keep EIS input ordering stable across solves | open, 1 reply |
| [pybamm-team/PyBaMM](https://github.com/pybamm-team/PyBaMM) | [#6073](https://github.com/pybamm-team/PyBaMM/pull/6073) | bug fix | fix: search experiment tags with string steps | open |
| [exoplanet-dev/celerite2](https://github.com/exoplanet-dev/celerite2) | [#208](https://github.com/exoplanet-dev/celerite2/pull/208) | bug fix | Include GP means in PyMC and NumPyro samples | open |
| [exoplanet-dev/celerite2](https://github.com/exoplanet-dev/celerite2) | [#209](https://github.com/exoplanet-dev/celerite2/pull/209) | bug fix | Return negative infinity after quiet factorization failures | open |
| [exoplanet-dev/celerite2](https://github.com/exoplanet-dev/celerite2) | [#210](https://github.com/exoplanet-dev/celerite2/pull/210) | bug fix | Handle PyMC marginal sample sizes | open |
| [exoplanet-dev/celerite2](https://github.com/exoplanet-dev/celerite2) | [#211](https://github.com/exoplanet-dev/celerite2/pull/211) | bug fix | Reallocate non-owning workspaces after pickling | open |
| [spglib/spglib](https://github.com/spglib/spglib) | [#650](https://github.com/spglib/spglib/pull/650) | bug fix | fix: preserve legacy Python error messages | open |
| [spglib/spglib](https://github.com/spglib/spglib) | [#651](https://github.com/spglib/spglib/pull/651) | bug fix | fix: identify magnetic groups in oblique primitive bases | open |
| [spglib/spglib](https://github.com/spglib/spglib) | [#652](https://github.com/spglib/spglib/pull/652) | bug fix | fix(fortran): forward stabilized reciprocal mesh arguments | open |
| [spglib/spglib](https://github.com/spglib/spglib) | [#653](https://github.com/spglib/spglib/pull/653) | speedup | perf: prune lattice symmetry candidates by axis length | open |
| [MultiQC/MultiQC](https://github.com/MultiQC/MultiQC) | [#3738](https://github.com/MultiQC/MultiQC/pull/3738) | bug fix | Fix grouped sample values in get_general_stats_data | open |
| [MultiQC/MultiQC](https://github.com/MultiQC/MultiQC) | [#3739](https://github.com/MultiQC/MultiQC/pull/3739) | bug fix | Fix module and data-key selection in get_module_data | open |
| [MultiQC/MultiQC](https://github.com/MultiQC/MultiQC) | [#3740](https://github.com/MultiQC/MultiQC/pull/3740) | bug fix | Preserve section order when merging parquet reports | open |
| [openmc-dev/openmc](https://github.com/openmc-dev/openmc) | [#4240](https://github.com/openmc-dev/openmc/pull/4240) | bug fix | Reshape each mesh filter along its expanded axes | open |
| [openmc-dev/openmc](https://github.com/openmc-dev/openmc) | [#4241](https://github.com/openmc-dev/openmc/pull/4241) | bug fix | Read matrix rotations from mesh filters through the C API | open |
| [openmc-dev/openmc](https://github.com/openmc-dev/openmc) | [#4242](https://github.com/openmc-dev/openmc/pull/4242) | bug fix | Scale shared mesh sources once when setting total strength | open |
| [openmc-dev/openmc](https://github.com/openmc-dev/openmc) | [#4243](https://github.com/openmc-dev/openmc/pull/4243) | bug fix | Preserve mesh identity and transformations when comparing filters | open |
| [LSSTDESC/CCL](https://github.com/LSSTDESC/CCL) | [#1329](https://github.com/LSSTDESC/CCL/pull/1329) | bug fix | Reject negative neutrino masses | open |
| [LSSTDESC/CCL](https://github.com/LSSTDESC/CCL) | [#1330](https://github.com/LSSTDESC/CCL/pull/1330) | bug fix | Fix comoving volume in curved cosmologies | open |
| [LSSTDESC/CCL](https://github.com/LSSTDESC/CCL) | [#1331](https://github.com/LSSTDESC/CCL/pull/1331) | bug fix | Include fc_bar in Duffy08 equality and representation | open |
| [LSSTDESC/CCL](https://github.com/LSSTDESC/CCL) | [#1332](https://github.com/LSSTDESC/CCL/pull/1332) | bug fix | Fix fourth-profile bias in the two-halo trispectrum | open |
| [pysam-developers/pysam](https://github.com/pysam-developers/pysam) | [#1431](https://github.com/pysam-developers/pysam/pull/1431) | bug fix | Allow VariantRecord POS=0 (start=-1), as used for telomeres | open |
| [dfm/corner.py](https://github.com/dfm/corner.py) | [#355](https://github.com/dfm/corner.py/pull/355) | bug fix | Fix linestyle aliases in overplot_points | open |
| [dfm/corner.py](https://github.com/dfm/corner.py) | [#356](https://github.com/dfm/corner.py/pull/356) | bug fix | Restore variable selection with ArviZ 1.x | open |
| [dfm/corner.py](https://github.com/dfm/corner.py) | [#357](https://github.com/dfm/corner.py/pull/357) | bug fix | Align divergence markers with selected coordinates | open |
| [mdtraj/mdtraj](https://github.com/mdtraj/mdtraj) | [#2236](https://github.com/mdtraj/mdtraj/pull/2236) | bug fix | Resolve mmCIF connections using label identifiers | open |
| [mdtraj/mdtraj](https://github.com/mdtraj/mdtraj) | [#2237](https://github.com/mdtraj/mdtraj/pull/2237) | bug fix | Apply atom selection after reading ARC topology | open |
| [mdtraj/mdtraj](https://github.com/mdtraj/mdtraj) | [#2238](https://github.com/mdtraj/mdtraj/pull/2238) | bug fix | Continue default XTC and TRR frame numbers across writes | open |
| [mdtraj/mdtraj](https://github.com/mdtraj/mdtraj) | [#2239](https://github.com/mdtraj/mdtraj/pull/2239) | bug fix | Restore integral bond orders when reading HDF5 topology | open |
| [mdtraj/mdtraj](https://github.com/mdtraj/mdtraj) | [#2240](https://github.com/mdtraj/mdtraj/pull/2240) | bug fix | Use written atom serials in PDB CONECT records | open |
| [adrn/gala](https://github.com/adrn/gala) | [#680](https://github.com/adrn/gala/pull/680) | bug fix | Preserve mock stream metadata through HDF5 | open |
| [adrn/gala](https://github.com/adrn/gala) | [#681](https://github.com/adrn/gala/pull/681) | bug fix | Honor the median option for Staeckel focal lengths | open |
| [adrn/gala](https://github.com/adrn/gala) | [#682](https://github.com/adrn/gala/pull/682) | bug fix | Use elapsed time in fast Lyapunov estimates | open |
| [adrn/gala](https://github.com/adrn/gala) | [#683](https://github.com/adrn/gala/pull/683) | bug fix | Use the toy potential time unit when fitting O2GF frequencies | open |
| [tenpy/tenpy](https://github.com/tenpy/tenpy) | [#779](https://github.com/tenpy/tenpy/pull/779) | bug fix | Fix MPO expectation values with supplied environments | open |
| [tenpy/tenpy](https://github.com/tenpy/tenpy) | [#780](https://github.com/tenpy/tenpy/pull/780) | bug fix | Fix joint probabilities in MPS.sample_measurements | open |
| [tenpy/tenpy](https://github.com/tenpy/tenpy) | [#781](https://github.com/tenpy/tenpy/pull/781) | bug fix | Fix dropping charges on grouped sites of different dimensions | open |
| [tenpy/tenpy](https://github.com/tenpy/tenpy) | [#782](https://github.com/tenpy/tenpy/pull/782) | bug fix | Fix MPO construction for empty Hamiltonians | open |
<!-- /auto -->

## How this was run

All of it with AI agents under a bounded harness, [rstack](https://github.com/rpinho/rstack): frozen tests before the first result, the scoring kept away from the agent doing the searching, and prior art reproduced with a command rather than quoted. The biology-specific lesson is in the [retro](RETRO.md): the agents were not the constraint; the data was.

## References

Nothing here is from scratch. Each repository carries its own references; this list covers the hub.

- Brian Armstrong, [publicly funded science as open source](https://x.com/brian_armstrong/status/2119150702446420027), November 7, 2026.
- Arc Institute, [Virtual Cell Challenge](https://virtualcellchallenge.org/).
- Anthropic and Adaptyv Bio, [the protein design competition](https://proteinbase.com/competitions/anthropic-adaptyv-2026).
- [Virtual Embryo Challenge](https://virtualembryo.ai/challenge).
- Márquez et al., ExOrthist, *Genome Biology* 2021, [doi:10.1186/s13059-021-02441-9](https://doi.org/10.1186/s13059-021-02441-9).
- Tapial et al., vast-tools / VastDB, *Genome Research* 2017, [doi:10.1101/gr.220962.117](https://doi.org/10.1101/gr.220962.117).
- Boyle et al., GO::TermFinder, *Bioinformatics* 2004, [doi:10.1093/bioinformatics/bth456](https://doi.org/10.1093/bioinformatics/bth456).
- Müller, Salathé and Kummervold, COVID-Twitter-BERT, [arXiv:2005.07503](https://arxiv.org/abs/2005.07503).
- Garcia, Bonhoeffer and Fu, *J. Theor. Biol.* 2020, [doi:10.1016/j.jtbi.2020.110185](https://doi.org/10.1016/j.jtbi.2020.110185).
- pyglmnet, [glm-tools/pyglmnet](https://github.com/glm-tools/pyglmnet); multimedia, structSSI and miniLNM on CRAN.
- Anthropic Economics, [AI for scientific discovery: how researchers use Claude](https://www.anthropic.com/research/how-researchers-use-claude), November 5, 2026 — the per-field numbers the retro uses.
- Pinho, Garcia and Feldman, *PLOS ONE* 2015, [doi:10.1371/journal.pone.0119972](https://doi.org/10.1371/journal.pone.0119972); Pinho, Garcia, Irimia and Feldman, *PLoS Comput Biol* 2014, [doi:10.1371/journal.pcbi.1003916](https://doi.org/10.1371/journal.pcbi.1003916).

Thanks to Arc Institute, to Adaptyv Bio and Anthropic for funding experimental validation, and to the scientists above for letting an outsider's agents read their code.
