# Chunk 1 Report Notes: Data Preparation, Cleaning, and Validation

**Project:** Indian Household Economics Macroeconomic Study (2014–15 to 2025–26)  
**Study Scope:** Household Income by Source, Household Expenditure Dynamics, and Household EMI Commitments across 28 Indian States/UTs and National Aggregates  
**Pipeline Author:** Macroeconomics Data Preparation Subsystem  
**Date:** October 2026  

---

## 1. Data Sources and Study Period

- **Primary Source:** Consumer Pyramids Household Survey (CPHS) / Household Economics database (Centre for Monitoring Indian Economy - CMIE).
- **Time Horizon:** 12 consecutive Indian Financial Years from **2014–15 to 2025–26** (April to March cycle).
- **Core Domains Audited:**
  1. **Household Income:** 12 distinct income streams decomposed across Total, Urban, and Rural sectors (36 numeric metrics + State).
  2. **Household Expenditure:** Total expenditure, average per-household expenditure, median expenditure, and household population across Total, Urban, and Rural sectors (12 numeric metrics + State).
  3. **Household EMI Obligations:** Total EMIs and four loan classifications (Housing, Vehicle, Durables, Other) across Total, Urban, and Rural sectors (15 numeric metrics + State).
- **Data File Universe:** Exactly 36 raw data files (12 annual files per domain).

---

## 2. File Format and Parsing Approach

### 2.1 Pseudo-Excel File Structure
Although distributed with `.xls` extensions, binary file signature analysis confirms that all 36 files are **plain-text tab-separated values (TSV)** with UTF-8 / Windows-1252 text encoding. None of the files are genuine OLE compound binary workbooks (`.xls`) or OpenXML zip archives (`.xlsx`).

### 2.2 Header Layout and Dynamic Row Parsing
All 36 files contain multirow header hierarchies:
- **Line 0:** Table Title (e.g., `Total Income of Households by Sources of Income`).
- **Line 1:** Subtitle, reporting geography, unit descriptor, and financial year (e.g., `India : Rs. million : 2014-15`).
- **Line 2:** Geographic aggregation tier (`States` / `Region Name`, followed by sector markers: `Total`, `Urban`, `Rural`).
- **Line 3:** Domain-specific indicator / metric names (e.g., `All sources of income`, `Wages`, `EMIs (all EMIs)`).
- **Line 4 (Expenditure only):** Physical/monetary unit definitions (`Million nos`, `Rs. million`, `Rupees`).

### 2.3 Parsing Invariants & Edge Cases Handled
1. **Quotation Marks and Indian Numbering:** Several historical files (notably `EMI_2014_15.xls`) enclose figures in literal double quotes and contain Indian numbering comma formatting (e.g., `"2,21,794.39"`). The parsing engine explicitly strips all bounding quotes, removes comma delimiters, and converts valid numeric strings to IEEE 754 `float64`.
2. **Dynamic Header Alignment:** In Income and EMI files, data rows start strictly at line index 4 (0-indexed); in Expenditure files, data rows start at line index 5. The pipeline parses header labels directly into standardized snake/title-case variables and aligns rows by state identifier.
3. **Footnote/Disclaimer Separation:** Trailing survey notes are dynamically identified and extracted into metadata rather than causing numeric type coercion errors.

---

## 3. Cleaning and Transformation Steps

1. **Standardized Column Nomenclature:**
   - **Income (37 columns):** `State`, followed by `{Sector}_{Source}` across `Total`, `Urban`, and `Rural` for:
     `All sources of income`, `Wages`, `Pensions`, `Imputed income`, `Profits`, `Interest and dividends`, `Rent`, `Sale of assets and lotteries`, `Transfer from government`, `Transfer in kind from government`, `Private transfer`, `Transfer in kind from NGO`.
   - **Expenditure (13 columns):** `State`, followed by `{Sector}_{Metric}` across `Total`, `Urban`, and `Rural` for:
     `Households_million`, `Total_expenditure_million_Rs`, `Average_expenditure_Rs`, `Median_expenditure_Rs`.
   - **EMI (16 columns):** `State`, followed by `{Sector}_{Metric}` across `Total`, `Urban`, and `Rural` for:
     `All_EMIs`, `House_EMI`, `Vehicle_EMI`, `Durables_EMI`, `Other_EMI`.
2. **Temporal Dimension:** Financial years extracted from filenames (e.g., `Income_2014_15.xls` $\rightarrow$ `2014-15`) and inserted as the leading index column (`Year`) in all state and national tables.
3. **Automated Pipeline Implementation:** All transformations are encapsulated in [`src/data_cleaner.py`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/src/data_cleaner.py) and verified inside [`notebooks/01_data_audit.ipynb`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/notebooks/01_data_audit.ipynb).

---

## 4. Missing-Data Policy and Detailed Taxonomy

> [!IMPORTANT]
> **Strict Non-Imputation Rule:** Blank cells and unmeasured metrics are retained strictly as `NaN` (Not a Number). Under no circumstance are missing cells imputed with zero.

### 4.1 Econometric Justification:
1. **Administrative Specificity (Chandigarh):** Chandigarh is an entirely urbanized Union Territory. In raw source files, CMIE reports Chandigarh strictly under the `Urban_*` columns, leaving both `Total_*` and `Rural_*` unpopulated (`NaN`). Imputing zero for rural columns would spuriously imply that rural households exist in Chandigarh but consume zero goods and earn zero wages, introducing severe distortion into rural inequality and poverty estimators.
2. **Unreported State-Years (All-NaN Rows in Northeastern States):**
   - **Meghalaya & Tripura:** Completely unpopulated across all numeric columns in 2014–15, 2015–16, and 2016–17 across Income, Expenditure, and EMI. Full reported observations begin in 2017–18.
   - **Sikkim:** Completely unpopulated across all numeric columns from 2014–15 through 2017–18. Reported observations begin in 2018–19.
   Imputing zeroes for unrepresented state-years would create artificial, massive growth spikes upon survey inclusion.
3. **Questionnaire Phasing (In-Kind Transfers):** Prior to 2021–22, in-kind transfers from government and NGOs were not tracked as separate questionnaire items in CPHS Income surveys. Across Total, Urban, and Rural sectors (6 columns total), these values are 100% blank from 2014–15 to 2020–21 for all states and the national aggregate. Preserving `NaN` correctly documents variable unavailability.

---

## 5. Treatment of National Aggregates and Missing Value Reconciliation

The national summary record (`India`) is systematically segregated from the state/UT tables:
- **Rationale:** Mixing `India` with individual states introduces fatal aggregation errors: simple summing doubles all macroeconomic variables, and unweighted panel regressions suffer severe heteroskedasticity and bias.
- **Resulting Structure:**
  - State Datasets: 336 rows (28 states/UTs $\times$ 12 years).
  - National Datasets: 12 rows (1 aggregate $\times$ 12 years).

### 5.1 Reconciliation of National Missing Values:
- **National Expenditure Dataset:** **0 missing cells** across all 12 years (100% complete).
- **National EMI Dataset:** **0 missing cells** across all 12 years (100% complete).
- **National Income Dataset:** Exactly **42 missing cells** total across the entire 12-year dataset.

#### Mathematical Reconciliation of the 42 Missing Cells:
- If one considers only the aggregate `Total` sector, there are 2 in-kind income measures:
  1. `Total_Transfer in kind from government`
  2. `Total_Transfer in kind from NGO`
  Across the 7 early years (2014–15 to 2020–21), $2 \times 7 = 14$ missing cells.
- However, the dataset disaggregates all measures across **three sectors**:
  1. `Total` (2 measures: Government & NGO in-kind)
  2. `Urban` (2 measures: Government & NGO in-kind)
  3. `Rural` (2 measures: Government & NGO in-kind)
  This yields **6 distinct in-kind columns**:
  $$\text{6 in-kind columns} \times \text{7 financial years (2014–15 to 2020–21)} = \mathbf{42\text{ missing cells}}.$$
- In all other 30 numeric columns of `income_national_all_years.csv` across all 12 years, there are **0 missing cells**.
- In the subsequent 5 years (2021–22 through 2025–26), there are **0 missing cells** in national income.

---

## 6. State/UT Coverage, Boundary Evolution, and Year-by-Year Missingness

### 6.1 State and Union Territory Coverage
All 36 files contain exactly the same 28 geographic entities. National aggregate `India` is strictly excluded from all state-level datasets.

#### Administrative Boundaries Over the Study Period:
1. **Andhra Pradesh & Telangana:** Andhra Pradesh was bifurcated under the Andhra Pradesh Reorganisation Act, 2014 on June 2, 2014. In our dataset (starting FY 2014–15), both "Andhra Pradesh" and "Telangana" are reported as separate entities across all 12 financial years.
2. **Jammu & Kashmir:** Bifurcated into the Union Territories of Jammu & Kashmir and Ladakh on October 31, 2019. In the CMIE dataset, the entity continues to be labelled strictly as `"Jammu & Kashmir"` throughout all 12 years without a separate Ladakh series. Researchers should note that post-2019 data may reflect the newly demarcated UT of J&K or a continuous historical frame.
3. **Union Territories:** Chandigarh, Delhi, and Puducherry are included alongside the 25 States.

### 6.2 Year-by-Year Coverage and Missingness Table

| Category | Financial Year | State/UT Labels | Valid Numeric Cells | Missing Numeric Cells | All-NaN Rows | States with All-NaN Rows |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Income** | 2014–15 | 28 | 730 | 278 | 3 | Meghalaya, Tripura, Sikkim |
| **Income** | 2015–16 | 28 | 730 | 278 | 3 | Meghalaya, Tripura, Sikkim |
| **Income** | 2016–17 | 28 | 730 | 278 | 3 | Meghalaya, Tripura, Sikkim |
| **Income** | 2017–18 | 28 | 790 | 218 | 1 | Sikkim |
| **Income** | 2018–19 | 28 | 820 | 188 | 0 | None |
| **Income** | 2019–20 | 28 | 820 | 188 | 0 | None |
| **Income** | 2020–21 | 28 | 820 | 188 | 0 | None |
| **Income** | 2021–22 | 28 | 984 | 24 | 0 | None (Chandigarh only) |
| **Income** | 2022–23 | 28 | 984 | 24 | 0 | None (Chandigarh only) |
| **Income** | 2023–24 | 28 | 984 | 24 | 0 | None (Chandigarh only) |
| **Income** | 2024–25 | 28 | 984 | 24 | 0 | None (Chandigarh only) |
| **Income** | 2025–26 | 28 | 984 | 24 | 0 | None (Chandigarh only) |
| **Expenditure** | 2014–15 | 28 | 292 | 44 | 3 | Meghalaya, Tripura, Sikkim |
| **Expenditure** | 2015–16 | 28 | 292 | 44 | 3 | Meghalaya, Tripura, Sikkim |
| **Expenditure** | 2016–17 | 28 | 292 | 44 | 3 | Meghalaya, Tripura, Sikkim |
| **Expenditure** | 2017–18 | 28 | 316 | 20 | 1 | Sikkim |
| **Expenditure** | 2018–19 to 2025–26 (each yr) | 28 | 328 | 8 | 0 | None (Chandigarh only) |
| **EMI** | 2014–15 | 28 | 365 | 55 | 3 | Meghalaya, Tripura, Sikkim |
| **EMI** | 2015–16 | 28 | 365 | 55 | 3 | Meghalaya, Tripura, Sikkim |
| **EMI** | 2016–17 | 28 | 365 | 55 | 3 | Meghalaya, Tripura, Sikkim |
| **EMI** | 2017–18 | 28 | 395 | 25 | 1 | Sikkim |
| **EMI** | 2018–19 to 2025–26 (each yr) | 28 | 410 | 10 | 0 | None (Chandigarh only) |

---

## 7. Source Notes and Sampling Disclaimer Analysis

### 7.1 Exact Footnote Text
Across all 36 raw data files, the only sample-related note detected has the following exact text:
> `"2025-2026 observation is based on 75% sample for Mar 2026."`

### 7.2 Presence and Scope Classification
- **Present in 34 of 36 files:**
  - All 12 Expenditure files (`Expenditure_2014_15.xls` to `Expenditure_2025_26.xls`).
  - All 12 EMI files (`EMI_2014_15.xls` to `EMI_2025_26.xls`).
  - 10 of 12 Income files (present in all except `Income_2021_22.xls` and `Income_2022_23.xls`).
- **Methodological Distinction:**
  1. **For 2025–26 Files (`Income_2025_26.xls`, `Expenditure_2025_26.xls`, `EMI_2025_26.xls`):**  
     The note is a **Year-Specific Data Qualification** indicating that the March 2026 wave data within FY 2025–26 was based on a 75% completed sample at the time of export.
  2. **For 2014–15 to 2024–25 Files:**  
     The note is a **Global Portal Export Disclaimer**. Because the note explicitly specifies "2025-2026 observation", its presence in downloads for historical years is an artifact of the CMIE web portal rendering an active server-wide banner during bulk download. It does **not** indicate that historical years were sampled at 75%.
  3. **Unsupported Assumptions Removed:** Claims that the data is "annualized" or represents "provisional projections" are unsupported by the raw text and have been excised. The text documents solely that observations are based on a 75% sample for March 2026.

---

## 8. Unit and Definition Comparability Issues (Resolution for Chunk 2)

Before computing macroeconomic ratios (e.g., EMI-to-Income, Consumption Propensities), the following unit and definition issues must be addressed:

1. **Monetary Unit Disparity:**
   - Income metrics: **Rs. million**
   - EMI metrics: **Rs. million**
   - Total Expenditure: **Rs. million**
   - Average & Median Expenditure: **Rupees per household**
   - Household Counts: **Million households**  
   *Action for Chunk 2:* Standardize all state aggregates to Rs. million or convert per-capita / per-household metrics into consistent rupee units ($\text{Total Expenditure} = \text{Average Expenditure} \times \text{Households}$).
2. **Nominal vs. Real Values:**
   All figures across the 12 years are in **nominal Indian Rupees**. Real economic growth and expenditure analysis will require state-level or national CPI / deflator adjustments.
3. **In-Kind Transfer Break (2021–22):**
   Prior to 2021–22, "All sources of income" excluded in-kind transfers because they were uncollected. From 2021–22 onward, in-kind transfers are included. When constructing 12-year longitudinal panels, researchers should analyze income both with and without in-kind transfers to isolate survey design artifacts from genuine income growth.

---

## 9. Inventory of Processed Artifacts for Final Report

The following clean datasets are saved in [`outputs/processed/`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed) (relative paths confirmed):

1. [`outputs/processed/income_states_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/income_states_all_years.csv) (336 rows $\times$ 38 cols)
2. [`outputs/processed/expenditure_states_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/expenditure_states_all_years.csv) (336 rows $\times$ 14 cols)
3. [`outputs/processed/emi_states_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/emi_states_all_years.csv) (336 rows $\times$ 17 cols)
4. [`outputs/processed/income_national_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/income_national_all_years.csv) (12 rows $\times$ 38 cols)
5. [`outputs/processed/expenditure_national_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/expenditure_national_all_years.csv) (12 rows $\times$ 14 cols)
6. [`outputs/processed/emi_national_all_years.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/emi_national_all_years.csv) (12 rows $\times$ 17 cols)
7. [`outputs/processed/data_quality_audit.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/data_quality_audit.csv) (36 rows $\times$ 10 cols)
8. [`outputs/processed/source_notes.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/source_notes.csv) (36 rows $\times$ 9 cols)
9. [`outputs/processed/state_consistency.csv`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/state_consistency.csv) (3 rows $\times$ 7 cols)
10. [`outputs/processed/chunk1_verification.txt`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/chunk1_verification.txt) (Human-readable verification audit)
11. [`outputs/processed/chunk1_followup_verification.txt`](file:///c:/Users/harsh/OneDrive/HARSHIT_HOME/VIT/SEMESTER%205/Macroeconomics/household-economics/outputs/processed/chunk1_followup_verification.txt) (Targeted verification and reconciliation report)
