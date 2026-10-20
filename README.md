# Indian Household Economics: Income, Expenditure and EMI Trends

## Project Overview

This project analyses Indian household income, expenditure and Equated Monthly Instalment (EMI) trends from 2014–15 to 2025–26. It uses state-level and national-level data to examine changes over time, differences across states, rural–urban expenditure patterns and the composition of EMI repayments.

## Objectives

- Examine changes in aggregate household income and expenditure.
- Compare household expenditure across states and between rural and urban areas.
- Study changes in the composition of EMI repayments.
- Generate summary tables and visualisations to support the findings.
- Interpret the observed trends using concepts from macroeconomics.

## Project Structure

- `src/` — Python analysis scripts.
- `outputs/processed/` — processed datasets and summary tables.
- `outputs/figures/` — charts generated for the analysis.
- `report/` — supporting documentation and analysis guide.

## Methodology

The analysis uses Python to process the available income, expenditure and EMI datasets, prepare summary tables, calculate trends and generate visualisations. Missing values are retained where data are unavailable rather than being automatically imputed.

The figures are nominal unless explicitly stated otherwise. Therefore, increases in income and expenditure should not be interpreted as equivalent increases in real purchasing power.

## Running the Analysis

Run the analysis script from the project root:

```bash
python -m src.remaining_analysis
```

Install the required Python packages before running the script. See `requirements.txt` if provided.

## Limitations

- Nominal figures are not adjusted for inflation.
- Some observations are missing for particular states or years.
- Changes in EMI repayments do not directly measure new borrowing or outstanding debt.
- The observed trends are descriptive and do not establish causal relationships.

## Outputs

The processed datasets and charts are available in the `outputs/` directory.

## Data Sources

Refer to the source datasets and accompanying documentation for the original data providers, coverage and measurement notes.
