from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

fl_bcrypt = Bcrypt()


db = SQLAlchemy()

def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)



class User(db.Model):
    """ USER. """

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)


    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """ Register user w/hashed password $& return user. """

        hashed = fl_bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)



    @classmethod
    def authenticate(cls, username, pwd):
        """ Validate that user exists & password is correct.

        Return user if valid; else return false.
        """

        u = User.query.filter_by(username=username).first()

        if u and fl_bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False



# class CryptoCurrency(db.Model):
#     """ CRYPTOCURRENCY. """

#     __tablename__ = "currencies"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     name = db.Column(db.String, null=False)

#     symbol = db.Column(db.String, null=False)
    
#     category = db.Column(db.String, null=False)

#     slug = db.Column(db.String, null=False)

#     logo = db.Column(db.String, null=False)

#     description = db.Column(db.String, null=False)

#     platform = db.Column(db.String, null=False)



# class Tag(db.Model):
#     """ TAG. """

#     __tablename__ = "tags"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     tag = db.Column(db.String, null=False)



# class Currency_Tag(db.Model):
#     """ CURRENCY_TAGS. """

#     __tablename__ = "currency_tags"

#     id = db.Column(db.Integer, primary_key=True)

#     currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), primary_key=True)

#     tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)



# class URLs(db.Model):
#     """ URLs. """

#     __tablename__ = "urls"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     url = db.Column(db.String, null=False)



# class Currency_Url(db.Model):
#     """ CURRENCY_URLS. """

#     __tablename = "currency_urls"

#     id = db.Column(db.Integer, primary_key=True)

#     currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), primary_key=True)

#     url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), primary_key=True)



# class Note(db.Model):
#     """ NOTES. """

#     __tablename__ = "notes"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     user_currency_id = 

#     comment = 


# class User_Currency(db.Model):
    """ USER_CURRENCY. """

    __tablename__ = "users_currencies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = 

    currency_id = 