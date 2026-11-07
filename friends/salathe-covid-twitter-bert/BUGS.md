# Confirmed correctness bugs

Six defects, six private fixes. The three selected repositories, paper links, stars, issue histories and pinned commits are in [REPOSITORIES.md](REPOSITORIES.md). Every repro runs the pinned source, records its failing output, applies its own minimal Git patch in a temporary local checkout, and compares the result against a separately written reference check. Ordinary inputs are compared before/after. The reference checks are separate implementations, not another person's review.

These are software-correctness findings. **NEW: no** under the stated paper-result definition: no printed benchmark number was beaten, open research problem settled, or scientific prediction tested on new data. No claim is made that the original paper results change. No training, large checkpoint download, authenticated FoodRepo request, or public write occurred.

## CT001 — prediction truncation reserves the special tokens with the wrong sign

- **Repo / pin:** `digitalepidemiologylab/covid-twitter-bert` @ `86909698f104525b13d8ab0e22ae666e264ac5c6`.
- **File:line:** [`run_predict.py:77`](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/run_predict.py#L77).
- **Wrong:** the branch for an overlong token sequence slices at `max_seq_length + 2`, then adds `[CLS]` and `[SEP]`. It must reserve two positions by slicing at `max_seq_length - 2`.
- **Repro:** [repro/CT001/](repro/CT001/), run `./repro/CT001/run.sh`.
- **Before → after:** with a six-position configuration, five wordpieces yield word-ID/mask lengths 7 and segment-ID length 6; ten wordpieces yield lengths 10/10/6. After the one-line fix all three inputs have length 6 and the expected four-wordpiece prefix plus special tokens. Two- and four-wordpiece normal/boundary inputs are byte-for-byte unchanged.
- **Independent check:** a standard-library reference constructs expected token IDs from the shipped vocabulary and the six-position budget; it does not call the repo's tokenizer or input builder.
- **Effect:** overlength single-text, interactive and text-file prediction inputs violate the classifier's configured shapes. This can prevent predictions; it is not a measured change to a paper score. Real TensorFlow tensors and the exact pinned BERT tokenizer were used, with no model weights.
- **Confidence:** high for the input-construction defect. Full BERT/cloud inference was not run.

## CT002 — the Unicode-symbol removal option silently removes nothing

- **Repo / pin:** `covid-twitter-bert` @ `86909698f104525b13d8ab0e22ae666e264ac5c6`.
- **File:line:** [`utils/preprocess.py:69`](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/utils/preprocess.py#L69).
- **Wrong:** `unicodedata.category(ch)[0]` is one character, so it never equals the two-character category `So`. The CLI help explicitly says this option removes category `So`.
- **Repro:** [repro/CT002/](repro/CT002/), run `./repro/CT002/run.sh`.
- **Before → after:** the helper returns `A℗B` and `A⏣B` unchanged before; after it returns `AB`. With default preprocessing options the corresponding results change from `a℗b` / `a⏣b` to `ab`. These non-emoji symbols survive the preceding emoji conversion. Ordinary text, accented letters, numbers, math signs and punctuation remain unchanged.
- **Independent check:** a separate character-by-character Unicode-category reference agrees with both the helper and the complete preprocessing function.
- **Effect:** users requesting symbol removal receive different model input text from the documented cleaning policy. Fixing this changes affected preprocessing and requires keeping training and inference preprocessing consistent; no benefit to an existing trained checkpoint is asserted.
- **Confidence:** high. The repro imports the actual preprocessing module; it restores only the documented Python-3.8 HTML-unescape API on the host Python 3.9.

## CT003 — numeric TSV class labels crash TFRecord generation

- **Repo / pin:** `covid-twitter-bert` @ `86909698f104525b13d8ab0e22ae666e264ac5c6`.
- **File:line:** [`preprocess/create_finetune_data.py:145`](https://github.com/digitalepidemiologylab/covid-twitter-bert/blob/86909698f104525b13d8ab0e22ae666e264ac5c6/preprocess/create_finetune_data.py#L145), feeding the mapping at lines 150–155 and `TextClassificationProcessor._create_examples`.
- **Wrong:** pandas infers numeric labels as integers, while the processor reads the emitted TSV labels as strings. The pinned TensorFlow-models converter indexes an integer-keyed label map with a string.
- **Repro:** [repro/CT003/](repro/CT003/), run `./repro/CT003/run.sh`. Each train/dev split has only two rows in the documented `id / label / text` format.
- **Before → after:** labels `0,1` fail with `KeyError: '0'`; after requesting string dtype for the label column, the real writer emits two training TFRecords with label IDs `[0,1]` and label mapping `["0","1"]`. Normal `label_a,label_b` mapping and TFRecord label IDs are unchanged.
- **Independent check:** Python's CSV reader independently derives the textual label vocabulary and IDs, without pandas, TensorFlow or repo code.
- **Effect:** a common binary/numeric classification dataset cannot reach fine-tuning through the supplied preparation script. This is a data-preparation crash, not proof that the published datasets or scores were affected.
- **Confidence:** high. The repro runs the actual `main`, processor and pinned converter, and reads the serialized TFRecords. Runtime substitutions are documented in the repro README.

## FR001 — JavaScript product-detail requests omit the requested product ID

- **Repo / pin:** `digitalepidemiologylab/foodrepo_api` @ `61b437d948e6c21acfedcc49aa8ff6dde2a1b945`.
- **File:line:** [`v3/code/javascript/foodrepo_api_v3.js:114`](https://github.com/digitalepidemiologylab/foodrepo_api/blob/61b437d948e6c21acfedcc49aa8ff6dde2a1b945/v3/code/javascript/foodrepo_api_v3.js#L114).
- **Wrong:** a nonempty ID adds only `/` to `products`, never the ID. The bundled page itself calls `endpoint.product(product0.id, null, ...)`.
- **Repro:** [repro/FR001/](repro/FR001/), run `./repro/FR001/run.sh`. A local XHR recorder captures the real client's outgoing request; no network request occurs.
- **Before → after:** `product(2663, null, callback)` targets `/api/v3/products/?` before and `/api/v3/products/2663?` after. The ordinary `products(2,5,callback)` listing request is identical before/after.
- **Independent check:** a separate Python REST-path check verifies the requested ID against the API's documented single-product resource pattern (also used by the bundled Python example).
- **Effect:** callers and the bundled demo fail to retrieve the requested product detail and may receive a collection or an error instead. The observed defect is request construction; live server behavior and any paper-level effect were not tested.
- **Confidence:** high.

## FR002 — a scalar include option crashes the JavaScript client

- **Repo / pin:** `foodrepo_api` @ `61b437d948e6c21acfedcc49aa8ff6dde2a1b945`.
- **File:line:** [`v3/code/javascript/foodrepo_api_v3.js:27`](https://github.com/digitalepidemiologylab/foodrepo_api/blob/61b437d948e6c21acfedcc49aa8ff6dde2a1b945/v3/code/javascript/foodrepo_api_v3.js#L27).
- **Wrong:** the helper promises a value or list of values. Its scalar branch stores `[values]` in an unused `includes` variable, then calls `.map` on the original scalar.
- **Repro:** [repro/FR002/](repro/FR002/), run `./repro/FR002/run.sh`.
- **Before → after:** `product(2663, 'images', callback)` raises `TypeError: values.map is not a function`; after normalizing `values` itself, it constructs exactly the same query as `['images']`. Existing array/null calls are unchanged.
- **Independent check:** Python independently parses the recorded URL query and checks `include=images` plus scalar/list equivalence.
- **Effect:** a supported option form aborts before any request, preventing data retrieval. This patch is intentionally independent of FR001: its detail URL still has FR001's separate defect unless both patches are applied.
- **Confidence:** high for the helper's explicitly stated scalar/list contract. The JavaScript file describes itself as an alpha draft; no official deployed-client usage is asserted.

## PV001 — a one-iteration Caffe log loses its output rows and crashes CSV export

- **Repo / pin:** `digitalepidemiologylab/plantvillage_deeplearning_paper_analysis` @ `90dd7555352a77e427918c124306780e0951f46d`.
- **File:line:** [`googLeNet/color-80-20/finetune/results/parse_log.py:132`](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/blob/90dd7555352a77e427918c124306780e0951f46d/googLeNet/color-80-20/finetune/results/parse_log.py#L132) (missing EOF flush); CSV export fails at line 219. The same parser is copied into 62 experiment folders, listed in the repro.
- **Wrong:** the first train/test row is retained in a local variable until another iteration establishes the row schema. EOF never flushes those remaining rows. A log containing one train and one test output at one iteration consequently returns two empty lists.
- **Repro:** [repro/PV001/](repro/PV001/), run `./repro/PV001/run.sh`.
- **Before → after:** a valid four-line log returns 0 train / 0 test rows, and CSV export raises `IndexError: list index out of range`. After flushing pending rows at EOF, it writes 1 train / 1 test row. The ordinary two-iteration case is identical. The archived full Caffe log still produces 602 train / 31 test rows, with identical CSV bytes before/after.
- **Independent check:** a separate EOF/CSV check derives the expected iteration rows directly from the fixture's records. It imports no repo code. The patch changes only the same EOF handling in all 62 parser copies.
- **Effect:** short/debug/interrupted single-iteration runs cannot produce their analysis CSVs through the bundled parser. No effect on the published full-run results is demonstrated; the full archived run is explicitly unchanged.
- **Confidence:** high for the parser defect. Python-2 print syntax is converted in memory; the parsing logic is unchanged. Caffe itself and model training were not run.

# Suspected — not included in the confirmed count

- **CT-BERT training versus direct-text inference preprocessing:** `create_finetune_data.py` calls `preprocess_bert`, while `run_predict.py`'s text paths tokenize their input directly. This suggests that raw handles/URLs may be represented differently unless the caller already preprocesses them. No matched small trained checkpoint with an established raw-input contract was available under the checkpoint limit; no prediction failure or numerical effect was demonstrated, and no patch is supplied.
- **PlantVillage external-image preprocessing:** `googLeNet/segmented-80-20/test_bing/test_bing.prototxt` references an external-test mean file, while its training configuration references the PlantVillage mean. The means, original HDF5 predictions and weights are not released here. Different file paths alone do not prove different means or changed predictions. No confirmed bug or paper correction is claimed.

# Known issues and rejected candidates excluded

- **CT-BERT:** open issues [17](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/17) and [30](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/30) already concern dataset download / Colab errors. Closed [6](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/6) fixed malformed tweet IDs; [10](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/10) and [11](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/11) concern model conversion / historical Hugging Face weights; [5](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/5) concerns lowercasing; [12](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/12) concerns GPU memory. [21](https://github.com/digitalepidemiologylab/covid-twitter-bert/issues/21)'s multi-token COVID words are normal WordPiece behavior. Dependency bump PRs and the README's known TF 2.3 incompatibility are excluded.
- **PlantVillage:** [issue 1](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/issues/1) already reports standard-Caffe HDF5Output incompatibility; [issue 2](https://github.com/digitalepidemiologylab/plantvillage_deeplearning_paper_analysis/issues/2) reports broken external-image links. PR 3 changes the README. The suspected divisible-batch loss did **not** reproduce: unchanged constants 32,400 / 24 / 1,351 retain all 32,400 rows and discard only the extra repeated batch. Its speculative patch was withdrawn before application; the investigation is retained under `survey/suspected-PV-batch/`.
- **FoodRepo:** open [20](https://github.com/digitalepidemiologylab/foodrepo_api/issues/20) concerns nutrient/unit naming, [1](https://github.com/digitalepidemiologylab/foodrepo_api/issues/1) requests brand fields, [23](https://github.com/digitalepidemiologylab/foodrepo_api/issues/23) requests a new dump, and [28](https://github.com/digitalepidemiologylab/foodrepo_api/issues/28) requests an API key. Historical pagination [17](https://github.com/digitalepidemiologylab/foodrepo_api/issues/17), CORS [15](https://github.com/digitalepidemiologylab/foodrepo_api/issues/15), sorting [10](https://github.com/digitalepidemiologylab/foodrepo_api/issues/10), malformed-request [11](https://github.com/digitalepidemiologylab/foodrepo_api/issues/11) / [12](https://github.com/digitalepidemiologylab/foodrepo_api/issues/12), and deprecated-v2 problems are excluded. Python 3 conversion (PR 24) and dependency bumps are not new findings.

None of the six confirmed failures was described in the selected repositories' saved visible issue/PR histories. This is a scoped duplicate check, not a claim of worldwide priority.
