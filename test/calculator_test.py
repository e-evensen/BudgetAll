from base import BaseTestCase
import unittest


class TestCalculator(BaseTestCase):
    def test_no_user(self):
        response = self.client.get('/calculator')
        assert response.status_code == 200
        assert b'Enter how much you want to save up' in response.data

    def test_logged_in_user(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        response = self.client.get('/calculator')
        assert response.status_code == 200
        assert b'Enter how much you want to save up' in response.data


if __name__ == " __main__":
    unittest.main()
