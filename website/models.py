from . import db
from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy_utils import ChoiceType


class Category(db.Model):

    TRANSACTIONS = [
        ('in', 'Income'),
        ('ex', 'Expense')
    ]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20))
    transaction = db.Column(ChoiceType(TRANSACTIONS))
    transactions = db.relationship('Transaction', backref='category')


class Transaction(db.Model):

    TYPES = [
        ('in', 'Income'),
        ('ex', 'Expense')
    ]

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    transaction_type = db.Column(ChoiceType(TYPES))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    value = db.Column(db.Integer)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    description = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction', backref='account')
    balance = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30))
    l_name = db.Column(db.String(30))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(150))
    accounts = db.relationship('Account')
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime)
