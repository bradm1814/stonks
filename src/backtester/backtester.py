

def backtest(df):

    df = df.copy()

    #calculate return from previous close to today's close
    df["return"] = df["close"].pct_change()

    # apply position based on yesterday's signal
    df["strategy_return"] = df["position"].shift(1) * df["return"]

    #build equity curve
    df["equity_curve"] = (1 + df["strategy_return"]).cumprod()

    #calculate drawdown
    running_max = df["equity_curve"].cummax()
    df["drawdown"] = (df["equity_curve"] / running_max) - 1

    return df


