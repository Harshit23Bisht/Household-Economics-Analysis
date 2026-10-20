# Chunk 2 Report Notes: National Trends Analysis (2014–15 to 2025–26)

**Project:** Indian Household Economics Macroeconomic Study  
**Scope:** Macroeconomic Trajectories of Household Income, Consumption Expenditure, and Debt Servicing (EMI) Obligations at the National Aggregate Level  
**Analyst:** Macroeconomics Data Preparation Subsystem  
**Date:** October 2026  

---

## 1. Executive Overview

This report provides the empirical analysis for **Chunk 2: National Trends**, utilizing the verified national aggregate datasets:
- [`outputs/processed/income_national_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/income_national_all_years.csv)
- [`outputs/processed/expenditure_national_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/expenditure_national_all_years.csv)
- [`outputs/processed/emi_national_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/emi_national_all_years.csv)

All monetary aggregates in this section are presented in **nominal Indian Rupees** (Rs. Million and Rs. Trillion / Lakh Crore). Growth rates are computed as year-on-year percentage changes ($\text{YoY } \% = \frac{X_t - X_{t-1}}{X_{t-1}} \times 100$) between strictly comparable definitions. Missing values are preserved as `NaN` and are never treated as zero.

### Data Caveat for 2025–26:
> [!WARNING]
> In accordance with the raw source files across all three categories (`Income_2025_26.xls`, `Expenditure_2025_26.xls`, `EMI_2025_26.xls`), the observation for **2025–26 is based on a 75% sample for March 2026**. While this does not affect historical years (2014–15 to 2024–25), 2025–26 figures must be interpreted with this sample qualification.

---

## 2. Key Empirical Findings (Analysis $\rightarrow$ Inference $\rightarrow$ Result)

### Finding 1: Macroeconomic Contraction and Asymmetric Shock Transmission During COVID-19 (2020–21)

- **Analysis:**
  - Between 2014–15 and 2019–20, national household income expanded steadily from Rs. 45.16 trillion (Rs. 45,161,310 million) to Rs. 77.83 trillion (Rs. 77,833,225 million), while consumption expenditure grew from Rs. 27.67 trillion to Rs. 47.08 trillion.
  - In FY 2020–21, India experienced a synchronized macroeconomic contraction across all three domains:
    - **Nominal Income:** Declined from Rs. 77.83 trillion to Rs. 68.09 trillion, a contraction of **-12.51% YoY**.
    - **Nominal Expenditure:** Declined from Rs. 47.08 trillion to Rs. 40.38 trillion, a contraction of **-14.22% YoY**.
    - **Total EMI Commitments:** Declined from Rs. 1.57 trillion to Rs. 1.12 trillion, a contraction of **-28.25% YoY**.
    - **Wages & Profits:** Wages contracted by **-12.82%** (falling from Rs. 53.34T to Rs. 46.51T) while household business profits dropped by **-14.82%** (from Rs. 16.47T to Rs. 14.03T).
- **Inference:**
  - The pandemic shock transmitted asymmetrically through the household economy. Consumption expenditure contracted more sharply than headline income (-14.22% vs. -12.51%), illustrating a surge in precautionary savings and severe lockdown-induced supply constraints on discretionary services.
  - The disproportionately steep collapse in EMI debt servicing (-28.25%) was more than double the rate of income decline, reflecting the combined effect of voluntary repayment deferrals, credit freeze, and the regulatory loan moratorium instituted by the Reserve Bank of India (RBI) from March to August 2020.
  - Both income (+14.45% YoY) and expenditure (+17.45% YoY) staged rapid V-shaped nominal rebounds in 2021–22, surpassing their pre-pandemic levels within a single financial year.
- **Result:**
  - Quantified 2020–21 shock: Income lost Rs. 9.74 trillion (-12.51%), Expenditure lost Rs. 6.70 trillion (-14.22%), and EMI servicing lost Rs. 0.44 trillion (-28.25%).
  - Illustrated in: [`outputs/figures/fig1_national_macro_aggregates.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig1_national_macro_aggregates.png) and [`outputs/figures/fig2_yoy_growth_dynamics.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig2_yoy_growth_dynamics.png).

---

### Finding 2: Bounded Stability of the Aggregate Consumption Ratio (Nominal APC)

- **Analysis:**
  - The ratio of nominal consumption expenditure to nominal income ($\frac{\text{Total Expenditure}}{\text{Total Income}}$), both expressed in identical units of Rs. million, was calculated across all 12 financial years:
    - 2014–15: **61.27%**
    - 2015–16: **67.48%** (peak)
    - 2016–17: **64.42%**
    - 2017–18: **62.25%**
    - 2018–19: **60.53%**
    - 2019–20: **60.49%**
    - 2020–21: **59.31%** (trough)
    - 2021–22: **60.86%**
    - 2022–23: **66.38%**
    - 2023–24: **65.56%**
    - 2024–25: **61.67%**
    - 2025–26: **63.88%**
- **Inference:**
  - At the national macroeconomic level, Indian households allocate between 59% and 67% of nominal income toward consumption expenditures (12-year average: **62.88%**, standard deviation: **2.48 percentage points**).
  - The dip to 59.31% in 2020–21 marks the only financial year in the series where the consumption share fell below 60%, confirming the macro-level impact of forced savings and service-sector cessation during national lockdowns.
  - The post-pandemic rise back to 66.38% in 2022–23 captures "revenge spending" and demand normalization, before stabilizing around 62–64% in 2024–26.
- **Result:**
  - The national nominal propensity to consume exhibits strong structural persistence around ~63% of household income, with pandemic-induced compression of 3.57 percentage points below its long-term average.
  - Data stored in: [`outputs/processed/national_trends_summary.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/national_trends_summary.csv).

---

### Finding 3: Explosive Growth and Structural Reorientation in Household Debt Servicing (EMIs)

- **Analysis:**
  - Total household EMI obligations grew from Rs. 221,794 million (Rs. 0.22 trillion) in 2014–15 to Rs. 2,994,991 million (Rs. 2.99 trillion) in 2025–26.
  - This represents an unprecedented **13.5-fold expansion (+1,250.3%)** over the 12-year period, far outpacing the growth of both nominal income (+241.7%) and expenditure (+256.3%).
  - Two distinct credit expansion regimes are evident:
    1. **The 2016–19 Retail Credit Boom:** Following demonetization and GST rollout, EMIs surged by **+209.58% YoY in 2017–18** (jumping from Rs. 333.8B to Rs. 1,033.5B) and **+61.89% YoY in 2018–19** (reaching Rs. 1,673.1B).
    2. **Post-Pandemic Credit Resurgence (2021–24):** After contracting -28.25% during COVID, EMIs accelerated by +18.33% (2021–22), +41.19% (2022–23), and +31.65% (2023–24).
  - Structural composition of the debt portfolio underwent a profound transformation:
    - **Housing Loans:** Fell from **33.29%** of total EMIs in 2014–15 to **13.98%** in 2025–26.
    - **Vehicle Loans:** Peaked at **41.62%** in 2022–23 before moderating to **29.34%** in 2025–26.
    - **Other Loans (Personal / Unsecured / Retail):** Surged from **31.24%** in 2014–15 to **50.19%** in 2025–26, becoming the absolute majority of all debt servicing payments.
    - **Consumer Durables:** Accounted for a steady **5.0% to 9.1%** of EMIs.
- **Inference:**
  - Household debt in India has structurally decoupled from residential mortgage asset creation. In 2014–15, housing was the single largest EMI category; by 2025–26, **86.02% of all household EMIs paid are non-housing obligations** (vehicle financing and unsecured/personal retail credit).
  - The EMI-to-income ratio expanded from **0.49%** in 2014–15 to **2.25%** in 2018–19, reaching a peak of **2.44%** in 2023–24 before easing slightly to **1.94%** in 2025–26.
- **Result:**
  - In 2025–26, households paid Rs. 2.99 trillion in EMIs, comprising Rs. 1.50 trillion in Other Loans (50.19%), Rs. 0.88 trillion in Vehicle Loans (29.34%), Rs. 0.42 trillion in Housing Loans (13.98%), and Rs. 0.19 trillion in Consumer Durables (6.48%).
  - Illustrated in: [`outputs/figures/fig3_household_emi_composition.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig3_household_emi_composition.png).

---

### Finding 4: Distributional Skewness in Household Consumption (Mean-Median Gap)

- **Analysis:**
  - Average annual household expenditure increased from Rs. 101,282 in 2014–15 to Rs. 285,735 in 2025–26 (+182.1%).
  - Median annual household expenditure increased from Rs. 89,303 in 2014–15 to Rs. 253,650 in 2025–26 (+184.0%).
  - The Mean-to-Median ratio ($\frac{\text{Average}}{\text{Median}}$) was tracked annually:
    - 2014–15: **1.134** (Gap: Rs. 11,979)
    - 2017–18: **1.131** (Gap: Rs. 15,643)
    - 2018–19: **1.123** (Gap: Rs. 16,600)
    - 2019–20: **1.110** (Gap: Rs. 15,278)
    - 2020–21: **1.083** (Gap: Rs. 9,935 — pandemic compression)
    - 2021–22: **1.074** (Gap: Rs. 10,239 — compression trough)
    - 2023–24: **1.092** (Gap: Rs. 16,889)
    - 2024–25: **1.124** (Gap: Rs. 25,298)
    - 2025–26: **1.126** (Gap: Rs. 32,085)
- **Inference:**
  - Across every single financial year, the arithmetic mean expenditure significantly exceeds the median expenditure ($1.07\times$ to $1.13\times$), confirming that Indian household consumption is characterized by pronounced positive skewness (a long right-tail of high-spending affluent households).
  - The mean-median gap compressed substantially during the pandemic shock (falling from 1.110 in 2019–20 to 1.083 in 2020–21 and bottoming at 1.074 in 2021–22). This proves that top-decile households experienced severe curtailment of high-ticket discretionary consumption during pandemic travel and hospitality restrictions.
  - With full post-pandemic reopening, the mean-to-median ratio rebounded to 1.126 in 2025–26, and the absolute mean-median gap widened to a series high of Rs. 32,085 per household.
- **Result:**
  - Consumption skewness compressed from $1.13\times$ pre-pandemic to $1.07\times$ during COVID-19 before fully re-widening to $1.13\times$ by 2025–26.
  - Illustrated in: [`outputs/figures/fig4_expenditure_inequality_rural_urban.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig4_expenditure_inequality_rural_urban.png).

---

### Finding 5: Urban vs. Rural Consumption Dynamics and Pandemic Resilience

- **Analysis:**
  - Total Rural Expenditure: Rose from Rs. 16.54 trillion in 2014–15 to Rs. 56.28 trillion in 2025–26 (+240.2%).
  - Total Urban Expenditure: Rose from Rs. 11.13 trillion in 2014–15 to Rs. 42.30 trillion in 2025–26 (+280.1%).
  - Sectoral Shares of Domestic Demand:
    - Rural share of consumption shifted modestly from **59.78%** (2014–15) to **57.09%** (2025–26).
    - Urban share increased from **40.22%** to **42.91%**.
  - During the 2020–21 Contraction:
    - Urban consumption fell by **-15.34% YoY** (dropping by Rs. 2.97 trillion).
    - Rural consumption fell by **-13.45% YoY** (dropping by Rs. 3.73 trillion).
- **Inference:**
  - Urban spending grew slightly faster over the full cycle (+280% vs +240%), reflecting urbanization, demographic migration, and urban income wage premiums.
  - However, rural household demand proved more resilient during the pandemic crisis, suffering ~1.9 percentage points less contraction than urban areas (-13.45% vs. -15.34%). Rural consumption was insulated by normal agricultural operations, reverse urban-to-rural migration, and public safety nets (MGNREGA and PM-GKAY grain allocations).
- **Result:**
  - Rural India remains the dominant anchor of national household consumption, accounting for **57.09%** of aggregate domestic spending in 2025–26.

---

## 3. Methodological Guardrails and Unit Discipline

1. **Distinction Between Nominal Expansion and Real Growth:**
   All series evaluated in Chunk 2 are in **nominal Indian Rupees**. Over the 2014–15 to 2025–26 period, CPI inflation averaged approximately 4.5% to 5.5% annually. Therefore, a substantial portion of the headline +241.7% income growth and +256.3% expenditure growth reflects general price-level increases rather than volume-level living standard gains. State-level deflators and real adjustments are deferred to subsequent analytical chunks.
2. **Strict Unit Compatibility:**
   Ratios were constructed solely between metrics sharing identical units:
   - Expenditure-to-Income: $\frac{\text{Rs. Million}}{\text{Rs. Million}}$ (valid percentage).
   - EMI-to-Income: $\frac{\text{Rs. Million}}{\text{Rs. Million}}$ (valid percentage).
   - Mean-to-Median: $\frac{\text{Rupees}}{\text{Rupees}}$ (dimensionless ratio).
   No cross-unit ratios mixing physical household counts with rupee totals were computed without dimensional normalization ($\text{Total Expenditure (Rs. M)} / \text{Households (M)} = \text{Average Expenditure in Rupees}$).

---

## 4. Generated Artifacts and Figure Inventory

### Processed Datasets Saved in `outputs/processed/`:
1. [`national_trends_summary.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/national_trends_summary.csv): Full 12-year national macro trends (levels, household counts, APC ratios, EMI shares, mean-median ratios).
2. [`national_yoy_growth.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/national_yoy_growth.csv): Annual YoY growth rates across all comparable nominal indicators, including rural-urban disaggregations.
3. [`emi_composition_trends.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/emi_composition_trends.csv): Historical levels and percentage shares for Housing, Vehicle, Durables, and Other EMI debt obligations.
4. [`income_sources_composition.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/income_sources_composition.csv): Decomposition of income streams (Wages, Profits, Pensions, Transfers) and their shares of national income.

### Publication-Quality Figures Saved in `outputs/figures/`:
1. [`fig1_national_macro_aggregates.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig1_national_macro_aggregates.png): Dual-axis macroeconomic trajectories of Household Income, Expenditure, and EMI debt servicing (in Rs. Trillion / Lakh Crore), highlighting the 2020–21 COVID-19 shock and the 2025–26 sample qualification.
2. [`fig2_yoy_growth_dynamics.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig2_yoy_growth_dynamics.png): Comparative YoY growth dynamics illustrating the 2017–19 credit boom, the synchronized 2020–21 contraction, and the post-pandemic recovery.
3. [`fig3_household_emi_composition.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig3_household_emi_composition.png): Two-panel visualization of debt servicing volume and structural portfolio shift, documenting the decline of housing mortgages and the ascendancy of unsecured/other loans.
4. [`fig4_expenditure_inequality_rural_urban.png`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/figures/fig4_expenditure_inequality_rural_urban.png): Two-panel visualization of consumption inequality (Mean vs. Median gap in Rupees) and the geographic divide between Urban and Rural household expenditure.
