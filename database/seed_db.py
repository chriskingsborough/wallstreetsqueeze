"""Seed database tables"""
import sqlite3
import yfinance as yf
import os
import logging
import pandas as pd

from stock_info import get_sp_companies, write_df_to_db, seed_all_data

LOGGER = logging.getLogger(__name__)

def seed_companies():

    # get the sp header data
    headers, data = get_sp_companies()

    df = pd.DataFrame(data=data, columns=headers)

    write_df_to_db(df, 'companies')

    # # header parsing
    # headers = [header.replace(' ', '_').lower() for header in headers]

    # # open connection to sqlite
    # conn = sqlite3.connect('pyfi.db')

    # # all tables can be text
    # create_cols = ' TEXT DEFAULT NULL, '.join(headers)

    # # add last statement
    # create_cols = create_cols + ' TEXT DEFAULT NULL'

    # table = 'companies'
    # # make the full statement
    # create_table = """
    # CREATE TABLE IF NOT EXISTS {table} (
    #     {},
    #     sp INTEGER DEFAULT 0
    # )
    # """.format(create_cols, table=table)

    # cur = conn.cursor()

    # cur.execute(create_table)
    # conn.commit()
    # # clean up conn
    # cur.close()
    # conn.close()

    # headers.append('sp')

    # data = [row.append(1) for row in data]
    # # write data to the db
    # write_data_to_db(table, headers, data)
    # return stock tickers
    return [stock[0] for stock in data]

def main():
    try:
        os.remove('pyfi.db')
    except FileNotFoundError:
        LOGGER.debug('No Existing DB')

    tickers = seed_companies()

    # seed data for every share
    for ticker in tickers:
        LOGGER.info('Seeding Data')
        LOGGER.critical(ticker)
        share = yf.Ticker(ticker)
        seed_all_data(share)
    

if __name__ == '__main__':
    main()