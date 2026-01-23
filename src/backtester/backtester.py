

def backtest(df):

    """
    runs positions taken during strategy back through data and calculates how the strategy performed over the interval.
    
    :param df: dataframe produced after running strategy across data
    """

    df = df.copy()

    #calculate return from previous close to today's close
    df["return"] = df["close"].pct_change() # the return value for each day is calculated by the difference in percentage

    # apply position based on yesterday's signal
    df["strategy_return"] = df["position"].shift(1) * df["return"] # this aligns positions that were based off of yesterdays data with the actual data to show what the strategy returned that day

    #build equity curve
    df["equity_curve"] = (1 + df["strategy_return"]).cumprod() #the equity curve shows performance over time, probably the most important factor. It takes the cumulative product of your strategies return

    #calculate drawdown
    running_max = df["equity_curve"].cummax()
    df["drawdown"] = (df["equity_curve"] / running_max) - 1 #this takes the most recent maximum and the compares how much your strategy is underwater relative to that maximum

    return df


