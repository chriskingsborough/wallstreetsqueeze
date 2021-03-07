"""Get stock info"""
import yfinance
import datetime

from db_helpers import get_conn, log_failure

def get_info(ticker):
    """Get info for a ticker and write to db"""

    try:
        conn = get_conn()
        cur = conn.cursor()

        yticker = yfinance.Ticker(ticker)

        # get all the info
        info = yticker.get_info()

        # get all relevant info
        shortName = info.get("shortName")
        longName = info.get("longName")
        sector = info.get("sector")
        industry = info.get("industry")
        longBusinessSummary = info.get("longBusinessSummary")
        state = info.get("state")
        country = info.get("country")
        website = info.get("website")
        logo_url = info.get("logo_url")
        marketCap = info.get("marketCap")
        beta = info.get("beta")
        enterpriseValue = info.get("enterpriseValue")
        netIncomeToCommon = info.get("netIncomeToCommon")
        fiftyTwoWeekLow = info.get("fiftyTwoWeekLow")
        fiftyTwoWeekHigh = info.get("fiftyTwoWeekHigh")
        fiftyTwoWeekChange = info.get("52WeekChange")
        fiftyDayAverage = info.get("fiftyDayAverage")
        twoHundredDayAverage = info.get("twoHundredDayAverage")
        dividendRate = info.get("dividendRate")
        dividendYield = info.get("dividendYield")
        lastDividendDate = info.get("lastDividendDate")
        lastDividendValue = info.get("lastDividendValue")
        floatShares = info.get("floatShares")
        sharesOutstanding = info.get("sharesOutstanding")
        sharesShort = info.get("sharesShort")
        sharesShortPriorMonth = info.get("sharesShortPriorMonth")
        shortPercentOfFloat = info.get("shortPercentOfFloat")
        shortRatio = info.get("shortRatio")
        trailingPE = info.get("trailingPE")
        forwardPE = info.get("forwardPE")
        trailingEps = info.get("trailingEps")
        forwardEps = info.get("forwardEps")
        bookValue = info.get("bookValue")
        enterpriseToEbitda = info.get("enterpriseToEbitda")
        enterpriseToRevenue = info.get("enterpriseToRevenue")
        payoutRatio = info.get("payoutRatio")
        priceToSalesTrailing12Months = info.get("priceToSalesTrailing12Months")
        profitMargins = info.get("profitMargins")
        priceToBook = info.get("priceToBook")
        pegRatio = info.get("pegRatio")
        earningsQuarterlyGrowth = info.get("earningsQuarterlyGrowth")

        # handle last lastDividendDate
        if lastDividendDate:
            timestamp = datetime.datetime.fromtimestamp(lastDividendDate)
            lastDividendDate = timestamp.strftime('%Y-%m-%d')

        sql = """
        INSERT INTO stock_info
        (
            last_updated,
            ticker,
            "shortName",
            "longName",
            sector,
            industry,
            "longBusinessSummary",
            state,
            country,
            website,
            logo_url,
            "marketCap",
            beta,
            "enterpriseValue",
            "netIncomeToCommon",
            "fiftyTwoWeekLow",
            "fiftyTwoWeekHigh",
            "fiftyTwoWeekChange",
            "fiftyDayAverage",
            "twoHundredDayAverage",
            "dividendRate",
            "dividendYield",
            "lastDividendDate",
            "lastDividendValue",
            "floatShares",
            "sharesOutstanding",
            "sharesShort",
            "sharesShortPriorMonth",
            "shortPercentOfFloat",
            "shortRatio",
            "trailingPE",
            "forwardPE",
            "trailingEps",
            "forwardEps",
            "bookValue",
            "enterpriseToEbitda",
            "enterpriseToRevenue",
            "payoutRatio",
            "priceToSalesTrailing12Months",
            "profitMargins",
            "priceToBook",
            "pegRatio",
            "earningsQuarterlyGrowth"
        )
        VALUES(NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        cur.execute(
            sql,
            (
                ticker,
                shortName,
                longName,
                sector,
                industry,
                longBusinessSummary,
                state,
                country,
                website,
                logo_url,
                marketCap,
                beta,
                enterpriseValue,
                netIncomeToCommon,
                fiftyTwoWeekLow,
                fiftyTwoWeekHigh,
                fiftyTwoWeekChange,
                fiftyDayAverage,
                twoHundredDayAverage,
                dividendRate,
                dividendYield,
                lastDividendDate,
                lastDividendValue,
                floatShares,
                sharesOutstanding,
                sharesShort,
                sharesShortPriorMonth,
                shortPercentOfFloat,
                shortRatio,
                trailingPE,
                forwardPE,
                trailingEps,
                forwardEps,
                bookValue,
                enterpriseToEbitda,
                enterpriseToRevenue,
                payoutRatio,
                priceToSalesTrailing12Months,
                profitMargins,
                priceToBook,
                pegRatio,
                earningsQuarterlyGrowth
            )
        )
        conn.commit()

        delete_sql = """
        DELETE FROM stock_info
        WHERE ticker = %s
        AND last_updated != (
            SELECT max(last_updated)
            FROM stock_info
            WHERE ticker = %s
        )
        """
        cur.execute(delete_sql, (ticker, ticker))
    except Exception as e:
        print(e)

        log_failure(ticker, 'stock_info', 'Update Info', e)

    finally:
        conn.commit()
        conn.close()

def get_price(ticker):
    """Get price for ticker for previous close"""

    try:
        conn = get_conn()
        cur = conn.cursor()

        yticker = yfinance.Ticker(ticker)

        price_df = yticker.history(period='1d')
        price_df.reset_index(inplace=True)

        price_close = float(price_df.iloc[0]['Close'])
        volume = int(price_df.iloc[0]['Volume'])

        sql = """
        INSERT INTO stock_prices
        (ticker, last_updated, price, volume)
        VALUES(%s, NOW(), %s, %s);
        """

        cur.execute(
            sql,
            (ticker, price_close, volume)
        )
        conn.commit()
        # delete where last_updated != max last_updated
        delete_sql = """
        DELETE FROM stock_prices
        WHERE ticker = %s
        AND last_updated != (
            SELECT max(last_updated)
            FROM stock_prices
            WHERE ticker = %s
        )
        """

        cur.execute(delete_sql, (ticker, ticker))
    except Exception as e:
        print(e)
        log_failure(ticker, 'stock_prices', 'Update Prices', e)
    finally:
        conn.commit()
        conn.close()

def get_all_tickers():
    """Get all tickers from database"""

    try:
        conn = get_conn()
        cur = conn.cursor()

        sql = """
            select distinct ticker from collections;
        """

        cur.execute(sql)

        results = cur.fetchall()
        tickers = [res[0] for res in results]

    except Exception as e:
        print(e)
        tickers = []
    finally:
        cur.close()
        conn.close()

    return tickers
