"""Utilities to pull stock info"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3
import time
import logging
import urllib

LOGGER = logging.getLogger(__name__)

def get_sp_companies():
    try:
        # pull list of S&P 500 stocks
        page = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
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
        return header_cols, stocks
    # TODO: better error handling
    except:
        return []


# pull data from yahoo-finance
def write_data_to_db(table, cols, data):
    """Write data to a sqlite table.

    Assumes order of data matches order of cols
    """

    conn = sqlite3.connect('pyfi.db')
    cur = conn.cursor()
    # make the insert statement
    insert_statement = """
    INSERT INTO {tablename} VALUES ({num_cols});
    """.format(
        tablename=table,
        num_cols = ','.join(['?' for i in cols])
    )

    cur.executemany(insert_statement, data)

    cur.close()
    conn.commit()
    conn.close()

    return True

def write_df_to_db(df, tablename):
    """Write a dataframe to SQL"""

    conn = sqlite3.connect('pyfi.db')
    cur = conn.cursor()

    df.columns = [
        col.lower().replace(' ', '_') for col in df.columns
    ]

    # use df to_sql
    df.to_sql(
        tablename,
        conn,
        if_exists='append'
    )

    cur.close()
    conn.commit()
    conn.close()

    return True

def get_historical_data(share):
    """Pull stock info"""

    # pull all stock historical prices
    history = share.history(
        period="max"
    )

    history.reset_index(inplace=True)

    history['Ticker'] = share.ticker

    return history

def get_info(share):
    """Return stock info"""

    info = share.info
    # TODO: parse info result
    # TODO: info is a dict, need to turn into data that can be written to sqlite

    return info

def get_dividends(share):

    dividends = share.dividends

    df_div = dividends.to_frame()

    df_div.reset_index(inplace=True)

    df_div['Ticker'] = share.ticker

    return df_div



def get_recommendations(share):

    recommendations = share.recommendations

    recommendations.reset_index(inplace=True)

    recommendations['Ticker'] = share.ticker

    return recommendations

def get_calendar(share):

    calendar = share.calendar

    calendar.reset_index(
        inplace=True
    )

    pivot_calendar = pivot_to_cols(calendar)

    return pivot_calendar

def get_institutional_holders(share):

    institutional_holders = share.institutional_holders

    institutional_holders.reset_index(
        inplace=True,
        drop=True
    )
    institutional_holders.rename(
        columns={'Name': 'Holder'},
        inplace=True
    )

    # some stocks report a subset of institutional holder info
    standard_cols = {'Holder', 'Shares', 'Date Reported', '% Out', 'Value'}
    set_cols = set(institutional_holders.columns)

    # see if there are missing cols
    missing_cols = standard_cols - set_cols

    # if there are, add them to the dataframe as a null column
    if len(missing_cols) > 0:
        for col in missing_cols:
             institutional_holders[col] = np.nan

    institutional_holders['Ticker'] = share.ticker


    return institutional_holders

def get_sustainability(share):

    ticker = share.ticker

    sustainability = share.sustainability

    sustainability.reset_index(inplace=True)

    ## swap the sustainabilty column name to be value
    # get period value
    period = sustainability.columns[0]

    # assign new column name
    sustainability.columns = ['category', 'value']

    # add the period
    sustainability = pd.DataFrame(
        [['period', period]],
        columns=['category', 'value']
    ).append(sustainability)
    # add the ticker name
    sustainability = pd.DataFrame(
            [['ticker', ticker]],
            columns=['category', 'value']
        ).append(sustainability)


    columns = sustainability['category'].to_list()
    values = sustainability['value'].to_list()

    pivot_sustainability = pd.DataFrame(
        data=[values],
        columns=columns
    )
    return pivot_sustainability

def seed_all_data(share):
    # wrap all of these in try/excepts to handle missing data errors
    try:
        historical_data = get_historical_data(share)
        if len(historical_data) > 0:
            write_df_to_db(historical_data, 'historical_data')
    except (IndexError, AttributeError, urllib.error.HTTPError, ValueError):
        # set historical data to an empty list
        historical_data = []
        LOGGER.warning("Missing Historical Data: {}".format(share.ticker))

    # only try the other stuff if there's some historical data
    if len(historical_data) > 0:
        try:
            write_df_to_db(get_dividends(share), 'dividends')
        except (IndexError, AttributeError, urllib.error.HTTPError, ValueError):
            LOGGER.warning("Missing Dividend Data: {}".format(share.ticker))

        try:
            write_df_to_db(get_recommendations(share), 'recommendations')
        except (IndexError, AttributeError, urllib.error.HTTPError, ValueError):
            LOGGER.warning("Missing Recommendation Data: {}".format(share.ticker))

        try:
            write_df_to_db(get_calendar(share), 'calendar')
        except (IndexError, AttributeError, urllib.error.HTTPError, ValueError):
            LOGGER.warning("Missing Calendar Data: {}".format(share.ticker))

        try:
            write_df_to_db(get_institutional_holders(share), 'institutional_holders')
        except (IndexError, AttributeError, urllib.error.HTTPError, ValueError):
            LOGGER.warning("Missing Institutional Data: {}".format(share.ticker))

        try:
            write_df_to_db(get_sustainability(share), 'sustainability')
        except (IndexError, AttributeError, urllib.error.HTTPError, ValueError):
            LOGGER.warning("Missing Sustainability Data: {}".format(share.ticker))
    else:
        LOGGER.warning("WARNING - NO DATA AVAILABLE: {}".format(share.ticker))

    # pause between API calls
    time.sleep(1)

def pivot_to_cols(df):
    """Takes a dataframe and pivots first column to be column values"""

    # assign arbitrary column value names
    cols = ['column']
    cols.extend(
        ['value{}'.format(i) for i in range(1, len(df.columns))]
    )
    df.columns = cols
    columns = df['column'].to_list()
    
    values = []
    for col in cols[1:]:
        values.append(df[col].to_list())

    pivot_df = pd.DataFrame(
        data=values,
        columns=columns
    )

    return pivot_df
