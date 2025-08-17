import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score

# --------------------
# Load data
# --------------------
def load_data(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)

# --------------------
# Feature engineering
# --------------------
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    grp = df.groupby("partner_id", as_index=False)

    agg = grp.agg(
        avg_trips_per_week=("trips", "mean"),
        earnings_mean=("earnings", "mean"),
        avg_rating_mean=("avg_rating", "mean"),
        total_cancels=("trips_cancelled", "sum"),
        earnings_std=("earnings", "std")
    )

    agg["earning_volatility"] = (
        agg["earnings_std"] / agg["earnings_mean"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    agg["cancel_rate"] = (
        agg["total_cancels"] / agg["avg_trips_per_week"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    return agg

# --------------------
# Create labels with safety
# --------------------
def make_labels(features: pd.DataFrame):
    perf_score = (
        (features["avg_trips_per_week"] / features["avg_trips_per_week"].max()) * 0.35 +
        (features["earnings_mean"] / features["earnings_mean"].max()) * 0.25 +
        (features["avg_rating_mean"] / 5) * 0.25 +
        ((features["earning_volatility"].max() - features["earning_volatility"]) /
         features["earning_volatility"].max()) * 0.15
    )

    threshold = np.median(perf_score)
    y = (perf_score > threshold).astype(int)

    # Safety: If only one class, randomly assign half as 0
    if len(set(y)) == 1:
        print("⚠ Warning: Only one class detected — forcing 50/50 split randomly.")
        rng = np.random.default_rng(seed=42)
        idx = rng.choice(len(y), size=len(y)//2, replace=False)
        y[:] = 1
        y[idx] = 0

    print(f"Label distribution: {Counter(y)} (threshold={threshold:.3f})")
    return y, perf_score

# --------------------
# Build model
# --------------------
def build_model():
    num_cols = ["avg_trips_per_week", "earnings_mean", "avg_rating_mean",
                "earning_volatility", "cancel_rate"]

    pre = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), num_cols),
        ]
    )
    model = Pipeline([
        ("prep", pre),
        ("lr", LogisticRegression(max_iter=1000))
    ])
    return model, num_cols

# --------------------
# Main
# --------------------
def main(args):
    df = load_data(Path(args.data))
    feats = engineer_features(df)
    y, perf_score = make_labels(feats)

    model, cols = build_model()

    X_train, X_test, y_train, y_test, ps_train, ps_test = train_test_split(
        feats[cols], y, perf_score,
        test_size=0.3, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    y_proba = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, y_proba)
    nova_scores = np.round(1000 * y_proba).astype(int)

    out = pd.DataFrame({
        "partner_id": feats.loc[X_test.index, "partner_id"],
        "performance_score": ps_test,
        "predicted_prob_good": y_proba,
        "nova_score": nova_scores,
        "actual_good_outcome": y_test
    })
    out.to_csv(Path(args.out), index=False)

    print(f"ROC-AUC: {auc:.3f}")
    print(f"Saved predictions to {args.out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--out", type=str, default="nova_scores.csv")
    args = parser.parse_args()
    main(args)
