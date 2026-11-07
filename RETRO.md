# Math is easy, physics is harder, biology is hardest

I was explaining to someone what I'm doing this year. Math, physics and biology. And why math is easier, physics is harder and biology is the hardest. This is that explanation, written down.

I ran AI agents on open problems in all three. I'm a data engineer. My PhD was on the evolution of gene regulatory networks, in Marcus Feldman's lab at Stanford. So evolutionary biology and population genetics. It was very theoretical. I was dealing with matrices, not real gene expression.

The usage numbers Anthropic published by field show the same order. More on that below.

## Math is the easiest

Each bound has a number and a program that checks it. Interval arithmetic, exact rationals and two independent checkers. Six bounds were merged into [Terence Tao's public table][tao]. The [certificates are public][certificates].

The agent can be wrong a thousand times. Checking one more attempt costs almost nothing. Finding a better bound was hard. Knowing when we had one wasn't.

## Physics: is there new physics inside?

A physicist I studied with replied to the math results. This is my paraphrase of his reply: math, cool, but is there new physics inside? If not, who cares?

I think he's right. My [planet work][planets] produced four candidate reports from public NASA TESS data. A later audit found errors in them, including credit we had missed, and they are being corrected. They aren't four confirmed planets. That needs follow-up observations that haven't happened yet.

Even a perfect analysis is not the bar. The question is whether we learned anything about the physical system. I don't think a clean computation answers that by itself.

## Biology is the hardest

I came back to biology expecting more progress. I knew some of these problems from my PhD. It was still much harder than I thought.

People disagree a lot here. Some expect AI to cure most diseases soon. [Demis Hassabis][hassabis] puts a full virtual cell further out, with measurement still missing. Others think the cure claims outrun the evidence. My challenges don't settle that. On the bottleneck I'm closer to [Mile Šikić][sikic] and Jason Kelly. We need more experimental data.

I think there are five reasons biology is harder.

### 1. We're missing data

We need many more experiments. Many, many more. New conditions, new cell types, new organisms. Better instruments and better measurements too. That's why we need to automate experiments.

My own numbers show it. In the [cell challenge][cell-retro] my predictions could tell perturbations apart: discrimination was 0.86. But alignment with their real effects was only 0.084 mean cosine. Two halves of the same real cells agree at 0.65. So we missed most of the measurable response.

Data from the same cell type changed that. It lifted alignment from 0.115 to 0.42. The final phase withholds exactly that data.

[Jason Kelly of Ginkgo][kelly-video] calls new experimental data biotech's ultimate constraint, at 53:13. [Dave Ricks of Eli Lilly][ricks] makes a similar argument. AI needs data that doesn't exist yet, and robotic labs could make collecting it tractable. Ginkgo reports [160 devices running around the clock][ginkgo]. Nature's AutoDNA write-up describes [human effort limited to hardware maintenance][autodna]. [Purpose-built instruments][instruments] are another piece.

### 2. The data we have is stuck in labs

Think of every student, intern, PhD student and postdoc pipetting away for decades. Turkey, Portugal, the US, Russia, China. Most of that data isn't shared anywhere. A lot of it is in paper notebooks, not even on a computer. Negative results don't get published. All of that would be super helpful for AI.

Even that is not enough. We'd still need new data.

Others are saying the same. [Liam Fedus's Periodic Labs announcement][periodic] mentions unpublished negative results. [Will DePue][depue] writes about knowledge stuck inside organizations and people's heads. Outside biology, [a published failure log][negative-log] helped a community move faster.

[The protein design competition I entered][adaptyv-repo] publishes every measurement, failures included. That's rare and good. The [competition][competition] also supplies the lab validation.

Models can also mishandle the data we already have. A [November 5 benchmark write-up][kenbwork] found agents treating missing observations as negatives and mismatching records. They also mistook measurement artifacts for real signal.

### 3. There's no theory

If you don't have a theory, your science is empirical. If it's empirical, you need data. AI is fine without a theory. But then it needs a lot of data.

The closest thing to a theory is the central dogma. DNA makes RNA makes protein. It was criticized during my PhD, and the criticism is decades old. It's not one way. The three layers influence each other. And the protein is not the end. Having a protein doesn't mean you have a function, a phenotype or a disease.

To be fair to [Crick][crick], his actual statement was narrower. It was about where sequence information can flow. It wasn't a claim that regulation only goes one way. [Shapiro's 2009 revisit][shapiro] covers the bigger picture. Neither gives us equations that predict a cell.

### 4. Everything is stochastic

Two scientist friends have pushed this on me for years. This is my paraphrase of their comments. One stresses noise, chaos and quantum effects at the molecular scale. The other has long argued that gene expression is stochastic. He thought my gene network models were too deterministic.

I agree with both. My [last paper][pinho2015] added random error. That's not the same as building truly stochastic equations. I should have done more of that. We cited [Elowitz and colleagues][elowitz] and [Raj and van Oudenaarden][raj] in that paper.

Watch the videos below. Everything is shaking. Everything is very tiny and inside a liquid. So nothing moves in a straight line. Even if the protein is right and it has to go somewhere, it won't go there in a straight line. Things hit and things miss, in timing and in location.

The molecules look drunk. They also have to travel. They walk on the cell's highways, the microtubules and actin filaments. I'm not the first to see it. Harvard Medical School [described dynein][hms-dynein], one of these motors, as one that "staggers like a drunken sailor".

Drug discovery is building keys. The right key for the right lock. Now picture a drunk guy coming home late from drinking with his buddies. He's trying to open the door. He's shaking. Even if the key is right, he might not get it in. Many times the key is wrong. And it's not just the key. The lock is shaking too, because the lock is also stochastic. Sometimes it's the wrong lock. Sometimes he's so drunk he went to the wrong house.

I think these analogies help. People may not realize how stochastic everything is.

### 5. We can't see much

We know one street and one drunk guy. We're blind to thousands of other streets. Maybe we know a city, but not the world. Maybe a planet, but not the solar system or the galaxy.

In math the object we check is fully specified. In physics we can often observe the system. In biology we get a sliver, usually through an indirect measurement. That's why I put biology so far behind math and physics.

## The usage numbers

[Anthropic's Economics team][anthropic] published how researchers use Claude on November 5. [Ethan Mollick][mollick] circulated the headline on November 7. With current models and wide adoption, AI could take on 27 to 52% of researcher time per study. The median across 34 fields is 38%.

Mathematics is at 43%. Physics and astronomy, 40%. Biology is 32%, biomedical sciences 30 to 31%, chemistry 29%. Life sciences rank 23rd to 27th of 34. Those come from Figure 13. I read them off the chart, so they're within about one point.

If all non-lab steps were automated, formal sciences would get 15 to 16x output. Biology and chemistry get roughly 3 to 4x. In their words: “Absent automated labs, their physical steps, representing about 40% of researcher time, remain the bottleneck.” They call these “illustrative scenarios, not forecasts.” They assume wide adoption, including extrapolations across fields.

The order matches what I just lived through. I don't think it means models are worse at biology. The physical steps are still there.

[OpenAI and Ligo's BioBasicsBench][biobasics] tests something else. Its 100 tasks are about reading real lab evidence: gels, plates, microscopy, plate-reader exports. The best score is about two thirds of the rubric credit. I don't think that means reliable judgment in a lab yet.

## Videos

Animations are illustrations, not data. The microscopy is real, but it only shows a thin slice. Both helped me explain the shaking.

The highways are microtubules and actin filaments. Kinesin and dynein walk on microtubules. Myosin walks on actin.

- Real cargo on the highways. Saikat Ghosh at NIH filmed [mitochondria and lysosomes moving along microtubule tracks in neurons][nikon]. Confocal microscopy, an honorable mention in Nikon's 2024 Small World in Motion.
- A real motor walking. Toshio Ando's lab filmed [myosin V walking on actin][hsafm] with high-speed atomic force microscopy ([Kodera et al., Nature 2010][kodera]). It's the [molecule itself][kanazawa], not a fluorescent dot attached to it.
- Kinesin, animated. Janet Iwasa's [kinesin stepping along a microtubule][iwasa-kinesin], made in 2021 for Erik Schäffer's lab. It's based on their [2021 Science measurements][sudhakar].
- Dynein, the drunken sailor. Iwasa's [dynein animation for Harvard Medical School][dynein-video], from 2012.
- DNA. Drew Berry and Etsuko Uno's [DNA animation][dna]. Berry's [TED talk][ted] is about showing biology nobody can see. More in [WEHI's library][wehi].
- Inside living animals. [Lattice light-sheet microscopy with adaptive optics][microscopy], Janelia and Harvard, 2018. Real cells inside living organisms.

In 2023 two groups tracked single kinesin steps with MINFLUX, about 16 nm each. [One worked outside cells][wolff]. [The other worked inside living cells][deguchi].

## What was easy and what was hard

Math: rejecting a wrong answer was easy. Finding a better one still took search.

Astronomy: producing candidates was easy. Knowing what they mean was hard. Confirmation needs observations I don't have.

Biology: generating designs was easy. Ranking them was hard. The models' confidence scores varied more across repeated runs of one design than across different designs. So ranking by those scores was close to random. Hardest was calibration. What probability does a score actually mean?

## What data is missing

Measured failures. Paired data across many conditions. Matched controls. Replicates, because they tell you the noise ceiling for each target. And cheap assays. If we could measure many more candidates, we wouldn't need to rank so well.

## What would make it easier

- Publish failures next to successes, with the experimental context.
- Measure responses in more cell types and conditions.
- Report how repeatable a confidence score is before ranking with it.
- Automate experiments, and build better instruments to watch them.

## What is still open

I don't know how much better models alone can do. Two results would change my mind.

If my submitted protein ranking agrees with the lab measurements, selection is easier than I think. Those results weren't out when I wrote this.

If a top cell-challenge entry used no same-cell-type data and still beat 0.3, I'd rethink the data bottleneck. That would point to a modelling limit in my approach.

## Open science with AI, in biology

Weights are open, targets are public and compute is rentable. One person with agents got into the top third of 1,580 entries. My cell validation score was 0.164, around 463rd. That's a validation score, not the final one. Final scores weren't out when I wrote this.

Open tools didn't tell me which answer was right. They didn't give me data from cell types nobody has measured. The cell challenge scored me in minutes. A wet lab answers in weeks, and once. I couldn't iterate against that.

## Credits and thanks

I'm not building anything from scratch. This is inspired by the posts below, by the replies to my emails, by the challenges and by my PhD.

Thanks to Mile Šikić, Jason Kelly and Ethan Mollick. To the Anthropic Economics authors Johannes Hermle, Ben Jones and Lukas Althoff. To [Arc Institute for the cell challenge][cell-challenge], and to Adaptyv Bio and Anthropic for funding the lab validation. To Janet Iwasa, Drew Berry, Etsuko Uno, Saikat Ghosh and the Ando lab for the videos. And to the friends whose comments I paraphrased.

## References

### Reports and papers

- [Anthropic Economics, AI for scientific discovery: How researchers use Claude][anthropic]. November 5, 2026.
- [OpenAI and Ligo, Measuring how AI agents handle everyday wet-lab science][biobasics]. November 6, 2026.
- [Crick, Central Dogma of Molecular Biology][crick]. Nature, 1970. DOI: 10.1038/227561a0.
- [Shapiro, Revisiting the Central Dogma in the 21st Century][shapiro]. Annals of the New York Academy of Sciences, 2009. DOI: 10.1111/j.1749-6632.2009.04990.x.
- [Elowitz et al., Stochastic Gene Expression in a Single Cell][elowitz]. Science, 2002. DOI: 10.1126/science.1070919.
- [Raj and van Oudenaarden, Nature, Nurture, or Chance][raj]. Cell, 2008. DOI: 10.1016/j.cell.2008.09.050.
- [Kodera, Yamamoto, Ishikawa and Ando, Video imaging of walking myosin V by high-speed atomic force microscopy][kodera]. Nature, 2010. DOI: 10.1038/nature09450.
- [Sudhakar et al., Germanium nanospheres for ultraresolution picotensiometry of kinesin motors][sudhakar]. Science, 2021. DOI: 10.1126/science.abd9944.
- [Wolff et al., MINFLUX dissects the unimpeded walking of kinesin-1][wolff]. Science, 2023. DOI: 10.1126/science.ade2650.
- [Deguchi et al., Direct observation of motor protein stepping in living cells using MINFLUX][deguchi]. Science, 2023. DOI: 10.1126/science.ade2676.
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
- [Saikat Ghosh, Dynamic trafficking of mitochondria and lysosomes along microtubule tracks of neuronal highways][nikon]. Nikon Small World in Motion 2024, honorable mention.
- [Ando, Uchihashi and Kodera, high-speed AFM supplemental video 4][hsafm], myosin V on actin. Annual Reviews, 2013. [Kanazawa University summary][kanazawa].
- [Janet Iwasa for the Schäffer lab, rotational hand-over-hand kinesin stepping][iwasa-kinesin], 2021.
- [Janet Iwasa for Harvard Medical School, dynein animation][dynein-video], 2012; [the HMS story][hms-dynein].
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
[kodera]: https://doi.org/10.1038/nature09450
[sudhakar]: https://doi.org/10.1126/science.abd9944
[wolff]: https://doi.org/10.1126/science.ade2650
[deguchi]: https://doi.org/10.1126/science.ade2676
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
[nikon]: https://www.nikonsmallworld.com/galleries/2024-small-world-in-motion-competition/dynamic-trafficking-of-mitochondria-and-lysosomes
[hsafm]: https://www.youtube.com/watch?v=0B-NYEJtdkw
[kanazawa]: https://www.kanazawa-u.ac.jp/research_bulletin/highlights_010.html
[iwasa-kinesin]: https://www.youtube.com/watch?v=plvQCOE9s_k
[dynein-video]: https://www.youtube.com/watch?v=-7AQVbrmzFw
[hms-dynein]: https://hms.harvard.edu/news/molecular-motor-struts-drunken-sailor
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
