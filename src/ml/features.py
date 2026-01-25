import pandas as pd
from src import indicators

def build_feature_matrix(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: price_df with OHLCV and calculated indicators
    Output: X_df with engineered Features, indexed by date

    # during development I wondered why i couldn't just use the prebuilt indicators df from main.py. It is because it is important to be able to control what parameters
    are allowed to be features in the ML
    
    :param market_data_df: Description
    """
    df = price_df.copy()

    # reuse indicators
    df = indicators.EMA(df)
    df = indicators.RSI(df)
    df = indicators.SMA(df)

    #select columns that will be used for features
    feature_cols = [col for col in df.columns if col not in ['date', 'future_return', 'label', 'close']]
    X = df[feature_cols]

    X = X.dropna()

    return X