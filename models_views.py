"""Database schema definition"""
from app import db
from sqlalchemy.dialects.postgresql import JSON, DATE, REAL, BIGINT

class HighShortInterest(db.Model):
    """High Short Interest"""

    __tablename__ = 'high_short'

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

class HighDividend(db.Model):
    """High Dividend Stocks"""

    __tablename__ = 'high_dividend'

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

class HighDividendSansReit(db.Model):
    """High Dividend Stocks sans REITS"""

    __tablename__ = 'high_dividend_sans_reit'

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
