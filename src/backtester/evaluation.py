from backtester import metrics

def evaluate_strategy(df, trades):

    """
    This function executes whatever metric you want to see 
    
    :param df: Description
    :param trades: Description
    """

    report = {} #empty dictionary for report

    #enact metrics and save to keys
    report["Total Return"] = metrics.total_return(df)
    report["Max Drawdown"] = metrics.max_drawdown(df)
    report["Sharpe Ratio"] = metrics.sharpe_ratio(df)
    report["Number of Trades"] = metrics.number_of_trades(df)
    report["Win Rate"] = metrics.win_rate(trades)
    report["Average Win"] = metrics.avg_win(trades)
    report["Average Loss"] = metrics.avg_loss(trades)
    report["Profit Factor"] = metrics.profit_factor(trades)
    report["Expectency"] = metrics.expectancy(trades)
    report["Average Trade Duration"] = metrics.average_trade_duration(trades)
    report["Max Consecutive Losses"] = metrics.max_consecutive_losses(trades)
    report["Max Consecutive Wins"] = metrics.max_consecutive_wins(trades)

    return report

def print_evaluation(report):
    print("\n=== Strategy Evaluation ===\n")
    for key, value in report.items():
        print(f"{key:25}: {value}")
    print("\n===========================\n")

