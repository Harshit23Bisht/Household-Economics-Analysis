"""
Chunk 4: Income Composition and EMI Patterns Analysis
Analyzes national and state-level income sources and EMI loan distributions.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_composition_analysis():
    root = Path.cwd()
    proc_dir = root / "outputs" / "processed"
    fig_dir = root / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    inc_nat = pd.read_csv(proc_dir / "income_national_all_years.csv")
    emi_nat = pd.read_csv(proc_dir / "emi_national_all_years.csv")
    inc_st = pd.read_csv(proc_dir / "income_states_all_years.csv")
    emi_st = pd.read_csv(proc_dir / "emi_states_all_years.csv")

    years = inc_nat["Year"].tolist()

    # 1. National Income Source Composition & Shares
    # Avoid double-counting: Headline is Total_All sources of income
    tot_inc = inc_nat["Total_All sources of income"]
    inc_shares = pd.DataFrame({
        "Year": years,
        "Total_Income_Rs_Million": tot_inc,
        "Wages_Share_Pct": (inc_nat["Total_Wages"] / tot_inc) * 100,
        "Profits_Share_Pct": (inc_nat["Total_Profits"] / tot_inc) * 100,
        "Pensions_Share_Pct": (inc_nat["Total_Pensions"] / tot_inc) * 100,
        "Rent_Share_Pct": (inc_nat["Total_Rent"] / tot_inc) * 100,
        "Interest_Dividends_Share_Pct": (inc_nat["Total_Interest and dividends"] / tot_inc) * 100,
        "Imputed_Income_Share_Pct": (inc_nat["Total_Imputed income"] / tot_inc) * 100,
        "Govt_Transfer_Share_Pct": (inc_nat["Total_Transfer from government"] / tot_inc) * 100,
        "Private_Transfer_Share_Pct": (inc_nat["Total_Private transfer"] / tot_inc) * 100,
        "Govt_InKind_Share_Pct": (inc_nat["Total_Transfer in kind from government"] / tot_inc) * 100,
        "NGO_InKind_Share_Pct": (inc_nat["Total_Transfer in kind from NGO"] / tot_inc) * 100,
        "Sale_Assets_Share_Pct": (inc_nat["Total_Sale of assets and lotteries"] / tot_inc) * 100
    })
    inc_shares.to_csv(proc_dir / "national_income_shares.csv", index=False)

    # 2. National EMI Category Shares
    tot_emi = emi_nat["Total_All_EMIs"]
    emi_shares = pd.DataFrame({
        "Year": years,
        "Total_EMI_Rs_Million": tot_emi,
        "Housing_EMI_Share_Pct": (emi_nat["Total_House_EMI"] / tot_emi) * 100,
        "Vehicle_EMI_Share_Pct": (emi_nat["Total_Vehicle_EMI"] / tot_emi) * 100,
        "Durables_EMI_Share_Pct": (emi_nat["Total_Durables_EMI"] / tot_emi) * 100,
        "Other_EMI_Share_Pct": (emi_nat["Total_Other_EMI"] / tot_emi) * 100
    })
    emi_shares.to_csv(proc_dir / "national_emi_shares.csv", index=False)

    # 3. State-Level Income Composition (Latest Year: 2025-26)
    inc_st_2025 = inc_st[inc_st["Year"] == "2025-26"].copy()
    st_tot_inc = inc_st_2025["Total_All sources of income"]
    st_inc_comp = pd.DataFrame({
        "State": inc_st_2025["State"],
        "Total_Income_Rs_Million": st_tot_inc,
        "Wages_Share_Pct": (inc_st_2025["Total_Wages"] / st_tot_inc) * 100,
        "Profits_Share_Pct": (inc_st_2025["Total_Profits"] / st_tot_inc) * 100,
        "Govt_Transfer_Share_Pct": (inc_st_2025["Total_Transfer from government"] / st_tot_inc) * 100,
        "Private_Transfer_Share_Pct": (inc_st_2025["Total_Private transfer"] / st_tot_inc) * 100,
        "Pensions_Share_Pct": (inc_st_2025["Total_Pensions"] / st_tot_inc) * 100,
        "Rent_Share_Pct": (inc_st_2025["Total_Rent"] / st_tot_inc) * 100
    }).sort_values("Wages_Share_Pct", ascending=False).reset_index(drop=True)
    st_inc_comp.to_csv(proc_dir / "state_income_composition_2025_26.csv", index=False)

    # 4. State-Level EMI Composition (Latest Year: 2025-26)
    emi_st_2025 = emi_st[emi_st["Year"] == "2025-26"].copy()
    st_tot_emi = emi_st_2025["Total_All_EMIs"]
    st_emi_comp = pd.DataFrame({
        "State": emi_st_2025["State"],
        "Total_EMI_Rs_Million": st_tot_emi,
        "Housing_EMI_Share_Pct": (emi_st_2025["Total_House_EMI"] / st_tot_emi) * 100,
        "Vehicle_EMI_Share_Pct": (emi_st_2025["Total_Vehicle_EMI"] / st_tot_emi) * 100,
        "Durables_EMI_Share_Pct": (emi_st_2025["Total_Durables_EMI"] / st_tot_emi) * 100,
        "Other_EMI_Share_Pct": (emi_st_2025["Total_Other_EMI"] / st_tot_emi) * 100
    }).dropna(subset=["Total_EMI_Rs_Million"]).sort_values("Housing_EMI_Share_Pct", ascending=False).reset_index(drop=True)
    st_emi_comp.to_csv(proc_dir / "state_emi_composition_2025_26.csv", index=False)

    # -----------------------------
    # Matplotlib Figures (Max 4)
    # -----------------------------
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3})
    x = np.arange(len(years))

    # Figure 9: National Income Source Shares Over Time (100% Stacked)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    w_s = inc_shares["Wages_Share_Pct"]
    p_s = inc_shares["Profits_Share_Pct"]
    t_s = inc_shares["Govt_Transfer_Share_Pct"]
    pt_s = inc_shares["Private_Transfer_Share_Pct"]
    o_s = 100 - (w_s + p_s + t_s + pt_s)

    ax.stackplot(x, w_s, p_s, t_s, pt_s, o_s,
                 labels=["Wages", "Profits", "Govt Transfers", "Private Transfers", "Other (Rent, Pensions, Int)"],
                 colors=["#2b5c8f", "#e67e22", "#27ae60", "#9b59b6", "#95a5a6"], alpha=0.85)
    ax.set_ylabel("Share of Total Household Income (%)", weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=40, ha="right")
    ax.set_ylim(0, 100)
    ax.set_title("Figure 9: Evolution of National Household Income Sources (2014-15 to 2025-26)\n*In-kind transfers recorded separately from 2021-22 onward", weight="bold")
    ax.legend(loc="lower left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(fig_dir / "fig9_national_income_source_shares.png")
    plt.close()

    # Figure 10: National EMI Shares Over Time
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.plot(x, emi_shares["Housing_EMI_Share_Pct"], marker="o", linewidth=2.2, color="#4e79a7", label="Housing EMI %")
    ax.plot(x, emi_shares["Vehicle_EMI_Share_Pct"], marker="s", linewidth=2.2, color="#f28e2b", label="Vehicle EMI %")
    ax.plot(x, emi_shares["Durables_EMI_Share_Pct"], marker="^", linewidth=2.0, color="#e15759", label="Durables EMI %")
    ax.plot(x, emi_shares["Other_EMI_Share_Pct"], marker="D", linewidth=2.2, color="#76b7b2", label="Other Loans EMI %")
    ax.set_ylabel("Share of Total EMIs (%)", weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=40, ha="right")
    ax.set_ylim(0, 60)
    ax.set_title("Figure 10: Structural Trajectory of Household Debt Servicing Shares (2014-15 to 2025-26)", weight="bold")
    ax.legend(loc="upper right", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(fig_dir / "fig10_national_emi_category_shares.png")
    plt.close()

    # Figure 11: State Comparison of Wage vs Profit Shares (2025-26)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    sorted_st_inc = st_inc_comp.sort_values("Wages_Share_Pct", ascending=True)
    y_idx = np.arange(len(sorted_st_inc))
    ax.barh(y_idx, sorted_st_inc["Wages_Share_Pct"], color="#2b5c8f", label="Wages Share (%)")
    ax.barh(y_idx, sorted_st_inc["Profits_Share_Pct"], left=sorted_st_inc["Wages_Share_Pct"], color="#e67e22", label="Profits Share (%)")
    ax.set_yticks(y_idx)
    ax.set_yticklabels(sorted_st_inc["State"])
    ax.set_xlabel("Combined Share of Wages and Business Profits (%)")
    ax.set_title("Figure 11: State Variation in Wage and Profit Income Shares (2025-26)\n*States ordered by Wage Share", weight="bold")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig11_state_wage_share_comparison_2025_26.png")
    plt.close()

    # Figure 12: State Comparison of EMI Composition (2025-26)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    sorted_st_emi = st_emi_comp.sort_values("Housing_EMI_Share_Pct", ascending=True)
    y_idx = np.arange(len(sorted_st_emi))
    ax.barh(y_idx, sorted_st_emi["Housing_EMI_Share_Pct"], color="#4e79a7", label="Housing %")
    ax.barh(y_idx, sorted_st_emi["Vehicle_EMI_Share_Pct"], left=sorted_st_emi["Housing_EMI_Share_Pct"], color="#f28e2b", label="Vehicle %")
    ax.barh(y_idx, sorted_st_emi["Other_EMI_Share_Pct"], left=sorted_st_emi["Housing_EMI_Share_Pct"] + sorted_st_emi["Vehicle_EMI_Share_Pct"], color="#76b7b2", label="Other %")
    ax.set_yticks(y_idx)
    ax.set_yticklabels(sorted_st_emi["State"])
    ax.set_xlabel("Share of Total State EMIs (%)")
    ax.set_title("Figure 12: State-wise EMI Portfolio Composition (2025-26)\n*Ordered by Housing Loan Share (Chandigarh excluded: unreported Total EMI)", weight="bold")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig12_state_emi_composition_2025_26.png")
    plt.close()

    print("Chunk 4 completed: 4 CSVs and 4 figures generated successfully.")

if __name__ == "__main__":
    run_composition_analysis()
