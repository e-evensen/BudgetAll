from flask_testing import TestCase
from main import create_app
from database import db
from models import User as User
from models import Balance as Balance
import bcrypt
from forms import RegisterForm
from base import BaseTestCase
import unittest


class TestBalancePage(TestCase):
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
        self.balance = Balance(bal=1000.0, user_id=self.user.id)
        self.db.session.add(self.balance)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()

    def test_balance_page_access(self):
        with self.app.test_client() as client:
            # Test that user can access the balance page
            response = client.post('/set_balance', data={'balance': '100'})
            assert response.status_code == 302  # expect a redirect to index page
            assert response.headers['Location'] == 'http://localhost/'

    def test_balance_update(self):
        with self.app.test_client() as client:
            # Test that user can update the balance
            response = client.post('/set_balance', data=dict(
                balance='2000.0'
            ), follow_redirects=True)

            # Test that balance is updated in the database
            balance = Balance.query.filter_by(user_id=self.user.id).first()
            self.assertEqual(balance.bal, 2000.0)

    def test_balance_invalid_input(self):
        with self.app.test_client() as client:
            # Test that user cannot enter non-numeric input for balance
            response = client.post('/balance', data=dict(
                balance='invalid'
            ), follow_redirects=True)

            # Test that an error message is displayed
            self.assertIn(b'Balance must be a number.', response.data)

    def test_set_balance(self):
        with self.app.test_client() as client:
            # send a POST request with a valid balance form
            response = client.post('/set_balance', data={'balance': '100'})
            assert response.status_code == 302  # expect a redirect to index page
            assert response.headers['Location'] == 'http://localhost/'

            # check that the latest balance is displayed on index page
            response = client.get('/')
            assert response.status_code == 200
            assert b'Latest Balance: 100' in response.data

            # send a GET request and expect a 200 response with the balance form
            response = client.get('/set_balance')
            assert response.status_code == 200
            assert b'<form method="post">' in response.data


if __name__ == " __main__":
    unittest.main()
