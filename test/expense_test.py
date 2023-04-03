from models import User, Expense
from base import BaseTestCase
import unittest


class TestExpense(BaseTestCase):
    def test_expense_page_with_user(self):
        with self.client:
            self.client.post('/login', data=dict(
                email='testing@test.com',
                password='test_password'
            ), follow_redirects=True)
            response = self.client.get('/view_expenses')
            self.assert200(response)
            self.assertIn(b'test name', response.data)
            self.assertIn(b'100', response.data)
            self.assertIn(b'test cat', response.data)

    def test_add_expenses(self):
        with self.client:
            # Simulate a login session
            with self.client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user'] = 'testy'

            # Test adding a new expense
            response = self.client.post('/add_expenses', data={
                'expense_description': 'Test expense',
                'expense_amount': 10.99,
                'expense_category': 'Test category'
            })

            assert response.status_code == 200

            # Check that the expense was added to the database
            expense = Expense.query.filter_by(exp_name='Test expense').first()
            assert expense
            assert expense.exp == 10.99
            assert expense.exp_cat == 'Test category'

            # Check that the expense is displayed on the view expenses page
            response = self.client.get('/view_expenses')
            assert b'Test expense' in response.data


if __name__ == " __main__":
    unittest.main()
