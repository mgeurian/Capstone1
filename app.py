from flask import Flask, request, render_template, jsonify, session, flash, url_for, redirect
import requests
from requests import Request, Session

from flask_debugtoolbar import DebugToolbarExtension

from secret import API_KEY

from forms import RegisterForm, LoginForm

from user_models import db, connect_db, User
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db_educryption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "educryption"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

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


# ****************************************************
# ****************************************************

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 
        email = form.email.data   
        first_name = form.first_name.data   
        last_name = form.last_name.data   

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another username')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data 

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/')

        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

# ****************************************************
# ****************************************************


# implement flash messaging for login/register routes