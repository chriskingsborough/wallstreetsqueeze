from rq import Queue
from rq.job import Job
from rq import Retry
import yfinance
import json
from worker import conn
from db_helpers import get_conn
from worker import write_ticker_to_db
from scraper import get_sp_companies, get_high_short_interest, _parse_tickers
from indices import get_index_prices, populate_tickers

q = Queue(connection=conn)

def queue_stocks(tickers, collection):

    jobs = [q.enqueue_call(
        func=write_ticker_to_db,
        args=(tick, collection),
        retry=Retry(3),
        result_ttl=5000
    )
        for tick in tickers
    ]
    return jobs

def large_cap():

    collection = "S&P 500"
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tickers = _parse_tickers(*get_sp_companies(url))

    jobs = queue_stocks(
        tickers,
        collection
    )

def medium_cap():

    collection = "S&P 400 Stocks"
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
    tickers = _parse_tickers(*get_sp_companies(url))

    jobs = queue_stocks(
        tickers,
        collection
    )

def high_short():

    collection = "High Short Interest"
    tickers = get_high_short_interest()

    jobs = queue_stocks(
        tickers,
        collection
    )

def index_prices():

    job = q.enqueue_call(
        func=populate_tickers,
        retry=Retry(3),
        result_ttl=5000
    )


    job = q.enqueue_call(
        func=get_index_prices,
        retry=Retry(3),
        result_ttl=5000
    )

if __name__ == "__main__":

    index_prices()
    large_cap()
    medium_cap()
    high_short()
