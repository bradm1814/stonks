import joblib
import pandas as pd
from src.ml.features import build_feature_matrix

def generate_ensemble_signals(
        price_df: pd.DataFrame,
        dir_model_path: str,
        reg5_model_path: str,
        reg10_model_path: str,
        prob_threshold: float=0.55,
        return_threshold: float=0.0
) -> pd.Series:
    """
    Generate long-only ensemble signals using both:
    - a directional classifier (probability of positive return)
    - a regression model (predicted magnitude of return)
    """

    df = price_df.copy()

    #load models
    dir_model = joblib.load(dir_model_path)
    reg5_model = joblib.load(reg5_model_path)
    reg10_model = joblib.load(reg10_model_path)

    #build_features
    X = build_feature_matrix(df)

    #align feature matrix with price_df
    df = df.loc[X.index]

    df['prob_up'] = dir_model.predict_proba(X)[:, 1]
    df['predicted_return_5_bar'] = reg5_model.predict(X)
    df['predicted_return_10_bar'] = reg10_model.predict(X)

    #ensemble logic

    df["ensemble_score"] = (
        0.5 *df["prob_up"] +
        0.3 *df['predicted_return_5_bar'] +
        0.2 *df['predicted_return_10_bar']
    )

    df["signal"] = (df["ensemble_score"]>0).astype(int)

    #backtester wants position
    df['position'] = df['signal']
    return df , df['position']