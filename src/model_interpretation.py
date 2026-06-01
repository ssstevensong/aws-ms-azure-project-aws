from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from train_model import build_preprocessor, load_clean_data


LOGISTIC_FEATURES_PATH = Path("reports/logistic_regression_features.csv")
RANDOM_FOREST_FEATURES_PATH = Path("reports/random_forest_features.csv")
SUMMARY_PATH = Path("reports/top_features.txt")


def clean_feature_name(feature_name: str) -> str:
    return (
        feature_name.replace("numeric__", "")
        .replace("categorical__", "")
        .replace("_", " ")
    )


def get_feature_names(model: Pipeline) -> list[str]:
    preprocessor = model.named_steps["preprocessor"]
    return [clean_feature_name(name) for name in preprocessor.get_feature_names_out()]


def train_pipeline(estimator, x_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(x_train)),
            ("model", estimator),
        ]
    )
    pipeline.fit(x_train, y_train)
    return pipeline


def summarize_logistic_model(model: Pipeline) -> pd.DataFrame:
    feature_names = get_feature_names(model)
    coefficients = model.named_steps["model"].coef_[0]

    df = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": coefficients,
            "absolute_coefficient": abs(coefficients),
        }
    )
    return df.sort_values("absolute_coefficient", ascending=False)


def summarize_random_forest_model(model: Pipeline) -> pd.DataFrame:
    feature_names = get_feature_names(model)
    importances = model.named_steps["model"].feature_importances_

    df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": importances,
        }
    )
    return df.sort_values("importance", ascending=False)


def write_summary(
    logistic_features: pd.DataFrame,
    random_forest_features: pd.DataFrame,
) -> None:
    positive_logistic = logistic_features.sort_values("coefficient", ascending=False).head(10)
    negative_logistic = logistic_features.sort_values("coefficient", ascending=True).head(10)
    top_random_forest = random_forest_features.head(10)

    lines = [
        "Top Logistic Regression Features Increasing Predicted Churn",
        positive_logistic[["feature", "coefficient"]].to_string(index=False),
        "",
        "Top Logistic Regression Features Decreasing Predicted Churn",
        negative_logistic[["feature", "coefficient"]].to_string(index=False),
        "",
        "Top Random Forest Features",
        top_random_forest[["feature", "importance"]].to_string(index=False),
        "",
        "Notes",
        "- Logistic Regression coefficients show direction after preprocessing.",
        "- Positive coefficients are associated with higher predicted churn.",
        "- Negative coefficients are associated with lower predicted churn.",
        "- Random Forest feature importance shows predictive usefulness, not direction.",
    ]

    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    df = load_clean_data()

    x = df.drop(columns=["churn"])
    y = df["churn"]

    x_train, _, y_train, _ = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    logistic_model = train_pipeline(
        LogisticRegression(max_iter=1000, class_weight="balanced"),
        x_train,
        y_train,
    )
    random_forest_model = train_pipeline(
        RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced",
        ),
        x_train,
        y_train,
    )

    LOGISTIC_FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)

    logistic_features = summarize_logistic_model(logistic_model)
    random_forest_features = summarize_random_forest_model(random_forest_model)

    logistic_features.to_csv(LOGISTIC_FEATURES_PATH, index=False)
    random_forest_features.to_csv(RANDOM_FOREST_FEATURES_PATH, index=False)
    write_summary(logistic_features, random_forest_features)

    print(f"Saved Logistic Regression feature summary to {LOGISTIC_FEATURES_PATH}")
    print(f"Saved Random Forest feature summary to {RANDOM_FOREST_FEATURES_PATH}")
    print(f"Saved top feature notes to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
