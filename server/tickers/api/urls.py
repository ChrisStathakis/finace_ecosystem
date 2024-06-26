from django.urls import path

from .views import (TickerListApiView, ticker_homepage_api_view, PortfolioListApiView,
                    TickerRetrieveApiView, TickerDataFrameListApiView
                    )

app_name = 'api_tickers'

urlpatterns = [
    path('', ticker_homepage_api_view, name="home"),
    path('tickers/list/', TickerListApiView.as_view(), name="tickers_list"),
    path("detail/<int:pk>/", TickerRetrieveApiView.as_view(), name="ticker_detail"),
    path("portfolios/list/", PortfolioListApiView.as_view(), name="portfolio_list"),
    path("tickers/dataframe/", TickerDataFrameListApiView.as_view(), name="ticker_dataframe")

]