from src.database.data_loader import load_ohlcv
from src.ml.training import train_ml_model
from src.ml.signals import generate_directional_signals, generate_regression_signals
from src.ml.labeling import make_directional_labels, make_x_bar_future_labels
from src.ml.signal_generation import generate_ensemble_signals
from src.backtester.backtester import backtest
from backtester.trade_log import extract_trades
from backtester.evaluation import evaluate_strategy, print_evaluation

def time_series_split(df, train_ratio=0.8):
    n=len(df)
    split_idx = int(n * train_ratio)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    return train_df, test_df

def main():
    price_df = load_ohlcv("AAPL", "2015-01-01", "2026-01-01") # load data from database

    train_df, test_df = time_series_split(price_df, train_ratio=0.8) # split the data %80 train %20 test Allows for out of sample evaluation

    #create a directional predictor, train to predict whether the stock direction for the next day will be up or down
    dir_1bar_features, dir_model, dir_metrics, dir_path = train_ml_model(
        train_df,
        label_func = make_directional_labels,
        model_type = "xgb_class",
        model_name="directional_1bar",
        horizon=1)
    
    
    dir_1bar_features.to_csv("data/features/dir_1bar_features.csv")

    #Create a return predictor, train to predict the return at 5 days
    reg_5bar_features, reg5_model, reg5_metrics, reg5_path = train_ml_model(
        train_df,
        label_func= make_x_bar_future_labels,
        model_type="xgb_reg",
        model_name="5_bar_future",
        x=5
    )

    reg_5bar_features.to_csv("data/features/reg_5bar_features.csv")

    #Create a return predictor, train to predict the return at 10 days
    reg_10bar_features, reg10_model, reg10_metrics, reg10_path = train_ml_model(
        train_df,
        label_func= make_x_bar_future_labels,
        model_type="xgb_reg",
        model_name="5_bar_future",
        x=10
    )

    reg_10bar_features.to_csv("data/features/reg_10bar_features.csv")

    raw_signal_data, signals = generate_ensemble_signals(test_df, dir_path, reg5_path, reg10_path)

    raw_signal_data.to_csv("data/raw/raw_signal_data.csv")

    signals.to_csv("results/signals.csv")

    backtest_results = backtest(test_df, signals)

    backtest_results.to_csv("results/strategy_timeline.csv") #export the dataframe in the context of strategy to return

    trade_log = extract_trades(backtest_results) # this looks a every strategy position and extracts when and where trades were made

    trade_log.to_csv("results/trade_log.csv") #export out the trade log for interrogation

    report = evaluate_strategy(backtest_results, trade_log) #1 pager showing high level key metrics for strategy

    print_evaluation(report) #print it into the terminal

if __name__ == "__main__":
    main()
