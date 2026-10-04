"""Trainable fit scorer with a reproducible synthetic bootstrap dataset."""

from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "fit_scorer.joblib"


def feature_vector(semantic: float, text: float, skill: float, experience: float, evidence: float) -> list[float]:
    return [semantic, text, skill, experience, evidence]


def train_bootstrap_model(path: Path = MODEL_PATH, seed: int = 42) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    features = rng.uniform(0, 1, size=(1200, 5))
    labels = np.clip(
        features[:, 0] * 0.38 + features[:, 1] * 0.12 + features[:, 2] * 0.30
        + features[:, 3] * 0.12 + features[:, 4] * 0.08 + rng.normal(0, 0.04, 1200), 0, 1
    )
    model = RandomForestRegressor(n_estimators=180, random_state=seed, min_samples_leaf=3, n_jobs=-1)
    model.fit(features, labels)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return {"model": "RandomForestRegressor", "samples": len(labels), "path": str(path), "source": "synthetic bootstrap"}


def train_labeled_model(csv_path: str, path: Path = MODEL_PATH, seed: int = 42) -> dict[str, object]:
    """Train on recruiter labels with columns: semantic,text,skill,experience,evidence,label."""
    import csv

    columns = ["semantic", "text", "skill", "experience", "evidence"]
    with open(csv_path, newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    missing = sorted(set(columns + ["label"]) - set(rows[0]) if rows else set(columns + ["label"]))
    if missing:
        raise ValueError(f"Training CSV is missing columns: {', '.join(missing)}")
    features = np.asarray([[float(row[column]) for column in columns] for row in rows])
    labels = np.asarray([float(row["label"]) for row in rows])
    model = RandomForestRegressor(n_estimators=240, random_state=seed, min_samples_leaf=2, n_jobs=-1)
    model.fit(features, labels)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return {"model": "RandomForestRegressor", "samples": len(rows), "path": str(path), "source": "recruiter labels"}


def _load_model():
    if not MODEL_PATH.exists():
        train_bootstrap_model()
    return joblib.load(MODEL_PATH)


def predict_fit(features: list[float]) -> float:
    return round(float(np.clip(_load_model().predict([features])[0] * 100, 0, 100)), 2)