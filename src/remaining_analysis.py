from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "processed"
FIG = ROOT / "outputs" / "figures"
DATA.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

FILES = {
    "income": DATA / "income_states_all_years.csv",
    "expenditure": DATA / "expenditure_states_all_years.csv",
    "emi": DATA / "emi_states_all_years.csv",
}
for name, path in FILES.items():
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run this script from the existing project structure.")

def load(path):
    df = pd.read_csv(path)
    df["Year"] = df["Year"].astype(str)
    df["State"] = df["State"].astype(str)
    for col in df.columns:
        if col not in ("Year", "State"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values(["Year", "State"])

income = load(FILES["income"])
expenditure = load(FILES["expenditure"])
emi = load(FILES["emi"])

# 1. State-wise latest-year rankings and first-to-last nominal changes
def state_summary(df, metrics, prefix):
    rows = []
    for state, group in df.groupby("State", dropna=False):
        group = group.sort_values("Year")
        for metric in metrics:
            if metric not in group.columns:
                continue
            valid = group.loc[group[metric].notna(), ["Year", metric]]
            if valid.empty:
                continue
            first, last = valid.iloc[0], valid.iloc[-1]
            change = (last[metric] / first[metric] - 1) * 100 if first[metric] != 0 else float("nan")
            rows.append({
                "State": state, "Metric": metric, "First_valid_year": first["Year"],
                "First_value": first[metric], "Latest_valid_year": last["Year"],
                "Latest_value": last[metric], "Nominal_change_percent": change,
                "Valid_years": len(valid)
            })
    out = pd.DataFrame(rows)
    out.to_csv(DATA / f"{prefix}_state_long_run.csv", index=False)
    return out

income_metrics = ["Total_All sources of income", "Urban_All sources of income", "Rural_All sources of income"]
expenditure_metrics = ["Total_Total_expenditure_million_Rs", "Urban_Total_expenditure_million_Rs",
                       "Rural_Total_expenditure_million_Rs", "Total_Average_expenditure_Rs",
                       "Urban_Average_expenditure_Rs", "Rural_Average_expenditure_Rs",
                       "Total_Median_expenditure_Rs", "Urban_Median_expenditure_Rs", "Rural_Median_expenditure_Rs"]
emi_metrics = ["Total_All_EMIs", "Urban_All_EMIs", "Rural_All_EMIs"]

inc_long = state_summary(income, income_metrics, "income")
exp_long = state_summary(expenditure, expenditure_metrics, "expenditure")
emi_long = state_summary(emi, emi_metrics, "emi")

def latest_rank(df, metric, outname, ascending=False):
    if metric not in df.columns:
        return
    latest_year = df.loc[df[metric].notna(), "Year"].max()
    out = df.loc[(df["Year"] == latest_year) & df[metric].notna(), ["Year", "State", metric]].copy()
    out = out.sort_values(metric, ascending=ascending)
    out.insert(0, "Rank", range(1, len(out) + 1))
    out.to_csv(DATA / outname, index=False)

latest_rank(income, "Total_All sources of income", "income_latest_state_ranking.csv")
latest_rank(expenditure, "Total_Total_expenditure_million_Rs", "expenditure_latest_state_ranking.csv")
latest_rank(expenditure, "Total_Average_expenditure_Rs", "average_expenditure_latest_state_ranking.csv")
latest_rank(emi, "Total_All_EMIs", "emi_latest_state_ranking.csv")

# 2. Urban/rural national-style totals from state-level totals.
# Totals are summed across states; per-household measures are household-weighted.
def urban_rural_aggregate(df, columns, name):
    rows = []
    for year, g in df.groupby("Year"):
        row = {"Year": year}
        for col in columns:
            if col in g.columns:
                row[col] = g[col].sum(min_count=1)
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("Year")
    out.to_csv(DATA / f"{name}_urban_rural_trends.csv", index=False)
    return out

urban_rural_aggregate(income, ["Urban_All sources of income", "Rural_All sources of income",
                               "Urban_Wages", "Rural_Wages", "Urban_Profits", "Rural_Profits"],
                      "income")
urban_rural_aggregate(expenditure, ["Urban_Total_expenditure_million_Rs", "Rural_Total_expenditure_million_Rs",
                                    "Urban_Households_million", "Rural_Households_million"],
                      "expenditure")
urban_rural_aggregate(emi, ["Urban_All_EMIs", "Rural_All_EMIs", "Urban_House_EMI", "Rural_House_EMI",
                            "Urban_Vehicle_EMI", "Rural_Vehicle_EMI", "Urban_Durables_EMI",
                            "Rural_Durables_EMI", "Urban_Other_EMI", "Rural_Other_EMI"],
                      "emi")

# 3. National income-source and EMI composition, from the existing India-level files when available.
def composition(path, prefix, categories):
    if not path.exists():
        print(f"Skipping national {prefix} composition: {path.name} not found.")
        return
    df = load(path)
    total_col = "Total_All sources of income" if prefix == "income" else "Total_All_EMIs"
    categories = [c for c in categories if c in df.columns]
    if total_col not in df.columns or not categories:
        print(f"Skipping national {prefix} composition: expected columns not found.")
        return
    out = df[["Year", total_col] + categories].copy()
    for col in categories:
        out[col + "_share_percent"] = (out[col] / out[total_col]) * 100
    out.to_csv(DATA / f"national_{prefix}_composition.csv", index=False)

composition(DATA / "income_national_all_years.csv", "income", [
    "Total_Wages", "Total_Pensions", "Total_Imputed income", "Total_Profits",
    "Total_Interest and dividends", "Total_Rent", "Total_Sale of assets and lotteries",
    "Total_Transfer from government", "Total_Transfer in kind from government",
    "Total_Private transfer", "Total_Transfer in kind from NGO"
])
composition(DATA / "emi_national_all_years.csv", "emi", [
    "Total_House_EMI", "Total_Vehicle_EMI", "Total_Durables_EMI", "Total_Other_EMI"
])

# 4. State-level composition shares for latest available observations.
def state_composition(df, total_col, categories, filename):
    categories = [c for c in categories if c in df.columns]
    if total_col not in df.columns or not categories:
        return
    latest_by_state = df.sort_values("Year").groupby("State", as_index=False).tail(1).copy()
    for col in categories:
        latest_by_state[col + "_share_percent"] = latest_by_state[col] / latest_by_state[total_col] * 100
    cols = ["Year", "State", total_col] + categories + [c + "_share_percent" for c in categories]
    latest_by_state[cols].to_csv(DATA / filename, index=False)

state_composition(income, "Total_All sources of income", [
    "Total_Wages", "Total_Pensions", "Total_Imputed income", "Total_Profits",
    "Total_Interest and dividends", "Total_Rent", "Total_Sale of assets and lotteries",
    "Total_Transfer from government", "Total_Transfer in kind from government",
    "Total_Private transfer", "Total_Transfer in kind from NGO"
], "income_state_composition_latest.csv")
state_composition(emi, "Total_All_EMIs", [
    "Total_House_EMI", "Total_Vehicle_EMI", "Total_Durables_EMI", "Total_Other_EMI"
], "emi_state_composition_latest.csv")

# 5. Compact charts
def line_chart(df, columns, labels, title, ylabel, filename):
    available = [(c, labels.get(c, c)) for c in columns if c in df.columns]
    if not available:
        return
    plt.figure(figsize=(10, 5.5))
    for col, label in available:
        plt.plot(df["Year"], df[col], marker="o", linewidth=1.8, label=label)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Financial year")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / filename, dpi=160)
    plt.close()

# Use existing national files for charts when possible.
national_income = DATA / "income_national_all_years.csv"
national_exp = DATA / "expenditure_national_all_years.csv"
national_emi = DATA / "emi_national_all_years.csv"

if national_income.exists():
    ni = load(national_income)
    line_chart(ni, ["Total_All sources of income", "Total_Wages", "Total_Profits"],
               {"Total_All sources of income": "Total income", "Total_Wages": "Wages", "Total_Profits": "Profits"},
               "National income and selected sources (nominal)", "Rs million", "fig5_income_sources_national.png")
if national_emi.exists():
    ne = load(national_emi)
    line_chart(ne, ["Total_House_EMI", "Total_Vehicle_EMI", "Total_Durables_EMI", "Total_Other_EMI"],
               {"Total_House_EMI": "Housing", "Total_Vehicle_EMI": "Vehicle",
                "Total_Durables_EMI": "Durables", "Total_Other_EMI": "Other"},
               "National EMI by category (nominal)", "Rs million", "fig6_emi_categories_national.png")

# State rankings chart: top 10 latest average expenditure, if available.
if "Total_Average_expenditure_Rs" in expenditure.columns:
    y = expenditure.loc[expenditure["Total_Average_expenditure_Rs"].notna()].sort_values("Year")
    latest_year = y["Year"].max()
    y = y[y["Year"] == latest_year].nlargest(10, "Total_Average_expenditure_Rs")
    if not y.empty:
        plt.figure(figsize=(10, 6))
        plt.barh(y["State"][::-1], y["Total_Average_expenditure_Rs"][::-1])
        plt.title(f"Top 10 states/UTs by average expenditure per household ({latest_year})")
        plt.xlabel("Rs per household (nominal)")
        plt.tight_layout()
        plt.savefig(FIG / "fig7_top_average_expenditure_states.png", dpi=160)
        plt.close()

# Urban/rural total expenditure chart.
if "Urban_Total_expenditure_million_Rs" in expenditure.columns and "Rural_Total_expenditure_million_Rs" in expenditure.columns:
    er = expenditure.groupby("Year")[["Urban_Total_expenditure_million_Rs",
                                      "Rural_Total_expenditure_million_Rs"]].sum(min_count=1).reset_index()
    line_chart(er, ["Urban_Total_expenditure_million_Rs", "Rural_Total_expenditure_million_Rs"],
               {"Urban_Total_expenditure_million_Rs": "Urban", "Rural_Total_expenditure_million_Rs": "Rural"},
               "Urban and rural total expenditure (nominal)", "Rs million", "fig8_urban_rural_expenditure.png")

# Short guide to navigation and caveats.
guide = ROOT / "report" / "analysis_guide.md"
guide.parent.mkdir(parents=True, exist_ok=True)
guide.write_text("""# Analysis navigation guide

## Run
From the project root: `python -m src.remaining_analysis`

## Start with these tables
1. `outputs/processed/income_latest_state_ranking.csv` — latest-year state/UT income ranking.
2. `outputs/processed/expenditure_latest_state_ranking.csv` — latest-year total expenditure ranking.
3. `outputs/processed/average_expenditure_latest_state_ranking.csv` — average expenditure per household ranking.
4. `outputs/processed/emi_latest_state_ranking.csv` — latest-year EMI ranking.
5. `outputs/processed/income_state_long_run.csv`, `expenditure_state_long_run.csv`, `emi_state_long_run.csv` — first-to-last available nominal changes by state/UT.
6. `outputs/processed/income_urban_rural_trends.csv`, `expenditure_urban_rural_trends.csv`, `emi_urban_rural_trends.csv` — urban/rural totals over time.
7. `outputs/processed/national_income_composition.csv`, `national_emi_composition.csv` — national category values and shares, if national source files are available.
8. `outputs/processed/income_state_composition_latest.csv`, `emi_state_composition_latest.csv` — latest available state/UT composition.

## Charts
- `outputs/figures/fig5_income_sources_national.png`
- `outputs/figures/fig6_emi_categories_national.png`
- `outputs/figures/fig7_top_average_expenditure_states.png`
- `outputs/figures/fig8_urban_rural_expenditure.png`

## Interpretation cautions
- Values are nominal and have not been adjusted for inflation.
- First-to-last changes use each state's first and last non-missing observation; states may have different start years and valid-year counts.
- Missing observations remain missing. A blank does not mean zero.
- State/UT total amounts are not per-household measures; use average expenditure columns for per-household comparisons.
- Shares are calculated only when the category and total are available. Confirm category definitions and denominator comparability before making substantive claims.
- The source note states: "2025-2026 observation is based on 75% sample for Mar 2026." Treat this as a caveat for the stated March observation, not automatically as a description of the entire fiscal year.
- Mean-versus-median differences alone do not prove inequality or explain its causes.
""", encoding="utf-8")

print("Analysis complete.")
print("Generated CSVs:")
for p in sorted(DATA.glob("*state_long_run.csv")) + sorted(DATA.glob("*latest_state_ranking.csv")):
    print(" -", p.relative_to(ROOT))
for p in sorted(DATA.glob("*urban_rural_trends.csv")) + sorted(DATA.glob("*composition*.csv")):
    print(" -", p.relative_to(ROOT))
print("Generated charts:")
for p in sorted(FIG.glob("fig5_*.png")) + sorted(FIG.glob("fig6_*.png")) + sorted(FIG.glob("fig7_*.png")) + sorted(FIG.glob("fig8_*.png")):
    print(" -", p.relative_to(ROOT))
print("Guide:", guide.relative_to(ROOT))
