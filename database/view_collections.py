import yaml
import logging
from rq import Queue
from rq.job import Job
from rq import Retry
from worker import conn

from db_helpers import get_ps_conn

logger = logging.getLogger(__name__)

def read_yaml():

    with open('database/views/view_config.yaml', 'r') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)

    return y

def get_view_tickers(view_name, limit):

    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        sql = f"""
        SELECT
            ticker
        FROM
            {view_name}
        LIMIT {limit}
        """

        cur.execute(sql)
        res = cur.fetchall()

        tickers = {row[0] for row in res}
    except Exception as e:
        logger.warning(e)
        tickers = set() # empty set
    finally:
        conn.close()
        return tickers

def get_existing_tickers(view_name):

    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        sql = f"""
        SELECT
            ticker
        FROM
            collections
        WHERE
            collection = '{view_name}'
        """
        cur.execute(sql)
        res = cur.fetchall()

        tickers = {row[0] for row in res}
    except Exception as e:
        logger.warning(e)
        tickers = set() # empty set
    finally:
        conn.close()
        return tickers

def compare_tickers(new_tickers, existing_tickers):

    added = list(new_tickers - existing_tickers)

    removed = list(existing_tickers - new_tickers)

    # return tuple with added and removed lists
    return added, removed

def write_ticker_collections(tickers, view_name):

    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        # delete the existing collection
        delete_sql = """
        DELETE FROM collections
        WHERE collection = %s
        """

        cur.execute(
            delete_sql,
            (view_name,)
        )

        conn.commit()

        data = [
            (ticker, view_name)
            for ticker in tickers
        ]

        insert_sql = """
        INSERT INTO collections
        (ticker, collection, last_updated)
        VALUES (%s, %s, NOW())
        """

        cur.executemany(
            insert_sql,
            data
        )
        conn.commit()
    except Exception as e:
        logger.warning(e)
    finally:
        conn.close()

def write_changes(added, removed, view_name):
    """Write collection changes to DB"""

    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        # write added
        added_sql = f"""
        INSERT INTO collection_changes
        (ticker, collection, change, date)
        VALUES (
            %s, '{view_name}', 'Added', NOW()
        )
        """

        added_data = [
            (ticker,)
            for ticker in added
        ]

        cur.executemany(
            added_sql,
            added_data
        )
        conn.commit()

        removed_sql = f"""
        INSERT INTO collection_changes
        (ticker, collection, change, date)
        VALUES (
            %s, '{view_name}', 'Removed', NOW()
        )
        """

        removed_data = [
            (ticker,)
            for ticker in removed
        ]

        cur.executemany(
            removed_sql,
            removed_data
        )
        conn.commit()

    except Exception as e:
        logger.warning(e)
    finally:
        conn.close()

def refresh_view_changes(view_name, limit):

    new_tickers = get_view_tickers(view_name, limit)
    existing_tickers = get_existing_tickers(view_name)

    added, removed = compare_tickers(
        new_tickers,
        existing_tickers
    )

    write_ticker_collections(
        new_tickers,
        view_name
    )

    write_changes(
        added,
        removed,
        view_name
    )
