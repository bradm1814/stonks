from src.indicators import EMA, RSI, SMA

def indicator_pipeline(df, EMA_window = 20, SMA_window = 14, RSI_window = 20):
    """
    This pipeline brings all of the indicators together into a simple function without being too messy. quick in and out of indicators without changing main.py
    
    :param df: the dataframe containing stock information
    :param EMA_window: duration of time for calculations
    :param SMA_window: duration of time for calculations
    :param RSI_window: duration of time for calculations
    """
    df = EMA(df, EMA_window)
    df = RSI(df, RSI_window)
    df = SMA(df, SMA_window)

    return df