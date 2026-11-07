<!-- 2026-11-07 draft, not published; friends' views are paraphrased, never quoted from private email. -->
# Math is easy, physics is harder, biology is hardest

Biology has been much harder than math for me. I was explaining to my wife why math went faster. This year I ran AI agents on open problems across three fields. Math moved fastest, then astronomy, with biology far behind. I'm a data engineer with a computational biology PhD.

## Math: exact certificates

The math results were the easiest to settle. Each bound has a number and a checking program. We used interval arithmetic, exact rationals, and two independent checkers. Six bounds were merged into [Terence Tao's public table][tao]. The [certificates are public too][certificates].

The agent can be wrong a thousand times. For these problems, checking another attempt costs almost nothing. The check is exact and cheap. That's why this work moved fastest. Finding a bound was hard, but recognizing success wasn't.

## Physics: is there new physics inside?

A physicist I studied with pushed back on this. This is my paraphrase of his private reply. A result alone isn't worth much without new physics or intuition. People won't necessarily enjoy watching agents solve problems just because they can.

I think he's right. My [planet work][planets] produced four candidate reports from public NASA TESS data. A re-audit corrected all four reports. They aren't four confirmed planets. Confirmation needs telescope time nobody has given me.

The data was public. Checking the analysis wasn't the final bar. Had we learned anything about the physical system? I don't think a clean computation answers that by itself.

## Biology: hardest

I came back to biology expecting more progress. My PhD studied Boolean gene regulatory networks in Marcus Feldman's Stanford lab. I knew some of these problems already.

There are several camps on AI and biology. Some expect rapid progress toward curing most diseases. [Demis Hassabis][hassabis] puts a full virtual cell further out, with measurement still missing. Others think the cure claims outrun the evidence.

My challenges don't settle that argument. On the bottleneck, I land closer to Mile Šikić and Jason Kelly. We need more experimental data. I think there are five reasons biology is harder.

### 1. Missing data

My [cell-challenge predictions][cell-retro] distinguished perturbations well: discrimination was 0.86. Alignment with their actual effects was only 0.084 mean cosine. Two halves of the same real cells agreed at 0.65. So the predictions missed much of the measurable response.

In-context data from the same cell type changed things. It lifted alignment from 0.115 to 0.42. The final phase withholds exactly that information.

We need many more experiments in new conditions. New cell types, new organisms, and better instrumentation too. That argues for automating experiments.

[Mile Šikić][sikic] describes observing only a few dimensions of biology. We see a slice, leaving discovery dependent on luck. His phrase is blunt: "luck is not something LLMs with better reasoning can fix." [CHECK: the `sikic` link points at his 2026-07-29 post about DeepMind's direction, which is a different post from the slice-and-luck quote. The quote is transcribed in the KB page `wiki/ai/Data is the Bottleneck - Robotics and Biology Converge (July 2026).md`. Find the original post's URL before publishing, or attribute it as "writing in July 2026" without a link.]

[Jason Kelly of Ginkgo][kelly-video], at 53:13, calls new experimental data biotechnology's ultimate constraint. [Eli Lilly's Dave Ricks][ricks] makes a similar argument. AI needs data that doesn't exist yet. Robotic labs could make collecting it tractable.

Ginkgo reports [160 devices running around the clock][ginkgo]. Nature's AutoDNA write-up describes [human effort limited to hardware maintenance][autodna]. [Purpose-built instruments][instruments] look like another useful niche here.

### 2. Siloed data and unpublished negative results

Think of decades of students, interns, PhDs and postdocs pipetting. In every country, much stayed in paper notebooks. Experiments that failed often never became papers. All of that could help a model. Even all of it wouldn't be enough. We'd still need new experiments.

[Liam Fedus's Periodic Labs announcement][periodic] explicitly mentions unpublished negative results. [Will DePue][depue] describes knowledge trapped inside organizations and people's heads. Outside biology, [a published failure log][negative-log] helped a community move faster.

[The protein design competition I entered][adaptyv-repo] publishes every measurement, including failures. That's rare and good. The [competition][competition] also supplies the experimental validation.

But models can mishandle the evidence we already have. A [November 5 benchmark finding][kenbwork] reports familiar mistakes. Agents treated missing observations as negatives and mismatched records. They also mistook measurement artifacts for real signal.

### 3. No general theory, so more dependence on data

Biology doesn't have a predictive theory with physics' reach. It's much more empirical, so it runs on data. AI can work without an explicit theory. But it needs lots of examples. The two dependencies multiply.

The central dogma is the closest shorthand people reach for. Its simplified version was already being criticized during my PhD. DNA, RNA and proteins regulate one another. A protein isn't a function, phenotype or disease.

But that feedback doesn't refute [Crick's actual statement][crick]. His dogma concerned the transfer of sequence information. It wasn't a claim that regulation only runs one way. [Shapiro's 2009 revisit][shapiro] discusses the broader picture. Neither gives us equations that predict a whole cell.

### 4. Stochasticity

Two friends, both scientists, have pushed this at me for years. This is a paraphrase of their private comments. One stresses noise, chaos and molecular-scale quantum effects. The other has long argued that gene expression is stochastic. He thought my gene-network models were too deterministic.

I agree with both about the noise. My [last paper][pinho2015] added random error. That isn't the same as building genuinely stochastic equations. I should have done more of that. We cited [Elowitz and colleagues][elowitz] and [Raj and van Oudenaarden][raj] in that paper.

The molecules are drunks. At that scale everything is liquid and shaking. Nothing travels in a straight line. Motors walk cargo along cytoskeleton highways, and timing and location are hit and miss.

Drug discovery is a key and a lock, except the drunk coming home late cannot get the key in, and the lock is shaking too. Often it is the wrong key, the wrong lock, or the wrong house.

### 5. Observability

We know one street and one drunk. We are blind to the city, the country, the world, the galaxy.

In my math problems, the checked object is fully specified. In physics, we can often observe the relevant system. Biology gives us a sliver, usually through an indirect measurement. That's why I put it far behind the other two.

## The usage statistics

The ranking matches what I just lived through. I don't think it means models are inherently worse at biology. The physical steps remain.

[Anthropic's Economics team][anthropic] studied scientific Claude use on November 5. [Ethan Mollick's November 7 post][mollick] circulated the headline. With current capabilities and wide adoption, AI could take on 27–52% of researcher time per study. The median across 34 fields is 38%.

Figure 13 puts biology at 32%, biomedical sciences at 30–31%, and chemistry at 29%. Mathematics is 43%, physics and astronomy 40%. Life sciences rank 23rd to 27th of 34. These chart readings carry about one percentage point of error.

Automating all non-physical steps gives formal sciences 15–16x output. Biology and chemistry reach roughly 3–4x. The authors write: “Absent automated labs, their physical steps, representing about 40% of researcher time, remain the bottleneck.” These are “illustrative scenarios, not forecasts.” They assume wide adoption, including extrapolations across fields.

[OpenAI and Ligo's BioBasicsBench][biobasics] measures something different. Its 100 tasks test reading actual lab evidence. That includes gels, plates, microscopy and plate-reader exports. The best score is about two thirds of rubric credit. Higher scores don't yet establish reliable judgment in a lab. Anthropic measured researchers' use. OpenAI tested interpretation of experimental evidence.

## Videos: see it for yourself

Animations are illustrations, not data. These three examples help explain what I mean.

1. XVIVO's [Protein Packing][packing] shows molecular crowding and jitter. The [original Inner Life of the Cell][inner-life] gives the wider view.
2. Drew Berry and Etsuko Uno's [DNA animation][dna] makes molecular motion visible. Berry's [TED talk][ted] explains depicting unseeable biology. More is in [WEHI's educational library][wehi].
3. [Lattice light-sheet microscopy with adaptive optics][microscopy] shows real cells inside living organisms. These Janelia and Harvard movies are actual measurements. Even this view captures only a thin slice of events.

## What is easy and what is hard

For these math bounds, exact checking made rejection easy. Finding something better still took search. In astronomy, producing candidates was easier than establishing their meaning. Confirmation needs observations I don't have.

In biology, generation was easier than ranking and validation. The models' confidence scores varied more across repeated runs of one design than across different designs. Ranking by those scores was close to random. Hardest was calibration: what probability does a score actually imply?

## What data is missing

Measured failures, paired multi-condition data, matched controls and replicates. Replicates tell us the noise ceiling for each target. We need cheap assays too. Measuring many more candidates would let screening replace uncertain ranking.

## What would make it easier

Publish failures alongside successes, with their experimental context. Measure responses across more cell types and conditions. Report repeatability before treating confidence scores as ranking rules. Automate experiments and improve the instruments that observe them.

## What is still open

I don't know how much better models alone can do. Two results would change my mind.

If my submitted ranking agrees with experimental measurements, selection is more tractable than I think. The lab-results status needs updating before publication. [CHECK: confirm Adaptyv results and evaluate that comparison.]

If a top cell-challenge entry used no same-cell-type data and still beat 0.3, I'd rethink the data bottleneck. That would point toward a modelling limitation in my approach.

## How hard open science with AI is here

Weights are open, targets are public, and compute is rentable. One person with agents reached the top third of 1,580 entries. My cell validation score was 0.164, around 463rd. That isn't a final challenge score. [CHECK: verify the final score and distinguish its metric.]

Open tools didn't tell me which answer was right. They didn't supply data from cell types nobody measured. The cell challenge scored me in minutes. A wet lab answers in weeks, once. I couldn't iterate against that answer.

## Credits and thanks

Thanks to [Mile Šikić][sikic], [Jason Kelly][kelly-video] and [Ethan Mollick][mollick]. And to Anthropic Economics authors Johannes Hermle, Ben Jones and Lukas Althoff. Thanks to [Arc Institute for the cell challenge][cell-challenge], and Adaptyv Bio and Anthropic for funding experimental validation. Also to the two scientist friends whose comments I paraphrased.

## References

### Reports and papers

- [Anthropic Economics, AI for scientific discovery: How researchers use Claude][anthropic]. November 5, 2026.
- [OpenAI and Ligo, Measuring how AI agents handle everyday wet-lab science][biobasics]. November 6, 2026.
- [Crick, Central Dogma of Molecular Biology][crick]. Nature, 1970. DOI: 10.1038/227561a0.
- [Shapiro, Revisiting the Central Dogma in the 21st Century][shapiro]. Annals of the New York Academy of Sciences, 2009. DOI: 10.1111/j.1749-6632.2009.04990.x.
- [Elowitz et al., Stochastic Gene Expression in a Single Cell][elowitz]. Science, 2002. DOI: 10.1126/science.1070919.
- [Raj and van Oudenaarden, Nature, Nurture, or Chance][raj]. Cell, 2008. DOI: 10.1016/j.cell.2008.09.050.
- [Virtual Cell Challenge][cell-challenge], Arc Institute.
- [Anthropic x Adaptyv competition][competition], including experimental measurement release.

### X posts

- [Mile Šikić, data limitations and his interpretation of DeepMind's direction][sikic].
- [Dave Ricks, AI, missing data and robotic labs][ricks].
- [Jason Kelly, Ginkgo's 160-device laboratory][ginkgo].
- [Eric Topol, Nature's AutoDNA write-up][autodna].
- [Omics! Omics!, purpose-built instrumentation][instruments].
- [Liam Fedus, Periodic Labs and unpublished negative results][periodic].
- [Will DePue, tacit knowledge and the dark matter of the internet][depue].
- [Rohan Arun, a community's published negative-result log][negative-log].
- [Ken Workman, biological-evidence benchmark failures][kenbwork].
- [Ethan Mollick, the Anthropic report headline][mollick].

### Videos and microscopy

- [Jason Kelly interview][kelly-video], experimental-data argument at 53:13.
- [Demis Hassabis interview][hassabis], virtual cells and measurement.
- [XVIVO for Harvard BioVisions, Protein Packing][packing], 2013–2014; [The Inner Life of the Cell][inner-life].
- [Drew Berry and Etsuko Uno, WEHI DNA animation][dna]; [Berry's TED talk][ted]; [WEHI library][wehi].
- [Janelia, new microscope captures detailed 3-D movies inside living systems][microscopy], April 2018. Betzig and collaborators, including Kirchhausen's Harvard laboratory; Science work described in the release.

### My repos and papers

- [Terence Tao's optimization problems and public constants table][tao].
- [Math certificates][certificates].
- [Planet hunt][planets].
- [Virtual Cell Challenge retrospective][cell-retro].
- [Protein design competition repository][adaptyv-repo].
- [Pinho, Garcia and Feldman, 2015 paper][pinho2015]. PLOS ONE. DOI: 10.1371/journal.pone.0119972.

[anthropic]: https://www.anthropic.com/research/how-researchers-use-claude
[biobasics]: https://openai.com/index/measuring-how-ai-agents-handle-wet-lab-science/
[crick]: https://doi.org/10.1038/227561a0
[shapiro]: https://doi.org/10.1111/j.1749-6632.2009.04990.x
[elowitz]: https://doi.org/10.1126/science.1070919
[raj]: https://doi.org/10.1016/j.cell.2008.09.050
[cell-challenge]: https://virtualcellchallenge.org/
[competition]: https://proteinbase.com/competitions/anthropic-adaptyv-2026
[sikic]: https://x.com/msikic/status/2082404380578296045
[ricks]: https://x.com/DaveARicks/status/2112516340833751349
[ginkgo]: https://x.com/jrkelly/status/2112537118811574459
[autodna]: https://x.com/EricTopol/status/2118015564933407206
[instruments]: https://x.com/OmicsOmicsBlog/status/2118194341625934014
[periodic]: https://x.com/LiamFedus/status/1973055380193431965
[depue]: https://x.com/willdepue/status/2074178395462848800
[negative-log]: https://x.com/RohanArun/status/2109921746694385777
[kenbwork]: https://x.com/kenbwork/status/2118416895795707946
[mollick]: https://x.com/emollick/status/2118859591798980657
[kelly-video]: https://youtu.be/vvsdHs_3lRU
[hassabis]: https://www.youtube.com/watch?v=JNyuX1zoOgU
[packing]: https://www.youtube.com/watch?v=uHeTQLNFTgU
[inner-life]: https://www.youtube.com/watch?v=wJyUtbn0O5Y
[dna]: https://www.youtube.com/watch?v=7Hk9jct2ozY
[ted]: https://www.youtube.com/watch?v=WFCvkkDSfIU
[wehi]: https://www.wehi.edu.au/wehi-tv/
[microscopy]: https://www.janelia.org/news/new-microscope-captures-detailed-3-d-movies-of-cells-deep-within-living-systems
[tao]: https://github.com/teorth/optimizationproblems
[certificates]: https://github.com/rpinho/math-certificates
[planets]: https://github.com/rpinho/planet-hunt
[cell-retro]: https://github.com/rpinho/virtual-cell-challenge/blob/main/RETRO.md
[adaptyv-repo]: https://github.com/rpinho/adaptyv-challenges
[pinho2015]: https://doi.org/10.1371/journal.pone.0119972

## Names to approve

[Ricardo to approve: the two scientist friends are Manuel Irimia and Hugo Fernandes. Keep their names out of the body unless they approve attribution. The physicist remains unnamed.]

## [CHECK] items

- Approve the anonymous physicist paraphrase, including his objection to agent demonstrations without new physical insight. No private wording is quoted.
- Approve both scientist-friend paraphrases and the bracketed names above. Confirm whether the molecular quantum-effects point should remain. The body doesn't assert that quantum effects alone explain gene-expression noise.
- Confirm Adaptyv's lab-results status as of publication. Replace the inline marker with the dated outcome or an explicit pending status. Check that the general ranking falsifier preserves the intended experimental comparison.
- Verify the final cell-challenge score and metric. The 0.164 and approximately 463rd/1,580 figures above are validation results. Check whether any entry above 0.3 meets the stated no-same-cell-type-data condition.
- Approve the distinction between regulatory feedback and Crick's sequence-information claim. The brief's broader criticism is retained without presenting feedback as a refutation of that dogma.
- Treat the two drunk analogies as illustrations. The absolute wording about liquid and straight-line motion is deliberately retained from the dictation and needs Ricardo's approval.
- The full Šikić slice/distribution passage was read in the local bottleneck page. His linked DeepMind-direction post is the supplied contextual pointer. Verify the exact public location of the quoted sentence before publication; don't present the private KB as its public source.
- Recheck the dated external claims before release: six merged bounds, all four corrected candidate reports, telescope access, competition measurement-release policy, Ginkgo's reported device count and AutoDNA's maintenance-only human role.
- Verify the precise Figure 13 readings against the report if quoting greater precision. Keep the wide-adoption assumptions, roughly one-point chart uncertainty and scenario caveat.
