"""Poll and handle requests"""
import stock_info as si
from db_helpers import get_ps_conn, get_redis_queue

from worker import q

def action_requests():
    """Action requests in request table"""

    # q = get_redis_queue()

    # get distinct list of tickers from requests table
    tickers = get_requests()

    for ticker in tickers:

        try:
            q.enqueue_call(
                func=si.get_info,
                args=(ticker,)
            )

            q.enqueue_call(
                func=si.get_price,
                args=(ticker,)
            )

            delete_request(ticker)
        except Exception as e:
            print(e)

def clear_bad_requests():
    """Clear bad requests"""

    conn = get_ps_conn()
    cur = conn.cursor()

    sql = """
        DELETE FROM stock_requests
        WHERE ticker in (
            SELECT DISTINCT
                ticker
            FROM stock_info
        )
    """

    cur.execute(sql)

    conn.commit()
    conn.close()

def add_to_collections():
    """Add any stocks in stock_info to collections"""

    conn = get_ps_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO collections (
            ticker,
            collection,
            last_updated
        )
        SELECT DISTINCT
            si.ticker,
            'Manually Requested' as collection,
            NOW() as last_updated
        FROM stock_info as si
        WHERE si.ticker not in (
            SELECT DISTINCT ticker FROM collections
        );
    """

    cur.execute(sql)

    conn.commit()
    conn.close()

def get_requests():
    """Get all actionable requests"""

    conn = get_ps_conn()
    cur = conn.cursor()

    sql = """
        SELECT DISTINCT
            sr.ticker
        FROM stock_requests as sr
        LEFT JOIN stock_info as si
        ON sr.ticker = si.ticker
        WHERE si.ticker is NULL;
    """

    cur.execute(sql)
    res = cur.fetchall()

    tickers = []
    for row in res:
        tickers.append(row[0])

    cur.close()
    conn.close()

    return tickers

def delete_request(ticker):
    """Delete the request from request table"""

    conn = get_ps_conn()
    cur = conn.cursor()

    sql = """
        DELETE FROM stock_requests sr
        WHERE sr.ticker = %s
    """

    cur.execute(sql, (ticker,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    action_requests()
    add_to_collections()
    clear_bad_requests()
