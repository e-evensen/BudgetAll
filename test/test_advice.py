from base import BaseTestCase
import unittest


class TestAdvice(BaseTestCase):
    def test_no_user(self):
        response = self.client.get('/advice')
        assert response.status_code == 200
        assert b'Budgeting is the process of creating a plan to manage your income and expenses.' in response.data

    def test_logged_in_user(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        response = self.client.get('/advice')
        assert response.status_code == 200
        assert b'Budgeting is the process of creating a plan to manage your income and expenses.' in response.data

    def test_navbar_logged_in(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.get('/advice')
            assert b'Home' in response.data
            assert b'Calculator' in response.data
            assert b'Update Balance' in response.data
            assert b'Update Income' in response.data
            assert b'View Expenses' in response.data
            assert b'Total Income Calculator' in response.data
            assert b'Logout' in response.data

    def test_navbar_not_logged_in(self):
        response = self.client.get('/advice')
        assert b'Home' in response.data
        assert b'Calculator' in response.data
        assert b'Sign In' in response.data
        assert b'Register' in response.data


if __name__ == " __main__":
    unittest.main()
