# Tableau Dashboard Guide

This guide describes how to build a simple Tableau Public dashboard for the
customer churn project.

## Data File

Use this CSV file:

```text
data/processed/dashboard_churn_data.csv
```

Generate it with:

```bash
python src/download_data.py
python src/clean_data.py
python src/train_model.py
python src/score_customers.py
python src/create_dashboard_data.py
```

## Dashboard Title

```text
Telco Customer Churn Analysis
```

## Recommended Sheets

### 1. Overall Churn Rate

Goal: show the share of customers who churned.

In Tableau:

1. Create a new sheet named `Overall Churn Rate`.
2. Drag `Actual Churn` to Text.
3. Change aggregation to Average.
4. Format the value as a percentage.

Expected value:

```text
26.54%
```

### 2. Churn Rate by Contract

Goal: compare churn across contract types.

In Tableau:

1. Create a new sheet named `Churn by Contract`.
2. Drag `Contract` to Rows.
3. Drag `Actual Churn` to Columns.
4. Change aggregation to Average.
5. Format the axis as a percentage.
6. Sort descending by churn rate.

Expected pattern:

| contract | churn_rate |
|---|---:|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

### 3. Churn Rate by Payment Method

Goal: compare churn across payment methods.

In Tableau:

1. Create a new sheet named `Churn by Payment Method`.
2. Drag `Paymentmethod` to Rows.
3. Drag `Actual Churn` to Columns.
4. Change aggregation to Average.
5. Format the axis as a percentage.
6. Sort descending by churn rate.

Expected highest group:

```text
Electronic check
```

### 4. Customers by Risk Level

Goal: show how many customers fall into each model risk group.

In Tableau:

1. Create a new sheet named `Customers by Risk Level`.
2. Drag `Risk Level` to Columns.
3. Drag `Customerid` to Rows.
4. Change aggregation to Count Distinct if needed.
5. Sort risk levels as `High`, `Medium`, `Low`.

Expected counts:

| risk_level | customers |
|---|---:|
| High | 2,090 |
| Medium | 1,699 |
| Low | 3,254 |

### 5. Tenure vs Monthly Charges

Goal: explore whether short-tenure or high-charge customers look different by
risk level.

In Tableau:

1. Create a new sheet named `Tenure vs Monthly Charges`.
2. Drag `Tenure` to Columns.
3. Drag `Monthlycharges` to Rows.
4. Drag `Risk Level` to Color.
5. Drag `Customerid` to Detail.
6. Reduce mark opacity if the points overlap too much.

## Dashboard Layout

Suggested layout:

```text
Title

Overall Churn Rate | Customers by Risk Level

Churn by Contract  | Churn by Payment Method

Tenure vs Monthly Charges
```

## Publish

When the dashboard is ready:

1. Save it to Tableau Public.
2. Copy the public dashboard URL.
3. Add the URL to the `Dashboard` section in `README.md`.

Only publish dashboards built from public or non-sensitive data.
