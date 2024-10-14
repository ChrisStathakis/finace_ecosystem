from django.db.models.signals import post_save
from django.dispatch import receiver

import pandas as pd
import yfinance as yf
from datetime import datetime
from decimal import Decimal
from .models import Ticker, TickerDataFrame
from portfolio.models import UserTicker


@receiver(post_save, sender=Ticker)
def create_dataframe_sql_data(sender, instance: Ticker, **kwargs):
    TickerDataFrame.objects.all().delete()
    df: pd.DataFrame = yf.download(instance.ticker, start='2010-01-01', end=datetime.now())
    df.reset_index(inplace=True)
    for _, row in df.iterrows():
        TickerDataFrame.objects.create(date=row['Date'],close=Decimal(row['Close']),ticker=instance)



@receiver(post_save, sender=Ticker)
def update_user_tickers(sender, instance: Ticker, **kwargs):
    user_tickers = UserTicker.objects.filter(ticker=instance)
    for tic in user_tickers:
        tic.save()



@receiver(post_save, sender=UserTicker)
def create_and_update_user_ticker(sender, instance: UserTicker, created,  **kwargs):
    if created:
        ticker = instance.ticker
        instance.starting_value_of_ticker = instance.ticker.price if instance.starting_value_of_ticker == 0 \
            else instance.starting_value_of_ticker
        instance.qty = instance.starting_investment/instance.starting_value_of_ticker if instance.starting_value_of_ticker !=0 else 0
        instance.save()