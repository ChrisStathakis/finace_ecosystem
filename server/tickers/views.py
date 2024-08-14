from django.shortcuts import render, get_object_or_404

from .models import Ticker
from .ticker_helper import TickerHelper


def initial_data_view(request):
    Ticker.create_ticker_database()
    
    return render(request, "initial_data.html")


def ticker_play_area_view(request, pk):
    instance = get_object_or_404(Ticker, id=pk)
    helper = TickerHelper(ticker=instance, market='^GSPC')
    helper.analyze_ticker_wiki()
    return render(request, "play_area.html")