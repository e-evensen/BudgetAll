from models import User, Purchase
from base import BaseTestCase
import unittest


class TestPurchase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()

    def test_page(self):
        response = self.client.get('/purchases')
        assert response.status_code == 200

    def test_purchase_requires_login(self):
        with self.client:
            response = self.client.get('/purchases', follow_redirects=True)
            assert response.status_code == 200
            assert b'Sign In' in response.data

    def test_purchase_page_with_user(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )

            response = self.client.get('/purchases')
            assert response.status_code == 200
            assert b'test purchase' in response.data
            assert b'300' in response.data

    def test_purchases(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )

            response = self.client.post(
                '/add_purchases',
                data=dict(product_name='test purchase',
                          product_amount='10.99'
                          ),
                follow_redirects=True)
            assert response.status_code == 200

            purchase = Purchase.query.filter_by(pur_name='test purchase').first()
            assert purchase is not None
            assert b'<td>$ 10.99</td>' in response.data

            response = self.client.get('/purchases')
            assert b'test purchase' in response.data

    def test_amount_negative_input(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.post(
                '/add_purchases',
                data=dict(product_name='test purchase',
                          product_amount='-10'
                          ), follow_redirects=True
            )
            assert b'$ -10.00' not in response.data
            assert b'<td>$ 300.0</td>\n' in response.data


if __name__ == " __main__":
    unittest.main()

