# scDrugPerturb-Bench Paper Website Plan

## 1. Page Goal

This page introduces the scDrugPerturb-Bench paper as a focused research story within the broader Simucella project. It should not reproduce the manuscript section by section. Instead, it should explain the scientific question, show why the benchmark is needed, summarize the principal findings and direct visitors to the paper, code, benchmark and citation.

The central message is:

> **Expression reconstruction is not mechanism recovery.**

Supporting message:

> Single-cell drug perturbation models should be evaluated not only by how closely they reconstruct expression profiles, but also by whether they recover case-specific drug mechanisms in the correct genes, pathways and directions.

## 2. Intended Audience

- Researchers developing virtual-cell and perturbation-prediction models
- Computational biologists evaluating single-cell foundation models
- Drug-discovery researchers using transcriptomic models for screening
- Dataset and benchmark users looking for reproducible evaluation resources

## 3. Page Structure

### 3.1 Paper Hero

Content:

- Paper title: *Do single-cell drug perturbation models recover mechanisms beyond expression reconstruction?*
- One-sentence conclusion
- Author list and affiliations
- Simucella / HITSZ / MindFlow.AI identity
- Paper status, publication venue or preprint information
- Primary actions: `Paper`, `Code`, `Benchmark`, `Citation`

Recommended visual:

- Use the Figure 2a mechanism-mismatch case as the main visual signal.
- Do not place the complete Figure 1 in the hero because its small labels are too dense at normal webpage width.

### 3.2 The Evaluation Gap

Section question:

> Does an expression-like prediction imply that a model has learned the drug mechanism?

Use the T0901317-treated human iPSC-derived microglia example. The measured response upregulates the LXR target genes `ABCA1`, `ABCG1`, `APOE` and `ACSL1`, whereas the evaluated model predicts the opposite direction for all four genes at 30 nM and 100 nM despite high expression-similarity scores.

Recommended visual:

- Figure 2a as a dedicated, readable panel
- A short comparison between `High expression similarity` and `Incorrect mechanism direction`

### 3.3 scDrugPerturb-Bench At a Glance

Headline statistics:

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

Response-case composition:

- 195 upregulated
- 126 downregulated
- 102 non-significant

Recommended visual treatment:

- Split Figure 1 into three responsive blocks:
  1. Literature-to-matrix data curation
  2. Benchmark evaluation pipeline
  3. Dataset coverage and composition
- Keep the statistics as live HTML text rather than baking them into an image.

### 3.4 What the Benchmark Evaluates

Benchmark scope:

- 12 published perturbation-prediction models
- 3 baselines
- 10 data splits
- Raw expression plus 9 representation methods
- 8 frozen single-cell foundation models plus PCA
- 7 expression-similarity metrics
- 6 mechanism-fidelity metrics

Generalization regimes:

- Cell-line regime: IID-sample, OOD-drug, OOD-cell, OOD-tissue and OOD-drug-cell-pair
- Source regime: IID-sample and held-out experimental-source settings

Mechanism Fidelity Score components:

| Metric | Question |
| --- | --- |
| Pattern Consistency Score (PCS) | Are the annotated key genes changed in the correct direction? |
| Effect Size Recovery (ESR) | Is the predicted response magnitude calibrated to the measured effect? |
| Gene-set Coherence Score (GCS) | Are mechanism genes predicted as a coordinated response? |
| Mechanism Specificity Score (MSS) | Is signal concentrated on mechanism-relevant genes rather than matched background genes? |
| Pathway Spearman | Are predicted and observed pathway-enrichment profiles concordant? |
| Pathway Sign Accuracy | Are activated and suppressed pathways assigned the correct polarity? |

The website should present these definitions as compact HTML components. A full screenshot of the metric diagram should remain optional.

### 3.5 Main Finding: Expression Similarity Does Not Imply Mechanism Fidelity

Key results:

- Across 175 expression-mechanism metric comparisons, median Spearman correlation was `0.052`.
- Median absolute correlation was `0.241`.
- `58.9%` of absolute correlations were below `0.3`.
- `88.6%` were below `0.5`.
- MFS and ESS never selected the same top-ranked model across the five cell-line splits.
- Their median model-rank correlation was `-0.104`.
- ESS recovered the MFS-optimal model at Hit@3 of only `0.176`.

Recommended panels:

- Figure 2c: metric correlations
- Figure 2d: different model rankings
- Figure 2f: mechanism loss under expression-based model selection

The website copy should distinguish non-redundancy from opposition: weak or unstable alignment does not mean every expression metric is negatively associated with mechanism fidelity.

### 3.6 Downstream Relevance for Drug Screening

Explain how MFS- and ESS-selected representations were evaluated with a fixed CURE-based compound-retrieval workflow.

Key results:

- Top-1 near-oracle representation recovery increased from `26.7%` with ESS to `40.0%` with MFS.
- Top-3 recovery increased from `73.3%` to `80.0%`.
- Top-5 recovery increased from `86.7%` to `93.3%`.
- At mechanism weight `r = 0.9`, Hit@5, Hit@10 and Hit@50 improved by `27.3%`, `16.7%` and `9.3%` relative to ESS-based selection.
- In the etoposide example, the MFS-selected representation reached Hit@50 of `1.0`, compared with `0.2` for the ESS-selected representation.

Recommended panels:

- Figure 3d: near-oracle selection
- Figure 3e: MFS-weight sensitivity
- Figure 3f: etoposide retrieval case study

Claim boundary:

The paper reports an aggregate and context-dependent advantage. The paired comparison was not statistically significant after correction. Website language should therefore use formulations such as `more informative in aggregate` or `better aligned in selected settings`, rather than claiming universal superiority.

### 3.7 Model and Representation Landscape

Main messages:

- Absolute mechanism recovery remains weak across cell-line and cross-source settings.
- No single perturbation predictor or representation dominates across metrics and splits.
- Frozen single-cell foundation-model embeddings do not provide a universal mechanism-enhancing input.
- Representation gains are local, metric dependent and strongly shaped by the downstream predictor.
- Raw expression and PCA remain competitive in multiple settings.
- Model choice should account for GPU runtime, peak RAM and peak GPU memory as separate constraints.

Recommended use of figures:

- Keep Figures 4 and 5 out of the primary narrative flow at full size.
- Use selected panels as a secondary results section:
  - Figure 4a: cell-line evaluation design
  - Figure 4b: absolute mechanism-fidelity landscape
  - Figure 4e: embedding-predictor gain map
  - Figure 5a: cross-source evaluation design
  - Figure 5b: cross-source mechanism-fidelity landscape
  - Figure 5e: cross-source gain map
- Provide complete Figures 4 and 5 in a click-to-zoom figure gallery.

### 3.8 Shortcut and Failure Modes

Use hard negatives to explain why plausible non-zero responses may still fail to recover the current case-specific mechanism.

Failure modes:

- Mean-response memorization
- Direction failure
- Magnitude mismatch
- Generic-response shortcut
- Signature-specificity failure
- Global-strength shortcut

Key results:

- Overall shortcut and failure burden ranged from `44.6%` to `61.5%`.
- No-change collapse was `0%` for all evaluated methods.
- Signature-specificity failure ranged from `84.3%` to `99.9%`.
- Generic-response shortcut ranged from `54.3%` to `88.9%`.
- No model had a positive median signature-specificity gap.
- The median true-signature-first fraction across methods was approximately `1.9%`.
- Median strength-controlled discrimination accuracy was approximately `48.7%`.

Recommended panels:

- Figure 6a: overview of failure burden
- Figure 6d: generic-response shortcut
- Figure 6e: non-matching signature decoys
- Figure 6f: strength-matched decoys

### 3.9 Scope and Limitations

The website should include a concise, visible limitations section rather than hiding limitations in the publication footer.

- Literature-curated mechanism genes are incomplete and biased toward well-studied biology.
- The benchmark evaluates transcriptional mechanism fidelity, not direct target engagement, protein activity, phenotypic rescue or clinical efficacy.
- CURE-based retrieval is an application-level validation, not a universal therapeutic endpoint.
- MFS rankings depend on metric definitions and aggregation choices.
- scFMs were evaluated as frozen representations rather than with fine-tuning or end-to-end adaptation.
- Dataset coverage is uneven across drugs, doses, times and cellular states.

### 3.10 Open Resources and Citation

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

## 4. Figure Asset Requirements

### 4.1 First Batch: Required for the Main Page

1. Figure 1, preferably as separate panels `a-d`
2. Figure 2 panels `a`, `c` and `f`
3. Figure 3 panels `d`, `e` and `f`
4. Figure 6 panels `a`, `d`, `e` and `f`

### 4.2 Second Batch: Full Results Coverage

1. Figure 4 panels `a`, `b` and `e`, plus the complete figure
2. Figure 5 panels `a`, `b` and `e`, plus the complete figure
3. Selected supplementary figures for an expandable analysis gallery, if needed

### 4.3 Preferred Formats

Format priority:

1. Separate-panel SVG or genuinely vector-based PDF
2. Original PPTX, AI, EPS, Figma or plotting source
3. Lossless PNG or TIFF, preferably 2x/3x web display resolution and at least 2,500-3,000 px wide per dense panel

Avoid screenshots, messaging-app-compressed images and JPEG exports.

The current Figure 1-6 PDFs each contain a single 300 dpi JPEG rather than fully vectorized plot elements. They are adequate for manuscript rendering, but dense labels can become blurred or unreadable after responsive webpage scaling. Separate panels are more important than simply increasing the resolution of the complete figure.

## 5. Responsive Figure Strategy

- Do not display dense full-page figures at normal article width and expect labels to remain readable.
- Use panel-level crops in the narrative.
- Keep statistical values and explanatory labels as HTML text wherever possible.
- Provide full figures through click-to-zoom or a lightbox.
- Use mobile-specific stacking for multi-panel comparisons.
- Export web assets as WebP or AVIF with PNG fallback after receiving the master files.
- Preserve scientific figure colors unless accessibility or contrast checks require small adjustments.

## 6. Required Project Information

Before implementation, confirm:

- Final author list and author order
- Affiliations and corresponding authors
- Paper status: manuscript, preprint, accepted or published
- Publication venue, date, DOI and/or arXiv identifier
- Paper PDF URL
- Code repository URL
- Dataset and benchmark download URL
- Citation / BibTeX
- License
- Contact email
- Preferred acknowledgement of HITSZ and MindFlow.AI
- Whether a public leaderboard will be included in the first release
