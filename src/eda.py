from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


CLEAN_DATA_PATH = Path("data/processed/telco_churn_clean.csv")
FIGURE_DIR = Path("reports/figures")
SUMMARY_PATH = Path("reports/eda_summary.txt")


def load_clean_data() -> pd.DataFrame:
    if not CLEAN_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {CLEAN_DATA_PATH}. Run `python src/clean_data.py` first."
        )
    return pd.read_csv(CLEAN_DATA_PATH)


def save_churn_rate_by_category(
    df: pd.DataFrame,
    column: str,
    title: str,
    filename: str,
) -> pd.DataFrame:
    churn_rate = (
        df.groupby(column)["churn"]
        .agg(["count", "mean"])
        .reset_index()
        .rename(columns={"mean": "churn_rate", "count": "customers"})
        .sort_values("churn_rate", ascending=False)
    )

    plt.figure(figsize=(9, 5))
    sns.barplot(data=churn_rate, x=column, y="churn_rate", color="#2f80ed")
    plt.title(title)
    plt.ylabel("Churn rate")
    plt.xlabel(column)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=160)
    plt.close()

    return churn_rate


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_clean_data()

    contract_summary = save_churn_rate_by_category(
        df,
        "contract",
        "Churn Rate by Contract Type",
        "churn_rate_by_contract.png",
    )
    internet_summary = save_churn_rate_by_category(
        df,
        "internetservice",
        "Churn Rate by Internet Service",
        "churn_rate_by_internet_service.png",
    )
    payment_summary = save_churn_rate_by_category(
        df,
        "paymentmethod",
        "Churn Rate by Payment Method",
        "churn_rate_by_payment_method.png",
    )

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="churn", y="monthlycharges", color="#27ae60")
    plt.title("Monthly Charges by Churn Status")
    plt.xlabel("Churn")
    plt.ylabel("Monthly charges")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "monthly_charges_by_churn.png", dpi=160)
    plt.close()

    churn_rate = df["churn"].mean()
    summary = [
        f"Overall churn rate: {churn_rate:.2%}",
        "",
        "Churn rate by contract:",
        contract_summary.to_string(index=False),
        "",
        "Churn rate by internet service:",
        internet_summary.to_string(index=False),
        "",
        "Churn rate by payment method:",
        payment_summary.to_string(index=False),
    ]
    SUMMARY_PATH.write_text("\n".join(summary), encoding="utf-8")

    print(f"Saved EDA summary to {SUMMARY_PATH}")
    print(f"Saved figures to {FIGURE_DIR}")
    print(f"Overall churn rate: {churn_rate:.2%}")


if __name__ == "__main__":
    main()
