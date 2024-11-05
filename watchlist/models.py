from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))                                                     # username
    password_hash = db.Column(db.String(128))                                               # password hash

    def set_password(self, password):                                                       # set_password method, password is a parameter here
        self.password_hash = generate_password_hash(password)                               # 

    def validate_password(self, password):                                                  # validate password method, password is a parameter here
        return check_password_hash(self.password_hash, password)                            # return a bool

class Movie(db.Model):                                                                      # table name: movie
    id = db.Column(db.Integer, primary_key=True)                                            # Primary Key
    title = db.Column(db.String(60))                                                        # Movie title
    year = db.Column(db.String(4))                                                          # Movie year
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       