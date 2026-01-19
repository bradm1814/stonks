from sqlalchemy import Column, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

class Price(Base):
    __tablename__ = "Prices"

    date = Column(Date, primary_key = True)
    ticker = Column(String, primary_key = True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    def __repr__(self):
        return f"<Price {self.ticker} {self.date}>"

engine = create_engine("sqlite:///data/market_data.db")
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)


