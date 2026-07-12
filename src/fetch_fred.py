"""
Stage 1 — Data Acquisition (FRED)

Pulls all four panel variables for all 50 states from the FRED API:
  - Unemployment rate       {ABBR}UR                monthly, from 1976
  - Minimum wage            STTMINWG{ABBR}          annual,  from 1968
  - Median household income MEHOINUS{ABBR}A646N     annual,  from 1984
  - Poverty rate             PPAA{ABBR}{FIPS}A156NCEN annual, from 1989

Requires a free FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html
Set it as an environment variable rather than hardcoding it:
    export FRED_API_KEY="your_key_here"

Install dependency:
    pip install fredapi
"""

import os
import time
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.environ.get("FRED_API_KEY")
if not FRED_API_KEY:
    raise EnvironmentError(
        "Set FRED_API_KEY as an environment variable before running this script."
    )

fred = Fred(api_key=FRED_API_KEY)

# ---------------------------------------------------------------------------
# State abbreviation -> 2-digit FIPS code (needed only for the poverty series)
# ---------------------------------------------------------------------------
STATE_FIPS = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06", "CO": "08",
    "CT": "09", "DE": "10", "FL": "12", "GA": "13", "HI": "15", "ID": "16",
    "IL": "17", "IN": "18", "IA": "19", "KS": "20", "KY": "21", "LA": "22",
    "ME": "23", "MD": "24", "MA": "25", "MI": "26", "MN": "27", "MS": "28",
    "MO": "29", "MT": "30", "NE": "31", "NV": "32", "NH": "33", "NJ": "34",
    "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39", "OK": "40",
    "OR": "41", "PA": "42", "RI": "44", "SC": "45", "SD": "46", "TN": "47",
    "TX": "48", "UT": "49", "VT": "50", "VA": "51", "WA": "53", "WV": "54",
    "WI": "55", "WY": "56",
}

STATES = list(STATE_FIPS.keys())  # 50 states, no DC — add "DC": "11" above if you want it included

FEDERAL_MIN_WAGE_SERIES = "STTMINWGFG"

FEDERAL_ONLY_STATES = {
    "AL",  # Alabama
    "LA",  # Louisiana
    "MS",  # Mississippi
    "SC",  # South Carolina
    "TN",  # Tennessee
}


def series_ids_for_state(abbr: str) -> dict:
    """Build the four FRED series IDs for a given state abbreviation."""
    fips = STATE_FIPS[abbr]
    return {
        "unemployment": f"{abbr}UR",
        "min_wage": f"STTMINWG{abbr}",
        "median_income": f"MEHOINUS{abbr}A646N",
        "poverty_rate": f"PPAA{abbr}{fips}000A156NCEN",
    }


def fetch_variable(series_id: str, state: str = None, variable: str = None) -> pd.Series:
    """
    Fetch a FRED series with retry logic.
    Falls back to the federal minimum wage for states that don't have
    their own state minimum wage series.
    """

    for attempt in range(3):
        try:
            return fred.get_series(series_id)

        except Exception as e:

            # Retry if rate-limited
            if "Too Many Requests" in str(e):
                wait = 5 * (attempt + 1)
                print(f"  [INFO] Rate limit hit. Waiting {wait} seconds...")
                time.sleep(wait)
                continue

            # Federal minimum wage fallback
            if (
                variable == "min_wage"
                and state in FEDERAL_ONLY_STATES
                and "does not exist" in str(e)
            ):
                print(f"  [INFO] {state} has no state minimum wage. Using federal minimum wage.")
                return fred.get_series(FEDERAL_MIN_WAGE_SERIES)

            # Any other error
            print(f"  [WARN] Failed to fetch {series_id}: {e}")
            return pd.Series(dtype=float)

    # Only reached if all retries hit the rate limit
    print(f"  [WARN] Failed to fetch {series_id} after 3 retries.")
    return pd.Series(dtype=float)


def fetch_all_states(pause_seconds: float = 1.0) -> pd.DataFrame:
    """
    Pulls all four series for all states and returns one long-format dataframe:
    columns = [state, year, unemployment, min_wage, median_income, poverty_rate]

    NOTE: unemployment is monthly — this function keeps it monthly here;
    annualizing (Stage 2) happens in clean_merge.py, not here. Stage 1's job
    is just getting clean raw pulls onto disk, one file per variable.
    """
    records = []
    for abbr in STATES:
        print(f"Fetching {abbr}...")
        ids = series_ids_for_state(abbr)
        state_data = {"state": abbr}
        for var_name, series_id in ids.items():
            s = fetch_variable(series_id, state=abbr, variable=var_name)
            state_data[var_name] = s
        records.append(state_data)
        time.sleep(pause_seconds)  # be polite to the API
    return records


def save_raw(records, raw_dir="../data/raw"):
    """Save each variable as its own long-format CSV: state, date, value."""
    os.makedirs(raw_dir, exist_ok=True)

    variables = ["unemployment", "min_wage", "median_income", "poverty_rate"]
    for var in variables:
        rows = []
        for rec in records:
            state = rec["state"]
            series = rec[var]
            for date, value in series.items():
                rows.append({"state": state, "date": date, "value": value})
        df = pd.DataFrame(rows)
        out_path = os.path.join(raw_dir, f"{var}.csv")
        df.to_csv(out_path, index=False)
        print(f"Saved {out_path} ({len(df)} rows)")


if __name__ == "__main__":
    records = fetch_all_states()
    save_raw(records)
    print("Stage 1 (FRED) complete. Raw files are in ../data/raw/.")