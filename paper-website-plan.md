# scDrugPerturb-Bench Paper Website Plan

## 1. Page Goal

The paper page should make one argument, not reproduce the manuscript section by section:

> **Expression reconstruction is not mechanism recovery.**

The page should establish three linked claims:

1. Mechanism Fidelity Score (MFS) measures information that traditional expression-reconstruction metrics do not capture.
2. Changing the evaluation target changes which model appears best.
3. Current models reconstruct expression much better than they recover case-specific mechanisms.

MFS should always be presented as an important **complement** to traditional metrics, not as a universal replacement for them.

## 2. Intended Audience

- Researchers developing virtual-cell and perturbation-prediction models
- Computational biologists evaluating single-cell foundation models
- Drug-discovery researchers using transcriptomic models for screening
- Dataset and benchmark users looking for reproducible evaluation resources

## 3. Page Structure

### 3.1 Paper Hero

Content:

- Paper title: *Do single-cell drug perturbation models recover mechanisms beyond expression reconstruction?*
- One-sentence conclusion: `Expression reconstruction is not mechanism recovery.`
- Author list and affiliations
- Simucella / HITSZ / MindFlow.AI identity
- Paper status, publication venue or preprint information
- Primary actions: `Paper`, `Code`, `Benchmark`, `Citation`

Layout and typography:

- Use a compact title scale: `48-54 px` on desktop and `34-40 px` on mobile.
- Keep the hero text-led and shallow enough that the first evidence section is visible in the initial viewport.
- Do not place a scientific figure in the hero.
- Do not include a `Figure resources` button.
- Hide unavailable actions rather than linking to placeholders.

### 3.2 At a Glance: A Three-Visual Argument

This is the main body of the page. It should occupy most of the editorial attention and contain only three large scientific visuals. The visuals form a continuous evidence chain:

> **Different question → different winner → unresolved model weakness**

The original manuscript panels are source material for these redraws. They should not be pasted into the primary scroll as separate figures.

#### Visual 1 — High expression similarity can mask mechanism failure

Claim:

> **A prediction can look expression-like while recovering little of the case-specific mechanism.**

Final composition:

- Draw only the PCS–MSE relationship; do not combine it with other metric pairs or a biological case inset.
- Main plot:
  - x-axis: similarity-based score derived from MSE.
  - y-axis: Pattern Consistency Score (PCS).
  - Each point represents one evaluated perturbation case.
  - Model families are encoded with restrained marker shapes rather than many colours.
- Highlight the high-MSE/low-PCS quadrant as `expression-like, mechanism-low`.
- Show the exact PCS and MSE thresholds with subtle dashed lines and a pale coral background band.
- Add one clean zoom of the highlighted quadrant outside the main plotting area.
- Use the real headline count from the current analysis: `399/683 cases`, `58.4% [55-62]`.
- Keep the title declarative: `High expression similarity can mask mechanism failure`.

Recommended real-data redraw:

- Use the PCS–MSE panel structure as the data reference, but redraw it as a single website-native composition.
- Retain every real case and its model-family identity; do not estimate points from the SVG.
- Calculate the highlighted count and confidence interval from the source table rather than hard-coding the displayed result.
- Keep the full `0-1` axes so the threshold region is not exaggerated by cropping.
- The zoom is supporting evidence only; it must not obscure the original points or thresholds.

Interpretation boundary:

- Low PCS indicates poor directional recovery of annotated mechanism genes; it does not by itself prove every part of the predicted mechanism is reversed.
- Describe PCS/MFS as complementary to reconstruction metrics, not a replacement for expression reconstruction.
- Report the denominator, threshold definitions and interval method alongside the final chart.

Current simulated concept:

- `design-drafts/claim-1-complementary-metrics.svg`
- The current version uses 683 simulated cases and reproduces the intended `399/683` highlighted composition. Replace every point with the verified source data before publication.

#### Visual 2 — The evaluation target changes which model appears best

Claim:

> **A reconstruction-only leaderboard can select the wrong model for mechanism-oriented use.**

Final composition:

- A slopegraph or rank-flow chart linking each model's ESS rank to its MFS rank.
- Highlight the ESS winner in blue and the MFS winner in green; keep other models neutral.
- Put the aggregate results directly above or beside the chart:
  - MFS and ESS selected different top models in all five cell-line splits.
  - Median model-rank correlation: `-0.104`.
  - ESS recovered the MFS-optimal model at Hit@3 of only `0.176`.
- If the slopegraph shows one representative split, label the split in content-based language and keep the five-split statistics visible as the primary evidence.

Recommended real-data redraw:

- Calculate ranks from the same model set and split before drawing connections.
- Show ties explicitly and document the tie-breaking rule.
- A small split selector may be added later, but the default static view must communicate the result without interaction.
- Do not create a conventional dense leaderboard table in the main scroll.

Current simulated concept:

- `design-drafts/claim-2-ranking-shift.svg`

#### Visual 3 — Current models recover mechanisms poorly

Claim:

> **Reasonable reconstruction scores coexist with low mechanism fidelity and common shortcut failures.**

Final composition:

- Left: a model-level reconstruction-versus-mechanism comparison that makes the gap immediately visible.
- Right: a compact prevalence chart for the dominant failure modes, especially signature-specificity and generic-response shortcuts.
- Use the real failure evidence as the headline:
  - Overall shortcut/failure burden: `44.6-61.5%`.
  - Signature-specificity failure: `84.3-99.9%`.
  - Generic-response shortcut: `54.3-88.9%`.
  - Median true-signature-first fraction: approximately `1.9%`.
  - Median strength-controlled discrimination accuracy: approximately `48.7%`.

Recommended real-data redraw:

- Do not place ESS and MFS on one numerical axis unless their transformation creates a genuinely comparable scale.
- Preferred options are two aligned axes, a clearly defined fraction-of-achievable-range scale, or a reconstruction/MFS plane with separate labeled axes.
- Show uncertainty across seeds, folds or splits where available.
- Put denominators and the definition of each failure rate in the methods tooltip or expandable note.
- Preserve the distinction between an incorrect mechanism and a zero-response collapse; the benchmark observed `0%` no-change collapse for all evaluated methods.

Current simulated concept:

- `design-drafts/claim-3-mechanism-failure.svg`
- Its shared normalized axis is illustrative only and must not be retained unless the real normalization is scientifically justified.

#### Section rhythm

- Each visual starts with a short declarative heading and one sentence of interpretation.
- Alternate text and visual alignment on wide screens, but keep the scientific chart at least 60% of the content width.
- On mobile, stack heading → one-sentence claim → chart → two-line interpretation.
- Avoid cards around every item. The three visuals should feel like consecutive chapters of one argument.
- Do not display figure numbers or panel letters in headings, captions, buttons, alt text or image labels.

### 3.3 Why the Benchmark Is Credible

This section supports the three claims without adding another large scientific figure.

Use live HTML statistics and a restrained curation-to-evaluation flow:

| Statistic | Value |
| --- | ---: |
| PubMed records screened | >50,000 |
| Studies | 93 |
| Datasets | 181 |
| Cells | 2.5 million |
| Drugs | 101 |
| Cellular contexts | 137 |
| Tissue groups | 13 |
| Experimental sources | 5 |
| Unique annotated key genes | 717 |
| Directionally annotated response cases | 423 |
| Model evaluations | 4,500 |

Supporting scope:

- 12 published perturbation-prediction models and 3 baselines
- 10 data splits
- Raw expression plus 9 representation methods
- 8 frozen single-cell foundation models plus PCA
- 7 expression-similarity metrics and 6 mechanism-fidelity metrics

Use a single CSS/HTML flow line for `literature → curated mechanisms → perturbation matrix → model evaluation`. Do not add the full manuscript overview figure to the main narrative.

### 3.4 What MFS Measures

Present the six MFS components as compact HTML rows or an expandable glossary:

| Metric | Evaluation question |
| --- | --- |
| Pattern Consistency Score | Are annotated key genes changed in the correct direction? |
| Effect Size Recovery | Is the predicted response magnitude calibrated to the measured effect? |
| Gene-set Coherence Score | Are mechanism genes predicted as a coordinated response? |
| Mechanism Specificity Score | Is signal concentrated on mechanism-relevant genes rather than matched background genes? |
| Pathway Spearman | Are predicted and observed pathway-enrichment profiles concordant? |
| Pathway Sign Accuracy | Are activated and suppressed pathways assigned the correct polarity? |

This section explains the metric; it should not introduce another large image.

### 3.5 Why the Distinction Matters

Use one short downstream-validation paragraph and a live HTML number strip rather than a fourth full-width plot:

- Top-1 near-oracle representation recovery: `26.7%` with ESS versus `40.0%` with MFS.
- Top-3 recovery: `73.3%` versus `80.0%`.
- Top-5 recovery: `86.7%` versus `93.3%`.
- At mechanism weight `r = 0.9`, Hit@5, Hit@10 and Hit@50 improved by `27.3%`, `16.7%` and `9.3%` relative to ESS-based selection.

Claim boundary:

- Describe MFS as `more informative in aggregate` or `better aligned in selected settings`.
- The paired comparison was not statistically significant after correction, so do not claim universal downstream superiority.
- The etoposide example may appear as an optional expandable case, not as a fourth main visual.

### 3.6 Scope and Limitations

- Literature-curated mechanism genes are incomplete and biased toward well-studied biology.
- The benchmark evaluates transcriptional mechanism fidelity, not direct target engagement, protein activity, phenotypic rescue or clinical efficacy.
- CURE-based retrieval is an application-level validation, not a universal therapeutic endpoint.
- MFS rankings depend on metric definitions and aggregation choices.
- scFMs were evaluated as frozen representations rather than with fine-tuning or end-to-end adaptation.
- Dataset coverage is uneven across drugs, doses, times and cellular states.

### 3.7 Open Resources and Citation

Include:

- Manuscript / preprint / published paper
- Benchmark download
- Code and evaluation toolkit
- Version and release notes
- Model outputs or leaderboard, when available
- Reproducibility information
- BibTeX citation block
- License and contact information
- Link back to the Simucella project homepage

### 3.8 Optional Evidence Gallery

- Keep complete manuscript figures outside the primary narrative.
- Expose them through a collapsed `Explore all results` section or separate resources page.
- Use content-based labels, not manuscript figure numbers, in the public interface.
- The gallery is supporting evidence and must not interrupt the three-visual argument.

## 4. Real-Data Requirements for the Three Redraws

### 4.1 Complementarity visual

- One row per displayed perturbation case
- MSE-derived similarity score and PCS value for every row
- Model-family label and stable case identifier
- Exact MSE and PCS threshold definitions
- Highlighted-case flag or the inputs required to recalculate it
- Numerator, denominator and confidence-interval method for `399/683` and `58.4% [55-62]`
- Any filtering, missing-value handling and score clipping applied before plotting

### 4.2 Ranking-shift visual

- Model-level ESS and MFS aggregates for every displayed split
- Model names, baseline labels, rank values and tie information
- Per-split top model, Top-3 set, rank correlation and Hit@3 calculation
- Seed/fold summaries or uncertainty when available

### 4.3 Mechanism-failure visual

- Model-level ESS and MFS summaries with the exact aggregation and normalization definitions
- Per-model/per-split uncertainty
- Failure-mode numerator, denominator and prevalence for every method
- Baseline and no-change-collapse results
- Definitions for signature-specificity, generic-response, global-strength, magnitude and direction failures

## 5. Simulated Storyboard Deliverables

All current values are synthetic placeholders and every draft is visibly marked `SIMULATED DATA | CONCEPT DRAFT`.

- `design-drafts/claim-1-complementary-metrics.png` and `.svg`
- `design-drafts/claim-2-ranking-shift.png` and `.svg`
- `design-drafts/claim-3-mechanism-failure.png` and `.svg`
- `design-drafts/simulated_storyboard.py`
- `design-drafts/source-data/*.csv`

The SVG files retain editable text. The Python script is the single rendering source for both SVG and PNG outputs.

## 6. Visual and Implementation Rules

- Main narrative budget: exactly three large scientific visuals.
- Use blue for expression reconstruction, green for mechanism fidelity, coral for critical mismatch/failure and neutral grey for context.
- Do not rely on red/green alone; use text labels, position and line structure as redundant encodings.
- Keep all key numbers as live HTML where possible, even when echoed in a chart.
- Use SVG for primary charts and responsive PNG/WebP fallbacks only when needed.
- Preserve editable text in SVG exports.
- Public-facing labels must be content-based; internal asset filenames may retain manuscript panel identifiers.
- All simulated drafts must remain clearly labeled until they are replaced by verified real-data exports.
- Document metric definitions, splits, seeds/folds, uncertainty and baselines alongside the final quantitative redraws.
