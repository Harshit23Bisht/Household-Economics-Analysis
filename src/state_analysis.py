"""
Chunk 3: State-Wise and Urban/Rural Analysis
Generates state summaries, rankings, long-run growth, and urban/rural disparities.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_state_analysis():
    root = Path.cwd()
    proc_dir = root / "outputs" / "processed"
    fig_dir = root / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    inc = pd.read_csv(proc_dir / "income_states_all_years.csv")
    exp = pd.read_csv(proc_dir / "expenditure_states_all_years.csv")
    emi = pd.read_csv(proc_dir / "emi_states_all_years.csv")

    # Merge on Year and State
    df = inc.merge(exp, on=["Year", "State"]).merge(emi, on=["Year", "State"])

    # 1. State-Level Core Summary
    summary = pd.DataFrame({
        "Year": df["Year"],
        "State": df["State"],
        "Total_Income_Rs_Million": df["Total_All sources of income"],
        "Total_Expenditure_Rs_Million": df["Total_Total_expenditure_million_Rs"],
        "Total_EMI_Rs_Million": df["Total_All_EMIs"],
        "Average_Expenditure_Rs": df["Total_Average_expenditure_Rs"],
        "Median_Expenditure_Rs": df["Total_Median_expenditure_Rs"],
        "Households_Million": df["Total_Households_million"],
        "Urban_Income_Rs_Million": df["Urban_All sources of income"],
        "Rural_Income_Rs_Million": df["Rural_All sources of income"],
        "Urban_Expenditure_Rs_Million": df["Urban_Total_expenditure_million_Rs"],
        "Rural_Expenditure_Rs_Million": df["Rural_Total_expenditure_million_Rs"],
        "Urban_EMI_Rs_Million": df["Urban_All_EMIs"],
        "Rural_EMI_Rs_Million": df["Rural_All_EMIs"],
        "Urban_Avg_Exp_Rs": df["Urban_Average_expenditure_Rs"],
        "Rural_Avg_Exp_Rs": df["Rural_Average_expenditure_Rs"]
    })

    # Economic ratios
    summary["Expenditure_to_Income_Pct"] = (summary["Total_Expenditure_Rs_Million"] / summary["Total_Income_Rs_Million"]) * 100
    summary["EMI_to_Income_Pct"] = (summary["Total_EMI_Rs_Million"] / summary["Total_Income_Rs_Million"]) * 100
    summary["Urban_to_Rural_Avg_Exp_Ratio"] = summary["Urban_Avg_Exp_Rs"] / summary["Rural_Avg_Exp_Rs"]

    summary.to_csv(proc_dir / "state_timeseries_summary.csv", index=False)

    # 2. State Rankings for Latest Year (2025-26)
    df_2025 = summary[summary["Year"] == "2025-26"].copy()
    rankings = df_2025[[
        "State", "Total_Income_Rs_Million", "Total_Expenditure_Rs_Million", "Total_EMI_Rs_Million",
        "Average_Expenditure_Rs", "Median_Expenditure_Rs", "EMI_to_Income_Pct", "Expenditure_to_Income_Pct"
    ]].copy()

    rankings["Income_Rank"] = rankings["Total_Income_Rs_Million"].rank(ascending=False, method="min")
    rankings["Expenditure_Rank"] = rankings["Total_Expenditure_Rs_Million"].rank(ascending=False, method="min")
    rankings["Avg_Exp_Rank"] = rankings["Average_Expenditure_Rs"].rank(ascending=False, method="min")
    rankings["EMI_to_Income_Rank"] = rankings["EMI_to_Income_Pct"].rank(ascending=False, method="min")
    rankings = rankings.sort_values("Total_Income_Rs_Million", ascending=False).reset_index(drop=True)
    rankings.to_csv(proc_dir / "state_rankings_2025_26.csv", index=False)

    # 3. Long-run Nominal Growth (earliest available year to 2025-26)
    states = summary["State"].unique()
    growth_records = []
    for st in states:
        st_df = summary[summary["State"] == st].dropna(subset=["Total_Income_Rs_Million"]).sort_values("Year")
        if len(st_df) >= 2:
            base_row = st_df.iloc[0]
            latest_row = st_df.iloc[-1]
            base_yr = base_row["Year"]
            latest_yr = latest_row["Year"]

            inc_growth = ((latest_row["Total_Income_Rs_Million"] - base_row["Total_Income_Rs_Million"]) / base_row["Total_Income_Rs_Million"]) * 100
            exp_growth = ((latest_row["Total_Expenditure_Rs_Million"] - base_row["Total_Expenditure_Rs_Million"]) / base_row["Total_Expenditure_Rs_Million"]) * 100
            emi_growth = ((latest_row["Total_EMI_Rs_Million"] - base_row["Total_EMI_Rs_Million"]) / base_row["Total_EMI_Rs_Million"]) * 100 if base_row["Total_EMI_Rs_Million"] > 0 else np.nan
            avg_exp_growth = ((latest_row["Average_Expenditure_Rs"] - base_row["Average_Expenditure_Rs"]) / base_row["Average_Expenditure_Rs"]) * 100

            growth_records.append({
                "State": st,
                "Base_Year": base_yr,
                "Latest_Year": latest_yr,
                "Nominal_Income_Growth_Pct": inc_growth,
                "Nominal_Expenditure_Growth_Pct": exp_growth,
                "Nominal_EMI_Growth_Pct": emi_growth,
                "Average_Expenditure_Growth_Pct": avg_exp_growth
            })
    longrun_growth = pd.DataFrame(growth_records).sort_values("Nominal_Income_Growth_Pct", ascending=False).reset_index(drop=True)
    longrun_growth.to_csv(proc_dir / "state_longrun_growth.csv", index=False)

    # 4. Urban vs Rural Comparison Table
    urban_rural = summary[[
        "Year", "State", "Urban_Income_Rs_Million", "Rural_Income_Rs_Million",
        "Urban_Expenditure_Rs_Million", "Rural_Expenditure_Rs_Million",
        "Urban_EMI_Rs_Million", "Rural_EMI_Rs_Million",
        "Urban_Avg_Exp_Rs", "Rural_Avg_Exp_Rs", "Urban_to_Rural_Avg_Exp_Ratio"
    ]].copy()
    urban_rural["Urban_Income_Share_Pct"] = (urban_rural["Urban_Income_Rs_Million"] / (urban_rural["Urban_Income_Rs_Million"] + urban_rural["Rural_Income_Rs_Million"])) * 100
    urban_rural["Urban_Exp_Share_Pct"] = (urban_rural["Urban_Expenditure_Rs_Million"] / (urban_rural["Urban_Expenditure_Rs_Million"] + urban_rural["Rural_Expenditure_Rs_Million"])) * 100
    urban_rural["Urban_EMI_Share_Pct"] = (urban_rural["Urban_EMI_Rs_Million"] / (urban_rural["Urban_EMI_Rs_Million"] + urban_rural["Rural_EMI_Rs_Million"])) * 100
    urban_rural.to_csv(proc_dir / "state_urban_rural_comparison.csv", index=False)

    # -----------------------------
    # Matplotlib Figures (Max 4)
    # -----------------------------
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3})

    # Figure 5: Top 10 States by Nominal Income & Expenditure (2025-26)
    top10 = rankings.head(10).sort_values("Total_Income_Rs_Million", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    y_pos = np.arange(len(top10))
    bar_width = 0.38
    ax.barh(y_pos + bar_width/2, top10["Total_Income_Rs_Million"] / 1e6, height=bar_width, color="#1f77b4", label="Income (Rs. Trillion)")
    ax.barh(y_pos - bar_width/2, top10["Total_Expenditure_Rs_Million"] / 1e6, height=bar_width, color="#2ca02c", label="Expenditure (Rs. Trillion)")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top10["State"])
    ax.set_xlabel("Nominal Value (Rs. Trillion / Lakh Crore)")
    ax.set_title("Figure 5: Top 10 States by Household Income and Expenditure (2025-26)\n*2025-26 based on 75% sample for Mar 2026", weight="bold")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig5_state_income_expenditure_2025_26.png")
    plt.close()

    # Figure 6: All 28 States Ranked by Average Annual Household Expenditure (2025-26)
    all_exp = rankings.sort_values("Average_Expenditure_Rs", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.barh(np.arange(len(all_exp)), all_exp["Average_Expenditure_Rs"] / 1000, color="#4e79a7")
    ax.set_yticks(np.arange(len(all_exp)))
    ax.set_yticklabels(all_exp["State"])
    ax.set_xlabel("Average Expenditure per Household ('000 Rupees)")
    ax.set_title("Figure 6: State Rankings by Average Household Expenditure (2025-26)\n*2025-26 based on 75% sample for Mar 2026", weight="bold")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig6_state_avg_expenditure_ranking.png")
    plt.close()

    # Figure 7: State EMI-to-Income Ratios (2025-26)
    emi_ranked = rankings.dropna(subset=["EMI_to_Income_Pct"]).sort_values("EMI_to_Income_Pct", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.barh(np.arange(len(emi_ranked)), emi_ranked["EMI_to_Income_Pct"], color="#e15759")
    ax.set_yticks(np.arange(len(emi_ranked)))
    ax.set_yticklabels(emi_ranked["State"])
    ax.set_xlabel("EMI-to-Income Ratio (%)")
    ax.set_title("Figure 7: State/UT Household Debt Servicing Burden (EMI as % of Income: 2025-26)\n*Excludes Chandigarh (unreported Total EMI)", weight="bold")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig7_state_emi_to_income_ratio.png")
    plt.close()

    # Figure 8: Urban vs Rural Disparity: Ratio of Urban to Rural Average Expenditure (2025-26)
    disparity_df = urban_rural[urban_rural["Year"] == "2025-26"].dropna(subset=["Urban_to_Rural_Avg_Exp_Ratio"]).sort_values("Urban_to_Rural_Avg_Exp_Ratio", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.barh(np.arange(len(disparity_df)), disparity_df["Urban_to_Rural_Avg_Exp_Ratio"], color="#76b7b2")
    ax.axvline(1.0, color="red", linestyle="--", alpha=0.7, label="Parity (1.0)")
    ax.set_yticks(np.arange(len(disparity_df)), labels=disparity_df["State"])
    ax.set_xlabel("Ratio (Urban Average Expenditure / Rural Average Expenditure)")
    ax.set_title("Figure 8: Urban-to-Rural Consumption Disparity Across States (2025-26)\n*Chandigarh excluded (100% urban, rural unpopulated)", weight="bold")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "fig8_state_urban_rural_disparity.png")
    plt.close()

    print("Chunk 3 completed: 4 CSVs and 4 figures generated successfully.")

if __name__ == "__main__":
    run_state_analysis()
