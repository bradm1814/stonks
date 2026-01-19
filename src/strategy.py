import re

def basic_strategy(df):
    df = df.copy()

    columns = df.columns

    ema_column = None
    rsi_column = None

    for col in columns:
        if re.match(r'ema_\d+', col):
            ema_column = col
        if re.match(r"rsi_\d+", col):
            rsi_column = col

    bullish_trend = df['close'] > df[ema_column]
    bearish_trend = df['close'] < df[ema_column]

    rsi_rising = df[rsi_column].diff() > 0
    rsi_falling = df[rsi_column].diff() < 0

    buy_condition = (bullish_trend & rsi_rising)
    sell_condition = (bearish_trend | rsi_falling)

    df["signal"] = 0
    df.loc[buy_condition, "signal"] = 1
    df.loc[sell_condition, "signal"] = -1

    df["position"] = df["signal"].replace(0, method="ffill")

    return df

