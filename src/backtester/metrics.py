import math as m
import pandas as pd


def total_return(df):

    #calculate total return
    final_equity = df["equity_curve"].iloc[-1]
    total_return = final_equity - 1

    return total_return

def max_drawdown(df):

    df = df.copy()

    #calculate drawdown
    running_max = df["equity_curve"].cummax()
    df["drawdown"] = (df["equity_curve"] / running_max) - 1
    max_drawdown = df["drawdown"].min()

    return max_drawdown

def sharpe_ratio(df):
    #calculate sharpe ratio
    sharpe = df["strategy_return"].mean() / df["strategy_return"].std() * m.sqrt(252)

    return sharpe

def number_of_trades(df):
    
    changes = df["position"].diff()

    number_of_trades = (changes != 0).sum()

    return number_of_trades

def win_rate(trades):
    wins = trades[trades["return"]>0]
    return len(wins) / len(trades)

def avg_win(trades):
    return trades[trades["return"]>0]["return"].mean()

def avg_loss(trades):
    return trades[trades["return"]<0]["return"].mean()

def profit_factor(trades):
    profit = trades[trades["return"]>0]["return"].sum()
    loss = trades[trades["return"]<0]["return"].sum()

    profit_factor = profit/abs(loss)

    return profit_factor

def expectancy(trades):
    win = win_rate(trades)
    loss = 1-win
    aw = avg_win(trades)
    al = abs(avg_loss(trades))

    return (win*aw)-(loss*al)

def average_trade_duration(trades):
    return trades["bars_held"].mean()

def max_consecutive_losses(trades):
    losses = trades["return"] < 0
    return losses.groupby((losses != losses.shift()).cumsum()).sum().max()

def max_consecutive_wins(trades):
    wins = trades["return"] > 0
    return wins.groupby((wins != wins.shift()).cumsum()).sum().max()







    
