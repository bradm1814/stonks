from sqlalchemy import Column, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base() #declaritive base creates an Object Relation Mapping that allows the class that inherits it's properties to be represented as a table. It is the tie
                          #between Python and SQL turning Python type language into SQL language

class Price(Base):
    __tablename__ = "Prices" #since Base is in there the Prices class knows that the created table is Prices

    date = Column(Date, primary_key = True)#declare date column. Works ensure unique values in rows but here it is paired with ticker to ensure only unique values between the two
    ticker = Column(String, primary_key = True)# columns can have the same date, they can have the same ticker, but they can never have the same date and ticker simultaneously
    open = Column(Float) #create a column for float
    high = Column(Float) #create a column for High
    low = Column(Float) #create a column for low
    close = Column(Float) #create a column for close
    volume = Column(Float) #create a column for volume

    def __repr__(self): #this is a magic method that when the class itself is called will automatically return this function if nothing else is asked for
        return f"<Price {self.ticker} {self.date}>" 

engine = create_engine("sqlite:///data/market_data.db") #the engine effectively knows how to talk to the database. it executes the SQL that is derived from code
SessionLocal = sessionmaker(bind=engine)#this creates an object that when called makes engages the engine to make a connection to the database and do work

def init_db():
    """
    This function creates a table instance of all ORM models. 
    if the tables already existed it would not overwrite them, only creating any new tables that were added
    """
    Base.metadata.create_all(engine)


