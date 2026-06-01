from pathlib import Path

import joblib
import pandas as pd

from clean_data import RAW_DATA_PATH, clean_telco_data
from train_model import MODEL_PATH


SCORES_PATH = Path("data/processed/customer_churn_scores.csv")
SUMMARY_PATH = Path("reports/risk_score_summary.txt")


def assign_risk_level(probability: float) -> str:
    if probability >= 0.65:
        return "High"
    if probability >= 0.35:
        return "Medium"
    return "Low"


def load_raw_data() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {RAW_DATA_PATH}. Run `python src/download_data.py` first."
        )
    return pd.read_csv(RAW_DATA_PATH)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing {MODEL_PATH}. Run `python src/train_model.py` first."
        )
    return joblib.load(MODEL_PATH)


def create_score_table(raw_df: pd.DataFrame, model) -> pd.DataFrame:
    cleaned_df = clean_telco_data(raw_df)
    features = cleaned_df.drop(columns=["churn"])

    churn_probability = model.predict_proba(features)[:, 1]
    predicted_churn = (churn_probability >= 0.5).astype(int)

    score_df = pd.DataFrame(
        {
            "customerid": raw_df["customerID"],
            "churn_probability": churn_probability.round(4),
            "predicted_churn": predicted_churn,
            "risk_level": [
                assign_risk_level(probability) for probability in churn_probability
            ],
            "actual_churn": cleaned_df["churn"],
            "contract": cleaned_df["contract"],
            "tenure": cleaned_df["tenure"],
            "monthlycharges": cleaned_df["monthlycharges"],
            "totalcharges": cleaned_df["totalcharges"],
            "paymentmethod": cleaned_df["paymentmethod"],
            "internetservice": cleaned_df["internetservice"],
        }
    )
    return score_df


def write_summary(score_df: pd.DataFrame) -> None:
    risk_counts = (
        score_df.groupby("risk_level", observed=True)
        .agg(
            customers=("customerid", "count"),
            avg_churn_probability=("churn_probability", "mean"),
            actual_churn_rate=("actual_churn", "mean"),
        )
        .reindex(["High", "Medium", "Low"])
        .reset_index()
    )

    lines = [
        "Customer Churn Risk Score Summary",
        "",
        risk_counts.to_string(index=False, formatters={
            "avg_churn_probability": "{:.4f}".format,
            "actual_churn_rate": "{:.4f}".format,
        }),
        "",
        "Risk level definitions:",
        "- High: churn_probability >= 0.65",
        "- Medium: 0.35 <= churn_probability < 0.65",
        "- Low: churn_probability < 0.35",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    raw_df = load_raw_data()
    model = load_model()
    score_df = create_score_table(raw_df, model)

    SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    score_df.to_csv(SCORES_PATH, index=False)
    write_summary(score_df)

    print(f"Saved customer churn scores to {SCORES_PATH}")
    print(f"Saved risk score summary to {SUMMARY_PATH}")
    print(score_df["risk_level"].value_counts().to_string())


if __name__ == "__main__":
    main()
