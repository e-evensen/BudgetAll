from flask_testing import TestCase
from main import create_app
from database import db
from models import User as User
import bcrypt
from forms import RegisterForm
from base import BaseTestCase
import unittest


class TestRegister(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.username = 'test_user'
        self.email = 'test@example.com'
        self.password = 'test_password'
        self.hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        self.db = db
        self.db.create_all()
        self.user = User(username=self.username, email=self.email, password=self.hashed_password)
        self.db.session.add(self.user)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    # Tests a valid registration and that the user was stored in the database
    def test_user_registration(self):
        with self.app.test_client() as client:
            client.get("/logout", follow_redirects=True)
            client.post("/register", data=dict(
                    email="test@example.com",
                    password="test_password"
                ), follow_redirects=True)
            user = User.query.filter_by(email="test@example.com").first()
            assert user.id
            assert user.email == "test@example.com"

    def test_invalid_registration(self):
        with self.app.test_client() as client:
            response = client.post('/register', data=dict(
                username=self.username,
                email=self.email,
                password=self.password,
                confirmPassword='password12'
            ), follow_redirects=True)

            # check if registration was unsuccessful
            assert response.status_code == 200
            assert b'Passwords must match' in response.data

    def test_register_link_on_home_page(self):
        with self.app.test_client() as client:
            response = client.get('/')
            assert b'<a href="/register">Register</a>' in response.data


if __name__ == " __main__":
    unittest.main()
