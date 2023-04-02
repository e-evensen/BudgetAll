
from models import User
from base import BaseTestCase
import unittest


class TestRegister(BaseTestCase):
    def test_page(self):
        response = self.client.get('/register')
        assert response.status_code == 200

    # Tests a valid registration and that the user was stored in the database
    def test_user_registration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='test',
                email='test@test.com',
                password='password123',
                confirmPassword='password123'
            ), follow_redirects=True)
            user = User.query.filter_by(email='test@test.com').first()
            assert b"Your balance is" in response.data
            assert user.username == 'test'

    def test_invalid_email(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='test',
                email='t',
                password='password123',
                confirmPassword='password12'
            ), follow_redirects=True)

            # check if registration was unsuccessful
            assert response.status_code == 200
            assert b'Not a valid email address.' in response.data

    def test_confirm_password(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='test',
                email='test@test.com',
                password='password123',
                confirmPassword='password12'
            ), follow_redirects=True)

            # check if registration was unsuccessful
            assert response.status_code == 200
            assert b'Passwords must match' in response.data

    def test_no_username(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='',
                email='test@test.com',
                password='password123',
                confirmPassword='password123'
            ), follow_redirects=True)

            # check if registration was unsuccessful
            assert response.status_code == 200
            assert b'Field must be between 1 and 10 characters long.' in response.data

    def test_same_email(self):
        with self.client:
            self.client.post('/register', data=dict(
                username='test',
                email='test@test.com',
                password='password123',
                confirmPassword='password123'
            ), follow_redirects=True)

            response = self.client.post('/register', data=dict(
                username='test1',
                email='test@test.com',
                password='password123',
                confirmPassword='password123'
            ), follow_redirects=True)
            assert response.status_code == 200
            assert b'Email already in use.' in response.data


if __name__ == " __main__":
    unittest.main()
