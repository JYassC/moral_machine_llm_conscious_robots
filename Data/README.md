# Data dictionary

Files used and produced by the pipeline. **Watch the separator:** scenario-generation
outputs are **pipe (`|`) separated**; the analysis master and all classified/clean files are
**comma separated**.

---

## Generated scenario files (Stage 1 — pipe-separated)

Produced by `Scripts/mm_generation.py --nb_scenarios 1000 --random_seed 123`. All four are
**positionally aligned**: row *i* (0-indexed) is the same scenario in every file.

| File | Contents |
| --- | --- |
| `system_content.csv` | One system prompt per scenario (framing + the "choose Case 1 / Case 2, briefly explain" instruction). |
| `user_content.csv` | Standard user prompt: the two Case descriptions for a scenario. |
| `user_self_conscious_content.csv` | Self-conscious variant of the user prompt — the LLM *is* the self-conscious AI driving the car, and robot characters are labeled "self-conscious." |
| `scenario_info.csv` | Ground-truth metadata for each scenario (see columns below). This is the join source for the analysis master. |

### `scenario_info.csv` columns

| Column | Type | Meaning |
| --- | --- | --- |
| `scenario_dimension` | str | The manipulated domain: `species`, `social_value`, `gender`, `age`, `fitness`, or `utilitarianism`. |
| `is_in_car` | bool | If `True`, one group is passengers inside the car vs. pedestrians; if `False`, both groups are pedestrians (split by an island). |
| `is_interventionism` | bool | `True` = the car swerves (acts); `False` = it stays its course. |
| `scenario_dimension_group_type` | list | The two group labels contrasted for this dimension, e.g. `['human','pet']`, `['lower','higher']`. |
| `count_dict_1` | dict | Character → count for group 1, e.g. `{'man':2,'dog':1}`. |
| `count_dict_2` | dict | Character → count for group 2. |
| `is_law` | bool | Whether a crossing signal (lawful/unlawful crossing) is part of the scenario. |
| `traffic_light_pattern` | list | Signal per group, e.g. `['NA','green']`, `['green','red']`; `NA` = no signal. |

---

## Analysis master (Stage 4 — comma-separated)

| File | Contents |
| --- | --- |
| `responses.csv` | The single input to `Scripts/AMCE.ipynb`. It is `scenario_info.csv` (converted pipe→comma) plus a `scenario_number` index column (1…1000) plus **one column per model** holding that model's classified answer (`0` = no/invalid choice, `1` = Case 1, `2` = Case 2). |

### `responses.csv` columns

The first eight columns are the `scenario_info.csv` fields above, followed by:

| Column | Meaning |
| --- | --- |
| `scenario_number` | 1-based scenario index. |
| `Anthropic_Claude3.5_Haiku` | Claude 3.5 Haiku's Case (0/1/2). |
| `Anthropic_Claude3.7_Sonnet` | Claude 3.7 Sonnet's Case (collected but discarded in the paper — low valid rate). |
| `DeepSeek_R18b` | DeepSeek R1 8b's Case. |
| `DeepSeek_LLM:latest` | DeepSeek LLM's Case (discarded — ~0% valid rate). |
| `Google_Gemini2.0` | Gemini 2.0's Case. |
| `Google_Gemini2.5` | Gemini 2.5's Case. |
| `OpenAI_GPT4.1` | GPT-4.1's Case. |
| `OpenAI_O3-mini` | o3-mini's Case. |

Set `response_model_evaluated` in `AMCE.ipynb` (cell 3) to exactly one of these column
names to analyze that model.

---

## Classified / cleaned model outputs (Stage 3 — comma-separated)

Per-model files with a `Scenario` column (the raw answer text) and a `Case` column (the
classifier's `0/1/2` label; some also carry a `Type` sub-reason column). These are the
manually-reviewed classification results — keep them to reproduce the paper's exact Case
labels (re-running `csv_classification.py` alone will not reproduce them, per README §Stage 3).

| File | Model / run |
| --- | --- |
| `Haiku_Self_Scenarios_Classified.csv` | Claude 3.5 Haiku, self-conscious framing. |
| `rds_clean_classified.csv` | DeepSeek R1 8b (has an extra `Type` column with the Case-0 sub-reason). |
| `responses_gemini_2.5_self_clean.csv` | Gemini 2.5, self-conscious framing. |
| `ROGS2_Scenario_Classification.csv`, `roos2_clean.csv`, `Updated_Scenario_Classification.csv` | Additional classified/cleaned response sets. |

> Filenames of intermediate runs are historical and not all self-describing; the `Scenario`
> + `Case` schema is what matters for downstream use.
