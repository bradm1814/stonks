import math as m
import pandas as pd


def total_return(df):
    """
    grabs total return
    
    :param df: Description
    """

    #calculate total return
    final_equity = df["equity_curve"].iloc[-1] # grab the last value in the equity curve. this represents total return
    total_return = final_equity - 1 

    return total_return

def max_drawdown(df):
    #Shows over time the worst performances relative to the best performances. basically when you were losing money compared to your best
    df = df.copy()

    #calculate drawdown
    running_max = df["equity_curve"].cummax() #find the most recent peak
    df["drawdown"] = (df["equity_curve"] / running_max) - 1 # calculate each positions drawdown
    max_drawdown = df["drawdown"].min() # out of all the drawdowns return the worst one

    return max_drawdown

def sharpe_ratio(df):
    """
    Sharpe Ratio takes the average strategy return divided by the standard deviation of returns.
    It shows how much money is made on the wild side of trades. high numbers indicate return was created out of less volatile events, lower means the opposite
    
    :param df: Description
    """
    #calculate sharpe ratio
    sharpe = df["strategy_return"].mean() / df["strategy_return"].std() * m.sqrt(252)

    return sharpe

def number_of_trades(df):
    """
    Currently this only works for a long/short strategy. basically everytime the position flips it indicates a trade happened

    To switch to long only you would have to indicate a trade from 1 -> 0 not 1 -> -1
    
    :param df: Description
    """
    entries = (df["position"].shift() == 0) & (df["position"] != 0)
    return entries.sum()

    return number_of_trades

def win_rate(trades):
    wins = trades[trades["return"]>0] # positive trades
    return len(wins) / len(trades) #number of wins compared to total trades

def avg_win(trades):
    return trades[trades["return"]>0]["return"].mean() # average of trades > 0

def avg_loss(trades):
    return trades[trades["return"]<0]["return"].mean() # average of trades < 0

def profit_factor(trades):
    """
    profit factor is how much you make per dollar lost
    
    :param trades: Description
    """
    profit = trades[trades["return"]>0]["return"].sum() #total amount of dollars made
    loss = trades[trades["return"]<0]["return"].sum() #total amounts of dollars lost

    profit_factor = profit/abs(loss) #dollars made per dollars lost

    return profit_factor

def expectancy(trades):
    """
    expectancy is how much you would expect to make on any given trade.
    its probability of winning times the average win divided by the probability of losing times the average loss

    if you executed a trade at any given signal you could only statistically "expect" to make the expectancy of the model
    
    :param trades: Description
    """
    win = win_rate(trades) # grab win rate metric (probability win)
    loss = 1-win # create losses from 1 - wins (probability loss)
    aw = avg_win(trades) # grab avg win metric (average win)
    al = abs(avg_loss(trades)) # grab avg loss metric (average loss)

    return (win*aw)-(loss*al)

def average_trade_duration(trades):
    """
    on average how many days did you hold a position
    
    :param trades: Description
    """
    return trades["bars_held"].mean()

def max_consecutive_losses(trades):
    """
    longest losing streat
    
    :param trades: Description
    """
    losses = trades["return"] < 0 #returns boolean series where if a return was less than 0 it is True else False

    return losses.groupby((losses != losses.shift()).cumsum()).sum().max() # losses!- losses.shift() compares the initial series to a shifted series 1 value. cumsum counts values in that bucket. sum adds them up. max returns the highest one

def max_consecutive_wins(trades):
    """
    longest winning streak
    
    :param trades: Description
    """
    wins = trades["return"] > 0
    return wins.groupby((wins != wins.shift()).cumsum()).sum().max()







    
