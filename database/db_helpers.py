"""Common DB Helpers"""
import os
import psycopg2 as ps

DATABASE_URL = os.environ['DATABASE_URL']

def get_conn():

    return ps.connect(DATABASE_URL)

def log_failure(symbol, table, action, exception):
    """Handle any failures and write to failure table"""
    try:
        conn = get_conn()
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
