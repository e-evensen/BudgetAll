from base import BaseTestCase
import unittest


class TestLogin(BaseTestCase):
    def test_page(self):
        response = self.client.get('/login')
        assert response.status_code == 200

    def test_successful_login(self):
        with self.client:
            response = self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            assert b'Your balance is' in response.data

    def test_invalid_email(self):
        with self.client:
            response = self.client.post(
                '/login', data=dict(
                    email='test',
                    password='test_password'
                ), follow_redirects=True
            )
            assert b'Not a valid email address.' in response.data

    def test_invalid_password(self):
        with self.client:
            response = self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test'
                ), follow_redirects=True
            )
            assert b'Incorrect password.' in response.data

    def test_logout(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.get(
                '/logout'
                , follow_redirects=True
            )
            assert b'Sign In' in response.data

    def test_navbar(self):
        response = self.client.get('/calculator')
        assert b'Home' in response.data
        assert b'Calculator' in response.data
        assert b'Sign In' in response.data
        assert b'Register' in response.data


if __name__ == " __main__":
    unittest.main()
