import os
from flask import Flask, render_template, Markup
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

    text = Markup("""
    <p>The S&P 500 is a stock market index consisting of 500 of the largest
    US companies. Along with the Dow Jones and Nasdaq Composite it is one of the
    most commonly followed stock indices.</p>
    """)

    stocks = fetch_stocks("S&P 500")
    date = fetch_refresh_date()

    return render_template(
        'basic_stocks.html',
        title='S&P 500',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/dow_jones')
def dow_jones():

    text = Markup("""
    <p>The Dow Jones Industrial Average, Dow Jones, or simply the Dow, is a
    stock market index that measures the stock performance of 30 large companies
    listed on stock exchanges in the United States.</p>
    """)

    stocks = fetch_stocks("Dow Jones")
    date = fetch_refresh_date()

    return render_template(
        'basic_stocks.html',
        title='Dow Jones Industrial Average',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/nasdaq')
def nasdaq():

    text = Markup("""
    <p>The NASDAQ-100 is a stock market index made up of the largest non-financial
    companies listed on the Nasdaq stock market. It is the most technology oriented of
    the major indices.</p>
    """)

    stocks = fetch_stocks("Nasdaq 100")
    date = fetch_refresh_date()

    return render_template(
        'basic_stocks.html',
        title='Nasdaq 100',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/medium_cap')
def medium_cap():

    text = Markup(
        """
        <p>The S&P 400 MidCap index seeks to track the performance of medium cap
        US companies. To be included on the index, a consituent must have a market cap
        between $3.2 and $9.8 billion at time of addition. The median market cap
        is $4.67 billion.</p>
        """
    )
    stocks = fetch_stocks("S&P 400")
    date = fetch_refresh_date()

    return render_template(
        'basic_stocks.html',
        title='S&P 400 MidCap',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/small_cap')
def small_cap():

    text = Markup(
        """The S&P 600 SmallCap index seeks to track the performance of small cap
        US companies. To be included, a consituent must have a market cap between
        $700 million and $3.2 billion at time of addition.
        """
    )
    stocks = fetch_stocks("S&P 600")
    date = fetch_refresh_date()

    return render_template(
        'basic_stocks.html',
        title='S&P 600 SmallCap',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/high_short')
def high_short():

    stocks = db.session.query(
        HighShortInterest
    ).filter(
        HighShortInterest.presShortPercentFloat > .20
    ).all()
    date = fetch_refresh_date()

    text = Markup(
        """<p>The High Short Interest collection contains stocks which have a significantly high
        short interest ratio. For this collection, stock were identified which have a short interest
        ratio greater than 10% of outstanding shares and 20% of floating shares.<br>
        Stocks with high short interest ratios are known for explosive upside movies due to
        short squeezes. A short squeeze is where a stock sees rapid upwards price pressure due
        to short sellers being forced to cover their shorts. The most famous example of this is
        of course GameStop.
        <br>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'high_short.html',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/dogs_of_the_dow')
def dogs_of_the_dow():

    stocks = db.session.query(
        DowDogs
    ).all()
    date = fetch_refresh_date()

    text = Markup(
        """<p>
        The Dogs of the Dow are the ten companies of the Dow Jones Industrial Average
        which have the highest dividend yields. The Small Dogs of the Dow is a subset
        of these companies, representing the five constituents with the highest dividend
        yields.<br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'dogs_of_the_dow.html',
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/high_dividend')
def high_dividend():

    stocks = db.session.query(
        HighDividend
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'High Dividend Stocks'

    text = Markup(
        """
        <p>
        This collection includes the 25 highest dividend yield stocks across all major indices.
        Many of these companies are REIT or Real Estate Investments Trusts. While REITs can be a great
        source of investment income, there are also some key differences between REITs and other equities.
        If you wish to find high dividend yield stock excluding REITs, please see our collection <strong>High Dividend ex REITs</strong>. <br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'dividend_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/high_dividend_no_reit')
def high_dividend_sans_reit():

    stocks = db.session.query(
        HighDividendSansReit
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'High Dividend Stocks excluding REITs'

    text = Markup(
        """
        <p>
        This collection includes the 25 highest dividend yield stocks across all major indices, excluding REITs.
        If you wish to find high dividend yield stock including REITs, please see our collection <strong>High Dividend</strong>. <br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'dividend_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/runners')
def runners():

    stocks = db.session.query(
        Runners
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Runners'

    text = Markup(
        """
        <p>
        The Runners collection contains stocks which are above both their 50 and 200 day moving averages, and
        where the 50 day moving average is higher than the 200 day moving average. This collection
        provide insight into which stocks are moving higher. Some investors believe stocks that are on
        a run will continue to move higher. <br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'momentum_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/dippers')
def dippers():

    stocks = db.session.query(
        Dippers
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Dippers'

    text = Markup(
        """
        <p>
        The Dippers collection contains stocks which are below both their 50 and 200 day moving averages.
        This collection provide insight into which stocks are currently dipping.
        For some stocks, this may represent a good buying opportunity, before the
        price moves higher again. On the other hand, there may be a fundamental issue
        dragging the stock price lower, and it may continue to lose value. <br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'momentum_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/52_week_high')
def fifty_two_week_high():

    stocks = db.session.query(
        PriceRangeHigh
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Top of Price Range'

    text = Markup(
        """
        <p>
        The Top of Price range collection contains stocks which are at the top of their
        52 week price range.<br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'price_range.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/52_week_low')
def fifty_two_week_low():

    stocks = db.session.query(
        PriceRangeLow
    ).limit(50).all()
    date = fetch_refresh_date()
    title = 'Bottom of Price Range'

    text = Markup(
        """
        <p>
        The Bottom of Price range collection contains stocks which are at the bottom of their
        52 week price range.<br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'price_range.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

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
