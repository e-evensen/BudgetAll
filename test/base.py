from flask_testing import TestCase
from main import create_app
from database import db
from models import User, Balance, Income, Expense
import bcrypt


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        db.create_all()
        password = "test_password"
        hpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User("testy", "testing@test.com", hpassword)
        db.session.add(user)
        db.session.flush()
        balance = Balance(bal=1000.0, user_id=user.id)
        db.session.add(balance)
        db.session.commit()
        income = Income(inc=30000, user_id=user.id)
        db.session.add(income)
        db.session.commit()
        expense = Expense(exp_name='test name',
                          exp=100,
                          exp_cat='test cat',
                          user_id=user.id
                          )
        db.session.add(expense)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
