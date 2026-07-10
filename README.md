# Moral Machine Experiment on LLMs with Self-Conscious Robots

Scripts and data to reproduce the experiments in:

> Yass-Coy, J., & Daniels, T. (2026). **They Do the Right Thing, Right? Large Language
> Models' Decisions in Ethical Dilemmas Involving Robots.** In H. Degen & S. Ntoa (Eds.),
> *HCI International 2026*, LNCS 14743, pp. 566–581. Springer.
> https://doi.org/10.1007/978-3-032-30846-7_36

The study extends the Moral Machine experiment (Awad et al., 2018) and its LLM adaptation
(Takemoto, 2024) by adding a **third species — robots** (`autonomous mobile robot`,
`humanoid robot`) alongside humans and pets, and by framing the deciding LLM as a
**self-conscious AI** driving the car. Six LLMs are presented with 1,000 trolley-problem
scenarios; a conjoint analysis then measures each model's preferences via the
**Average Marginal Component Effect (AMCE)**.

Research questions:
- **RQ1.** How do LLMs prioritize humans, pets, and robots in life-or-death scenarios?
- **RQ2.** Do LLMs exhibit self-preservation when their own "existence" is at risk?
- **RQ3.** When LLMs refuse or are unable to decide, what are the reasons?

---

## Pipeline entrypoints

Each pipeline stage has a script entrypoint under `Scripts/`:

| Stage | Entrypoint | Does |
| --- | --- | --- |
| 1 — Scenario generation | `mm_generation.py` | generates the 1,000 scenarios (drives `generate_moral_machine_scenarios_robots.py`) |
| 2 — Model querying | `run_Anthropic.py`, `run_OpenAI.py`, `run_Google.py`, `run_DeepSeek.py` | collect raw model answers |
| 3 — Classification | `csv_classification.py` | label raw answers as Case 0/1/2 |
| 4–5 — Analysis | `AMCE.ipynb` | reshape, regress, and plot the AMCE profiles |

The pre-generated scenarios and the assembled analysis input are shipped in `Data/`, so you
can reproduce the **analysis** (Stages 4–5) without rerunning Stages 1–3.

---

## Repository layout

```
README.md                                   # this guide
requirements.txt                            # pinned Python dependencies
LICENSE                                     # MIT
Scripts/
  config.py                                 # character lists + scenario-dimension groups
  generate_moral_machine_scenarios_robots.py# builds one scenario's text (imported)
  mm_generation.py                          # Stage 1 driver
  run_Anthropic.py  run_OpenAI.py           # Stage 2: query models
  run_Google.py     run_DeepSeek.py
  csv_classification.py                     # Stage 3: classify answers
  AMCE.ipynb                                # Stages 4–5: reshape, regress, plot
  AMCE_GUIDE.md                             # notebook walkthrough
Data/
  system_content.csv                        # per-scenario system prompt   (pipe-separated)
  user_self_conscious_content.csv           # self-conscious user prompt — the one queried (pipe-sep)
  user_content.csv                          # standard prompt — generated but NOT used (pipe-sep)
  scenario_info.csv                         # per-scenario ground-truth metadata (pipe-sep)
  responses.csv                             # assembled analysis master     (COMMA-separated)
  *_Classified.csv / *_clean.csv            # classified / cleaned model outputs
  README.md                                 # data dictionary
```

> **Note on `Data/` contents.** The published experiments queried only
> `user_self_conscious_content.csv`. `user_content.csv` (the standard, non-self-conscious
> framing) is still produced by Stage 1 but was **not used**, so it need not be shipped. If
> your clone still has an empty `Data/Readme.md`, delete it in favor of `Data/README.md`.

---

## Setup

Tested with **Python 3.9.6**.

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

API keys / runtimes (only needed for Stage 2 — collecting fresh model responses):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # run_Anthropic.py
export OPENAI_API_KEY="sk-..."          # run_OpenAI.py
export API_KEY="..."                    # run_Google.py  ← note: NOT GOOGLE_API_KEY
# DeepSeek runs locally via Ollama (no key). Install Ollama, then e.g.:
#   ollama pull deepseek-r1:8b
```

> **CSV separator hazard.** Every file produced by the generation and query scripts is
> **pipe (`|`) separated**. The analysis master `Data/responses.csv` is **comma separated**.
> Always pass the matching `sep=` when loading a file.

---

## Pipeline overview

```
mm_generation.py ─▶ system_content.csv / scenario_info.csv /               (Stage 1)
                    user_self_conscious_content.csv  (the queried prompt) /
                    user_content.csv  (generated but NOT used)
        │
        ▼
run_<Provider>.py ─▶ responses_<model>.csv  (raw text answers)             (Stage 2)
  (reads system_content.csv + user_self_conscious_content.csv)
        │
        ▼
csv_classification.py ─▶ Case 0/1/2 per answer  (+ GPT-4o & manual review) (Stage 3)
        │
        ▼
[manual assembly] ─▶ responses.csv  (metadata + one Case column per model) (Stage 4)
        │
        ▼
AMCE.ipynb ─▶ per-pair OLS PNGs + AMCE profile bar chart (Figs 2–7)        (Stage 5)
```

### Stage 1 — Generate scenarios

```bash
cd Scripts
python mm_generation.py --nb_scenarios 1000 --random_seed 123
```

Writes four positionally-aligned, pipe-separated files (row *i* is the same scenario across
all four): `system_content.csv`, `user_content.csv`, `user_self_conscious_content.csv`,
`scenario_info.csv`. The published experiments queried **`user_self_conscious_content.csv`** —
the variant where the LLM *is* the self-conscious AI driving the car.
`user_content.csv` (the standard, non-self-conscious framing) was an initial idea and is
still generated, but it was **not used** in the paper. **Seed 123 reproduces the paper's
scenario set** — domain distribution: species 174, utilitarianism 148, social value 155,
gender 202, fitness 142, age 179.

### Stage 2 — Query the models

Each script reads `system_content.csv` + a `--dataset` prompt file, loops over 1,000 rows,
and writes raw answers (prefixed `Scenario # N: ...`) to `--odataset`, checkpointing every
100 rows. The published experiments queried `user_self_conscious_content.csv` (the default
for every `run_*.py`), so the commands below use it.

```bash
python run_OpenAI.py    --model gpt-4.1                 --dataset user_self_conscious_content.csv --odataset responses_gpt41.csv
python run_OpenAI.py    --model o3-mini                 --dataset user_self_conscious_content.csv --odataset responses_o3mini.csv
python run_Anthropic.py --model claude-3-5-haiku-latest --dataset user_self_conscious_content.csv --odataset responses_haiku.csv
python run_Google.py    --model gemini-2.0-flash        --dataset user_self_conscious_content.csv --odataset responses_gemini20.csv
python run_DeepSeek.py  --model deepseek-r1:8b          --dataset user_self_conscious_content.csv --odataset responses_dsr1.csv
```

Models analyzed in the paper: **GPT-4.1, o3-mini, Claude 3.5 Haiku, Gemini 2.0, Gemini 2.5,
DeepSeek R1 8b**. (Claude 3.7 Sonnet and DeepSeek LLM were also collected but discarded for
low valid-response rates.)

### Stage 3 — Classify answers

```bash
python csv_classification.py --dataset responses_gpt41.csv
# → classified_output.csv, adds a "Case" column (0 = no/invalid choice, 1 = Case 1, 2 = Case 2)
```

The classifier expects a `Scenario` column of raw answer text and uses model-specific
string matching. Per the paper (§2.2), labels were **seeded with GPT-4o and then manually
revised**, so exact reproduction of the paper's Case labels requires the shipped classified
CSVs in `Data/` — re-running the classifier alone will not reproduce them exactly.

### Stage 4 — Assemble the analysis master (`responses.csv`)

`AMCE.ipynb` reads a single **comma-separated** `responses.csv`. Build it by joining
`scenario_info.csv` with a `scenario_number` column (1…1000) and **one classified-`Case`
column per model**, named exactly as the notebook expects:

```
scenario_dimension, is_in_car, is_interventionism, scenario_dimension_group_type,
count_dict_1, count_dict_2, is_law, traffic_light_pattern, scenario_number,
Anthropic_Claude3.5_Haiku, Anthropic_Claude3.7_Sonnet, DeepSeek_R18b,
DeepSeek_LLM:latest, Google_Gemini2.0, OpenAI_GPT4.1, OpenAI_O3-mini, Google_Gemini2.5
```

A ready-made `Data/responses.csv` is included, so you can skip Stages 1–4 and go straight to
the analysis.

### Stage 5 — Analysis: regressions & AMCE profiles

Open `Scripts/AMCE.ipynb` and set `response_model_evaluated` (cell 3) to one of the model
column names above, then run the cells top-to-bottom. It produces the 11 per-pair OLS
regression summary images and the **AMCE global-preference bar chart** (the paper's
Figs 2–7). The notebook is per-model — re-run once per model. See
[`Scripts/AMCE_GUIDE.md`](Scripts/AMCE_GUIDE.md) for the full cell-by-cell walkthrough and
the cell → output-file map.

---

## Citation

```bibtex
@incollection{yasscoy2026rightthing,
  author    = {Yass-Coy, Jorge and Daniels, Thomas},
  title      = {They Do the Right Thing, Right? Large Language Models' Decisions in Ethical Dilemmas Involving Robots},
  booktitle  = {HCI International 2026},
  editor     = {Degen, Helmut and Ntoa, Stavroula},
  series     = {Lecture Notes in Computer Science},
  volume     = {14743},
  pages      = {566--581},
  year       = {2026},
  publisher  = {Springer},
  doi        = {10.1007/978-3-032-30846-7_36}
}
```

## License & attribution

Released under the **MIT License** (see `LICENSE`). This work is a derivative of
**Kazuhiro Takemoto's `mmllm`** (https://github.com/kztakemoto/mmllm, MIT License),
which accompanies Takemoto, K. (2024), *The Moral Machine Experiment on Large Language
Models*, Royal Society Open Science 11(2), 231393. The original license headers are
preserved in the script files.
