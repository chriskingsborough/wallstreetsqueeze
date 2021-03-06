"""Database schema definition"""
from app import db
from sqlalchemy.dialects.postgresql import JSON, DATE, REAL, BIGINT

class HighShortInterest(db.Model):
    """High Short Interest"""

    __tablename__ = 'high_short'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    forwardEps = db.Column(REAL)
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    beta = db.Column(REAL)
    shortPercentOutstanding = db.Column(REAL)
    shortPercentOfFloat = db.Column(REAL)
    calculatedShortPercentFloat = db.Column(REAL)
    presShortPercentFloat = db.Column(REAL)

class DowDogs(db.Model):
    """Dogs of the Dow"""

    __tablename__ = "dogs_of_the_dow"
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)
    smallDog = db.Column(db.String())

class HighDividendStocks(db.Model):
    """High Dividend Stocks"""

    __tablename__ = 'high_dividend_stocks'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    trailingAnnualDividendRate = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)

class HighDividendReits(db.Model):
    """High Dividend Stocks sans REITS"""

    __tablename__ = 'high_dividend_reits'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    trailingAnnualDividendRate = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)

class Runners(db.Model):
    """Runners with high price over averages"""

    __tablename__ = 'runners'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    fiftyDayAverage = db.Column(REAL)
    twoHundredDayAverage = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    priceToSalesTrailing12Months = db.Column(REAL)

class Dippers(db.Model):
    """Dippers with low price under averages"""

    __tablename__ = 'dippers'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    fiftyDayAverage = db.Column(REAL)
    twoHundredDayAverage = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    priceToSalesTrailing12Months = db.Column(REAL)

class PriceRangeLow(db.Model):
    """Price Range Low"""

    __tablename__ = 'price_range_low'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    pricePercentOfRange = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)
    fiftyDayAverage = db.Column(REAL)
    twoHundredDayAverage = db.Column(REAL)
    priceToSalesTrailing12Months = db.Column(REAL)

class PriceRangeHigh(db.Model):
    """Price Range High"""

    __tablename__ = 'price_range_high'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    price = db.Column(REAL)
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    pricePercentOfRange = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    beta = db.Column(REAL)
    fiftyDayAverage = db.Column(REAL)
    twoHundredDayAverage = db.Column(REAL)
    priceToSalesTrailing12Months = db.Column(REAL)

class PEUnderFifteen(db.Model):
    """PE Under Fifteen"""

    __tablename__ = 'pe_under_fifteen'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    longName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    priceToBook = db.Column(REAL)
    pegRatio = db.Column(REAL)
    forwardEps = db.Column(REAL)
    beta = db.Column(REAL)

class PBUnderOne(db.Model):
    """PB Under Fifteen"""

    __tablename__ = 'pb_under_one'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    longName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    priceToBook = db.Column(REAL)
    pegRatio = db.Column(REAL)
    forwardEps = db.Column(REAL)
    beta = db.Column(REAL)

class PEGUnderOne(db.Model):
    """PEG Under Fifteen"""

    __tablename__ = 'peg_under_one'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    longName = db.Column(db.String())
    price = db.Column(REAL)
    marketCap = db.Column(REAL)
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    trailingAnnualDividendYield = db.Column(REAL)
    forwardPE = db.Column(REAL)
    priceToBook = db.Column(REAL)
    pegRatio = db.Column(REAL)
    forwardEps = db.Column(REAL)
    beta = db.Column(REAL)

class StockBasics(db.Model):
    """Stock basic information"""

    __tablename__ = 'stock_basics'
    __table_args__ = {'info': dict(is_view=True)}

    ticker = db.Column(db.String(), primary_key=True)
    shortName = db.Column(db.String())
    longName = db.Column(db.String())
    longBusinessSummary = db.Column(db.String())
    logo_url = db.Column(db.String())
    sector = db.Column(db.String())
    industry = db.Column(db.String())
    state = db.Column(db.String())
    country = db.Column(db.String())
    website = db.Column(db.String())
    price = db.Column(REAL)
    fiftyTwoWeekLow = db.Column(REAL)
    fiftyTwoWeekHigh = db.Column(REAL)
    fiftyDayAverage = db.Column(REAL)
    twoHundredDayAverage = db.Column(REAL)
    marketCap = db.Column(REAL)
    dividendYield = db.Column(REAL)
    dividendRate = db.Column(REAL)
    trailingAnnualDividendYield = db.Column(REAL)
    trailingAnnualDividendRate = db.Column(REAL)
    floatShares = db.Column(REAL)
    sharesOutstanding = db.Column(REAL)
    lastDividendDate = db.Column(DATE)
    lastDividendValue = db.Column(REAL)
    exDividendDate = db.Column(DATE)
    trailingPE = db.Column(REAL)
    forwardPE = db.Column(REAL)
    priceToBook = db.Column(REAL)
    pegRatio = db.Column(REAL)
    trailingEps = db.Column(REAL)
    forwardEps = db.Column(REAL)
    beta = db.Column(REAL)
    shortPercentOfFloat = db.Column(REAL)
    priceToSalesTrailing12Months = db.Column(REAL)
    profitMargins = db.Column(REAL)
    earningsQuarterlyGrowth = db.Column(REAL)
    sharesShort = db.Column(REAL)
    sharesShortPriorMonth = db.Column(REAL)
