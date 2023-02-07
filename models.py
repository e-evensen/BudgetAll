from database import db
import datetime


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
        self.registered_on = datetime.date.today()


class Balance(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    bal = db.Column("bal", db.Integer)
    bal_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, bal, bal_at, user_id):
        self.bal = bal
        self.bal_at = bal_at
        self.user_id = user_id
