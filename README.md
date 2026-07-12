
# Minimum Wage vs. Unemployment: A State-Level Panel Analysis

**Research question:** Do U.S. states that raise their minimum wage above the federal floor
experience measurably different outcomes in unemployment, poverty, and median household
income, once state and year fixed effects are controlled for?

Framed as a policy brief for a media-client audience, connecting the empirical evidence to
the active Warren–Murphy $17 federal minimum wage proposal.

## Summary of Findings

_[To be filled in once regressions are complete — one paragraph, plain language, real numbers.]_

## Data

All four variables are sourced from the [FRED API](https://fred.stlouisfed.org/docs/api/fred/):

| Variable                | Source series pattern         | Frequency | Available from |
| ----------------------- | ----------------------------- | --------- | -------------- |
| Unemployment rate       | `{STATE}UR`                 | Monthly   | 1976           |
| State minimum wage      | `STTMINWG{STATE}`           | Annual    | 1968           |
| Median household income | `MEHOINUS{STATE}A646N`      | Annual    | 1984           |
| Poverty rate            | `PPAA{STATE}{FIPS}A156NCEN` | Annual    | 1989           |

Panel window: **1989–[latest year]**, the range common to all four series.

## Method

Panel regression with state and year fixed effects (`linearmodels.PanelOLS`), clustered
standard errors by state. Three separate regressions — one per outcome (unemployment,
poverty, income) — same independent variable (minimum wage).

## Repo Structure

```
├── data/
│   ├── raw/            # untouched FRED pulls, one CSV per variable
│   └── processed/      # cleaned, merged state-year panel
├── src/
│   ├── style.py         # shared color palette + matplotlib theme
│   ├── fetch_fred.py     # Stage 1 — data acquisition
│   ├── clean_merge.py     # Stage 2–3 — annualize + merge into panel
│   └── regression.py       # Stage 5 — fixed-effects models
├── notebooks/
│   └── eda.ipynb           # Stage 4 — exploratory analysis
├── figures/                  # exported chart PNGs
└── output/
    └── Minimum_Wage_Policy_Brief.docx
```

## Reproducing

```bash
pip install -r requirements.txt
export FRED_API_KEY="your_key_here"
python src/fetch_fred.py
python src/clean_merge.py
python src/regression.py
```

## Limitations

See the Limitations section of the policy brief (`output/Minimum_Wage_Policy_Brief.docx`)
for a full discussion of what this analysis can and cannot conclude.
