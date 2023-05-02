from models import User, Expense
from base import BaseTestCase
import unittest


class TestExpense(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()

    def test_page(self):
        response = self.client.get('/view_expenses')
        assert response.status_code == 200

    def test_expense_requires_login(self):
        with self.client:
            response = self.client.get('/view_expenses', follow_redirects=True)
            assert response.status_code == 200
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
                          expense_category='High'
                          ),
                follow_redirects=True)
            assert response.status_code == 200

            expense = Expense.query.filter_by(exp_name='Test expense').first()
            assert expense is not None
            assert expense.exp == 10.99
            assert expense.exp_cat == 'High'

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
                data=dict(expense_description='Neg Expense',
                          expense_amount='-10.0',
                          expense_category='High'
                          ), follow_redirects=True
            )
            assert b'Neg Expense' not in response.data

    def test_delete_expense(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            self.client.post(
                '/add_expenses',
                data=dict(expense_description='Delete Desc',
                          expense_amount='50.0',
                          expense_category='Delete Cat'
                          ), follow_redirects=True
            )
            exp = Expense.query.filter_by(exp_name='Delete Desc').first()
            assert exp is not None
            response = self.client.post(f'/delete/{exp.id}', follow_redirects=True)
            assert response.status_code == 200
            del_exp = Expense.query.get(exp.id)
            assert del_exp is None
            assert b'Delete Desc' not in response.data

    def test_edit_expense(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            self.client.post(
                '/add_expenses',
                data=dict(expense_description='Update Desc',
                          expense_amount='75.0',
                          expense_category='Low'
                          ), follow_redirects=True
            )
            exp = Expense.query.filter_by(exp_name='Update Desc').first()
            response = self.client.post(
                f'/update/{exp.id}',
                data=dict(update_exp_name='New Desc',
                          update_exp='99.0',
                          update_exp_cat='High'
                          ), follow_redirects=True
            )
            assert exp.exp_name == 'New Desc'
            assert exp.exp == 99.0
            assert exp.exp_cat == 'High'
            assert b'New Desc' in response.data
            assert b'99.0' in response.data
            assert b'High' in response.data

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
