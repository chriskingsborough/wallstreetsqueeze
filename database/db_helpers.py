"""Common DB Helpers"""
import os
import psycopg2 as ps

DATABASE_URL = os.environ['DATABASE_URL']

def get_conn():

    return ps.connect(DATABASE_URL)
