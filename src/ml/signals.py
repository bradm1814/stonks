import pandas as pd
import joblib
from src.ml.features import build_feature_matrix

def generate_directional_signals(price_df: pd.DataFrame, model_path, threshold: float = 0.55):

    model = joblib.load(model_path)
    X = build_feature_matrix(price_df)

    # align with model training features (in practice, store feature list)

    y_proba = model.predict_proba(X)[:, 1]
    signals = (y_proba > threshold).astype(int)

    signals = pd.Series(signals, index=X.index, name="signal")

    return signals

def generate_regression_signals(price_df: pd.DataFrame, model_path: str, threshold: float = 0.0):
    """
    Generate long-only trading signals using a regression model that predicts
    future returns (e.g., 5-bar future return).

    :param price_df: OHLCV price data
    :param model_path: path to the saved regression model (.joblib)
    :param threshold: minimum predicted return required to go long
    """

    df = price_df.copy()

    #load model
    model = joblib.load(model_path)

    #build feature matrix

    X = build_feature_matrix(df)

    #predict future returns
    df["predicted_return"] = model.predict(X)

    # Long only Signal
    df["signal"] = 0
    df.loc[df["predicted_return"]>threshold, "signal"] = 1

    #align with backtester expectations
    df["position"] = df["signal"]

    return df
