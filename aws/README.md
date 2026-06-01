# AWS Notes

This folder contains the AWS-related files for the churn analysis project.

I used AWS for a small cloud analytics workflow:

1. Upload raw and cleaned CSV files to S3.
2. Register the cleaned CSV as a table in AWS Glue Data Catalog.
3. Query the table with Amazon Athena.

## Services

- Amazon S3: stores the CSV files
- AWS Glue Data Catalog: stores the table schema
- Amazon Athena: runs SQL queries on the CSV in S3

## S3 Layout

The project used this layout:

```text
s3://<bucket-name>/
  churn-project/
    raw/Telco-Customer-Churn.csv
    processed/telco_churn_clean.csv
    athena-results/
```

The exact bucket name is not included here because it is account-specific.

## Glue Table

The table schema is defined in:

```text
aws/glue_table_input.json
```

Table name:

```text
churn_project.telco_churn_clean
```

The table points to:

```text
s3://<bucket-name>/churn-project/processed/
```

The customer risk score schema is defined in:

```text
aws/glue_risk_scores_table_input.json
```

Risk score table name:

```text
churn_project.customer_churn_scores
```

The risk score table points to:

```text
s3://<bucket-name>/churn-project/scores/
```

## Athena Query

The main query used for checking churn rate by contract:

```sql
SELECT
  contract,
  COUNT(*) AS customers,
  ROUND(AVG(churn), 4) AS churn_rate
FROM churn_project.telco_churn_clean
GROUP BY contract
ORDER BY churn_rate DESC;
```

Result:

| contract | customers | churn_rate |
|---|---:|---:|
| Month-to-month | 3,875 | 0.4271 |
| One year | 1,473 | 0.1127 |
| Two year | 1,695 | 0.0283 |

Risk score query:

```sql
SELECT
  risk_level,
  COUNT(*) AS customers,
  ROUND(AVG(churn_probability), 4) AS avg_churn_probability,
  ROUND(AVG(actual_churn), 4) AS actual_churn_rate
FROM churn_project.customer_churn_scores
GROUP BY risk_level;
```

Result:

| risk_level | customers | avg_churn_probability | actual_churn_rate |
|---|---:|---:|---:|
| High | 2,090 | 0.7932 | 0.5919 |
| Medium | 1,699 | 0.4955 | 0.2678 |
| Low | 3,254 | 0.1282 | 0.0544 |

## Files

- `athena_setup.sql`: SQL notes for the Athena analysis
- `glue_table_input.json`: Glue table schema
- `glue_risk_scores_table_input.json`: Glue table schema for model scores
- `risk_scores_queries.sql`: Athena queries for model score analysis

## Security Notes

- AWS access keys should never be committed to GitHub.
- The project `.gitignore` excludes local data, model files, and virtual
  environment files.
- For a real deployment, I would replace broad learning permissions with a
  least-privilege IAM policy.
