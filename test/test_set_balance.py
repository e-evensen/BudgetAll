from base import BaseTestCase
import unittest
from models import User, Balance


class TestBalance(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()
        self.balance = Balance.query.filter_by(user_id=self.user.id).order_by(Balance.bal_at.desc()).first()

    def test_page(self):
        response = self.client.get('/set_balance')
        assert response.status_code == 200

    def test_set_balance_requires_login(self):
        with self.client:
            response = self.client.get('/set_balance', follow_redirects=True)
            assert response.status_code == 200
            assert b'Sign In' in response.data

    def test_balance_page_access(self):
        with self.client:
            # Test that user can access the balance page
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )

            response = self.client.get(
                '/set_balance')
            assert response.status_code == 200
            assert b'Set Balance' in response.data

    def test_balance_update(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/set_balance',
                data={'balance': 100.0},
                follow_redirects=True
            )

            balance = Balance.query.filter_by(user_id=self.user.id).order_by(
                Balance.bal_at.desc()).first()
            assert balance.bal == 100.0

    def test_balance_blank_input(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/set_balance',
                data={'balance': ''},
                follow_redirects=True
            )

            # Test that page never redirected away
            assert b'<h2 class="title">Set Balance</h2>\n' in response.data
            # Test that balance is NOT updated in the database
            balance = Balance.query.filter_by(user_id=self.user.id).order_by(Balance.bal_at.desc()).first()
            assert balance.bal != ''

    def test_navbar(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.get('/set_balance')
            assert b'Home' in response.data
            assert b'Calculator' in response.data
            assert b'Update Balance' in response.data
            assert b'Update Income' in response.data
            assert b'View Expenses' in response.data
            assert b'Total Income Calculator' in response.data
            assert b'Logout' in response.data


if __name__ == " __main__":
    unittest.main()
