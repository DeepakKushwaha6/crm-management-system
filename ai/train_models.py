"""Train ML models with sample data."""

import os
import numpy as np
from pathlib import Path

MODELS_DIR = Path(__file__).parent.parent / 'models'
MODELS_DIR.mkdir(exist_ok=True)


def train_lead_scoring_model():
    """Train XGBoost lead scoring model with synthetic data."""
    try:
        from sklearn.ensemble import RandomForestClassifier
        import joblib

        np.random.seed(42)
        n_samples = 1000
        X = np.random.rand(n_samples, 5)
        y = (X[:, 0] * 0.3 + X[:, 1] * 0.25 + X[:, 2] * 0.2 + np.random.rand(n_samples) * 0.25 > 0.5).astype(int)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        joblib.dump(model, MODELS_DIR / 'lead_scoring_rf.joblib')
        print('Lead scoring model trained and saved.')
        return True
    except ImportError:
        print('ML libraries not available, using rule-based scoring.')
        return False


def train_churn_model():
    """Train churn prediction model."""
    try:
        from sklearn.ensemble import GradientBoostingClassifier
        import joblib

        np.random.seed(42)
        n_samples = 1000
        X = np.random.rand(n_samples, 4)
        y = (X[:, 0] < 0.3).astype(int)

        model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        joblib.dump(model, MODELS_DIR / 'churn_gb.joblib')
        print('Churn model trained and saved.')
        return True
    except ImportError:
        return False


if __name__ == '__main__':
    train_lead_scoring_model()
    train_churn_model()
