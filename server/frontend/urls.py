from django.urls import path

from frontend.views import (homepage_view, PortfolioListView, PortfolioDetailView, create_portfolio_item_view,
                            TickerListView, ticker_detail_view
                            )
from .ajax_views import search_tickers_json_view

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path("portfolios/", PortfolioListView.as_view(), name="portfolios"),
    path("tickers/", TickerListView.as_view(), name="tickers_list"),
    path('ticker/<int:pk>/', ticker_detail_view, name="ticker_detail"),
    path("portfolio/<int:port_id>/", PortfolioDetailView.as_view(), name='portfolio'),
    path("create-item-portfolio/<int:dk>/<int:pk>/", create_portfolio_item_view, name="create_item_portfolio"),



    # ajax
    path('ajax-search-tickers/<int:pk>/', search_tickers_json_view, name='search_tickers_json_view'),


]