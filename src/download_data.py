from pathlib import Path
from urllib.request import urlretrieve


DATA_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)
RAW_DATA_PATH = Path("data/raw/Telco-Customer-Churn.csv")


def main():
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if RAW_DATA_PATH.exists():
        print(f"Dataset already exists: {RAW_DATA_PATH}")
        return

    print("Downloading Telco Customer Churn dataset...")
    urlretrieve(DATA_URL, RAW_DATA_PATH)
    print(f"Saved dataset to {RAW_DATA_PATH}")


if __name__ == "__main__":
    main()
