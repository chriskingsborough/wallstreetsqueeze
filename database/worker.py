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

def write_ticker_to_collections(ticker, collection):
    """Write ticker and collection to collection table"""

    try:
        # get ps connection details
        conn = get_conn()
        cur = conn.cursor()
        # first check if it already exists
        query_exists = """
        SELECT ticker FROM collections
        WHERE ticker = %s
            AND collection = %s
        """

        cur.execute(query_exists, (ticker, collection))

        result = cur.fetchall()
        exists = bool(result)
        if exists:
            # if ticker already exists
            # then update the last updated date and move on
            update_query = """
            UPDATE collections
            SET last_updated = NOW()
            WHERE ticker = %s
                AND collection = %s
            """
            cur.execute(update_query, (ticker, collection))
            conn.commit()
        # if it doesn't exist, then add it
        else:
            insert_query = """
            INSERT INTO collections (ticker, collection, last_updated)
            VALUES (%s, %s, NOW());
            """
            cur.execute(insert_query, (ticker, collection))
            conn.commit()

            # and since it's new, add it to the changes table
            insert_changes_query = """
            INSERT INTO collection_changes
            (ticker, collection, "change", "date")
            VALUES (%s, %s, 'Added', NOW());
            """

            cur.execute(insert_changes_query, (ticker, collection))
            conn.commit()
    except:
        print(f"FAILED: {ticker}")
    finally:
        conn.close()

def find_removed():

    try:
        # get ps connection details
        conn = get_conn()
        cur = conn.cursor()

        insert_query = """INSERT INTO collection_changes
        (ticker, collection, "change", "date")
        SELECT ticker, collection, 'Removed' as "change", NOW()
        FROM collections
        WHERE last_updated <> (
            SELECT max("last_updated") FROM collections
        )
        """

        cur.execute(insert_query)
        conn.commit()

        delete_query = """DELETE FROM collections
        WHERE last_updated <> (
            SELECT max("last_updated") FROM collections
        )
        """

        cur.execute(delete_query)
        conn.commit()

    except:
        print("UNABLE TO PROCESS REMOVED TICKERS")
    finally:
        conn.close()

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
    print(f"Existing queue count: {q.count}")
    # print(f"Clearing queue")
    # q.empty()
    print(f"New queue count: {q.count}")
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
