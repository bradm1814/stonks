from data_loader import load_ohlcv

def SMA(df, window=20):
    """
    Docstring for smi

    Simple Moving Average

    returns simple moving average over a given period of time
    What it is
    A straight arithmetic average of the last n closing prices.
    What it reveals
    - The overall trend direction
    - A smoothed version of price that filters out noise
    - Where price sits relative to its recent history
    How traders use it
    - Price above SMA → bullish environment
    - Price below SMA → bearish environment
    - Crossovers (e.g., SMA50 crossing SMA200) → trend shifts
    Mental model
    Think of SMA as a low‑pass filter in signal processing.
    It removes high‑frequency noise and leaves the underlying trend.

    :param df: df returned from ohlcv query sorted in date order with most recent first
    :param window: Window of time (days)
    """
    
    df[f"sma_{window}"] = df["close"].rolling(window).mean() # creates a column in the DF that is populated by the mean of the values returned from a "rolling" window across the data

    return df
def EMA(df, window=20):
    """
    Docstring for EMA

    Exponential moving average

    returns the exponential moving average over a given period

    What it is
    A moving average that gives more weight to recent prices.
    Instead of treating all 20 days equally (like SMA), EMA says:
    - Yesterday matters more than last week
    - Last week matters more than last month
    Mathematically, it uses an exponential decay factor.
    What it reveals
    - Trend direction, but more responsive than SMA
    - Faster reaction to reversals
    - Better for short‑term trading or momentum strategies
    How traders use it
    - EMA12 and EMA26 are the backbone of MACD
    - EMA crossovers generate faster signals than SMA
    - Price crossing EMA often signals momentum shifts

    :param df: df returned from ohlcv query sorted in date order with most recent first
    :param window: window of time
    """
    
    df[f"ema_{window}"] = df["close"].ewm(span=window, adjust=False).mean()# creates a column in the DF that is populated by the mean of the values returned from a "rolling" window across the data giving more weight to more recent data

    return df

def RSI(df, window=14):
    """

    Docstring for RSI

    Relative Strength Index

    What it is
    A momentum oscillator that measures the speed and magnitude of recent price changes.
    It outputs a value between 0 and 100.
    - Above 70 → overbought
    - Below 30 → oversold
    RSI is based on the ratio of average gains to average losses over the last n periods (usually 14).
    What it reveals
    - Momentum strength
    - Whether price is stretched too far in one direction
    - Potential reversal zones
    How traders use it
    - Buy when RSI crosses above 30
    - Sell when RSI crosses below 70
    - Divergences (price makes new high but RSI doesn’t) signal weakening momentum

    :param df: df returned from ohlcv query sorted in date order with most recent first
    :param window: window of time
    """

    #calculate price changes day to previous day
    delta = df["close"].diff() 

    #gains postive deltas and losess negative deltas

    gain = delta.clip(lower=0) #captures only the positive values in the series
    loss = -delta.clip(upper=0) #captures only the negative values in the series

    #Wilder's Smoothing (EMA with adjsut-False)

    avg_gain = gain.ewm(alpha=1/window, adjust=False).mean() # These take the gains made in a given window and attempt to smooth the erratic outliers
    avg_loss = loss.ewm(alpha=1/window, adjust=False).mean()

    #relative strength
    rs = avg_gain / avg_loss #a measure of the prices strength in a given window. higher values mean oversold and could reverse while lower values mean oversold and could reverse 

    #RSI formula
    df[f"rsi_{window}"] = 100 - (100/(1+rs))

    return df