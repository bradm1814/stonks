import pandas as pd

def extract_trades(df):
    """
    After positions have been taken on the dataset and returns have been calculated this function extracts all trades that happened during the time frame
    
    :param df: dataframe that has positions over time calculated
    """
    trades = [] #create an empty list to store trades as dictionaries
    current_position = 0 #assume you start with no position
    entry_price = None #default
    entry_date = None #default

    for date, row in df.iterrows(): # loop through each row in the df
        pos = row["position"] # set variable for position to rows value
        price = row['close'] # set variable for price to rows value 

        #Entry: 0 -> 1 or 0 -> -1
        # this is always the beginning case 
        if current_position == 0 and pos != 0: # this is always the beginning case 
            current_position = pos #changes current pos to the position of the entry row
            entry_price = price # your entry price is equal to the initial entry row
            entry_date = date # your entry date is equal to the initial entry date
            continue

        # exit 1 -> 0 or -1 -> 0
        # this is where a position ends but doesn't flip. instead the position is closed 
        if current_position != 0 and pos == 0:
            exit_price = price # price at exit
            exit_date = date # exit date
            trade_return = (exit_price - entry_price) / entry_price * current_position #return whether short or long

            #append trade
            trades.append({
                "entry_date": entry_date,
                "exit_date": exit_date,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "direction": current_position,
                "return": trade_return,
                "bars_held": (exit_date - entry_date).days
            })

        # reset to base condition and go back through loop
            current_position = 0
            entry_price = None
            entry_date = None
            continue

    #Flip 1 -> -1 or -1 -> 1
        #this is a complete reversal we need to exit the position and enter into a new one
        if current_position != 0 and pos != 0 and pos != current_position:

            exit_price = price
            exit_date = date
            trade_return = (exit_price - entry_price) / entry_price * current_position #calculates returns for position left

            #append the trade
            trades.append({ 
                "entry_date": entry_date,
                "exit_date": exit_date,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "direction": current_position,
                "return": trade_return,
                "bars_held": (exit_date - entry_date).days
            })
            
            #carry new position
            current_position = pos 
            entry_price = price
            entry_date = date
            continue

    #close open trade at end of data

    #if the position is already 0 you don't have to close
    if current_position != 0:
        exit_price = df["close"].iloc[-1] # last row close price
        exit_date = df.index[-1] # last date (which is the index of the df)
        trade_return = (exit_price - entry_price) / entry_price * current_position # return at the last date

        #exit and append trade
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



