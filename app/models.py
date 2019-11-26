from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login


class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    observed = db.relationship('UserShares', backref='observer', lazy=True)

    def __repr__(self):
        return '<User{} >'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Date (db.Model):
    day = db.Column( db.Date, index = True, primary_key = True,  unique =True)
    summaryDate = db.relationship('StockShares', backref = 'day', lazy = True)


class Company (db.Model):
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(300), index=True,  unique=True)
    dailySummary = db.relationship('StockShares', backref='name', lazy=True)
    observer = db.relationship('UserShares', backref='shareholder', lazy=True)

    def __repr__(self):
        return '<Name{} >'.format(self.name)


class StockShares(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, index=True)
    change = db.Column(db.Float)
    opening = db.Column(db.Float)
    min_v = db.Column(db.Float)
    max_v = db.Column(db.Float)
    trading_pcs = db.Column(db.Integer)
    trading_px = db.Column(db.Float)
    date = db.Column(db.Date, db.ForeignKey('date.day'), nullable=False)
    stockName = db.Column(db.String, db.ForeignKey('company.name'), nullable=False)

    def __repr__(self):
        return 'ID.{} Nazwa: {}, Wartosc: {} PLN '.format(self.id, self.stockName, self.price)

    def __int__(self, price, change):
        self.id = id
        self.price = price
        self.change = change


class UserShares(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_company = db.Column(db.String(300), db.ForeignKey('company.name'))