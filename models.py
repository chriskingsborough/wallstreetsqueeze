"""Database schema definition"""
from app import db
from sqlalchemy.dialects.postgresql import JSON, DATE, REAL, BIGINT

class StockInfo(db.Model):
    """Contains high level stock info

    Tickers come from Russell indices + any additionals
    PK is ticker
    """

    __tablename__ = "stock_info"

    id = db.Column(BIGINT, primary_key=True)
    last_updated = db.Column(DATE)
    # Company information
    ticker = db.Column(db.String())
    shortName = db.Column(db.String())
    longName = db.Column(db.String())
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    longBusinessSummary = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())
    website = db.Column(db.String())
    logo_url = db.Column(db.String())
    # financial info
    marketCap = db.Column(BIGINT)
    beta = db.Column(REAL)
    enterpriseValue = db.Column(REAL)
    netIncomeToCommon = db.Column(BIGINT)
    # fiftyTwoWeek stats
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    fiftyTwoWeekChange = db.Column(REAL) # 52WeekChange
    fiftyDayAverage = db.Column(REAL)
    twoHundredDayAverage = db.Column(REAL)
    # dividend information
    dividendRate = db.Column(REAL) # this is the dollar amount
    dividendYield = db.Column(REAL) # this is the % as a REAL
    lastDividendDate = db.Column(DATE)
    lastDividendValue = db.Column(REAL) # $ amount last dividend
    # short information
    floatShares = db.Column(BIGINT)
    sharesOutstanding = db.Column(BIGINT)
    sharesShort = db.Column(BIGINT)
    sharesShortPriorMonth = db.Column(BIGINT)
    shortPercentOfFloat = db.Column(REAL)
    shortRatio = db.Column(REAL)
    # ratios
    trailingPE = db.Column(REAL)
    forwardPE = db.Column(REAL)
    trailingEps = db.Column(REAL)
    forwardEps = db.Column(REAL)
    bookValue = db.Column(REAL)
    enterpriseToEbitda = db.Column(REAL)
    enterpriseToRevenue = db.Column(REAL)
    payoutRatio = db.Column(REAL)
    priceToSalesTrailing12Months = db.Column(REAL)
    profitMargins = db.Column(REAL)
    priceToBook = db.Column(REAL)
    pegRatio = db.Column(REAL)
    earningsQuarterlyGrowth = db.Column(REAL)
    # new dividend columns
    trailingAnnualDividendYield = db.Column(REAL)
    trailingAnnualDividendRate = db.Column(REAL)
    exDividendDate = db.Column(DATE)

class StockPrices(db.Model):
    """Stock price by day and ticker"""

    __tablename__ = "stock_prices"

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
    last_updated = db.Column(DATE)
    price = db.Column(REAL)
    volume = db.Column(REAL)

class Collections(db.Model):
    """Reference table mapping tickers to collections

    ie
    AAPL - S&P 500
    AAPL - Nasdaq 100
    GME - High Short Interest
    """

    __tablename__ = "collections"

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
    collection = db.Column(db.String())
    last_updated = db.Column(DATE)

class CollectionChanges(db.Model):
    """Tracks any changes in collections"""
    __tablename__ = 'collection_changes'

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
    collection = db.Column(db.String())
    change = db.Column(db.String()) # added or removed
    date = db.Column(DATE)

class IndexPrices(db.Model):
    """Holds daily index prices"""
    __tablename__ = 'index_prices'

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
    name = db.Column(db.String())
    date = db.Column(DATE)
    previous_close = db.Column(REAL)
    close = db.Column(REAL)
    dollar_change = db.Column(REAL)
    decimal_change = db.Column(REAL)

class IndexTickers(db.Model):
    """Holds index tickers and basic info"""
    __tablename__ = 'index_tickers'

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
    name = db.Column(db.String())
    active = db.Column(BIGINT)
    last_updated = db.Column(DATE)

class FailureLog(db.Model):
    """Holds log of failed operations"""
    __tablename__ = 'failure_log'

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
    date = db.Column(DATE)
    table = db.Column(db.String())
    action = db.Column(db.String())
    exception = db.Column(db.String())

class StockRequests(db.Model):
    """Holds new stock requests"""
    __tablename__ = 'stock_requests'

    id = db.Column(BIGINT, primary_key=True)
    ticker = db.Column(db.String())
