import pandas as pd
import joblib

def generate_directional_signals(price_df: pd.DataFrame, model_path, threshold: float = 0.55):
    from src.ml.features import build_feature_matrix

    model = joblib.load(model_path)
    X = build_feature_matrix(price_df)

    # align with model training features (in practice, store feature list)

    y_proba = model.predict_proba(X)[:, 1]
    signals = (y_proba > threshold).astype(int)

    signals = pd.Series(signals, index=X.index, name="signal")

    return signals