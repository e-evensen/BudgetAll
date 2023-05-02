from models import User, Expense
from base import BaseTestCase
import unittest


class TestDeleteSort (BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()

    # Test that page responds
    def test_page(self):
        response = self.client.get('view_expenses')
        assert response.status_code == 200

    # Test that page requires login
    def test_requires_login(self):
        with self.client:
            response = self.client.get('/view_expenses', follow_redirects=True)
            assert response.status_code == 200
            print(response.data)
            assert b'Sign In' in response.data

    # Test income is deleted
    # Uses delete(id) in main.py
    def test_delete_expense(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        response = self.client.post(
            '/delete/<int:id>',
            data=dict(expense_to_delete=1
            ), follow_redirects=True
        )
        assert response.status_code == 200

        deleted = Expense.query.filter_by(id=1).first()
        assert deleted is None

    # Tests sorting of expense table
    
    # Tests sorting, visually in expense.js, not sure where in python
    def test_sort_expenses(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        
            response = self.client.get('/view_expenses')


if __name__ == " __main__":
    unittest.main()
