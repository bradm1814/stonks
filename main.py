import pandas as pd
from pipelines import indicator_pipeline
from data_loader import load_ohlcv
from strategy import basic_strategy
from backtester.backtester import backtest
from backtester.trade_log import extract_trades
from backtester.evaluation import evaluate_strategy, print_evaluation


if __name__ == "__main__":

    df = load_ohlcv("AAPL", "2015-01-01", "2026-01-01")

    df = indicator_pipeline(df)

    df = basic_strategy(df)

    df = backtest(df)

    df.to_csv("data/raw/strategy_timeline.csv")

    trade_log = extract_trades(df)

    trade_log.to_csv("data/raw/trade_log.csv")

    report = evaluate_strategy(df, trade_log)

    print_evaluation(report)

    pd.DataFrame([report]).to_csv("data/raw/evaluation.csv")





    
    

    

    
    


