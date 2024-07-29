from django.db import models
from django.contrib.auth import get_user_model
import datetime
from datetime import timedelta
import pandas as pd

from tickers.models import Ticker
from tickers.helpers import read_stock_data, get_stock_data


User = get_user_model()


class Strategy(models.Model):
    CHOICES = (
        ('a', 'Moving Average Trading Strategy'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=CHOICES)

    class Meta:
        unique_together = ["user", "category"]


class StrategyTicker(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker.title

    def get_dataframe(self, days=360, is_updated=False):
        date_start = datetime.datetime.now() - timedelta(days=days)
        return read_stock_data(
            ticker=self.ticker.ticker,
            start=date_start,
            end=datetime.datetime.now().today(),
            updated=is_updated
        )

    def EMA(self, average_length=50):