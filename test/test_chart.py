from models import User, Balance
import pandas as pd
from main import generate_chart
from base import BaseTestCase
import unittest
from datetime import datetime, timedelta
from database import db


class TestChart(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.query.filter_by(username="testy").first()

        now = datetime.now()
        one_week = now - timedelta(weeks=1)
        one_month = now - timedelta(days=30)
        six_months = now - timedelta(days=30*6)
        one_year = now - timedelta(days=365)
        over_one_year = now - timedelta(days=380)

        balance_entries = [
            Balance(bal=1700, user_id=self.user.id),
            Balance(bal=1000.0, user_id=self.user.id, bal_at=one_week),
            Balance(bal=1500.0, user_id=self.user.id, bal_at=one_month),
            Balance(bal=2000.0, user_id=self.user.id, bal_at=six_months),
            Balance(bal=2500.0, user_id=self.user.id, bal_at=one_year),
            Balance(bal=3000.0, user_id=self.user.id, bal_at=over_one_year)
        ]

        db.session.add_all(balance_entries)
        db.session.commit()

        df = pd.DataFrame([(b.bal_at, b.bal) for b in balance_entries], columns=['date', 'balance'])
        self.df = df


