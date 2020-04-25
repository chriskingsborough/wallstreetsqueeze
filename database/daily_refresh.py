"""Daily Refresh"""
import yfinance as yf
from datetime import datetime, timedelta
import sqlite3
import logging

from stock_info import write_df_to_db

LOGGER = logging.getLogger(__name__)

def pull_yesterdays_data(share):

    # get dates
    today = datetime.now()
    yesterday = datetime.now() - timedelta(days=1)

    # turn it into a string
    str_today = datetime.strftime(today, '%Y-%m-%d')
    str_yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

    history = share.history(start=str_yesterday, end=str_today)
    history.reset_index(inplace=True)
    history['Ticker'] = share.ticker

    return history

def refresh_data_all_companies():

    conn = sqlite3.connect('pyfi.db')
    cur = conn.cursor()

    cur.execute('SELECT symbol FROM companies')
    res = cur.fetchall()

    companies = [i[0] for i in res]

    for company in companies:
        LOGGER.critical(company)
        share = yf.Ticker(company)
        data = pull_yesterdays_data(share)
        write_df_to_db(data, 'historical_data')

    conn.commit()
    cur.close()
    conn.close()

def main():
    refresh_data_all_companies()

if __name__ == '__main__':
    main()