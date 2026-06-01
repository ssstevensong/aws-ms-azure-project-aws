from pathlib import Path

import pandas as pd

from score_customers import SCORES_PATH


DASHBOARD_DATA_PATH = Path("data/processed/dashboard_churn_data.csv")
SUMMARY_PATH = Path("reports/dashboard_data_summary.txt")


def load_scores() -> pd.DataFrame:
    if not SCORES_PATH.exists():
        raise FileNotFoundError(
            f"Missing {SCORES_PATH}. Run `python src/score_customers.py` first."
        )
    return pd.read_csv(SCORES_PATH)


def create_tenure_group(tenure: int) -> str:
    if tenure <= 12:
        return "0-12 months"
    if tenure <= 24:
        return "13-24 months"
    if tenure <= 48:
        return "25-48 months"
    return "49+ months"


def create_charge_group(monthly_charge: float) -> str:
    if monthly_charge < 35:
        return "Under $35"
    if monthly_charge < 70:
        return "$35-$69"
    if monthly_charge < 100:
        return "$70-$99"
    return "$100+"


def create_dashboard_data(score_df: pd.DataFrame) -> pd.DataFrame:
    dashboard_df = score_df.copy()

    dashboard_df["actual_churn_label"] = dashboard_df["actual_churn"].map(
        {1: "Churned", 0: "Stayed"}
    )
    dashboard_df["predicted_churn_label"] = dashboard_df["predicted_churn"].map(
        {1: "Predicted churn", 0: "Predicted stay"}
    )
    dashboard_df["tenure_group"] = dashboard_df["tenure"].apply(create_tenure_group)
    dashboard_df["monthly_charge_group"] = dashboard_df["monthlycharges"].apply(
        create_charge_group
    )

    return dashboard_df[
        [
            "customerid",
            "actual_churn",
            "actual_churn_label",
            "predicted_churn",
            "predicted_churn_label",
            "churn_probability",
            "risk_level",
            "contract",
            "tenure",
            "tenure_group",
            "monthlycharges",
            "monthly_charge_group",
            "totalcharges",
            "paymentmethod",
            "internetservice",
        ]
    ]


def write_summary(dashboard_df: pd.DataFrame) -> None:
    lines = [
        "Dashboard Data Summary",
        "",
        f"Rows: {len(dashboard_df):,}",
        f"Columns: {len(dashboard_df.columns):,}",
        "",
        "Columns:",
        *[f"- {column}" for column in dashboard_df.columns],
        "",
        "Suggested Tableau charts:",
        "- KPI: overall churn rate",
        "- Bar chart: churn rate by contract",
        "- Bar chart: churn rate by payment method",
        "- Bar chart: customer count by risk level",
        "- Scatter plot: tenure vs monthly charges colored by risk level",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    score_df = load_scores()
    dashboard_df = create_dashboard_data(score_df)

    DASHBOARD_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    dashboard_df.to_csv(DASHBOARD_DATA_PATH, index=False)
    write_summary(dashboard_df)

    print(f"Saved dashboard data to {DASHBOARD_DATA_PATH}")
    print(f"Saved dashboard summary to {SUMMARY_PATH}")
    print(f"Rows: {len(dashboard_df):,}")
    print(f"Columns: {len(dashboard_df.columns):,}")


if __name__ == "__main__":
    main()
