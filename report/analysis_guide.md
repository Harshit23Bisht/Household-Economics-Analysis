# Analysis navigation guide

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
