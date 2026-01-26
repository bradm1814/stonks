import joblib
import pandas as pd
from src.ml.features import build_feature_matrix

def generate_ensemble_signals(
        price_df: pd.DataFrame,
        dir_model_path: str,
        reg_model_path: str,
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
    reg_model = joblib.load(reg_model_path)

    #build_features
    X = build_feature_matrix(df)

    #align feature matrix with price_df
    df = df.loc[X.index]

    df['prob_up'] = dir_model.predict_proba(X)[:, 1]
    df['predicted_return'] = reg_model.predict(X)

    #ensemble logic

    df["signal"] = 0
    df.loc[
        (df["prob_up"] > prob_threshold) &
        (df["predicted_return"]>return_threshold),
        "signal",
    ] = 1

    #backtester expects 'position'

    df['position'] = df['signal']

    return df['position']