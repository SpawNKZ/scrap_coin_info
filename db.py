from flask import Flask, redirect, url_for, render_template, request
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
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dias12345@localhost/p_db"
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
db = SQLAlchemy(app)


class coins(db.Model):
    __tablename__ = 'Coin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    symbol = db.Column(db.String())
    market_cap = db.Column(db.String())
    price = db.Column(db.Integer())
    circulating_supply = db.Column(db.String())
    volume24h = db.Column(db.String())
    one_hour = db.Column(db.String())
    twenty_four_hour = db.Column(db.String())
    seven_days = db.Column(db.String())

    def __init__(self, name):
        self.name = name


class ScrapCoinmarket:
    def __init__(self):
        self.data = {}

    def get_scrap(self):
        r = requests.get('https://coinmarketcap.com/all/views/all/')
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find('tbody')
        for row in table.find_all('tr'):
            try:
                symbol = row.find('td',
                                  class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--hide-sm cmc-table__cell--sort-by__symbol').text
                mkt_cap = row.find('td',
                                   class_='cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap').find(
                    'span', class_='sc-1ow4cwt-1 ieFnWP').text
                price = row.find('td',
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
                self.data = {
                    'Name': row.find('a', class_='cmc-table__column-name--name cmc-link').text,
                    'Symbol': symbol,
                    'Market Cap': mkt_cap,
                    'Price': price,
                    'Circulating Supply': circsup,
                    'Volume(24h)': volume,
                    '%1h': p_1h,
                    '%24h': p_24h,
                    '%7d': p_7d
                }
            except AttributeError:
                continue


scrapper = ScrapCoinmarket()
print(scrapper.get_scrap())