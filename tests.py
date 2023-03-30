from flask_testing import TestCase
import unittest
import requests
from main import create_app
from database import db
from models import User as User
import bcrypt


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

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_valid_registration(self):
        with self.app.test_client() as client:
            response = client.post('/register', data=dict(
                    username=self.username,
                    email=self.email,
                    password=self.password,
                    confirmPassword=self.password
            ), follow_redirects=False)

            # check if registration was successful
            self.assertEqual(response.status_code, 302)
            self.assertIn('/index', response.headers['Location'])

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

    def test_new_user_is_stored_in_database(self):
        with self.app.test_client():
            new_user = User(username=self.username, email=self.email, password=self.password)
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(username=self.username).first()

            assert user is not None
            assert user.username == self.username
            assert user.email == self.email
            assert user.password == self.password  # Password should be hashed


if __name__ == " __main__":
    unittest.main()