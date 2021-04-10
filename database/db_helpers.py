"""Common DB Helpers"""
import os
import psycopg2 as ps
import redis
from rq import Worker, Queue, Connection
import json
from urllib.parse import urlparse

DATABASE_URL = os.environ['DATABASE_URL']
REDIS_URL = os.getenv('REDIS_TLS_URL')

def get_ps_conn():

    return ps.connect(DATABASE_URL)

def log_failure(symbol, table, action, exception):
    """Handle any failures and write to failure table"""
    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        query = """
        INSERT INTO failure_log (
            ticker,
            "date",
            "table",
            "action",
            "exception"
        )
        VALUES (%s, NOW(), %s, %s, %s)
        """

        cur.execute(
            query,
            (symbol, table, action, str(exception))
        )
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print(cur.query)

def get_redis_conn():
    """Return Redis connection"""

    url = urlparse(REDIS_URL)
    conn = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)

    return conn

def get_redis_queue():
    """Return Redis queue"""

    conn = get_redis_conn()

    q = Queue(connection=conn)

    return q

def write_ticker_to_collections(ticker, collection):
    """Write ticker and collection to collection table"""

    try:
        # get ps connection details
        conn = get_ps_conn()
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
        conn = get_ps_conn()
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
    conn = get_ps_conn()
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
