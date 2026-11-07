HOLDS WITH CAVEATS
Referee: gpt-6.1-sol
NEW confirmed: yes

The note adds a later-data comparison that survives independent recomputation. It supports the frozen model beating the specified constant/logistic baselines on these reported fractions, with no claim of a new model, causal refutation or completed 2025 test.

Primary source: Victor Garcia is a coauthor. The abstract and Results genuinely print conditional 2025 resistance forecasts of France 25% (9–30), Denmark 84% (36–98), Sweden 62% (48–76). Equations 1–6 and Tables 1–2 were read in the [paper](https://doi.org/10.7717/peerj.8913). No later-surveillance MAE is printed there.

Independent code: `fresh_recompute.py` reconstructs the four compartments and likelihood, refits with Nelder–Mead, fits binomial logistic IRLS using only the original four Danish rows, and recomputes six outcomes, MAEs, rounding bounds and SBS. No claimant or earlier verifier code was imported. ODE/scalar solutions agree within 3.36e-11 in fraction.

Same-split unweighted MAE, percentage points; lower is better:

| Series | Trivial | Simple logistic | Frozen model | SBS |
|---|---:|---:|---:|---:|
| SSI 2021–2022 | 24.873192 | 13.919368 | 10.869207 | 0.782193 |
| MiBa 2021–2024 | 21.029515 | 19.946751 | 16.837261 | 0.258277 |

SBS was computed with the required sbs.py (`BASELINES.json`). This is mechanistic forecasting, not deep learning. The note's default-solver MAEs differ by only 0.0052/0.0062 points; independent refitting and published rounding do not reverse the advantage.

Primary surveillance checks confirm SSI 274 at 62.6% in 2021 (unique integer denominator 438), 311/436 in 2022; MiBa 60.6%, 63.2%, 63.6%, and rounded 65% in 2024. The 2022 source contrast is 8.1303 points. Sources: [SSI](https://en.ssi.dk/surveillance-and-preparedness/surveillance-in-denmark/annual-reports-on-disease-incidence/m/mycoplasma-genitalium), [MiBa 2023](https://en.ssi.dk/surveillance-and-preparedness/surveillance-in-denmark/annual-reports-on-disease-incidence/m/mycoplasma-genitalium-2011-2023), [2024](https://en.ssi.dk/surveillance-and-preparedness/surveillance-in-denmark/annual-reports-on-disease-incidence/m/mycoplasma-genitalium-2024).

The original model predates the outcomes; baseline fitting uses historical data only. The worker saw some later percentages before fixing its protocol, so researcher selection is not prospectively sealed. Kind: note is honest for the added empirical comparison; source reproduction alone is a rerun.

I ran cited-by myself for 10.7717/peerj.8913 and 10.1101/321216, opened potentially overlapping titles and relevant sections, and directly searched this question. No inspected work already contains this comparison. Riou concerns gonorrhoea; Bolaji uses another theoretical model; Almeida's open accepted manuscript additionally fits English 2016–2017 diagnoses. Details: PRIOR_ART.md.

Access caveats: Chua 2025 [10.1016/j.lanmic.2024.101047](https://doi.org/10.1016/j.lanmic.2024.101047) is gold OA, but Discussion/supplement remain unread after publisher/API, SSRN, Bern and Melbourne attempts. Kenyon 2021 [10.1097/OLQ.0000000000001404](https://doi.org/10.1097/OLQ.0000000000001404) was abstract-only; its PrEP cohort question excludes this comparison. The 2019 clinical item [10.1007/s15011-019-2392-x](https://doi.org/10.1007/s15011-019-2392-x) remains unread and predates the outcomes. OpenAlex reports 17 citations but returns 12 records. These are coverage limits, not evidence of an earlier result.

The authorized pod name is unavailable to its launcher (KeyError: fnew), so I did not repeat the full official R bootstrap. All light claimed comparisons were independently recomputed locally, one thread, nice 10.

Strongest author objection / weakest point: changed treatment, laboratory coverage, episode definitions and typing denominators make these fractions an imperfect target for the original conditional all-infection forecast. The note discloses this and every point remains inside its broad parameter band; only its limited transport comparison holds.

NEXT BAR: Obtain and inspect Chua's Discussion and supplement for any earlier comparison of the frozen Danish forecast with later surveillance.
