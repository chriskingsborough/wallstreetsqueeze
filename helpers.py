import os
import yfinance
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from datetime import datetime, timedelta

from app import db

from models import *
from models_views import *

def fetch_index_prices():

    subquery = db.session.query(func.max(IndexPrices.date)).subquery()
    res = db.session.query(IndexPrices).filter(
        IndexPrices.date == subquery
    ).order_by(
        IndexPrices.previous_close.desc()
    ).all()
    return res

def fetch_stocks(collection):

    res = db.session.query(
        Collections, StockPrices, StockInfo
    ).join(
        Collections, StockPrices.ticker == Collections.ticker
    ).join(
        StockInfo, StockPrices.ticker == StockInfo.ticker, isouter=True
    ).filter(
        Collections.collection == collection
    ).order_by(
        Collections.ticker
    ).all()

    return res

def fetch_refresh_date():

    res = db.session.query(func.max(IndexPrices.date)).one()
    dt = res[0]
    if dt:
        # subtract a day because of the UTC offset
        dt = dt - timedelta(days=1)
        formatted_date = datetime.strftime(dt, '%B %-d, %Y')
    else:
        formatted_date = ""
    return formatted_date

def unique_list(_list):
    """Remove duplicate values in a list, retain order"""

    seen = set()
    results = list()
    for item in _list:
        if item not in seen:
            results.append(item)
            seen.add(item)

    return results

def add_ticker_to_db(ticker):

    collect = StockRequests(
        ticker=ticker
    )

    db.session.add(collect)
    db.session.commit()

    # TODO: add a new table which contains these guys
    # run a job every five minutes which will read from table
    # run refresh on stock info & price for that ticker
    # delete from the temp table
