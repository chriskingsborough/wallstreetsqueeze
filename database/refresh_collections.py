from rq import Queue
from rq.job import Job
from rq import Retry
import yfinance
import json
# from worker import conn
from db_helpers import *
from scraper import get_sp_companies, get_high_short_interest, _parse_tickers, get_small_cap_tickers, get_dow_companies, get_nasdaq, read_russell_csv


q = get_redis_queue()


def queue_collection_tickers(tickers, collection):

    # iterate through tickers and write to db
    # jobs = [
    #     q.enqueue_call(
    #         func=write_ticker_to_collections,
    #         args=(tick, collection),
    #         retry=Retry(3),
    #         result_ttl=5000
    #     )
    #     for tick in tickers
    # ]

    for tick in tickers:
        q.enqueue_call(
            func=write_ticker_to_collections,
            args=(tick, collection),
            retry=Retry(3),
            result_ttl=5000
        )

    # return jobs

def large_cap():

    collection = "S&P 500"
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tickers = _parse_tickers(*get_sp_companies(url))

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def medium_cap():

    collection = "S&P 400"
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
    tickers = _parse_tickers(*get_sp_companies(url))

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def small_cap():
    collection = "S&P 600"
    tickers = get_small_cap_tickers()

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def dow_jones():
    collection = "Dow Jones"
    tickers = get_dow_companies()

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def nasdaq():
    collection = "Nasdaq 100"
    tickers = get_nasdaq()

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def high_short():

    collection = "High Short Interest"
    tickers = get_high_short_interest()

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def russell_3000():

    url = "https://www.ishares.com/us/products/239714/ishares-russell-3000-etf/1467271812596.ajax?fileType=csv&fileName=IWV_holdings&dataType=fund"

    collection = "Russell 3000"
    headers, data = read_russell_csv(url)

    tickers = [row[0] for row in data]

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

def russell_microcap():

    url = "https://www.ishares.com/us/products/239716/ishares-microcap-etf/1467271812596.ajax?fileType=csv&fileName=IWC_holdings&dataType=fund"

    collection = "Russell Microcap"
    headers, data = read_russell_csv(url)

    tickers = [row[0] for row in data]

    jobs = queue_collection_tickers(
        tickers,
        collection
    )

if __name__ == "__main__":


    print("Large Cap")
    large_cap()
    print("Medium Cap")
    medium_cap()
    print("Small Cap")
    small_cap()
    print("Dow Jones")
    dow_jones()
    print("Nasdaq")
    nasdaq()
    print("High Shorts")
    high_short()
    print("Russell 3000")
    russell_3000()
    print("Russell Microcap")
    russell_microcap()
    print("Finding Removed")
    find_removed()
