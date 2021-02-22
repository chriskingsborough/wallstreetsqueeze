import os
import yfinance
from db_helpers import get_conn
import redis
from rq import Worker, Queue, Connection
import json

listen = ['default']
redis_url = os.getenv('REDIS_URL')
conn = redis.from_url(redis_url)
q = Queue(connection=conn)

def write_ticker_to_db(ticker, collection):

    # get ps connection details
    conn = get_conn()
    cur = conn.cursor()

    try:
        stock = yfinance.Ticker(ticker)
        info = stock.info

        # find existing ticker and delete
        delete_sql = f"""
        DELETE FROM stocks
        WHERE ticker = '{ticker}'
        AND collection = '{collection}'
        """
        # delete existing entry
        cur.execute(delete_sql)
        conn.commit()

        sql = f"""
        INSERT INTO stocks
        (ticker, "date", collection, info)
        VALUES(%s, NOW(), %s, %s);
        """
        # currently dumping all data to the db
        cur.execute(sql, (ticker, collection, json.dumps(info)))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"FAILED TO FETCH DATA: {ticker}")
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
