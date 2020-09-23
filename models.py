from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

# fl_bcrypt = Bcrypt()


db = SQLAlchemy()

def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)


class Currency(db.Model):
    """ CRYPTOCURRENCY. """

    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)

    symbol = db.Column(db.String, nullable=False)
    
    category = db.Column(db.String)

    slug = db.Column(db.String, nullable=False)

    logo = db.Column(db.String)

    description = db.Column(db.String)

    platform = db.Column(db.String)

    price = db.Column(db.Float, nullable=False)

    hourly_change = db.Column(db.Float, nullable=False)

    daily_change = db.Column(db.Float, nullable=False)

    weekly_change = db.Column(db.Float, nullable=False)



    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'symbol': self.symbol,
            'category': self.category,
            'slug': self.slug,
            'logo': self.logo,
            'description': self.description,
            'platform': self.platform,
            'price': self.price,
            'hourly_change': self.hourly_change,
            'daily_change': self.daily_change,
            'weekly_change': self.weekly_change
        }



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
#     """ USER_CURRENCY. """

#     __tablename__ = "users_currencies"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     user_id = 

#     currency_id = 