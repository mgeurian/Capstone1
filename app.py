from flask import Flask, request, render_template, jsonify
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# from flask_debugtoolbar import DebugToolbarExtension

from secret import API_KEY

from user_models import db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db_educryption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "educryption"
# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/api/cryptodata', methods=["POST"])
def get_crypto_data():
    """Get CMC response."""
    # id = request.json["crypto_id"]
    name = request.json["name"]
    # print(name)
    # by slug
    res = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?CMC_PRO_API_KEY=' + API_KEY + '&slug=' + name)


    # res = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY=' + API_KEY)

    # res = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quote/latest?CMC_PRO_API_KEY=' + API_KEY)

    response_json = res.json()
    return response_json
