import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    r2_score,
    mean_squared_error,
    confusion_matrix
)

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def prepare_data(df, target_column):
    df = df.copy()

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Encode categorical features
    X = pd.get_dummies(X, drop_first=True)

    # Encode target if categorical
    if y.dtype == "object":
        le = LabelEncoder()
        y = le.fit_transform(y)

    return train_test_split(X, y, test_size=0.2, random_state=42)


def detect_task(y):
    if y.dtype == "object":
        return "Classification"

    if y.nunique() <= 10:
        return "Classification"

    return "Regression"


def train_classification_models(X_train, X_test, y_train, y_test):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier()
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="weighted")
        cm = confusion_matrix(y_test, preds)

        results[name] = {
            "Model": model,
            "Accuracy": round(acc, 4),
            "F1 Score": round(f1, 4),
            "Confusion Matrix": cm
        }

    return results


def train_regression_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor()
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        r2 = r2_score(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))

        results[name] = {
            "Model": model,
            "R2 Score": round(r2, 4),
            "RMSE": round(rmse, 4)
        }

    return results