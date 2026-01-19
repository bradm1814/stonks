from db import SessionLocal, Price
from sqlalchemy import select
import pandas as pd
import datetime as datetime

def load_ohlcv(ticker, start_date, end_date):

    #convert start date and end date to datetime
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)
    #open session
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
    rows = session.execute(query).scalars().all()

    #if empty return empty dataframe
    if not rows:
        return pd.DataFrame()

    #convert to DataFrame
    records = []

    for r in rows:
        records.append({
            "date": r.date,
            "high": r.high,
            "low": r.low,
            "open": r.open,
            "close": r.close,
            "volume": r.volume
        })
    df = pd.DataFrame(records)
    df = df.sort_values("date")
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    
    
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