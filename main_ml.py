from src.data_loader import load_ohlcv
from src.ml.training import train_ml_model
from src.ml.signals import generate_directional_signals, generate_regression_signals
from src.ml.labeling import make_directional_labels, make_x_bar_future_labels
from src.ml.signal_generation import generate_ensemble_signals
from src.backtester.backtester import backtest
from backtester.trade_log import extract_trades
from backtester.evaluation import evaluate_strategy, print_evaluation

def main():
    price_df = load_ohlcv("AAPL", "2015-01-01", "2026-01-01")

    dir_model, dir_metrics, dir_path = train_ml_model(
        price_df,
        label_func = make_directional_labels,
        model_type = "classification",
        model_name="directional_1bar",
        horizon=1)
    
    reg_model, reg_metrics, reg_path = train_ml_model(
        price_df,
        label_func= make_x_bar_future_labels,
        model_type="regression",
        model_name="5_bar_future",
        x=5
    )

    signals = generate_ensemble_signals(price_df, dir_path, reg_path)

    backtest_results = backtest(price_df, signals)

    backtest_results.to_csv("data/raw/strategy_timeline.csv") #export the dataframe in the context of strategy to return

    trade_log = extract_trades(backtest_results) # this looks a every strategy position and extracts when and where trades were made

    trade_log.to_csv("data/raw/trade_log.csv") #export out the trade log for interrogation

    report = evaluate_strategy(backtest_results, trade_log) #1 pager showing high level key metrics for strategy

    print_evaluation(report) #print it into the terminal

if __name__ == "__main__":
    main()
