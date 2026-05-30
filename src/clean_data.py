from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/Telco-Customer-Churn.csv")
CLEAN_DATA_PATH = Path("data/processed/telco_churn_clean.csv")


def load_raw_data() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {RAW_DATA_PATH}. Run `python src/download_data.py` first."
        )
    return pd.read_csv(RAW_DATA_PATH)


def clean_telco_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # totalcharges contains blank strings for brand-new customers. Convert them to 0.
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df["totalcharges"] = df["totalcharges"].fillna(0)

    binary_columns = [
        "partner",
        "dependents",
        "phoneservice",
        "paperlessbilling",
        "churn",
    ]
    for column in binary_columns:
        df[column] = df[column].map({"Yes": 1, "No": 0})

    df["seniorcitizen"] = df["seniorcitizen"].astype(int)
    df = df.drop(columns=["customerid"])

    return df


def main() -> None:
    CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_df = load_raw_data()
    clean_df = clean_telco_data(raw_df)
    clean_df.to_csv(CLEAN_DATA_PATH, index=False)

    print(f"Raw shape: {raw_df.shape}")
    print(f"Clean shape: {clean_df.shape}")
    print(f"Saved cleaned data to {CLEAN_DATA_PATH}")


if __name__ == "__main__":
    main()
