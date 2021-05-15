import os
from flask import Flask, flash, render_template, Markup, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy import or_
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from helpers import *
from models import *
from models_views import *

@app.route('/')
def home_page():

    indexes = fetch_index_prices()
    date = fetch_refresh_date()

    return render_template('index.html', indexes=indexes, refresh_date=date)

@app.route('/indexes')
def index_overview():

    indexes = fetch_index_prices()
    date = fetch_refresh_date()

    return render_template('indexes_overview.html', indexes=indexes, refresh_date=date)


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
        meta=text,
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
        $700 million and $3.2 billion at time of addition.</p>
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
        short interest ratio. High short interest stocks were identified by filtering for short interest
        ratios greater than 10% of outstanding shares and 20% of floating shares.<br>
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

@app.route('/high_dividend_stocks')
def high_dividend_sans_reit():

    stocks = db.session.query(
        HighDividendStocks
    ).filter(
        HighDividendStocks.marketCap > 500000000
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'High Dividend Stocks'

    text = Markup(
        """
        <p>
        This collection includes the 25 highest dividend yield stocks across all major indices, excluding REITs.
        If you wish to find high dividend yield REITs, please see our collection <strong>High Dividend REITs</strong>. <br/>
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

@app.route('/high_dividend_reits')
def high_dividend():

    stocks = db.session.query(
        HighDividendReits
    ).filter(
        HighDividendReits.marketCap > 500000000
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'High Dividend REITs'

    text = Markup(
        """
        <p>
        This collection includes the 25 highest dividend yield REITs. While REITs can be a great
        source of investment income, there are also some key differences between REITs and other equities.
        If you wish to find high dividend yield stocks excluding REITs, please see our collection <strong>High Dividend Stocks</strong>. <br/>
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
    title = 'Above Averages'

    text = Markup(
        """
        <p>
        This collection contains stocks which are above both their 50 and 200 day moving averages, and
        where the 50 day moving average is higher than the 200 day moving average. This collection
        provides insight into which stocks are moving higher. Some investors believe stocks that are on
        a run will continue to go up. Of course, they could also go the other way and
        retreat back towards their long term averages.<br/>
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
    title = 'Below Averages'

    text = Markup(
        """
        <p>
        This collection contains stocks which are below both their 50 and 200 day moving averages.
        This collection provides insight into which stocks are currently dipping.
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
    title = '52 Week High'

    meta = """
        This collection contains stocks at or near their 52 Week High. 52 Weeks Highs are
        updated on a weekly basis, so stocks may cross above their previous 52 Week High.
        These cases represent a fresh 52 Week High and will be reflected in the next update.
    """

    text = Markup(
        """
        <p>
        This collection contains stocks at or near their 52 Week High. 52 Weeks Highs are
        updated on a weekly basis, so stocks may cross above their previous 52 Week High.
        These cases represent a fresh 52 Week High and will be reflected in the next update.<br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'price_range.html',
        title=title,
        meta=meta,
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
    title = '52 Week Low'

    meta = """
        This collection contains stocks at or near their 52 Week Low. 52 Weeks Lows are
        updated on a weekly basis, so stocks may cross below their previous 52 Week Low.
        These cases represent a fresh 52 Week Low and will be reflected in the next update.
    """

    text = Markup(
        """
        <p>
        This collection contains stocks at or near their 52 Week Low. 52 Weeks Lows are
        updated on a weekly basis, so stocks may cross below their previous 52 Week Low.
        These cases represent a fresh 52 Week Low and will be reflected in the next update.<br/>
        Please note, while we do our best to provide accurate information, you should always double check
        and verify this information yourself prior to making any investment decisions.
        </p>
        """
    )

    return render_template(
        'price_range.html',
        title=title,
        meta=meta,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/pe_under_fifteen')
def pe_under_fifteen():

    stocks = db.session.query(
        PEUnderFifteen
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'PE Under Fifteen'

    text = Markup(
        """
        This collection contains stocks with lower Price to Earnings Ratios. A
        lower PE Ratio means that investors are willing to pay less for a companies earnings.
        As such, these companies may be undervalued compared to their earnings per share. 
        """
    )

    return render_template(
        'value_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/pb_under_one')
def pb_under_one():

    stocks = db.session.query(
        PBUnderOne
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'Price to Book Under One'

    text = Markup(
        """
        The Price to Book Ratio is the ratio of a company's share price compared
        to its book value. A P/B Ratio of 1 indicates a stock is trading in line
        with its book value. A P/B Ratio under 1 indicates a stock may be
        undervalued compared to its book value.
        """
    )

    return render_template(
        'value_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/peg_under_one')
def peg_under_one():

    stocks = db.session.query(
        PEGUnderOne
    ).limit(25).all()
    date = fetch_refresh_date()
    title = 'PEG Ratio Under One'

    text = Markup(
        """Price/Earnings to Growth is a broad metric used by investors to determine
        the value of a company relative to its growth prospects. A PEG ratio of 1 indicates
        a perfect correlation between a company's market value and its growth prospects. A
        PEG Ratio under 1 represents a company that may be undervalued relative to its growth
        potential.
        """
    )

    return render_template(
        'value_stocks.html',
        title=title,
        text=text,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/add_ticker', methods=["GET", "POST"])
def add_ticker():

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        ticker = ticker.upper()
        add_ticker_to_db(ticker)
        flash(f"Queued request for {ticker}. Most requests process in less than 24 hours.")
        return redirect('/')
    else:
        return redirect('/')

@app.route('/stocks', methods=["GET", "POST"])
def stock_search():
    """Handle search terms"""
    if request.method == 'POST':
        search = request.form.get('search')

        ticker_res = db.session.query(
            StockBasics
        ).filter(
            StockBasics.ticker == search.upper(),
        ).all()

        # now search other possibilities
        name_res = db.session.query(
            StockBasics
        ).filter(
            StockBasics.longName.ilike(f"%{search}%")
        ).all()

        # finally search for business summary
        if len(search) > 2:
            description_res = db.session.query(
                StockBasics
            ).filter(
                StockBasics.longBusinessSummary.ilike(f"%{search}%")
            ).all()
        else:
            description_res = []

        # combine results
        results = []
        results.extend(ticker_res[:10])
        results.extend(name_res[:10])
        results.extend(description_res[:10])

        results = unique_list(results)
        return render_template(
            'search_results.html',
            results=results,
            search=search
        )
    else:
        return redirect('/')

@app.route('/crypto')
def crypto():

    date = fetch_refresh_date()

    stocks = db.session.query(
        StockBasics, Collections
    ).filter(
        Collections.ticker == StockBasics.ticker
    ).filter(
        Collections.collection == 'Crypto'
    ).all()

    meta = """
        Top cryptocurrency stocks. A collection of the best crypto stocks which
        are related to cryptocurrencies and the blockchain. Contains stocks with various
        crypto business practices including mining and holding crypto currencies such as
        Bitcoin, Ethereum or Dogecoin, providing transaction processing services and
        the production of technology used for mining.
    """

    return render_template(
        'specialty_stocks.html',
        title='Cryptocurrencies & Blockchain',
        text="""This collection contains stocks which are related to cryptocurrencies or blockchain.
        This includes companies which mine cryptocurrencies such as Bitcoin, facilitate trading cryptocurrencies
        such as Bitcoin and Ethereum and companies which engage in other blockchain related operations.""",
        meta=meta,
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/electric_vehicles')
def electric_vehicles():

    date = fetch_refresh_date()

    stocks = db.session.query(
        StockBasics, Collections
    ).filter(
        Collections.ticker == StockBasics.ticker
    ).filter(
        Collections.collection == 'Electric Vehicles'
    ).all()

    return render_template(
        'specialty_stocks.html',
        title='Electric Vehicles',
        text="""This collection contains stocks which are related to Electric Vehicle manufacture or related
        industries such as EV charging stations.""",
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/gaming')
def gaming():

    date = fetch_refresh_date()

    stocks = db.session.query(
        StockBasics, Collections
    ).filter(
        Collections.ticker == StockBasics.ticker
    ).filter(
        Collections.collection == 'Gaming'
    ).all()

    return render_template(
        'specialty_stocks.html',
        title='Videogames',
        text='This collection contains stocks which are related to online and video games',
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/marijuana')
def marijuana():

    date = fetch_refresh_date()

    stocks = db.session.query(
        StockBasics, Collections
    ).filter(
        Collections.ticker == StockBasics.ticker
    ).filter(
        Collections.collection == 'Marijuana'
    ).all()

    return render_template(
        'specialty_stocks.html',
        title='Marijuana & Cannabis',
        text='This collection contains stocks which are related to the production and distribution of marijuana & cannabis.',
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/pets')
def pets():

    date = fetch_refresh_date()

    stocks = db.session.query(
        StockBasics, Collections
    ).filter(
        Collections.ticker == StockBasics.ticker
    ).filter(
        Collections.collection == 'Pets'
    ).all()

    return render_template(
        'specialty_stocks.html',
        title='Pets',
        text='This collection contains stocks which are related to pets. This includes pet food for dogs and cats, pet products and pet insurance providers.',
        stock_data=stocks,
        refresh_date=date
    )

@app.route('/<ticker>')
def stock_page(ticker):


    try:
        stock = db.session.query(
            StockBasics
        ).filter(
            StockBasics.ticker == ticker
        ).one()
    except:
        flash(f"Unable to find ticker: {ticker}")
        return redirect('/')

    collections = db.session.query(
        Collections
    ).filter(
        Collections.ticker == ticker
    ).all()

    _collections = [c.collection.replace('_', ' ').title() for c in collections]

    # TODO: might make sense to just pass the list
    collections_string = ', '.join(_collections)

    return render_template(
        'stock_info.html',
        stock=stock,
        collections=collections_string,
        refresh_date=None
    )

if __name__ == "__main__":
    app.run()
