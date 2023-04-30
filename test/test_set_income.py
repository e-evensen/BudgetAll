from base import BaseTestCase
import unittest
from models import User, Income


class TestIncome(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()
        self.income = Income.query.filter_by(user_id=self.user.id).order_by(Income.inc_at.desc()).first()

    def test_page(self):
        response = self.client.get('/set_income')
        assert response.status_code == 200

    def test_set_income_requires_login(self):
        with self.client:
            response = self.client.get('/set_income', follow_redirects=True)
            assert response.status_code == 200
            print(response.data)
            assert b'Sign In' in response.data

    def test_income_page_access(self):
        with self.client:
            # Test that user can access the income page
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )

            response = self.client.get(
                '/set_income')
            assert response.status_code == 200
            assert b'Set Income' in response.data

    def test_income_update(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/set_income',
                data={'income': 40000.0},
                follow_redirects=True
            )

            income = Income.query.filter_by(user_id=self.user.id).order_by(
                Income.inc_at.desc()).first()
            assert income.inc == 40000.0

    def test_income_blank_input(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/set_income',
                data={'income': ''},
                follow_redirects=True
            )

            # Test that page never redirected away
            assert b'<h2 class="title">Set Annual Income</h2>\n' in response.data
            # Test that income is NOT updated in the database
            income = Income.query.filter_by(user_id=self.user.id).order_by(Income.inc_at.desc()).first()
            print(income.inc)
            assert income.inc != 'test'

    def test_income_negative_input(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/set_income',
                data={'income': -10000},
                follow_redirects=True
            )

            # Test that page never redirected away
            assert b'Income must be greater than or equal to zero.' in response.data
            # Test that income is NOT updated in the database
            income = Income.query.filter_by(user_id=self.user.id).order_by(Income.inc_at.desc()).first()
            assert income.inc != -10000

    def test_navbar(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.get('/set_income')
            assert b'Home' in response.data
            assert b'Calculator' in response.data
            assert b'Update Balance' in response.data
            assert b'Update Income' in response.data
            assert b'View Expenses' in response.data
            assert b'Total Income Calculator' in response.data
            assert b'Logout' in response.data


if __name__ == " __main__":
    unittest.main()
