# app/model.py
# This module handles model loading and prediction for the Iris classifier.

from __future__ import annotations
from typing import Sequence, List, Tuple
import joblib
import numpy as np


class IrisModel:
    """
    Wraps the trained scikit-learn Logistic Regression model for Iris.
    - Loads the artifact saved by the training notebook
    - Exposes simple predict methods for single and batch inputs
    """

    def __init__(self, model_path: str):
        # Load model and metadata (feature names, labels, version)
        blob = joblib.load(model_path)
        self.model = blob["model"]
        self.feature_names = list(blob["feature_names"])
        self.class_labels = list(blob["class_labels"])
        self.version = str(blob.get("model_version", "1.0"))

    def predict_one(self, features: Sequence[float]) -> Tuple[str, float]:
        """
        features: a list/tuple of exactly 4 floats (Iris feature order).
        returns: (label_name, max_probability)
        """
        x = np.asarray(features, dtype=float).reshape(1, -1)
        probs = self.model.predict_proba(x)[0]
        idx = int(np.argmax(probs))
        label = self.class_labels[idx]
        return label, float(probs[idx])

    def predict_many(self, batch: List[Sequence[float]]) -> List[Tuple[str, float]]:
        """
        batch: list of multiple feature arrays (each with 4 numbers)
        returns: list of (label_name, probability)
        """
        X = np.asarray(batch, dtype=float)
        probs = self.model.predict_proba(X)
        idxs = np.argmax(probs, axis=1)
        results: List[Tuple[str, float]] = []
        for row, idx in enumerate(idxs):
            label = self.class_labels[int(idx)]
            results.append((label, float(probs[row, idx])))
        return results
