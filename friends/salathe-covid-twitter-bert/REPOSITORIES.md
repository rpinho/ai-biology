# Public-repository survey — 2026-11-06

Surveyed all 93 public repositories returned by the GitHub organization endpoint (one page of 100). Screened repository descriptions and available READMEs, and inspected paper/manuscript links. Historical `salathegroup` repository URLs resolve into `digitalepidemiologylab`; both old account listing endpoints return 404. See the saved API responses in `survey/`.

“Most used” is operationalized as GitHub stars, with forks shown as supporting context; these are popularity proxies, not download or active-user counts. Last commit means the default-branch HEAD committer date, not `pushed_at` (which can reflect PR activity). Dates are UTC. Inventory snapshots include hashes in `survey/inventory.json`.

## Selected runnable projects

1. **COVID-Twitter-BERT — 184 stars, 28 forks.** Highest-starred qualifying project; ships tokenization, preprocessing, training and inference code. Test input preparation and label handling without downloading the large model.
2. **PlantVillage analysis — 107 stars, 78 forks.** Runnable Caffe configurations and analysis scripts, explicitly the paper’s code release. Test analysis on tiny logs/HDF5 data without training Caffe.
3. **FoodRepo API — 63 stars, 6 forks.** The paper cites this repository’s executable client examples. It includes runnable JavaScript, Python, R and Ruby, in addition to dumps; it is not a data-only repository. Test request construction with a local XHR recorder, requiring no API account.

VaxGame has 85 stars/40 forks but its README identifies an outreach game developed by Ellsworth Campbell, and the paper search did not establish a Salathé-authored paper tied to this code. It is excluded on that evidence limit, not because of a guess about interest. The 59-star PlantVillage dataset is a data release. Neither outranks FoodRepo among established runnable paper-linked candidates.

## Established paper links (Salathé is a coauthor)

| Repository | Paper | Stars | Last commit | Role |
|---|---|---:|---|---|
| [covid-twitter-bert](https://github.com/digitalepidemiologylab/covid-twitter-bert) | [COVID-Twitter-BERT: A Natural Language Processing Model to Analyse COVID-19 Content on Twitter](https://arxiv.org/abs/2005.07503) | 184 | 2022-06-20 | model / training / preprocessing / inference code; SELECTED |
| [plantvillage_deeplearning_paper_analysis](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis) | [Using Deep Learning for Image-Based Plant Disease Detection](https://doi.org/10.3389/fpls.2016.01419) | 107 | 2016-08-15 | training configurations and executable analysis; SELECTED |
| [foodrepo_api](https://github.com/digitalepidemiologylab/foodrepo_api) | [FoodRepo: An Open Food Repository of Barcoded Food Products](https://doi.org/10.3389/fnut.2018.00057) | 63 | 2020-08-24 | runnable JS/Python/R/Ruby API clients and examples, plus data; SELECTED |
| [plantvillage_deeplearning_paper_dataset](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_dataset) | [Using Deep Learning for Image-Based Plant Disease Detection](https://doi.org/10.3389/fpls.2016.01419) | 59 | 2016-09-02 | image dataset; excluded from runnable-code selection |
| [crowdbreaks](https://github.com/digitalepidemiologylab/crowdbreaks) | [Crowdbreaks: Tracking Health Trends Using Public Social Media Data and Crowdsourcing](https://doi.org/10.3389/fpubh.2019.00081) | 12 | 2023-05-25 | platform code |
| [crowdbreaks-paper](https://github.com/digitalepidemiologylab/crowdbreaks-paper) | [Crowdbreaks: Tracking Health Trends Using Public Social Media Data and Crowdsourcing](https://doi.org/10.3389/fpubh.2019.00081) | 12 | 2020-05-19 | paper-specific code and data |
| [vaccine-sentiment](https://github.com/digitalepidemiologylab/vaccine-sentiment) | [Assessing Vaccination Sentiments with Online Social Media: Implications for Infectious Disease Dynamics and Control](https://doi.org/10.1371/journal.pcbi.1002199) | 12 | 2011-10-17 | paper-specific collection / classification code |
| [concept_drift_paper](https://github.com/digitalepidemiologylab/concept_drift_paper) | [Addressing machine learning concept drift reveals declining vaccine sentiment during the COVID-19 pandemic](https://arxiv.org/abs/2012.02197) | 6 | 2020-12-07 | paper code; README uses the earlier title How machine learning concept drift can negatively affect social media analysis |
| [experts-covid19-twitter](https://github.com/digitalepidemiologylab/experts-covid19-twitter) | [Experts and Authorities Receive Disproportionate Attention on Twitter During the COVID-19 Crisis](https://arxiv.org/abs/2008.08364) | 4 | 2020-11-10 | annotation data, model references and inference examples |
| [swisscovid_efficacy](https://github.com/digitalepidemiologylab/swisscovid_efficacy) | [Early Evidence of Effectiveness of Digital Contact Tracing for SARS-CoV-2 in Switzerland](https://doi.org/10.1101/2020.09.07.20189274) | 4 | 2020-09-19 | manuscript repository; not runnable code |
| [aerosol](https://github.com/digitalepidemiologylab/aerosol) | [Assessing the Dynamics and Control of Droplet- and Aerosol-Transmitted Influenza Using an Indoor Positioning System](https://doi.org/10.1038/s41598-019-38825-y) | 3 | 2020-01-13 | simulation / analysis code and data |
| [postprandial-glucose-traits-analyses](https://github.com/digitalepidemiologylab/postprandial-glucose-traits-analyses) | [Short-term postprandial glucose monitoring reveals stable traits from noisy free-living meals](https://doi.org/10.64898/2026.09.14.26362991) | 3 | 2026-09-09 | analysis notebooks / prepared inputs |
| [SocialContagion](https://github.com/digitalepidemiologylab/SocialContagion) | [Complex social contagion makes networks more vulnerable to disease outbreaks](https://arxiv.org/abs/1211.0518) | 2 | 2013-03-01 | simulation code and manuscript |
| [llm_crowd_experts_annotation](https://github.com/digitalepidemiologylab/llm_crowd_experts_annotation) | [Use of large language models as a scalable approach to understanding public health discourse](https://doi.org/10.1371/journal.pdig.0000631) | 2 | 2024-11-25 | analysis code and partial public annotation data |
| [vaccinationcontagionEPJDataScience](https://github.com/digitalepidemiologylab/vaccinationcontagionEPJDataScience) | [The dynamics of health behavior sentiments on a large online social network](https://doi.org/10.1140/epjds16) | 2 | 2013-04-04 | Java/SAS analysis code and data |
| [Collocation](https://github.com/digitalepidemiologylab/Collocation) | [A low-cost method to assess the epidemiological importance of individuals in controlling infectious disease outbreaks](https://doi.org/10.1186/1741-7015-11-35) | 1 | 2012-12-05 | simulation / collocation ranking scripts and matching input files |
| [FoodAndYou-PLOSDigitalHealth](https://github.com/digitalepidemiologylab/FoodAndYou-PLOSDigitalHealth) | [Food & You: A digital cohort on personalized nutrition](https://doi.org/10.1371/journal.pdig.0000389) | 1 | 2023-10-30 | R/Quarto figure code and aggregate data |
| [dietary-consistency-and-quality-associated-with-gut-microbiota-diversity-paper](https://github.com/digitalepidemiologylab/dietary-consistency-and-quality-associated-with-gut-microbiota-diversity-paper) | [Temporal nutrition analysis associates dietary regularity and quality with gut microbiome diversity: insights from the Food & You digital cohort](https://doi.org/10.1038/s41467-025-63799-z) | 1 | 2026-05-12 | analysis code and available data |
| [global-commons](https://github.com/digitalepidemiologylab/global-commons) | [Governing the Global Commons with Local Institutions](https://doi.org/10.1371/journal.pone.0034051) | 1 | 2012-04-17 | Java simulation code; paper named in repo description |
| [meal-pattern-analysis-paper](https://github.com/digitalepidemiologylab/meal-pattern-analysis-paper) | [Meal timing associations on dietary quality and glucose response](https://doi.org/10.1038/s44528-026-00033-2) | 1 | 2026-07-14 | analysis notebooks; README retains working title |
| [w3cRio](https://github.com/digitalepidemiologylab/w3cRio) | [Validating Models for Disease Detection Using Twitter](https://citeseerx.ist.psu.edu/document?doi=ef0f25bad89a16a43912a3296a36501b7bf9ad4c&repid=rep1&type=pdf) | 1 | 2014-01-28 | analysis material; README calls it Validating Methods |
| [UHS-Analysis](https://github.com/digitalepidemiologylab/UHS-Analysis) | [On the Ground Validation of Online Diagnosis with Twitter and Medical Records](https://doi.org/10.1145/2567948.2579272) | 0 | 2014-02-14 | analysis code and included manuscript source |
| [content_changes_paper](https://github.com/digitalepidemiologylab/content_changes_paper) | [Dynamics of social media behavior before and after SARS-CoV-2 infection](https://doi.org/10.3389/fpubh.2022.1069931) | 0 | 2023-01-17 | analysis / text-processing code |
| [covid-sources-timeliness](https://github.com/digitalepidemiologylab/covid-sources-timeliness) | [Timeliness of online COVID-19 reports from official sources](https://doi.org/10.3389/fpubh.2022.1027812) | 0 | 2022-11-07 | analysis code and data |
| [food-additives-gut-microbiota-public](https://github.com/digitalepidemiologylab/food-additives-gut-microbiota-public) | [Food additive exposure associated with reduction in gut microbiota diversity](https://doi.org/10.64898/2026.06.22.26356234) | 0 | 2026-01-22 | analysis code |
| [llm_benchmarking](https://github.com/digitalepidemiologylab/llm_benchmarking) | [Open-source solution for evaluation and benchmarking of large language models for public health](https://doi.org/10.1101/2025.03.20.25324040) | 0 | 2025-05-18 | R/Shiny benchmarking code and data |
| [mindays-estimation-paper](https://github.com/digitalepidemiologylab/mindays-estimation-paper) | [Minimum days estimation for reliable dietary intake information: findings from a digital cohort](https://doi.org/10.1038/s41430-025-01644-8) | 0 | 2025-03-27 | analysis notebooks |
| [network_assortativity_paper](https://github.com/digitalepidemiologylab/network_assortativity_paper) | [Positive Network Assortativity of Influenza Vaccination at a High School: Implications for Outbreak Risk and Herd Immunity](https://doi.org/10.1371/journal.pone.0087042) | 0 | 2017-06-29 | raw network data; not runnable-code target |
| [vaccine_sentiment_england](https://github.com/digitalepidemiologylab/vaccine_sentiment_england) | [Keep calm and carry on vaccinating: Is anti-vaccination sentiment contributing to declining vaccine coverage in England?](https://graphsearch.epfl.ch/en/publication/007ebfac-e128-41dc-9275-48da96ff935b) | 0 | 2019-12-23 | analysis code and aggregate data |

The UHS manuscript is saved at `survey/UHS-Analysis/paper.tex`; its title/authors and DOI are in that source. The Collocation association uses the named collocation method, the matching released scripts/data, and the source paper. Missing root READMEs are preserved as API 404 responses, not treated as evidence of absence of code.

## Related code/components — indirect paper associations

These project links are weaker than explicit paper data/code citations and do not alter the top-three selection.

| Repository | Related paper project | Stars | Last commit | Evidence / role |
|---|---|---:|---|---|
| [crowdbreaks-streamer-v1](https://github.com/digitalepidemiologylab/crowdbreaks-streamer-v1) | crowdbreaks | 6 | 2021-02-28 | platform stream processor; project association, not separately cited paper code |
| [caffe](https://github.com/digitalepidemiologylab/caffe) | plantvillage_deeplearning_paper_analysis | 4 | 2016-03-09 | framework fork referenced in paper; master is not proof of historical experiment branch |
| [PlantVillage-Analysis-Caffe](https://github.com/digitalepidemiologylab/PlantVillage-Analysis-Caffe) | plantvillage_deeplearning_paper_analysis | 3 | 2016-03-16 | earlier PlantVillage configuration repository; association inferred from project/files |
| [crowdbreaks-streamer](https://github.com/digitalepidemiologylab/crowdbreaks-streamer) | crowdbreaks | 2 | 2022-11-29 | platform stream processor; later implementation |
| [text-classification](https://github.com/digitalepidemiologylab/text-classification) | concept_drift_paper | 2 | 2022-02-24 | classification component; the paper repo has this as a submodule |
| [crowdbreaks-welcome](https://github.com/digitalepidemiologylab/crowdbreaks-welcome) | crowdbreaks | 1 | 2020-10-26 | project documentation, not runnable code |
| [plantvillage-analysis-env](https://github.com/digitalepidemiologylab/plantvillage-analysis-env) | plantvillage_deeplearning_paper_analysis | 1 | 2016-02-19 | Vagrant environment; project association inferred |
| [covid-scraper](https://github.com/digitalepidemiologylab/covid-scraper) | covid-sources-timeliness | 0 | 2022-08-23 | web scraper explicitly linked from the paper repository |
| [llm-prediction-tool](https://github.com/digitalepidemiologylab/llm-prediction-tool) | llm_benchmarking | 0 | 2025-03-20 | prediction prototype explicitly linked from the paper repository |
| [myfoodrepo_project](https://github.com/digitalepidemiologylab/myfoodrepo_project) | foodrepo_api | 0 | 2022-04-05 | link index also linking The Food Recognition Benchmark (10.3389/fnut.2022.875143); not executable analysis |
| [preprocess](https://github.com/digitalepidemiologylab/preprocess) | crowdbreaks | 0 | 2022-04-29 | platform data-processing component |

## Remaining repositories

No qualifying paper link/Salathé authorship was established for these within the survey. This is not a claim that none exists. The project descriptions are retained in the organization API snapshot. In particular, `brazil-vaccine-uptake` names a study topic but does not cite a paper, and `population-memetics` describes research in progress.

| Repository | Stars | Last commit |
|---|---:|---|
| [VaxGame](https://github.com/digitalepidemiologylab/VaxGame) | 85 | 2021-11-18 |
| [nodular.js](https://github.com/digitalepidemiologylab/nodular.js) | 12 | 2017-01-18 |
| [mkondo](https://github.com/digitalepidemiologylab/mkondo) | 5 | 2012-10-26 |
| [react-native-scandit](https://github.com/digitalepidemiologylab/react-native-scandit) | 5 | 2017-08-21 |
| [tweepy](https://github.com/digitalepidemiologylab/tweepy) | 4 | unavailable (fork/empty; not selected) |
| [covid-stream](https://github.com/digitalepidemiologylab/covid-stream) | 3 | 2020-05-06 |
| [openbeacon-case](https://github.com/digitalepidemiologylab/openbeacon-case) | 3 | 2016-02-01 |
| [population-memetics](https://github.com/digitalepidemiologylab/population-memetics) | 3 | 2012-03-22 |
| [COVID-documents](https://github.com/digitalepidemiologylab/COVID-documents) | 2 | 2020-04-22 |
| [MOOCnet](https://github.com/digitalepidemiologylab/MOOCnet) | 2 | 2013-08-16 |
| [google-images](https://github.com/digitalepidemiologylab/google-images) | 2 | unavailable (fork/empty; not selected) |
| [keyword_streamer](https://github.com/digitalepidemiologylab/keyword_streamer) | 2 | 2012-07-09 |
| [rails_ar_encryption](https://github.com/digitalepidemiologylab/rails_ar_encryption) | 2 | 2022-04-22 |
| [reverse-geocoder](https://github.com/digitalepidemiologylab/reverse-geocoder) | 2 | 2012-03-16 |
| [Minimal-Bag-of-Visual-Words-Image-Classifier](https://github.com/digitalepidemiologylab/Minimal-Bag-of-Visual-Words-Image-Classifier) | 1 | unavailable (fork/empty; not selected) |
| [VCFpreprocess](https://github.com/digitalepidemiologylab/VCFpreprocess) | 1 | 2016-10-03 |
| [Weighted_Network_Analysis](https://github.com/digitalepidemiologylab/Weighted_Network_Analysis) | 1 | unavailable (fork/empty; not selected) |
| [brazil-vaccine-uptake](https://github.com/digitalepidemiologylab/brazil-vaccine-uptake) | 1 | 2026-03-10 |
| [deep-height](https://github.com/digitalepidemiologylab/deep-height) | 1 | 2016-11-21 |
| [fuel](https://github.com/digitalepidemiologylab/fuel) | 1 | unavailable (fork/empty; not selected) |
| [pydeepgenomics](https://github.com/digitalepidemiologylab/pydeepgenomics) | 1 | 2017-01-26 |
| [sent2vec](https://github.com/digitalepidemiologylab/sent2vec) | 1 | unavailable (fork/empty; not selected) |
| [snakes](https://github.com/digitalepidemiologylab/snakes) | 1 | unavailable (fork/empty; not selected) |
| [twitter-visual](https://github.com/digitalepidemiologylab/twitter-visual) | 1 | 2012-08-25 |
| [2016_TwitterEpi](https://github.com/digitalepidemiologylab/2016_TwitterEpi) | 0 | 2017-09-20 |
| [Food-Repo-DNA-analysis-WIMF](https://github.com/digitalepidemiologylab/Food-Repo-DNA-analysis-WIMF) | 0 | 2021-10-04 |
| [JavaScriptAPIs_FoodRepo](https://github.com/digitalepidemiologylab/JavaScriptAPIs_FoodRepo) | 0 | 2019-11-27 |
| [JavaScriptAPIs_MyFoodRepo](https://github.com/digitalepidemiologylab/JavaScriptAPIs_MyFoodRepo) | 0 | 2019-10-28 |
| [JavaScriptAPIs_common](https://github.com/digitalepidemiologylab/JavaScriptAPIs_common) | 0 | 2019-09-03 |
| [Semester_Project](https://github.com/digitalepidemiologylab/Semester_Project) | 0 | 2018-01-11 |
| [Tweet_Filt](https://github.com/digitalepidemiologylab/Tweet_Filt) | 0 | 2017-09-13 |
| [barcode_test_swift](https://github.com/digitalepidemiologylab/barcode_test_swift) | 0 | 2016-02-11 |
| [coco-ui](https://github.com/digitalepidemiologylab/coco-ui) | 0 | unavailable (fork/empty; not selected) |
| [covid-stream-analysis](https://github.com/digitalepidemiologylab/covid-stream-analysis) | 0 | 2020-11-02 |
| [deepdetect](https://github.com/digitalepidemiologylab/deepdetect) | 0 | unavailable (fork/empty; not selected) |
| [deepimputation](https://github.com/digitalepidemiologylab/deepimputation) | 0 | 2016-11-07 |
| [django-tastypie](https://github.com/digitalepidemiologylab/django-tastypie) | 0 | unavailable (fork/empty; not selected) |
| [fastText](https://github.com/digitalepidemiologylab/fastText) | 0 | unavailable (fork/empty; not selected) |
| [grippenet](https://github.com/digitalepidemiologylab/grippenet) | 0 | 2017-01-23 |
| [hub](https://github.com/digitalepidemiologylab/hub) | 0 | unavailable (fork/empty; not selected) |
| [ladder](https://github.com/digitalepidemiologylab/ladder) | 0 | unavailable (fork/empty; not selected) |
| [lstm-char-cnn-tensorflow](https://github.com/digitalepidemiologylab/lstm-char-cnn-tensorflow) | 0 | unavailable (fork/empty; not selected) |
| [mini-challenges](https://github.com/digitalepidemiologylab/mini-challenges) | 0 | 2018-05-20 |
| [multi-lang-vaccine-sentiment](https://github.com/digitalepidemiologylab/multi-lang-vaccine-sentiment) | 0 | 2020-03-25 |
| [myfoodrepo-mask-rcnn](https://github.com/digitalepidemiologylab/myfoodrepo-mask-rcnn) | 0 | unavailable (fork/empty; not selected) |
| [nutrition-tracking-platform-v2](https://github.com/digitalepidemiologylab/nutrition-tracking-platform-v2) | 0 | 2025-04-16 |
| [paranoia](https://github.com/digitalepidemiologylab/paranoia) | 0 | unavailable (fork/empty; not selected) |
| [react-native-camera](https://github.com/digitalepidemiologylab/react-native-camera) | 0 | unavailable (fork/empty; not selected) |
| [rog-rl](https://github.com/digitalepidemiologylab/rog-rl) | 0 | 2024-04-08 |
| [swagger_engine](https://github.com/digitalepidemiologylab/swagger_engine) | 0 | unavailable (fork/empty; not selected) |
| [tensorflow_models_tf21](https://github.com/digitalepidemiologylab/tensorflow_models_tf21) | 0 | unavailable (fork/empty; not selected) |
| [twiprocess](https://github.com/digitalepidemiologylab/twiprocess) | 0 | 2022-08-16 |
| [vega-react-minimal-example](https://github.com/digitalepidemiologylab/vega-react-minimal-example) | 0 | 2018-05-29 |

## Pinned shallow clones

| Repository | Commit | Last commit |
|---|---|---|
| covid-twitter-bert | `86909698f104525b13d8ab0e22ae666e264ac5c6` | 2022-06-20T17:13:52+02:00 |
| foodrepo_api | `61b437d948e6c21acfedcc49aa8ff6dde2a1b945` | 2020-08-24T17:16:36+02:00 |
| plantvillage_deeplearning_paper_analysis | `90dd7555352a77e427918c124306780e0951f46d` | 2016-08-15T18:03:19+02:00 |

## Issues and PRs read before cloning

Fetched all open issues/PRs and up to 30 recent closed issues/PRs, sorted by last update, with issue comments and PR review comments/reviews. All selected projects have fewer than 30 closed entries, so this covers their complete visible histories. No open page reached the 100-entry limit. Raw responses are in `survey/<repo>/`.

| Repo | Open issues | Closed issues | Open PRs | Closed PRs |
|---|---:|---:|---:|---:|
| covid-twitter-bert | 6 | 12 | 2 | 10 |
| plantvillage_deeplearning_paper_analysis | 2 | 0 | 1 | 0 |
| foodrepo_api | 4 | 6 | 2 | 15 |

Dependency-bump PR release notes were screened by title/package/version; human issue bodies and discussion were read. Known issues excluded from the bug count are listed in `BUGS.md`.
