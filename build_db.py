import yfinance as yf
from src.db import SessionLocal, Price, init_db

def seed_data(ticker, start, end):
    """
    the seed_data function creates an empty SQL table from data pulled from Yahoo Finance
    
    :param ticker: ticker you would like to pull data for
    :param start: start date of desired time frame
    :param end: end date of desired time frame
    """
    df = yf.download(ticker, start=start, end=end) # create dataframe from yahoo finance data

    df.columns = [col[0] for col in df.columns] #sets first line of dataframe from the import to the column headers of the dataframe
    df = df.reset_index() # resets index after pulling the first item out and making it a header

    if df.empty: # safety just in case nothing is brought back
        print("No data returned")
        return

    session = SessionLocal() #create a session allowing a connection between the database and the engine created in db.py

    for row in df.itertuples(index=False): #iterate through each row of the dataframe and create a Price object for each row and then merge it to the table.
        record = Price(
            date=row.Date, #set the objects date to the value in the row. you do not need row["Date"] because of itertuples returning (Date=1-1-26)
            ticker=ticker,
            open=row.Open,
            high=row.High,
            low=row.Low,
            close=row.Close,
            volume=row.Volume

        )
        session.merge(record) #in this session merge all objects to the table

    session.commit() # commit the alterations to the actual table
    session.close() # close the session so no other changes are made

 
if __name__ == "__main__":

    #initiate the database and then seed it with data
    
    init_db()
    seed_data("AAPL", "2010-01-01", "2026-01-13")
    