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
from .models import Ticker
from portfolio.models import Portfolio, UserTicker
from .StockManager import StockManager
logger = logging.getLogger(__name__)




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


@shared_task
def update_user_tickers():
    user_tickers = UserTicker.objects.all()
    for ticker in user_tickers:
        ticker.ticker.save()
        ticker.save()

@shared_task 
def refresh_ticker_data():
    logger.info("==work!")
    print("--------------worked--------------------------------------------")
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
