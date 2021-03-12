import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from datetime import datetime

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *
from models_views import *

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

    stocks = db.session.query(
        HighShortInterest
    ).filter(
        HighShortInterest.presShortPercentFloat > .20
    ).all()
    date = fetch_refresh_date()

    return render_template('high_short.html', stock_data=stocks, refresh_date=date)

@app.route('/dogs_of_the_dow')
def dogs_of_the_dow():

    stocks = db.session.query(
        DowDogs
    ).all()
    date = fetch_refresh_date()

    return render_template('dogs_of_the_dow.html', stock_data=stocks, refresh_date=date)

@app.route('/high_dividend')
def high_dividend():

    stocks = db.session.query(
        HighDividend
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'High Dividend Stocks'

    return render_template('dividend_stocks.html', title=title, stock_data=stocks, refresh_date=date)

@app.route('/high_dividend_no_reit')
def high_dividend_sans_reit():

    stocks = db.session.query(
        HighDividendSansReit
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'High Dividend Stocks excluding REITs'

    return render_template('dividend_stocks.html', title=title, stock_data=stocks, refresh_date=date)

@app.route('/runners')
def runners():

    stocks = db.session.query(
        Runners
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Runners'

    return render_template('momentum_stocks.html', title=title, stock_data=stocks, refresh_date=date)

@app.route('/dippers')
def dippers():

    stocks = db.session.query(
        Dippers
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Dippers'

    return render_template('momentum_stocks.html', title=title, stock_data=stocks, refresh_date=date)

@app.route('/52_week_high')
def fifty_two_week_high():

    stocks = db.session.query(
        PriceRangeHigh
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Top of Price Range'

    return render_template('price_range.html',  title=title, stock_data=stocks, refresh_date=date)

@app.route('/52_week_low')
def fifty_two_week_low():

    stocks = db.session.query(
        PriceRangeLow
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Bottom of Price Range'


    return render_template('price_range.html',  title=title, stock_data=stocks, refresh_date=date)

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
