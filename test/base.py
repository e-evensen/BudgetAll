from flask_testing import TestCase
from main import create_app
from database import db
from models import User
from models import Balance
import bcrypt

class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        db.create_all()
        password = "test_password"
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.session.add(User("testy", "testing@test.com", password))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
