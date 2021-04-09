"""Get index quotes"""
import yfinance

from db_helpers import get_ps_conn

def populate_tickers():
    """Populate index_tickers table"""

    sql = """INSERT INTO index_tickers
    (ticker, "name", active, last_updated)
    VALUES (%s, %s, 1, NOW())
    """

    conn = get_ps_conn()

    cur = conn.cursor()

    # delete all records from table
    cur.execute(
        "DELETE FROM index_tickers WHERE 1=1"
    )

    indices = [
        ("^DJI", "Dow Jones Industrial Average"),
        ("^IXIC", "NASDAQ Composite"),
        ("^GSPC", "S&P 500"),
        ("^VIX", "CBOE Volatility Index")
    ]

    cur.executemany(sql, indices)
    cur.close()

    conn.commit()
    conn.close()

def get_index_prices():
    """Get daily price and change"""

    # get database conn and cursor
    conn = get_ps_conn()
    cur = conn.cursor()

    # get the tickers
    get_tickers_sql = """
    SELECT ticker, name FROM index_tickers
    """
    cur.execute(get_tickers_sql)

    ticker_results = cur.fetchall()

    print(ticker_results)
    for res in ticker_results:
        ticker = res[0]
        name = res[1]

        try:

            yticker = yfinance.Ticker(ticker)
            info = yticker.get_info()
            # previous_close = info["regularMarketPreviousClose"]
            closes = yticker.history(period="2d")
            closes.reset_index(inplace=True)
            previous_close = closes.iloc[0]['Close']
            most_recent_close = closes.iloc[1]['Close']
            dollar_change = most_recent_close - previous_close
            decimal_change = (most_recent_close - previous_close) / previous_close

            delete_sql = """
            DELETE FROM index_prices
            WHERE ticker = %s
            """

            cur.execute(delete_sql, (ticker,))
            conn.commit()

            sql = """
            INSERT INTO index_prices (
                ticker,
                name,
                date,
                previous_close,
                close,
                dollar_change,
                decimal_change
            ) VALUES (%s, %s, NOW(), %s, %s, %s, %s)
            """

            cur.execute(
                sql,
                (
                    ticker,
                    name,
                    previous_close,
                    most_recent_close,
                    dollar_change,
                    decimal_change
                )
            )
            print(f"Successfully inserted data for {ticker}")

            conn.commit()
        except Exception as e:
            print(e)
            print(f"Processing {ticker} failed")
            print("Moving to next ticker")

    cur.close()
    conn.close()

# if __name__ == '__main__':
#     populate_tickers()
#     get_index_prices()
