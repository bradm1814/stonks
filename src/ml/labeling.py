import pandas as pd

def make_directional_labels(price_df: pd.DataFrame, horizon: int=1) ->pd.Series:
    """
    Binary label: 1 if future return over horizon days > 0, else 0.
    Assumes price_df has ['date', 'close']
    
    :param price_df: Description
    :type price_df: pd.DataFrame
    :param horizon: Description
    :type horizon: int
    :return: Description
    :rtype: Series[Any]
    """
    df = price_df.copy()
    df = df.sort_values('date')
    df['future_return'] = df['close'].shift(-horizon) / df['close'] - 1
    df['label'] = (df['future_return']>0).astype(int)
    labels = df['label']

    # drop last horizon rows with NaN future_return

    labels = labels.iloc[:-horizon]
    return labels