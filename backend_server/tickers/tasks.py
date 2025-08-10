import datetime

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from celery import shared_task
from asgiref.sync import async_to_sync
import json
from django.core.serializers import serialize
import logging
from .models import Ticker, TickerDataFrame

logger = logging.getLogger(__name__)


@shared_task
def update_tickers_price_and_price_change():
    qs = Ticker.objects.all()
    for ticker in qs:
        ticker.soft_update()
        TickerDataFrame._create_dataframe(
            is_period=True,
            period="7d"
        )

"""
@shared_task
def refresh_unique_ticker_data(ticker_id: int):
    # refresh the data from ticker on signal to avoid delay
    ticker: Ticker = get_object_or_404(Ticker, id=ticker_id)
    ticker.update_ticker_data()
    ticker.wikipedia_url = ticker.find_wikipedia_url()
    ticker.create_tags()
    ticker.save()
    ticker.create_ticker_database()
    return f"f{Ticker.ticker} saved"


@shared_task
def refresh_ticker_data():
    tickers = Ticker.objects.all()
    for ticker in tickers:
        print("Ticker: " + ticker.title)
        try:
            ticker.update_ticker_data()
            ticker.create_ticker_database()
            ticker.save()
        except Exception as e:
            print("Failed:" + ticker.title)
            print("Exception: ", e)

"""



