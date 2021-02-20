import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from datetime import datetime

app = Flask(__name__)
print(os.environ['APP_SETTINGS'])
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from database.models import Stocks, Indices, IndexTickers


@app.route('/')
def home_page():

    indices = fetch_indices()
    date = fetch_refresh_date()
    print(date)
    return render_template('index.html', indices=indices, refresh_date=date)

@app.route('/large_cap')
def large_cap():

    stocks = fetch_stocks("S&P 500")

    return render_template('large_cap_stocks.html', stock_data=stocks, refresh_date=date)

@app.route('/medium_cap')
def medium_cap():

    stocks = fetch_stocks("S&P 400")

    return render_template('medium_cap_stocks.html', stock_data=stocks, refresh_date=date)

@app.route('/high_short')
def high_short():

    stocks = fetch_stocks("High Short Interest")

    return render_template('high_short.html', stock_data=stocks, refresh_date=date)


def fetch_indices():

    subquery = db.session.query(func.max(Indices.date)).subquery()
    res = db.session.query(Indices).filter(
        Indices.date == subquery
    ).all()
    return res

def fetch_stocks(collection):

    res = Stocks.query.filter(
        Stocks.collection == collection
    ).all()

    return res

def fetch_refresh_date():

    res = db.session.query(func.max(Indices.date)).one()
    dt = res[0]
    formatted_date = datetime.strftime(dt, '%B %-d, %Y')
    return formatted_date

if __name__ == "__main__":
    app.run()
