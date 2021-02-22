from app import db
from sqlalchemy.dialects.postgresql import JSON, DATE, REAL

class Stocks(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String())
    date = db.Column(DATE)
    collection = db.Column(db.String())
    info = db.Column(JSON)

    def __init__(self, ticker, date, collection, info):
        self.ticker = ticker
        self.date = date
        self.collection = collection
        self.info = info

    def __repr__(self):
        return f"<id {self.id}>"

class Indices(db.Model):
    __tablename__ = 'indices'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String())
    name = db.Column(db.String())
    date = db.Column(DATE)
    previous_close = db.Column(REAL)
    close = db.Column(REAL)
    dollar_change = db.Column(REAL)
    decimal_change = db.Column(REAL)

class IndexTickers(db.Model):
    __tablename__ = 'index_tickers'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String())
    name = db.Column(db.String())
    active = db.Column(db.Integer)
    last_updated = db.Column(DATE)
