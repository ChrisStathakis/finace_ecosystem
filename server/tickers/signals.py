from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import yfinance as yf
from datetime import datetime
from decimal import Decimal
from .models import Ticker, TickerDataFrame
from .tasks import update_tickers_price_and_price_change
from portfolio.models import UserTicker


@receiver(post_save, sender=Ticker)
def update_ticker_progress(sender, instance: Ticker, created, **kwargs):
    if created:
        # create starting data when object is created
        update_tickers_price_and_price_change.delay()



"""
@receiver(post_save, sender=Ticker)
def create_dataframe_sql_data(sender, instance: Ticker, **kwargs):
    TickerDataFrame.objects.all().delete()
    df: pd.DataFrame = yf.download(instance.ticker, start='2010-01-01', end=datetime.now())
    df.reset_index(inplace=True)
    for _, row in df.iterrows():
        TickerDataFrame.objects.create(date=row['Date'],close=Decimal(row['Close']),ticker=instance)



"""