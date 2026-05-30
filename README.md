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
Cleaned CSV uploaded to Amazon S3
        |
        v
AWS Glue table
        |
        v
Athena SQL queries
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
  eda_summary.txt
  model_metrics.txt
src/
  download_data.py
  clean_data.py
  eda.py
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
