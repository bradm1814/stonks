import pandas as pd

def extract_trades(df):
    trades = []
    current_position = 0
    entry_price = None
    entry_date = None

    for date, row in df.iterrows():
        pos = row["position"]
        price = row['close']

        #Entry: 0 -> 1 or 0 -> -1

        if current_position == 0 and pos != 0:
            current_position = pos
            entry_price = price
            entry_date = date
            continue

        # exit 1 -> 0 or -1 -> 0

        if current_position != 0 and pos == 0:
            exit_price = price
            exit_date = date
            trade_return = (exit_price - entry_price) / entry_price * current_position

            trades.append({
                "entry_date": entry_date,
                "exit_date": exit_date,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "direction": current_position,
                "return": trade_return,
                "bars_held": (exit_date - entry_date).days
            })

        # reset
            current_position = 0
            entry_price = None
            entry_date = None
            continue

    #Flip 1 -> -1 or -1 -> 1

        if current_position != 0 and pos != 0 and pos != current_position:
            #exit old trade

            exit_price = price
            exit_date = date
            trade_return = (exit_price - entry_price) / entry_price * current_position

            trades.append({
                "entry_date": entry_date,
                "exit_date": exit_date,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "direction": current_position,
                "return": trade_return,
                "bars_held": (exit_date - entry_date).days
            })
            current_position = pos
            entry_price = price
            entry_date = date
            continue

        #OPTIONAL: close open trade at end of data
    if current_position != 0:
        exit_price = df["close"].iloc[-1]
        exit_date = df.index[-1]
        trade_return = (exit_price - entry_price) / entry_price * current_position

        trades.append({
            "entry_date": entry_date,
            "exit_date": exit_date,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "direction": current_position,
            "return": trade_return,
            "bars_held": (exit_date - entry_date).days
        })
    
    return pd.DataFrame(trades)



