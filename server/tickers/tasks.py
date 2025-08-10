import datetime

from server.celery import app
from celery import shared_task
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core.serializers import serialize
import logging
from .models import Ticker, TickerDataFrame
from portfolio.models import Portfolio, UserTicker
from tickers.helpers_folder.StockManager import StockManager
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
@shared_task
def daily_update_data_task():
    
    tickers = Ticker.objects.all()
    for ticker in tickers:
        try:
            print("ticker", ticker)
            stock_manager = StockManager(ticker=ticker)
            # ticker.predict = stock_manager.predict_the_future()
            # ticker.date_predict = datetime.datetime.now()
            ticker.save()
        except:
            ticker.delete()
"""

"""

"""
"""
@shared_task 
def refresh_ticker_data():
    logger.info("==work!")
    tickers = Ticker.objects.all()
    for ele in tickers:
        print("Ticker: " + ele.title)
        try:
            ele.save()
        except Exception as e:
            print("Failed:" + ele.title)
            print("Exception: ", e)
            ele.delete()
    
    serialized_data = serialize('json', tickers)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'ticker_refresh_data',
        {
            "type": "refresh_data",
            "data": json.loads(serialized_data)
        }
    )


@shared_task
def refresh_portfolio_tickers(port_id):
    print('refreshed!')
    instance = get_object_or_404(Portfolio, id=port_id)
    tickers = UserTicker.objects.filter(portfolio=instance)
    context = {"my_tickers": tickers}
    html_message = render_to_string('ajax/tickers_container.html', context)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'portfolio_{instance.id}',
        {
            "type": "refresh_data",
            "message": html_message
        }
    )


@shared_task
def update_ticker_from_detail_page(ticker_id: id):
    instance = get_object_or_404(Ticker, id=ticker_id)
    instance.save()
    
"""
