"""
Chunk 2: National Trends Analysis Module
Analyzes national income, expenditure, and EMI trends from 2014-15 to 2025-26.
Generates summary tables, growth rates, and publication-quality figures.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def run_national_trends():
    project_root = Path.cwd()
    processed_dir = project_root / "outputs" / "processed"
    figures_dir = project_root / "outputs" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Processed National Data
    inc_nat = pd.read_csv(processed_dir / "income_national_all_years.csv")
    exp_nat = pd.read_csv(processed_dir / "expenditure_national_all_years.csv")
    emi_nat = pd.read_csv(processed_dir / "emi_national_all_years.csv")
    
    years = inc_nat["Year"].tolist()
    
    # 2. Build Core Macroeconomic Trend Summary Table
    # All values in Rs. million unless specified
    macro_summary = pd.DataFrame({
        "Year": years,
        "Households_Million": exp_nat["Total_Households_million"],
        "Nominal_Income_Rs_Million": inc_nat["Total_All sources of income"],
        "Nominal_Expenditure_Rs_Million": exp_nat["Total_Total_expenditure_million_Rs"],
        "Nominal_EMI_Rs_Million": emi_nat["Total_All_EMIs"],
        "Average_Expenditure_Rs": exp_nat["Total_Average_expenditure_Rs"],
        "Median_Expenditure_Rs": exp_nat["Total_Median_expenditure_Rs"],
        "Wages_Rs_Million": inc_nat["Total_Wages"],
        "Profits_Rs_Million": inc_nat["Total_Profits"],
        "Housing_EMI_Rs_Million": emi_nat["Total_House_EMI"],
        "Vehicle_EMI_Rs_Million": emi_nat["Total_Vehicle_EMI"],
        "Other_EMI_Rs_Million": emi_nat["Total_Other_EMI"]
    })
    
    # Meaningful Economic Ratios (both numerator and denominator in Rs. Million)
    macro_summary["Expenditure_to_Income_Pct"] = (
        macro_summary["Nominal_Expenditure_Rs_Million"] / macro_summary["Nominal_Income_Rs_Million"] * 100
    )
    macro_summary["EMI_to_Income_Pct"] = (
        macro_summary["Nominal_EMI_Rs_Million"] / macro_summary["Nominal_Income_Rs_Million"] * 100
    )
    macro_summary["EMI_to_Expenditure_Pct"] = (
        macro_summary["Nominal_EMI_Rs_Million"] / macro_summary["Nominal_Expenditure_Rs_Million"] * 100
    )
    macro_summary["Mean_to_Median_Exp_Ratio"] = (
        macro_summary["Average_Expenditure_Rs"] / macro_summary["Median_Expenditure_Rs"]
    )
    
    # 3. Calculate Year-on-Year Percentage Changes
    growth_cols = [
        "Nominal_Income_Rs_Million",
        "Nominal_Expenditure_Rs_Million",
        "Nominal_EMI_Rs_Million",
        "Average_Expenditure_Rs",
        "Median_Expenditure_Rs",
        "Wages_Rs_Million",
        "Profits_Rs_Million",
        "Housing_EMI_Rs_Million",
        "Vehicle_EMI_Rs_Million",
        "Other_EMI_Rs_Million",
        "Households_Million"
    ]
    
    yoy_growth = pd.DataFrame({"Year": years})
    for col in growth_cols:
        yoy_growth[f"{col}_YoY_Pct"] = macro_summary[col].pct_change() * 100
        
    # Sectoral Growth (Urban vs Rural)
    yoy_growth["Urban_Income_YoY_Pct"] = inc_nat["Urban_All sources of income"].pct_change() * 100
    yoy_growth["Rural_Income_YoY_Pct"] = inc_nat["Rural_All sources of income"].pct_change() * 100
    yoy_growth["Urban_Expenditure_YoY_Pct"] = exp_nat["Urban_Total_expenditure_million_Rs"].pct_change() * 100
    yoy_growth["Rural_Expenditure_YoY_Pct"] = exp_nat["Rural_Total_expenditure_million_Rs"].pct_change() * 100
    yoy_growth["Urban_EMI_YoY_Pct"] = emi_nat["Urban_All_EMIs"].pct_change() * 100
    yoy_growth["Rural_EMI_YoY_Pct"] = emi_nat["Rural_All_EMIs"].pct_change() * 100
    
    # 4. Debt Servicing (EMI) Composition Table
    emi_comp = pd.DataFrame({
        "Year": years,
        "Total_EMI_Rs_Million": emi_nat["Total_All_EMIs"],
        "House_EMI_Rs_Million": emi_nat["Total_House_EMI"],
        "Vehicle_EMI_Rs_Million": emi_nat["Total_Vehicle_EMI"],
        "Durables_EMI_Rs_Million": emi_nat["Total_Durables_EMI"],
        "Other_EMI_Rs_Million": emi_nat["Total_Other_EMI"],
        "House_EMI_Share_Pct": (emi_nat["Total_House_EMI"] / emi_nat["Total_All_EMIs"]) * 100,
        "Vehicle_EMI_Share_Pct": (emi_nat["Total_Vehicle_EMI"] / emi_nat["Total_All_EMIs"]) * 100,
        "Durables_EMI_Share_Pct": (emi_nat["Total_Durables_EMI"] / emi_nat["Total_All_EMIs"]) * 100,
        "Other_EMI_Share_Pct": (emi_nat["Total_Other_EMI"] / emi_nat["Total_All_EMIs"]) * 100
    })
    
    # 5. Income Composition Table (Wages, Profits, Rent, Transfers, etc.)
    inc_comp = pd.DataFrame({
        "Year": years,
        "All_Income_Rs_Million": inc_nat["Total_All sources of income"],
        "Wages_Rs_Million": inc_nat["Total_Wages"],
        "Profits_Rs_Million": inc_nat["Total_Profits"],
        "Pensions_Rs_Million": inc_nat["Total_Pensions"],
        "Rent_Rs_Million": inc_nat["Total_Rent"],
        "Govt_Transfer_Rs_Million": inc_nat["Total_Transfer from government"],
        "Private_Transfer_Rs_Million": inc_nat["Total_Private transfer"],
        "Wages_Share_Pct": (inc_nat["Total_Wages"] / inc_nat["Total_All sources of income"]) * 100,
        "Profits_Share_Pct": (inc_nat["Total_Profits"] / inc_nat["Total_All sources of income"]) * 100,
        "Govt_Transfer_Share_Pct": (inc_nat["Total_Transfer from government"] / inc_nat["Total_All sources of income"]) * 100
    })
    
    # Save CSV outputs
    macro_summary.to_csv(processed_dir / "national_trends_summary.csv", index=False)
    yoy_growth.to_csv(processed_dir / "national_yoy_growth.csv", index=False)
    emi_comp.to_csv(processed_dir / "emi_composition_trends.csv", index=False)
    inc_comp.to_csv(processed_dir / "income_sources_composition.csv", index=False)
    print("Saved processed trend tables to outputs/processed/")
    
    # Set Matplotlib Styling
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 14,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--"
    })
    
    # Convert Rs. Million to Rs. Lakh Crore (Trillion): 1 Trillion = 1,000,000 Million
    inc_trillion = macro_summary["Nominal_Income_Rs_Million"] / 1e6
    exp_trillion = macro_summary["Nominal_Expenditure_Rs_Million"] / 1e6
    emi_trillion = macro_summary["Nominal_EMI_Rs_Million"] / 1e6
    
    x = np.arange(len(years))
    
    # -------------------------------------------------------------
    # Figure 1: National Macro Aggregates Trajectory (Nominal Rs. Trillion)
    # -------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    
    color_inc = "#1f77b4"
    color_exp = "#2ca02c"
    color_emi = "#d62728"
    
    line1 = ax1.plot(x, inc_trillion, marker="o", linewidth=2.5, color=color_inc, label="Nominal Income (Rs. Trillion)")
    line2 = ax1.plot(x, exp_trillion, marker="s", linewidth=2.5, color=color_exp, label="Nominal Expenditure (Rs. Trillion)")
    
    ax1.set_ylabel("Income & Expenditure (Rs. Trillion / Lakh Crore)", color="#111111", weight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, rotation=35, ha="right")
    ax1.set_ylim(0, 175)
    
    # Secondary axis for EMI
    ax2 = ax1.twinx()
    line3 = ax2.plot(x, emi_trillion, marker="^", linewidth=2.2, linestyle="--", color=color_emi, label="Nominal EMI Debt Servicing (Rs. Trillion)")
    ax2.set_ylabel("Total EMI Commitments (Rs. Trillion)", color=color_emi, weight="bold")
    ax2.set_ylim(0, 3.8)
    ax2.grid(False)
    
    # Combine legends
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", frameon=True, framealpha=0.9)
    
    # Highlight COVID-19 shock in 2020-21
    covid_idx = years.index("2020-21")
    ax1.axvspan(covid_idx - 0.4, covid_idx + 0.4, color="gray", alpha=0.15, label="COVID-19 Shock")
    ax1.text(covid_idx, 160, "COVID-19 Contraction\n(2020-21)", ha="center", fontsize=8.5,
             bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3, ec="orange"))
    
    # Flag 2025-26 75% sample note
    sample_idx = years.index("2025-26")
    ax1.text(sample_idx, inc_trillion.iloc[-1] + 3, "* 75% sample for Mar 2026",
             ha="right", fontsize=8, color="#555555", style="italic")
    
    plt.title("Figure 1: National Macroeconomic Trajectories (2014-15 to 2025-26)\nNominal Household Income, Consumption Expenditure, and Debt Servicing (EMI)",
              weight="bold", pad=12)
    fig.tight_layout()
    fig1_path = figures_dir / "fig1_national_macro_aggregates.png"
    plt.savefig(fig1_path)
    plt.close()
    print("Saved Figure 1:", fig1_path.name)
    
    # -------------------------------------------------------------
    # Figure 2: Year-on-Year Growth Dynamics (%)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    
    growth_years = years[1:]
    gx = np.arange(len(growth_years))
    
    g_inc = yoy_growth["Nominal_Income_Rs_Million_YoY_Pct"].iloc[1:]
    g_exp = yoy_growth["Nominal_Expenditure_Rs_Million_YoY_Pct"].iloc[1:]
    g_emi = yoy_growth["Nominal_EMI_Rs_Million_YoY_Pct"].iloc[1:]
    
    ax.axhline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.7)
    ax.plot(gx, g_inc, marker="o", linewidth=2.2, color=color_inc, label="Household Income YoY (%)")
    ax.plot(gx, g_exp, marker="s", linewidth=2.2, color=color_exp, label="Household Expenditure YoY (%)")
    ax.plot(gx, g_emi, marker="^", linewidth=2.0, linestyle="--", color=color_emi, label="Total EMI Debt Servicing YoY (%)")
    
    ax.set_ylabel("Year-on-Year Percentage Change (%)", weight="bold")
    ax.set_xticks(gx)
    ax.set_xticklabels(growth_years, rotation=35, ha="right")
    ax.set_ylim(-35, 220)
    
    # Annotate 2017-18 EMI expansion and 2020-21 contraction
    idx_17 = growth_years.index("2017-18")
    ax.annotate(f"+{g_emi.iloc[idx_17]:.1f}%\nCredit Formalization",
                xy=(idx_17, g_emi.iloc[idx_17]), xytext=(idx_17 - 0.5, 175),
                arrowprops=dict(facecolor=color_emi, shrink=0.08, width=1, headwidth=5),
                fontsize=8, ha="center", weight="bold", color=color_emi)
    
    idx_20 = growth_years.index("2020-21")
    ax.annotate(f"Income: {g_inc.iloc[idx_20]:.1f}%\nExp: {g_exp.iloc[idx_20]:.1f}%\nEMI: {g_emi.iloc[idx_20]:.1f}%",
                xy=(idx_20, g_emi.iloc[idx_20]), xytext=(idx_20 + 0.4, -28),
                arrowprops=dict(facecolor="gray", shrink=0.08, width=1, headwidth=5),
                fontsize=8, ha="left", bbox=dict(boxstyle="round,pad=0.3", fc="#f0f0f0", ec="#cccccc"))
    
    ax.legend(loc="upper right", frameon=True, framealpha=0.9)
    plt.title("Figure 2: Year-on-Year Growth Dynamics (2015-16 to 2025-26)\nContraction Cycles, Expansion Phases, and Volatility Asymmetry",
              weight="bold", pad=12)
    fig.tight_layout()
    fig2_path = figures_dir / "fig2_yoy_growth_dynamics.png"
    plt.savefig(fig2_path)
    plt.close()
    print("Saved Figure 2:", fig2_path.name)
    
    # -------------------------------------------------------------
    # Figure 3: Household EMI Composition & Structural Shift
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    
    # Panel A: Stacked Area in Rs. Trillion
    h_emi_t = emi_comp["House_EMI_Rs_Million"] / 1e6
    v_emi_t = emi_comp["Vehicle_EMI_Rs_Million"] / 1e6
    d_emi_t = emi_comp["Durables_EMI_Rs_Million"] / 1e6
    o_emi_t = emi_comp["Other_EMI_Rs_Million"] / 1e6
    
    colors_emi = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2"]
    
    ax1.stackplot(x, h_emi_t, v_emi_t, d_emi_t, o_emi_t,
                  labels=["Housing EMI", "Vehicle EMI", "Durables EMI", "Other Loans EMI"],
                  colors=colors_emi, alpha=0.85)
    ax1.set_ylabel("EMI Debt Servicing (Rs. Trillion)", weight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, rotation=40, ha="right")
    ax1.set_title("(A) Total Volume by Loan Category (Rs. Trillion)", weight="bold", fontsize=11)
    ax1.legend(loc="upper left", frameon=True)
    ax1.set_ylim(0, 3.5)
    
    # Panel B: Percentage Share Over Time
    h_share = emi_comp["House_EMI_Share_Pct"]
    v_share = emi_comp["Vehicle_EMI_Share_Pct"]
    d_share = emi_comp["Durables_EMI_Share_Pct"]
    o_share = emi_comp["Other_EMI_Share_Pct"]
    
    ax2.plot(x, h_share, marker="o", linewidth=2.2, color=colors_emi[0], label="Housing EMI %")
    ax2.plot(x, v_share, marker="s", linewidth=2.2, color=colors_emi[1], label="Vehicle EMI %")
    ax2.plot(x, d_share, marker="^", linewidth=2.0, color=colors_emi[2], label="Durables EMI %")
    ax2.plot(x, o_share, marker="D", linewidth=2.2, color=colors_emi[3], label="Other Loans EMI %")
    
    ax2.set_ylabel("Share of Total Household EMIs (%)", weight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(years, rotation=40, ha="right")
    ax2.set_title("(B) Structural Shift in Debt Portfolio (%)", weight="bold", fontsize=11)
    ax2.legend(loc="center left", frameon=True)
    ax2.set_ylim(0, 58)
    
    plt.suptitle("Figure 3: Evolution of Household Debt Commitments by Loan Category (2014-15 to 2025-26)\nRapid Rise of Vehicle and Other/Unsecured Debt Relative to Residential Mortgages",
                 weight="bold", y=1.02)
    fig.tight_layout()
    fig3_path = figures_dir / "fig3_household_emi_composition.png"
    plt.savefig(fig3_path, bbox_inches="tight")
    plt.close()
    print("Saved Figure 3:", fig3_path.name)
    
    # -------------------------------------------------------------
    # Figure 4: Expenditure Inequality & Rural vs Urban Disparities
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    
    # Panel A: Average vs Median Expenditure in Rupees
    avg_exp = macro_summary["Average_Expenditure_Rs"]
    med_exp = macro_summary["Median_Expenditure_Rs"]
    
    ax1.plot(x, avg_exp, marker="o", linewidth=2.4, color="#2b5c8f", label="Average Expenditure (Rs./household)")
    ax1.plot(x, med_exp, marker="s", linewidth=2.4, color="#e67e22", label="Median Expenditure (Rs./household)")
    ax1.fill_between(x, med_exp, avg_exp, color="#f39c12", alpha=0.2, label="Mean-Median Gap (Skewness)")
    
    ax1.set_ylabel("Annual Expenditure per Household (Rupees)", weight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, rotation=40, ha="right")
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f"{int(val):,}"))
    ax1.set_title("(A) Consumption Distribution Skewness (Rupees)", weight="bold", fontsize=11)
    ax1.legend(loc="upper left", frameon=True)
    
    # Panel B: Urban vs Rural Total Expenditure (Rs. Trillion)
    urb_exp_t = exp_nat["Urban_Total_expenditure_million_Rs"] / 1e6
    rur_exp_t = exp_nat["Rural_Total_expenditure_million_Rs"] / 1e6
    
    ax2.plot(x, urb_exp_t, marker="o", linewidth=2.3, color="#8e44ad", label="Urban Total Expenditure (Rs. Trillion)")
    ax2.plot(x, rur_exp_t, marker="^", linewidth=2.3, color="#27ae60", label="Rural Total Expenditure (Rs. Trillion)")
    
    ax2.set_ylabel("Total Expenditure (Rs. Trillion)", weight="bold")
    ax2.set_xticks(x)
    ax2.set_xticklabels(years, rotation=40, ha="right")
    ax2.set_title("(B) Sectoral Divide: Urban vs Rural Expenditure", weight="bold", fontsize=11)
    ax2.legend(loc="upper left", frameon=True)
    
    plt.suptitle("Figure 4: Household Expenditure Dynamics: Distributional Skewness & Sectoral Divide (2014-15 to 2025-26)",
                 weight="bold", y=1.02)
    fig.tight_layout()
    fig4_path = figures_dir / "fig4_expenditure_inequality_rural_urban.png"
    plt.savefig(fig4_path, bbox_inches="tight")
    plt.close()
    print("Saved Figure 4:", fig4_path.name)
    
    print("\nAll 4 figures and trend tables generated successfully!")
    return {
        "macro_summary": macro_summary,
        "yoy_growth": yoy_growth,
        "emi_comp": emi_comp,
        "inc_comp": inc_comp
    }

if __name__ == "__main__":
    run_national_trends()
