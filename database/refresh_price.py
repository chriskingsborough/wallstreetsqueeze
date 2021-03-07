from rq import Queue
from rq.job import Job
from rq import Retry

import stock_info as si
from worker import conn

q = Queue(connection=conn)

def refresh_price():
    """Refresh stock info"""

    tickers = si.get_all_tickers()

    for symbol in tickers:
        q.enqueue_call(
            func=si.get_price,
            args=(symbol,),
            retry=Retry(3),
            result_ttl=5000
        )

if __name__ == '__main__':
    refresh_price()
