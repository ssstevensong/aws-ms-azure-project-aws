from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


CLEAN_DATA_PATH = Path("data/processed/telco_churn_clean.csv")
MODEL_PATH = Path("models/churn_model.joblib")
METRICS_PATH = Path("reports/model_metrics.txt")


def load_clean_data() -> pd.DataFrame:
    if not CLEAN_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {CLEAN_DATA_PATH}. Run `python src/clean_data.py` first."
        )
    return pd.read_csv(CLEAN_DATA_PATH)


def build_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    numeric_features = features.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = features.select_dtypes(include=["object"]).columns

    return ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ]
    )


def evaluate_model(name: str, model: Pipeline, x_test: pd.DataFrame, y_test: pd.Series) -> str:
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]

    report = classification_report(y_test, predictions)
    matrix = confusion_matrix(y_test, predictions)
    auc = roc_auc_score(y_test, probabilities)

    return (
        f"Model: {name}\n"
        f"ROC-AUC: {auc:.4f}\n\n"
        f"Confusion Matrix:\n{matrix}\n\n"
        f"Classification Report:\n{report}\n"
    )


def main() -> None:
    df = load_clean_data()

    x = df.drop(columns=["churn"])
    y = df["churn"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocessor = build_preprocessor(x_train)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced",
        ),
    }

    results = []
    fitted_models = {}
    for name, estimator in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", estimator),
            ]
        )
        pipeline.fit(x_train, y_train)
        fitted_models[name] = pipeline
        results.append(evaluate_model(name, pipeline, x_test, y_test))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

    best_model = fitted_models["Logistic Regression"]
    joblib.dump(best_model, MODEL_PATH)
    METRICS_PATH.write_text("\n" + "=" * 80 + "\n\n".join(results), encoding="utf-8")

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")
    print(results[0])


if __name__ == "__main__":
    main()
