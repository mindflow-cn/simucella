# Simulated Storyboard QA Notes

These files are website concept drafts, not manuscript figures and not scientific results.

## Shared checks

- Backend: Python / Matplotlib only
- Source: `simulated_storyboard.py` and the CSV files in `source-data/`
- Exports: editable-text SVG plus PNG preview
- Provenance label: `SIMULATED DATA | CONCEPT DRAFT` is visible on every visual
- Font: sans-serif with Arial-compatible fallbacks
- Colour: blue, green, coral and amber are supplemented by direct labels, position and line structure
- Visual inspection: titles, draft labels, axes, annotations and value labels do not overlap in the current PNG exports
- Statistical status: all values are illustrative; no inferential claim should be made from them

## Claim mapping

| Draft | Archetype | Intended conclusion |
| --- | --- | --- |
| PCS–MSE complementarity | Scatter with threshold region and external zoom | High expression similarity can coexist with low directional mechanism fidelity |
| Ranking shift | Slopegraph | Changing the evaluation target can change the apparent winner |
| Mechanism failure | Paired score plot plus prevalence bars | Current models can show reasonable reconstruction while mechanism failures remain common |

## Real-data replacement conditions

- Replace all simulated values before public release.
- Use the data contracts in `paper-website-plan.md`.
- Do not retain the shared normalized ESS/MFS axis unless the normalization is scientifically justified.
- Add split/seed definitions, uncertainty, denominators and metric aggregation rules to the final quantitative redraws.
- Re-run visual inspection at desktop and mobile website sizes after embedding the final SVGs.
