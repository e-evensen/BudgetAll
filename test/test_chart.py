from models import User, Balance
from base import BaseTestCase
import unittest
from datetime import datetime, timedelta
from database import db


class TestChart(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()

        now = datetime.now()
        one_week = now - timedelta(days=6)
        one_month = now - timedelta(days=29)
        six_months = now - timedelta(days=30*6)
        one_year = now - timedelta(days=360)
        over_one_year = now - timedelta(days=380)

        balance_entries = [
            Balance(bal=1250.0, user_id=self.user.id, bal_at=one_week),
            Balance(bal=1500.0, user_id=self.user.id, bal_at=one_month),
            Balance(bal=2000.0, user_id=self.user.id, bal_at=six_months),
            Balance(bal=2500.0, user_id=self.user.id, bal_at=one_year),
            Balance(bal=3000.0, user_id=self.user.id, bal_at=over_one_year)
        ]

        db.session.add_all(balance_entries)
        db.session.commit()

    def test_index_loads_chart(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'"balance": 1250.0' in response.data
        assert b'"balance": 1500.0' in response.data
        assert b'"balance": 2000.0' in response.data
        assert b'"balance": 2500.0' in response.data
        assert b'"balance": 3000.0' in response.data

    def test_chart_no_user(self):
        response = self.client.get('/')
        assert b'Sign In' in response.data
        assert b'"balance": 1250.0' not in response.data
        assert b'"balance": 1500.0' not in response.data
        assert b'"balance": 2000.0' not in response.data
        assert b'"balance": 2500.0' not in response.data
        assert b'"balance": 3000.0' not in response.data

    def test_dropdown_views(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
        now = datetime.now()
        one_week = (now - timedelta(days=6)).strftime('%Y-%m-%d')
        one_month = (now - timedelta(days=29)).strftime('%Y-%m-%d')
        six_months = (now - timedelta(days=30 * 6)).strftime('%Y-%m-%d')
        one_year = (now - timedelta(days=360)).strftime('%Y-%m-%d')
        over_one_year = (now - timedelta(days=380)).strftime('%Y-%m-%d')
        # default view is all time
        response = self.client.get('/')
        assert over_one_year.encode() in response.data

        response = self.client.get('index?time_range=1_week')
        assert one_week.encode() in response.data
        assert one_month.encode() not in response.data

        response = self.client.get('index?time_range=1_month')
        assert one_month.encode() in response.data
        assert six_months.encode() not in response.data

        response = self.client.get('index?time_range=6_months')
        assert six_months.encode() in response.data
        assert one_year.encode() not in response.data

        response = self.client.get('index?time_range=1_year')
        assert one_year.encode() in response.data
        assert over_one_year.encode() not in response.data

    def test_dropdown_list(self):
        with self.client:
            self.client.post(
                '/login', data=dict(
                    email='testing@test.com',
                    password='test_password'
                ), follow_redirects=True
            )
            response = self.client.get('/')
            assert b'<option value="1_week">1 Week</option>' in response.data
            assert b'<option value="1_month">1 Month</option>' in response.data
            assert b'<option value="6_months">6 Months</option>' in response.data
            assert b'<option value="1_year">1 Year</option>' in response.data
            assert b'<option value="all_time">All Time</option>' in response.data


if __name__ == " __main__":
    unittest.main()
