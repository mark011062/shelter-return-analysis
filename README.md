# Shelter Return Analysis

An analysis of Austin Animal Center adoption records examining factors associated with animals returning to the shelter within 30 days of adoption.

## Project Overview

Animal shelters work to create successful, lasting adoptions, but some animals return shortly after leaving the shelter.

This project analyzes historical intake and outcome records from the Austin Animal Center to answer the question:

What characteristics are associated with a higher likelihood of an animal returning to the shelter within 30 days of adoption?

The project combines data cleaning, event matching, feature engineering, exploratory analysis, visualization, and statistical modeling.

## Dataset

The analysis uses Austin Animal Center intake and outcome records covering October 2013 through May 2025.

The final analytical cohort contains:

- 84,143 adoption events
- 5,386 returns within 30 days
- 6.40% overall 30-day return rate

Only adoption events with a complete 30-day follow-up period were included in the final analysis.

## Key Findings

### Animal Type

Dogs had a substantially higher observed 30-day return rate than cats:

- Dogs: 9.03%
- Cats: 3.10%

After accounting for the other variables included in the statistical model, dogs had 2.28 times the odds of a 30-day return compared with cats.

### Age at Adoption

Age was strongly associated with return rates.

- Under 6 months: 3.22%
- 6–12 months: 6.91%
- 1–3 years: 9.47%
- 3–7 years: 9.80%
- 7+ years: 7.69%

Animals under six months had the lowest observed return rate.

### Prior Shelter History

Return rates increased with previous recorded shelter intakes:

- No previous intakes: 5.74%
- One previous intake: 11.05%
- Two or more previous intakes: 14.78%

Prior shelter history remained associated with higher return odds after accounting for the other modeled characteristics.

## Statistical Analysis

A multivariable logistic regression model was used to examine animal type, age, prior shelter history, and time from intake to adoption simultaneously.

Because the same animal can appear in multiple adoption events, cluster-robust standard errors were calculated using Animal ID.

The model identified animal type, age, and prior shelter history as meaningful characteristics associated with 30-day returns.

These results represent associations and should not be interpreted as causal effects.

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Jupyter Notebook
- Git and GitHub

## Project Structure

```text
shelter-return-analysis/
│
├── data/
│   ├── raw/
│   │   └── Raw shelter data excluded from GitHub
│   └── shelter_return_analysis.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_return_analysis.ipynb
│   └── 03_final_analysis.ipynb
│
├── README.md
└── .gitignore
```

## Analysis Workflow

1. Clean and validate shelter intake and outcome records.
2. Identify adoption events.
3. Match adoption events to subsequent shelter intakes.
4. Define whether each adoption resulted in a return within 30 days.
5. Restrict the final cohort to adoption events with complete 30-day follow-up.
6. Engineer features describing age, shelter history, and time to adoption.
7. Compare return rates across animal characteristics.
8. Examine the interaction between age and animal type.
9. Fit a multivariable logistic regression model.
10. Interpret results while distinguishing association from causation.

## Limitations

This analysis uses observational data from a single shelter system.

The available data does not capture every factor that may influence an adoption outcome, including adopter characteristics, household environment, behavioral concerns, and detailed reasons for returns.

Prior shelter history is also limited to intake events observable within the available records.

The findings should therefore be interpreted as patterns that may help identify areas for additional investigation or targeted support rather than deterministic predictions about individual adoptions.

## Next Step

An interactive Streamlit application will provide an accessible way to explore the major findings and return-rate patterns identified in this analysis.