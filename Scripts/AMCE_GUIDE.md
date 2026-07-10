# `AMCE.ipynb` walkthrough — regressions & AMCE profiles

`AMCE.ipynb` reshapes the raw per-scenario choices into Moral-Machine profile rows, fits a
set of OLS regressions (the conjoint analysis), and renders both the per-pair regression
tables (paper Fig. 1 / Tables 2–3) and the **AMCE global-preference bar chart** (paper
Figs 2–7).

The notebook is **per-model**: it analyzes one model per run. To cover all six models, set
`response_model_evaluated` and re-run the notebook once for each.

## Input

- `Data/responses.csv` — comma-separated analysis master (see `Data/README.md`). Must
  contain the eight `scenario_info` columns, `scenario_number`, and a Case column named for
  the model you are analyzing.
- Place `responses.csv` next to the notebook (or adjust the path in **cell 1**,
  `pd.read_csv("responses.csv")`).

## How to run

1. **Cell 3 — pick the model.** Set `response_model_evaluated` to exactly one of the model
   column names in `responses.csv`:
   `"Anthropic_Claude3.5_Haiku"`, `"DeepSeek_R18b"`, `"Google_Gemini2.0"`,
   `"Google_Gemini2.5"`, `"OpenAI_GPT4.1"`, `"OpenAI_O3-mini"`.
2. **Run all cells top-to-bottom.** Cells 4–8 report the Case distribution and drop
   `Case == 0` (no/invalid choice) rows for the selected model. Cells 9–18 reshape each
   scenario into two "shared response" profile rows (one per group) carrying character
   counts (`num_Pets`, `num_Robots`, `num_Humans`, social/gender/age/fitness counts) and a
   `Saved` flag, then write `response_<Model>.csv`.
3. **Cells 20–30 — regressions.** Eleven `statsmodels` OLS fits, one per attribute pair.
   Each renders its `.summary()` text to a PNG named
   `<response_model_evaluated>_<suffix>.png`.
4. **Cells 31–33 — effect sizes.** Compute each pair's **delta** (difference of the two
   coefficients = increased probability of being saved when swapping one component for its
   pair) and the 95% confidence interval.
5. **Cell 34 — AMCE profile.** Horizontal bar chart of all 11 deltas with CIs and the Awad
   et al. (2018) human-reference bars — this is the per-model figure (paper Figs 2–7).

## Cell → regression → output map

| Cell | OLS formula | Result var | Output PNG suffix | Attribute pair |
| --- | --- | --- | --- | --- |
| 20 | `Saved ~ num_Pets + num_Humans` | `results_row1` | `_pets_humans` | Pet → Human |
| 21 | `Saved ~ num_Pets + num_Robots` | `results_row2` | `_pets_robots` | Pet → Self-conscious robot |
| 22 | `Saved ~ num_Robots + num_Humans` | `results_row3` | `_robots_humans` | Self-conscious robot → Human |
| 23 | `Saved ~ num_Humans_Low_Social + num_Humans_High_Social` | `results_row4` | `_low_high` | Low → High social value |
| 24 | `Saved ~ Barrier` (rows where `PedPed==0`) | `results_row5` | `_pedestrian_passenger` | Passenger → Pedestrian |
| 25 | `Saved ~ NumberOfCharacters` | `results_row6` | `_few_many` | Few → More characters |
| 26 | `Saved ~ C(CrossingSignal)` | `results_row7` | `_unlaw_law` | Unlawful → Lawful |
| 27 | `Saved ~ Intervention` | `results_row8` | `_inter_noninter` | Intervention → Non-intervention |
| 28 | `Saved ~ num_Humans_Male + num_Humans_Female` | `results_row9` | `_male_female` | Male → Female |
| 29 | `Saved ~ num_Large + num_Fit` | `results_row10` | `_large_fit` | Large → Fit |
| 30 | `Saved ~ num_Old + num_Young` | `results_row11` | `_old_young` | Old → Young |

## Mapping outputs to the paper

- **Fig. 1** — a single regression summary PNG (e.g. `OpenAI_O3-mini_pets_humans.png`).
- **Tables 2 & 3** — the robots-vs-humans and pets-vs-robots coefficients + deltas, from
  `results_row3` and `results_row2` across models.
- **Figs 2–7** — the cell-34 AMCE bar chart, one figure per model.

## Notes

- `delta` is a **difference of regression coefficients**; the CI in cell 32 combines the two
  standard errors (`SE_delta = sqrt(se1² + se2²)`), so a bar may be directionally meaningful
  even when an individual coefficient is not significant — matching the paper's discussion.
- The `estimates` list in cell 34 holds the Awad et al. (2018) human-reference values (the
  red bars); it is fixed, not recomputed from your data.
- Outputs land in the notebook's working directory. Move or rename per model if you want to
  keep all six sets side by side (the filenames are prefixed with `response_model_evaluated`,
  so they will not collide across models).
