from flask import Flask, request, render_template, jsonify, session, flash, url_for, redirect
import requests
from requests import Request, Session

from flask_debugtoolbar import DebugToolbarExtension

from secret import API_KEY

from forms import RegisterForm, LoginForm, NotesForm

from models import db, connect_db, Currency

from user_models import User

from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///db_educryption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "educryption"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

# api connetion variables

base_api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/'
api_key = '?CMC_PRO_API_KEY=' + API_KEY


def update_db_currency(res):
    new_currency = Currency(
        id = request.json["flavor"],
        name = request.json["name"],
        symbol = request.json["symbol"],
        category = request.json["category"],
        slug = request.json["slug"],
        logo = request.json["logo"],
        description = request.json["description"],
        platform = request.json["platform"],
        price = request.json["price"],
        percent_change_1h = request.json["percent_change_1h"],
        percent_change_24h = request.json["percent_change_24h"],
        percent_change_7d = request.json["percent_change_7d"]

    )
    db.session.add(new_currency)
    db.session.commit()


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/api/cryptodata', methods=["POST"])
def update_crypto_data():
    """Get CMC response."""

    # id = request.json["crypto_id"]
    # name = request.json["name"]
    # print(name)
    # by slug

    # res = requests.get(base_api + 'info' + api_key + '&slug=' + name)
    # res = requests.get(base_api + 'map' + api_key)


    res = requests.get(base_api + 'listings/latest' + api_key)

    currencies = Currency.query.all()
    serialized = [c.serialize() for c in currencies]


    # response_json = res.json()
    return jsonify(currencies = serialized)


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
        return redirect(f'/users/{new_user.username}')

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
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect(url_for('home_page'))

# ****************************************************
# ****************************************************



#  ********** VIEW USER PROFILE **********

@app.route('/users/<username>')
def show_user(username):

    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('home_page'))
        
    user = User.query.get(username)

    return render_template("profile.html", user=user)

#  ********** DELETE USER **********

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ remove a user and notes from the database """

    if "username" not in session:
        flash("Please login first", "danger")
        return redirect(url_for('home_page'))

    user = User.query.get(username)
    if user.username == session['username']:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash("The user and their feedback have been deleted!", "danger")
        return redirect("/login")



# ****************************************************
# ****************************************************



# implement flash messaging for login/register routes


# have a file that requests all api data   