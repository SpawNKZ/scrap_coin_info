from flask import Flask, redirect, url_for, render_template, request, session
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
from functools import wraps
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from bs4 import BeautifulSoup
import requests

app = Flask(__name__, template_folder='template')
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dias12345@localhost/last_python"
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
db = SQLAlchemy(app)


class coins(db.Model):
    __tablename__ = 'Coin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    symbol = db.Column(db.String())
    market_cap = db.Column(db.String())
    price = db.Column(db.String())
    circulating_supply = db.Column(db.String())
    volume24h = db.Column(db.String())
    one_hour = db.Column(db.String())
    twenty_four_hour = db.Column(db.String())
    seven_days = db.Column(db.String())

    def __init__(self, name, symbol, market_cap, price, circulating_supply, volume24h, one_hour, twenty_four_hour, seven_days):
        self.name = name
        self.symbol = symbol
        self.market_cap = market_cap
        self.price = price
        self.circulating_supply = circulating_supply
        self.volume24h = volume24h
        self.one_hour = one_hour
        self.twenty_four_hour = twenty_four_hour
        self.seven_days = seven_days


class ScrapCoinmarket:
    def __init__(self):
        self.data = {}

    def get_scrap(self):
        r = requests.get('https://coinmarketcap.com/all/views/all/')
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('tbody')
        for row in table.find_all('tr'):
            try:
                sym = row.find('td',
                                  class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--hide-sm cmc-table__cell--sort-by__symbol').text
                mkt_cap = row.find('td',
                                   class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap').find(
                    'span', class_='sc-1ow4cwt-1 ieFnWP').text
                p = row.find('td',
                                 class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price').text
                circsup = row.find('td',
                                   class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply").text
                volume = row.find('td',
                                  class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h").text
                p_1h = row.find('td',
                                class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h').text
                p_24h = row.find('td',
                                 class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h').text
                p_7d = row.find('td',
                                class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-7-d').text
                Coinn = coins(name=row.find('a', class_='cmc-table__column-name--name cmc-link').text, symbol=sym, market_cap=mkt_cap, price=p, circulating_supply=circsup, volume24h=volume, one_hour=p_1h, twenty_four_hour=p_24h, seven_days=p_7d)
                db.session.add(Coinn)
                db.session.commit()
            except AttributeError:
                continue


@app.route("/coin", methods=["POST", "GET"])
def coin():
    if request.method == "POST":
        nn = request.form['coin']
        return render_template("example.html", query=coins.query.filter_by(name=nn))
    return render_template("index.html")


if __name__ == "__main__":
    db.create_all()
    scrapper = ScrapCoinmarket()
    scrapper.get_scrap()
    app.run(debug=True)
