import re

def basic_strategy(df):
    """
    this function creates positions from the inidicator data that has been appended to the initial stock price data
    
    :param df: dataframe with initial stock information AND indicator data appended
    """
    df = df.copy() # copy DF

    columns = df.columns # create a variable to contain header names

    ema_column = None #initiate a variable for an ema column and set it to none
    rsi_column = None #initiate a variable for an rsi column and set it to none

    #This checks for the name of ema and rsi column in the df. the window may have changed for calculations so it keeps it variable
    for col in columns:
        if re.match(r'ema_\d+', col):
            ema_column = col
        if re.match(r"rsi_\d+", col):
            rsi_column = col

    bullish_trend = df['close'] > df[ema_column] #define bearish or bullish based on ema_column
    bearish_trend = df['close'] < df[ema_column]

    rsi_rising = df[rsi_column].diff() > 0 # this determines if rsi is rising or falling from one day to the next
    rsi_falling = df[rsi_column].diff() < 0

    buy_condition = (bullish_trend & rsi_rising) # if there is a bullish trend AND momentum is rising it is a buy condition
    sell_condition = (bearish_trend | rsi_falling) # if there is a bearish trend or momentum is falling it is a short condition

    df["signal"] = 0 #initiate a signal at 0
    df.loc[buy_condition, "signal"] = 1 # for every condition where buy_condition is true, signal a buy position
    df.loc[sell_condition, "signal"] = -1 # for every condition where sell condition is true, signal a short position

    df["position"] = df["signal"].replace(0, method = "ffill")#this creates a position column and defaults it to the values of the signal column. 
                                                              #Then it takes any zeroes carried over from the signal column and "ffill" forward fills it with the last non zero number

    return df

