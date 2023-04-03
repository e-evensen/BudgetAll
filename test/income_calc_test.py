from base import BaseTestCase
import unittest


class TestCalculator(BaseTestCase):
    def test_page_requires_login(self):
        with self.client:
            response = self.client.get('/total_income', follow_redirects=True)
            assert response.status_code == 200
            print(response.data)
            assert b'Sign In' in response.data

    def test_logged_in_user(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        response = self.client.get('/total_income')
        assert response.status_code == 200
        assert b'Bi-Weekly Income:' in response.data

    def test_navbar_logged_in(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.get('/total_income')
            assert b'Home' in response.data
            assert b'Calculator' in response.data
            assert b'Update Balance' in response.data
            assert b'Update Income' in response.data
            assert b'View Expenses' in response.data
            assert b'Total Income Calculator' in response.data
            assert b'Logout' in response.data


if __name__ == " __main__":
    unittest.main()
