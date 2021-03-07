import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from datetime import datetime
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from database.models import *

@app.route('/')
def home_page():

    indexes = fetch_index_prices()
    date = fetch_refresh_date()

    return render_template('index.html', indexes=indexes, refresh_date=date)

@app.route('/s_and_p_500')
def large_cap():

    stocks = fetch_stocks("S&P 500")
    date = fetch_refresh_date()

    return render_template('basic_stocks.html', title='S&P 500', stock_data=stocks, refresh_date=date)

@app.route('/dow_jones')
def dow_jones():

    stocks = fetch_stocks("Dow Jones")
    date = fetch_refresh_date()

    return render_template('basic_stocks.html', title='Dow Jones Industrial Average', stock_data=stocks, refresh_date=date)

@app.route('/nasdaq')
def nasdaq():

    stocks = fetch_stocks("Nasdaq 100")
    date = fetch_refresh_date()

    return render_template('basic_stocks.html', title='Nasdaq 100', stock_data=stocks, refresh_date=date)

@app.route('/medium_cap')
def medium_cap():

    stocks = fetch_stocks("S&P 400")
    date = fetch_refresh_date()

    return render_template('basic_stocks.html', title='S&P 400', stock_data=stocks, refresh_date=date)

@app.route('/small_cap')
def small_cap():

    stocks = fetch_stocks("S&P 600")
    date = fetch_refresh_date()

    return render_template('basic_stocks.html', title='S&P 600', stock_data=stocks, refresh_date=date)


@app.route('/high_short')
def high_short():

    stocks = fetch_stocks("High Short Interest")
    date = fetch_refresh_date()

    return render_template('high_short.html', stock_data=stocks, refresh_date=date)

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
        formatted_date = datetime.strftime(dt, '%B %-d, %Y')
    else:
        formatted_date = ""
    return formatted_date

if __name__ == "__main__":
    app.run()
