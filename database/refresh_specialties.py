import os
import yaml
import logging

from db_helpers import get_ps_conn

logger = logging.getLogger(__name__)

def read_yaml(filename):

    with open(f'database/collections/{filename}', 'r') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)

    return y

def get_files():

    filenames = os.listdir('database/collections')

    return filenames

def update_collection(name: str, tickers: list):

    try:
        conn = get_ps_conn()
        cur = conn.cursor()

        delete_sql = """
        DELETE FROM collections
        WHERE collection = %s
        """

        cur.execute(delete_sql, (name,))
        conn.commit()

        insert_sql = """
        INSERT INTO collections
        (ticker, collection, last_updated)
        VALUES (%s, %s, NOW())
        """

        cur.executemany(
            insert_sql,
            tuple((ticker, name) for ticker in tickers)
        )
        conn.commit()
    except Exception as e:
        logger.warning(e)
    finally:
        cur.close()
        conn.close()

def main():

    filenames = get_files()

    for filename in filenames:
        collection = read_yaml(filename)
        update_collection(
            collection['name'],
            collection['tickers']
        )

if __name__ == '__main__':
    main()
