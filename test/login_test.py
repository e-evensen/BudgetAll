from flask_testing import TestCase
from main import create_app
from database import db
from models import User as User
from models import Balance as Balance
import bcrypt
from forms import LoginForm
from base import BaseTestCase
import unittest


class Login(BaseTestCase):
    def test_index(self):
        response = self.client.get('/login')
        assert response.status_code == 200

    def test_set_balance_requires_login(self):
        response = self.client.get('/set_balance', follow_redirects=True)
        assert response.status_code == 200
        assert b'Email' in response.data

    def test_successful_login(self):
        response = self.client.post(
            '/login',
            data=dict(email='testing@test.com', password='test_password'),
            follow_redirects=True
        )
        assert b'logout' in response.data


class LoginTest(TestCase):
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

    def test_login_form(self):
        form = LoginForm(email='test@example.com', password='test_password')
        assert form.validate()

    def test_login_link_present_when_not_logged_in(self):
        with self.app.app_context():
            with self.app.test_client() as client:
                with client.session_transaction() as session:
                    session.clear()
                response = client.get('/')
                assert b'<a href="/login"> Sign In</a>' in response.data

    def test_successful_login(self):
        with self.app.app_context():
            with self.app.test_client() as client:
                response = client.get('/')
                print(response.data)
                assert response.status_code == 200
                assert b'Logout' in response.data
                print(response.data)

    def test_login_with_invalid_email(self):
        with self.client:
            form = LoginForm(email='t@t.com', password='test_password')
            self.assertFalse(form.validate())

    def test_login_with_invalid_password(self):
        with self.client:
            form = LoginForm(email='test@example.com', password='wrong_password')
            self.assertFalse(form.validate())

    def test_logout(self):
        with self.app.test_client() as client:
            response = client.get('/logout', follow_redirects=True)
            assert response.status_code == 200
            assert b'Logout' not in response.data





if __name__ == " __main__":
    unittest.main()