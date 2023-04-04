from models import User, Expense
from base import BaseTestCase
import unittest


class TestExpense(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()

    def test_expense_requires_login(self):
        with self.client:
            response = self.client.get('/view_expenses', follow_redirects=True)
            assert response.status_code == 200
            print(response.data)
            assert b'Sign In' in response.data

    def test_expense_page_with_user(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )

            response = self.client.get('/view_expenses')
            assert response.status_code == 200
            assert b'test name' in response.data
            assert b'100' in response.data
            assert b'test cat' in response.data

    def test_add_expenses(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )

            response = self.client.post(
                '/add_expenses',
                data=dict(expense_description='Test expense',
                          expense_amount='10.99',
                          expense_category='Test category'
                          ),
                follow_redirects=True)
            assert response.status_code == 200

            # Check that the expense was added to the database
            expense = Expense.query.filter_by(exp_name='Test expense').first()
            assert expense is not None
            assert expense.exp == 10.99
            assert expense.exp_cat == 'Test category'

            # Check that the expense is displayed on the view expenses page
            response = self.client.get('/view_expenses')
            assert b'Test expense' in response.data

    def test_amount_negative_input(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/add_expenses',
                data=dict(expense_description='Test expense',
                          expense_amount='-10.0',
                          expense_category='Test category'
                          ), follow_redirects=True
            )
            assert b'<td>$ 100.0</td>\n' in response.data

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
