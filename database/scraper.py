"""Pull high short interest stocks"""
import os
import requests
from bs4 import BeautifulSoup
import re
import yfinance
import psycopg2 as ps
import json
import time

DATABASE_URL = os.environ['DATABASE_URL']

def get_conn():

    conn = ps.connect(DATABASE_URL)

    return conn

def get_sp_companies(url):
    try:
        # pull list of S&P 500 stocks
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # find the table
        tbody = soup.find('tbody')
        # separate the tbody into trs
        trs = tbody.find_all('tr')

        # pop off the first one because it's a header
        head = trs.pop(0)

        # get all the header columns
        header_cols = [col.text.strip() for col in head.find_all('th')]
        # add sp indicator
        header_cols.append('sp_flag')

        # use nested loop to parse each stock
        stocks = []
        for tr in trs:
            row = [td.text.strip() for td in tr.find_all('td')]
            row.append(1)
            stocks.append(row)
        # return [stock[0] for stock in stocks]
        return header_cols, stocks
    # TODO: better error handling
    except:
        return []

def get_high_short_interest():

    page_num = 1
    tickers = []
    pull_next_page = True

    while pull_next_page:
        url f"https://www.highshortinterest.com/all/{page_num}"
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            table = soup.find("table")

            trs = soup.find_all('tr')

            for tr in trs:
                m = re.match('[A-z]*\\n', tr.text)
                if m:
                    ticker = m.group().replace('\n', '')
                    if ticker not in tickers:
                        tickers.append(ticker)
                    else:
                        pull_next_page = False
                else:
                    pull_next_page = False
        except:
            print(f"Error fetching {url}")
            pull_next_page = False

        page_num += 1

    return list(filter(None, tickers))

def write_to_db(tickers, collection):

    failed_tickers = []

    conn = get_conn()

    for ticker in tickers:
        cur = conn.cursor()

        print(ticker)
        try:
            stock = yfinance.Ticker(ticker)
            # print(stock.info)
            info = stock.info
            # data = {}
            # data["sector"] = info.get("sector", None)
            # data["longBusinessSummary"] = info.get("longBusinessSummary", None)
            # data["previousClose"] = info.get("previousClose", None)
            # data["marketCap"] = info.get("marketCap", None)
            # data["fiveYearAvgDividendYield?"] = info.get("fiveYearAvgDividendYield?", None)
            # data["shortName"] = info.get("shortName", None)
            # data["52WeekChange"] = info.get("52WeekChange", None)
            # data["shortPercentOfFloat"] = info.get("shortPercentOfFloat", None)
            # data["SandP52WeekChange"] = info.get("SandP52WeekChange", None)
            # data["fiftyTwoWeekLow"] = info.get("fiftyTwoWeekLow", None)
            # data["fiftyTwoWeekHigh"] = info.get("fiftyTwoWeekHigh", None)
            # data["beta"] = info.get("beta", None)
            # data["dividendRate"] = info.get("dividendRate", None)
            # data["trailingPE"] = info.get("trailingPE", None)
            # data["forwardPE"] = info.get("forwardPE", None)
            # data["enterpriseToRevenue"] = info.get("enterpriseToRevenue", None)
            # data["profitMargins"] = info.get("profitMargins", None)
            # data["enterpriseToEbitda"] = info.get("enterpriseToEbitda", None)
            # data["bookValue"] = info.get("bookValue", None)
            # data["trailingEps"] = info.get("trailingEps", None)
            # data["forwardEps"] = info.get("forwardEps", None)
            # data["heldPercentInstitutions"] = info.get("heldPercentInstitutions", None)
            # data["pegRatio"] = info.get("pegRatio", None)

            sql = f"""
            INSERT INTO public.stocks
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
            failed_tickers.append(ticker)
        time.sleep(1)

    conn.close()
    return failed_tickers

def _parse_tickers(header_cols, stocks):
    """Parse out which column contains the ticker"""

    found_symbol = False
    for i in range(len(header_cols)):
        if header_cols[i].lower().find("symbol") >= 0:
            found_symbol = True
            break

    if found_symbol:
        return [stock[i] for stock in stocks]
    else:
        return []

if __name__ == '__main__':
    # print("High Short Interest Stocks")
    # short_tickers = get_high_short_interest()
    # write_to_db(short_tickers, 'High Short Interest')
    #
    # print("S&P 500 Stocks")
    # url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    # sp_tickers = _parse_tickers(*get_sp_companies(url))
    # write_to_db(sp_tickers, 'S&P 500')

    print("S&P 400 Stocks")
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
    sp_tickers = _parse_tickers(*get_sp_companies(url))
    write_to_db(sp_tickers, 'S&P 400')

    # print("S&P 600 Stocks")
    # url = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
    # sp_tickers = _parse_tickers(*get_sp_companies(url))
