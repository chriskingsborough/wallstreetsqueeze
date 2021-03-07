from rq import Queue
from rq.job import Job
from rq import Retry
from worker import conn
from indices import get_index_prices, populate_tickers

q = Queue(connection=conn)

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


if __name__ == '__main__':
    print("Index Prices")
    index_prices()
