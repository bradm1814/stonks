import yfinance as yf
from src.db import SessionLocal, Price, init_db

def seed_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)

    df.columns = [col[0] for col in df.columns]
    df = df.reset_index()

    if df.empty:
        print("No data returned")
        return

    session = SessionLocal()

    for row in df.itertuples(index=False):
        record = Price(
            date=row.Date,
            ticker=ticker,
            open=row.Open,
            high=row.High,
            low=row.Low,
            close=row.Close,
            volume=row.Volume

        )
        session.merge(record)

    session.commit()
    session.close()

 
if __name__ == "__main__":
    init_db()
    seed_data("AAPL", "2010-01-01", "2026-01-13")
    