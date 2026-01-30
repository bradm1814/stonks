from src.database.db import SessionLocal, Price
from sqlalchemy import select
import pandas as pd
import datetime as datetime

def load_ohlcv(ticker, start_date, end_date):

    """
    Once the database is seeded with data we then need to reach into the database to extract information we want to work with. this function does that
    
    :param ticker: ticker in question
    :param start_date: date from which you want to start grabbing information
    :param end_date: date from which you want to end grabbing information
    """

    #ensure that if a date is a string that it is converted to a datetime object
    if isinstance(start_date, str): 
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)
    
    #open a session as defined in db.py to interact directly with the database
    session = SessionLocal()

    #build query
    query = (
        select(Price)
        .where(Price.ticker == ticker)
        .where(Price.date >= start_date)
        .where(Price.date <= end_date)
        .order_by(Price.date.asc())
    )

    #execute
    rows = session.execute(query).scalars().all() #when the query is executed it returns Price objects in tuples, scalar() unpacks them, and all() turns them into a list

    #if empty return empty dataframe
    if not rows:
        return pd.DataFrame()

    #convert to DataFrame
    records = []

    for r in rows: # for each price object returned from the query we are appending an empty list containing its information
        records.append({
            "date": r.date,
            "high": r.high,
            "low": r.low,
            "open": r.open,
            "close": r.close,
            "volume": r.volume
        })
    df = pd.DataFrame(records) #after we go through each item we create a dataframe from the list
    df = df.sort_values("date") # sorts the created dataframe by date
    df["date"] = pd.to_datetime(df["date"])# could be redundant? we ensure this when that data is entered (Line 17)
    df = df.set_index("date") #removes date column and instead changes it to each rows index
    
    #ensures all values are set to what they need to be
    df = df.astype({
        "high": float,
        "low": float,
        "open": float,
        "close": float,
        "volume": float
        })

    #close session
    session.close()

    #return DF
    return df