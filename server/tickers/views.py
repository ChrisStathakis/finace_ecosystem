from django.shortcuts import render

from .models import Ticker


def initial_data_view(request):
    Ticker.create_ticker_database()
    
    return render(request, "initial_data.html")