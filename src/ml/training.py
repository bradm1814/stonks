import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib
from pathlib import Path

from src.ml.models import make_baseline_model
from src.ml.features import build_feature_matrix
from src.ml.labeling import make_directional_labels

def prepare_ml_dataset(price_df: pd.DataFrame):
    """
    This aligns the input X and the target y to a common index 'date' that are aligned based on the horizon used to generate direcitonal labels.
    Masks any values that are NaN
    
    :param price_df: Description
    :type price_df: pd.DataFrame
    """
    X = build_feature_matrix(price_df)
    y = make_directional_labels(price_df)

    # Align on index interstection

    common_index = X.index.intersection(y.index)
    X = X.loc[common_index]
    y = y.loc[common_index]

    # drop any remaining NaNs

    mask = X.notna().all(axis=1)
    X=X[mask]
    y=y[mask]

    return X,y

def train_baseline_directional_model(price_df, model_type="logistic", model_dir = "data/models"):
    X, y = prepare_ml_dataset(price_df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False #time series no random shuffle
    )

    model = make_baseline_model(model_type=model_type)
    model.fit(X_train, y_train)

    #basic metrics

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba > 0.5).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba)
    }

    # save model

    Path(model_dir).mkdir(parents=True, exist_ok=True)
    model_path = Path(model_dir) / f"directional_{model_type}.joblib"
    joblib.dump(model, model_path)

    return model, metrics, model_path

