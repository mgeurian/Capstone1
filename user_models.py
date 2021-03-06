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