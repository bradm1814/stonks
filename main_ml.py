from src.data_loader import load_ohlcv
from src.ml.training import train_baseline_directional_model
from src.ml.signals import generate_directional_signals
from src.backtester.backtester import backtest
from backtester.trade_log import extract_trades
from backtester.evaluation import evaluate_strategy, print_evaluation

def main():
    price_df = load_ohlcv("AAPL", "2015-01-01", "2026-01-01")

    model, metrics, model_path = train_baseline_directional_model(price_df)
    print("ML metrics: ", metrics)

    signals = generate_directional_signals(price_df, model_path)
    backtest_results = backtest(price_df, signals)

    backtest_results.to_csv("data/raw/strategy_timeline.csv") #export the dataframe in the context of strategy to return

    trade_log = extract_trades(backtest_results) # this looks a every strategy position and extracts when and where trades were made

    trade_log.to_csv("data/raw/trade_log.csv") #export out the trade log for interrogation

    report = evaluate_strategy(backtest_results, trade_log) #1 pager showing high level key metrics for strategy

    print_evaluation(report) #print it into the terminal

if __name__ == "__main__":
    main()
