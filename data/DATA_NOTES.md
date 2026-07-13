# Data Cleaning & Panel Construction Notes

Documents every  key judgment call made while building the state-year panel, so the
reasoning survives after the code is forgotten.

## Data Sources

All four variables are pulled from the FRED API — no separate DOL scrape or
Census pull needed, since FRED hosts DOL- and Census-derived state series directly.

| Variable                | FRED series pattern           | Frequency | Native range |
| ----------------------- | ----------------------------- | --------- | ------------ |
| Unemployment rate       | `{STATE}UR`                 | Monthly   | 1976–       |
| State minimum wage      | `STTMINWG{STATE}`           | Annual    | 1968–       |
| Median household income | `MEHOINUS{STATE}A646N`      | Annual    | 1984–2024   |
| Poverty rate            | `PPAA{STATE}{FIPS}A156NCEN` | Annual    | 1989–2024   |

Poverty is the only series whose ID requires the state's 2-digit FIPS code
rather than just its abbreviation.

## State Coverage

50 states only — no DC, no territories. Chosen for consistency across all four
series, since DC/territory coverage is inconsistent across them.

## Minimum Wage — Effective Rate

The FRED `STTMINWG{STATE}` series reports each state's own statutory rate,
which can sit *below* the federal floor in a given year. Since federal law
makes the higher of the two binding, we compute: effective_min_wage = max(state rate, federal rate for that year)

**Missing state-year gaps** (states with no state minimum wage law for part or
all of the sample) are filled with the federal rate for that year — applied as
a general rule to any gap, not limited to a hardcoded list of "federal-only"
states. This correctly handles both states that never adopted a state minimum
wage and states that adopted one partway through the sample.

Federal minimum wage by year is hardcoded from FLSA history (1968: $1.60 →
2009–present: $7.25), verified against DOL's official rate history.

## Poverty — SAIPE Production Gaps

The Census SAIPE program did not produce state poverty estimates every year in
its early history. Estimates exist for 1989, then a gap, then 1993, then
continuously from 1995 onward. Missing years: **1990, 1991, 1992, 1994.**

This is a documented gap in Census production, not a flaw in the FRED pull —
no interpolation or imputation was used to fill it.

## Panel Window: 1995–2024

**Decision: start the panel at 1995, not 1989.**

Reasoning:

- 1990–92 and 1994 are already missing from poverty regardless (SAIPE gap).
- Keeping 1989 and 1993 in would mean two isolated, disconnected data points
  contributing little identifying power to a fixed-effects model, at the cost
  of an unbalanced panel and extra missing-year handling logic.
- 1995–2024 is fully continuous across all four variables — no gaps, no NaNs,
  no unbalanced-panel caveat needed.
- Both key natural-experiment windows are preserved: the federal minimum wage
  freeze at $5.15 (1997–2007) and the freeze at $7.25 (2009–2024), the two
  periods with the richest state-vs-federal divergence.

## Known Range Mismatch (resolved by panel window choice)

Native ranges differ across sources (unemployment monthly to present; min wage
1968–2026; income 1984–2024; poverty 1989–2024, gappy). The 1995–2024 panel
window resolves this by using the range common to all four after excluding the
SAIPE gap years.

## Poverty — Final Cleaning Decision

Confirmed the 4 missing years are 1990, 1991, 1992, 1994 (SAIPE production gap).
Dropped all records for 1989–1994 rather than keeping an unbalanced panel —
two isolated points (1989, 1993) weren't worth the added complexity. Final
poverty panel: 1995–2024, fully continuous, no nulls.

## Unemployment — Cleaning & Annualization

Source is monthly, seasonally adjusted (`{STATE}UR`). Verified structural
completeness before collapsing:

- 604 monthly observations per state (raw pull included partial 2025/2026 data)
- Every (year, month) has exactly 50 state observations — no missing states in
  any month
- Dropped 2025 and 2026 entirely — incomplete years outside the panel window
  anyway

**Annualization method: calendar-year mean of the 12 monthly values**, rounded
to 1 decimal place. Chosen over a single point-in-time value (e.g., December)
since unemployment is a continuously fluctuating rate best represented by a
full-year average, unlike minimum wage, which is a policy level meaningfully
set on a specific date.

Renamed `value` → `pct_unemployed`.
