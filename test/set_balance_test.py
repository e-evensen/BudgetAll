from base import BaseTestCase
import unittest
from models import User, Balance


class TestBalancePage(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()
        self.balance = Balance.query.filter_by(user_id=self.user.id).first()

    def test_set_balance_requires_login(self):
        with self.client:
            response = self.client.get('/set_balance', follow_redirects=True)
            assert response.status_code == 200
            print(response.data)
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
                data={'balance': '100'},
                follow_redirects=True
            )

            # Test that balance is updated in the database
            balance = self.balance.query.filter_by().first()
            assert balance.bal == 100.0

    def test_balance_invalid_input(self):
        with self.app.test_client() as client:
            # Test that user cannot enter non-numeric input for balance
            response = client.post('/balance', data=dict(
                balance='invalid'
            ), follow_redirects=True)

            # Test that an error message is displayed
            self.assertIn(b'Balance must be a number.', response.data)


if __name__ == " __main__":
    unittest.main()
