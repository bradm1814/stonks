import pandas as pd
from pipelines import indicator_pipeline
from data_loader import load_ohlcv
from strategy import basic_strategy
from backtester.backtester import backtest
from backtester.trade_log import extract_trades
from backtester.evaluation import evaluate_strategy, print_evaluation


if __name__ == "__main__":

    df = load_ohlcv("AAPL", "2015-01-01", "2026-01-01") #load in data from database

    df = indicator_pipeline(df) #calculate indicators of stock price to set up to enact strategy

    df = basic_strategy(df) #develops positions from indicators

    df = backtest(df) #calculate returns, strategy returns, equity curve, and drawdown

    df.to_csv("data/raw/strategy_timeline.csv") #export the dataframe in the context of strategy to return to a csv

    trade_log = extract_trades(df) # this looks a every strategy position and extracts when and where trades were made

    trade_log.to_csv("data/raw/trade_log.csv") #export out the trade log for interrogation

    report = evaluate_strategy(df, trade_log) #1 pager showing high level key metrics for strategy

    print_evaluation(report) #print it into the terminal

    pd.DataFrame([report]).to_csv("data/raw/evaluation.csv") #export for posterity





    
    

    

    
    


