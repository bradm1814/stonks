from src.indicators import EMA, RSI, SMA

def indicator_pipeline(df, EMA_window = 20, SMA_window = 14, RSI_window = 20):
    df = EMA(df, EMA_window)
    df = RSI(df, RSI_window)
    df = SMA(df, SMA_window)

    return df