# Minimum Wage vs. Unemployment: A State-Level Panel Analysis

**Research question:** Do U.S. states that raise their minimum wage above the federal floor
experience measurably different outcomes in unemployment, poverty, and median household
income, once state and year fixed effects are controlled for?

Framed as a policy brief for a media-client audience, connecting the empirical evidence to
the active Raise the Wage Act, which proposes a $17 federal minimum wage.

**Demonstrates:** panel data construction from a public API, handling real government data
gaps, causal inference methodology (fixed effects, clustered standard errors), and honest
reporting of null results for a non-technical audience.

![Minimum wage trajectories across six states, 1995-2024](figures/01_min_wage_trajectory.png)

![Same unemployment trend](figures/02_unemployment_overlay.png)

## Summary of Findings

Using panel regression with state and year fixed effects and clustered standard errors,
across 50 states and 30 years (1995-2024):

- **Unemployment:** no statistically significant relationship with minimum wage
  (coefficient: 0.036, p = 0.312).
- **Poverty rate:** no statistically significant relationship with minimum wage
  (coefficient: 0.025, p = 0.690).
- **Median household income:** a statistically significant positive relationship
  (coefficient: 1265.50, p = 0.0001; 95% CI: 635.53 to 1895.50), though this magnitude
  likely reflects broader wage growth correlated with minimum wage policy, not a purely
  mechanical pass-through, and should be read as associative rather than causal.

Full findings, framing, and limitations in `output/Minimum_Wage_Policy_Brief.pdf`, which
includes a References section citing all literature referenced above (Card & Krueger, NBER,
Peterson Institute, Upjohn Institute, and primary government sources).

## Data

All four variables are sourced from the [FRED API](https://fred.stlouisfed.org/docs/api/fred/):

| Variable                | Source series pattern         | Frequency | Native range |
| ----------------------- | ----------------------------- | --------- | ------------ |
| Unemployment rate       | `{STATE}UR`                 | Monthly   | 1976-present |
| State minimum wage      | `STTMINWG{STATE}`           | Annual    | 1968-present |
| Median household income | `MEHOINUS{STATE}A646N`      | Annual    | 1984-2024    |
| Poverty rate            | `PPAA{STATE}{FIPS}A156NCEN` | Annual    | 1989-2024    |

**Panel window: 1995-2024**, narrower than several series' native range. The Census SAIPE
program (poverty) has documented gaps in 1990-1992 and 1994, plus isolated, disconnected
estimates for 1989 and 1993. Rather than keep an unbalanced panel around those two isolated
points, the panel starts in 1995, where all four variables are fully continuous through 2024.
Full reasoning in `data/DATA_NOTES.md`.

Final panel: 50 states x 30 years = 1,500 state-year observations, no missing values, no
duplicate keys.

## Method

Panel regression with state and year fixed effects (`linearmodels.PanelOLS`), clustered
standard errors by state. Three separate regressions, one per outcome (unemployment,
poverty, income), same independent variable (effective minimum wage, defined as the higher
of the state and federal rate for that year).

## Repo Structure

```
|-- data/
|   |-- raw/                    # untouched FRED pulls, one CSV per variable
|   |-- processed/              # cleaned, merged state-year panel
|   `-- DATA_NOTES.md           # every cleaning/scoping decision, with reasoning
|-- src/
|   |-- fetch_fred.py           # Stage 1: data acquisition
|-- notebooks/
|   |-- 01__cleaning.ipynb      # Stage 2-3: clean, annualize, merge into panel
|   |-- 02_eda.ipynb            # Stage 4: exploratory analysis
|   `-- 03_modeling.ipynb       # Stage 5: fixed-effects regressions
|-- figures/                    # exported chart PNGs
`-- output/
    `-- Minimum_Wage_Policy_Brief.pdf
```

## Reproducing

```bash
pip install -r requirements.txt
export FRED_API_KEY="your_key_here"

python src/fetch_fred.py                 # Stage 1: pulls raw data into data/raw/
# then run, in order:
# notebooks/01__cleaning.ipynb           # Stage 2-3: outputs data/processed/state_panel_1995_2024.csv
# notebooks/02_eda.ipynb                 # Stage 4: outputs figures/*.png
# notebooks/03_modeling.ipynb            # Stage 5: fixed-effects regressions
```

## Limitations

See the Limitations section of the policy brief (`output/Minimum_Wage_Policy_Brief.pdf`)
for a full discussion of what this analysis can and cannot conclude.
