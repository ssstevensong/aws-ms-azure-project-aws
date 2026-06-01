# Customer Churn Analysis with Python and AWS

Author: Steven Song

This is a data science project using the IBM Telco Customer Churn dataset. I used
Python for data cleaning, exploratory analysis, and baseline machine learning,
then moved the cleaned dataset to AWS so it could be queried with Athena.

The main question I looked at was:

> Which customer groups have higher churn rates, and can a simple model identify
> customers who are more likely to churn?

## What This Project Includes

- Data cleaning with pandas
- Exploratory data analysis on churn patterns
- Baseline classification models with scikit-learn
- Model evaluation with precision, recall, F1-score, and ROC-AUC
- Cloud storage with Amazon S3
- Table metadata with AWS Glue Data Catalog
- SQL analysis with Amazon Athena

## Project Flow

```text
IBM Telco Customer Churn CSV
        |
        v
Python cleaning and EDA
        |
        v
Logistic Regression / Random Forest
        |
        v
Customer risk scores
        |
        v
Cleaned CSV uploaded to Amazon S3
        |
        v
AWS Glue table
        |
        v
Athena SQL queries
        |
        v
Tableau dashboard
```

## Dataset

The dataset is the IBM Telco Customer Churn sample dataset. It contains customer
demographics, service information, billing details, contract type, and whether
the customer churned.

Source:
https://www.ibm.com/docs/en/cognos-analytics/12.1.0?topic=samples-telco-customer-churn

The raw dataset is downloaded by the project script and is not committed to this
repository.

## Repository Structure

```text
aws/
  athena_setup.sql        Athena query used for analysis
  glue_table_input.json   Glue table schema for the cleaned CSV
  README.md               Notes for the AWS part of the project
notebooks/
  01_churn_eda_model.ipynb
reports/
  dashboard_data_summary.txt
  eda_summary.txt
  logistic_regression_features.csv
  model_metrics.txt
  random_forest_features.csv
  risk_score_summary.txt
  top_features.txt
src/
  create_dashboard_data.py
  download_data.py
  clean_data.py
  eda.py
  model_interpretation.py
  score_customers.py
  train_model.py
requirements.txt
```

Large generated files are excluded from Git:

- raw data
- processed data
- trained model files
- generated charts
- local virtual environment files

## How To Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project scripts:

```bash
python src/download_data.py
python src/clean_data.py
python src/eda.py
python src/train_model.py
python src/model_interpretation.py
python src/score_customers.py
python src/create_dashboard_data.py
```

The notebook version is here:

```text
notebooks/01_churn_eda_model.ipynb
```

## Exploratory Analysis Results

Overall churn rate:

```text
26.54%
```

Churn rate by contract type:

| contract | customers | churn_rate |
|---|---:|---:|
| Month-to-month | 3,875 | 0.4271 |
| One year | 1,473 | 0.1127 |
| Two year | 1,695 | 0.0283 |

Churn rate by payment method:

| payment method | customers | churn_rate |
|---|---:|---:|
| Electronic check | 2,365 | 0.4529 |
| Mailed check | 1,612 | 0.1911 |
| Bank transfer automatic | 1,544 | 0.1671 |
| Credit card automatic | 1,522 | 0.1524 |

Main observations:

- Month-to-month customers had much higher churn than customers on longer
  contracts.
- Customers using electronic check had the highest churn rate among payment
  methods.
- These patterns are useful for a first-pass retention analysis, although they
  do not prove causation.

## Model Results

I trained two baseline classifiers:

- Logistic Regression
- Random Forest

The Logistic Regression model gave better recall for the churn class:

| metric | value |
|---|---:|
| ROC-AUC | 0.8416 |
| Churn precision | 0.50 |
| Churn recall | 0.78 |
| Churn F1-score | 0.61 |

For this problem, recall is useful because the model is meant to catch customers
who may churn. Higher recall means fewer churn customers are missed, though it
also creates more false positives.

## Model Interpretation

I added a simple interpretation step to compare Logistic Regression coefficients
and Random Forest feature importance.

Generated files:

```text
reports/logistic_regression_features.csv
reports/random_forest_features.csv
reports/top_features.txt
```

Logistic Regression coefficients are useful for direction:

- positive coefficients are associated with higher predicted churn
- negative coefficients are associated with lower predicted churn

Random Forest feature importance is useful for ranking predictive features, but
it does not show whether a feature increases or decreases churn.

Top features from this step:

| feature | interpretation |
|---|---|
| tenure | Longer-tenure customers were less likely to be predicted as churners. |
| contract Month-to-month | Month-to-month contracts were associated with higher predicted churn. |
| internetservice Fiber optic | Fiber optic customers had higher predicted churn in this model. |
| contract Two year | Two-year contracts were associated with lower predicted churn. |
| paymentmethod Electronic check | Electronic check appeared as a useful churn-related feature. |

These are model interpretation results, not causal claims. Some coefficients can
change when correlated features are included together.

## Customer Risk Scores

I used the trained Logistic Regression model to create customer-level churn risk
scores. The output file is generated locally and excluded from Git because it is
a processed data file:

```text
data/processed/customer_churn_scores.csv
```

The scoring script also writes a small summary:

```text
reports/risk_score_summary.txt
```

Risk levels are based on predicted churn probability:

| risk_level | definition |
|---|---|
| High | churn_probability >= 0.65 |
| Medium | 0.35 <= churn_probability < 0.65 |
| Low | churn_probability < 0.35 |

Risk score summary:

| risk_level | customers | avg_churn_probability | actual_churn_rate |
|---|---:|---:|---:|
| High | 2,090 | 0.7932 | 0.5919 |
| Medium | 1,699 | 0.4955 | 0.2678 |
| Low | 3,254 | 0.1282 | 0.0544 |

This file will be used for the Tableau dashboard.

## Tableau Dashboard

I prepared a Tableau-ready CSV with customer risk scores and grouped fields:

```text
data/processed/dashboard_churn_data.csv
```

The dashboard data is generated by:

```bash
python src/create_dashboard_data.py
```

Published dashboard:

https://public.tableau.com/app/profile/dahong.song/viz/TelcoCustomerChurnAnalysis_17803456933110/TelcoCustomerChurnAnalysis

Dashboard views:

- overall churn rate
- churn rate by contract
- churn rate by payment method
- customer count by risk level
- tenure vs monthly charges by risk level

## AWS Part

After cleaning the data locally, I uploaded the raw and processed CSV files to
Amazon S3. I then registered the cleaned CSV as a table in AWS Glue Data Catalog
and queried it in Amazon Athena.

AWS services used:

- Amazon S3
- AWS Glue Data Catalog
- Amazon Athena

The public repo uses placeholder paths instead of my exact AWS resource names:

```text
s3://<bucket-name>/churn-project/raw/Telco-Customer-Churn.csv
s3://<bucket-name>/churn-project/processed/telco_churn_clean.csv
```

Example Athena query:

```sql
SELECT
  contract,
  COUNT(*) AS customers,
  ROUND(AVG(churn), 4) AS churn_rate
FROM churn_project.telco_churn_clean
GROUP BY contract
ORDER BY churn_rate DESC;
```

The Athena result matched the local pandas analysis for churn rate by contract.

## Notes

This was mainly a learning project. I focused on getting a complete workflow
working first: clean the data, train a baseline model, upload the cleaned data to
AWS, define a table, and query it with SQL.

Things I would improve next:

- Add feature importance or coefficient interpretation.
- Save model predictions as a new CSV and upload them to S3.
- Add a dashboard in QuickSight, Tableau, or Power BI.
- Replace broad AWS learning permissions with a stricter IAM policy.
