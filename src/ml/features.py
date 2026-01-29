import pandas as pd
from src import indicators
import numpy as np

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
    df = add_sma_features(df)
    df = add_ema_features(df)
    df = add_rsi_features(df, 7)
    df = add_rsi_features(df, 14)
    df = add_rsi_features(df, 20)
    df = add_return_features(df)
    df = add_volatility_features(df)
    df = add_trend_features(df)
    df = add_volume_features(df)
    df = add_regime_features(df)

    #select columns that will be used for features
    feature_cols = [col for col in df.columns if col not in ['date', 'future_return', 'label', 'close']]
    X = df[feature_cols]

    X = X.dropna()

    return X

def add_return_features(df):
    df = df.copy()

    # basic returns

    df['ret_1'] = df['close'].pct_change(1)
    df['ret_5'] = df['close'].pct_change(5)
    df['ret_10'] = df['close'].pct_change(10)
    df['ret_20'] = df['close'].pct_change(20)

    #rolling stats

    df["ret_mean_5"] = df["ret_1"].rolling(5).mean()
    df["ret_mean_20"] = df["ret_1"].rolling(20).mean()

    df["ret_median_20"] = df["ret_10"].rolling(20).median()

    df['ret_skew_20'] = df["ret_1"].rolling(20).skew()
    df['ret_kurt_20'] = df['ret_1'].rolling(20).kurt()

    return df

def add_sma_features(df):
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
    
    df[f"sma_5"] = df["close"].rolling(5).mean() # creates a column in the DF that is populated by the mean of the values returned from a "rolling" window across the data
    df[f"sma_20"] = df["close"].rolling(20).mean()
    df[f"sma_50"] = df["close"].rolling(50).mean()
    df[f"sma_100"] = df["close"].rolling(100).mean()
    df[f"sma_200"] = df["close"].rolling(200).mean()

    return df

def add_ema_features(df):
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
    df[f"ema_12"] = df["close"].ewm(span=12, adjust=False).mean()# creates a column in the DF that is populated by the mean of the values returned from a "rolling" window across the data giving more weight to more recent data
    df[f"ema_26"] = df["close"].ewm(span=26, adjust=False).mean()
    return df

def add_rsi_features(df,window):
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

def add_volatility_features(df):

    df = df.copy()

    df['vol_10'] = df['ret_1'].rolling(10).std()
    df['vol_20'] = df['ret_1'].rolling(20).std()
    df['vol_50'] = df['ret_1'].rolling(50).std()

    df['vol_ratio'] = df['vol_10']/df['vol_50']

    #ATR

    tr = np.maximum(df["high"] - df['low'], np.maximum(abs(df['high'] - df['low'].shift(1)), abs(df["low"] - df["close"].shift(1))))

    df["atr_14"] = tr.rolling(14).mean()

    return df

def add_trend_features(df):
    df = df.copy()

    # slopes (normalized)
    for col in ['ema_12', 'ema_26', 'sma_5', 'sma_20', 'sma_50', 'sma_100', 'sma_200']:
        df[f'{col}_slope'] = df[col].pct_change()

    # MACD lesser (12-26)
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    return df

def add_volume_features(df):
    df = df.copy()

    df['vol_z'] = (df["volume"] - df["volume"].rolling(20).mean()) / df["volume"].rolling(20).std()
    df['vol_pct'] = df["volume"].rank(pct=True)

    df['vol_atr_ratio'] = df["volume"] / df['atr_14']

    return df

def add_regime_features(df):
    df= df.copy()

    df["trend_regime"] = (df["ema_12"] > df["ema_26"]).astype(int)
    df["volume_regime"] = (df["vol_10"] > df["vol_50"]).astype(int)
    df["momentum_regime"] = (df["ret_20"] > 0).astype(int)

    return df
