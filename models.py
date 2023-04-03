from database import db
from datetime import datetime


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.registered_on = datetime.now()


class Balance(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    bal = db.Column("bal", db.Float)
    bal_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, bal, user_id):
        self.bal = bal
        self.user_id = user_id
        self.bal_at = datetime.now()


class Expense(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    exp_name = db.Column("exp_name", db.String)
    exp = db.Column("exp", db.Float)
    exp_cat = db.Column("exp_cat", db.String)
    exp_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, exp_name, exp, exp_cat, user_id):
        self.exp_name = exp_name
        self.exp = exp
        self.exp_cat = exp_cat
        self.user_id = user_id
        self.exp_time = datetime.now()


class Income(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    inc = db.Column("inc", db.Float)
    inc_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, inc, user_id):
        self.inc = inc
        self.user_id = user_id
        self.inc_at = datetime.now()
