from django.urls import path

from frontend.views import (homepage_view, 
                            TickerListView, ticker_detail_view
                            )
from .ajax_views import search_tickers_json_view

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path("tickers/", TickerListView.as_view(), name="tickers_list"),
    path('ticker/<int:pk>/', ticker_detail_view, name="ticker_detail"),
   
    # ajax
    path('ajax-search-tickers/<int:pk>/', search_tickers_json_view, name='search_tickers_json_view'),


]