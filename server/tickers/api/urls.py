from django.urls import path

from .views import (TickerListApiView, ticker_homepage_api_view, PortfolioListApiView,
                    PortfolioUpdateRetrieveApiView, UserTickerListApiView,
                    TickerRetrieveApiView, TickerDataFrameListApiView, UserTickerRetrieveApiView,
                    UserTickerUpdateDeleteApiView, TickerPredictionsApiView, UserTickerCreateApiView,
                    efficient_frontier_view, TickerCreateApiView
                    )

app_name = 'api_tickers'

urlpatterns = [
    path('', ticker_homepage_api_view, name="home"),

    path("/efficient-frontier/", efficient_frontier_view, name="efficient_frontier"),
    path('tickers/list/', TickerListApiView.as_view(), name="tickers_list"),
    path("ticker/create/", TickerCreateApiView.as_view(), name="ticker_create"),
    path("detail/<int:pk>/", TickerRetrieveApiView.as_view(), name="ticker_detail"),
    path("tickers/dataframe/", TickerDataFrameListApiView.as_view(), name="ticker_dataframe"),
    path("tickers/prediction/<int:pk>/", TickerPredictionsApiView.as_view(), name="ticker_prediction"),

    path("portfolios/list/", PortfolioListApiView.as_view(), name="portfolio_list"),
    path("portfolio/detail/<int:pk>/", PortfolioUpdateRetrieveApiView.as_view(), name="portfolio_update"),

    path("user-tickers/list/", UserTickerListApiView.as_view(), name="user_ticker_list"),
    path("user-tickers/detail/<int:pk>/", UserTickerRetrieveApiView.as_view(), name="user_ticker_detail"),
    path("user-tickers/update/<int:pk>/", UserTickerUpdateDeleteApiView.as_view(), name="user_ticker_update"),
    path("user-tickers/create/", UserTickerCreateApiView.as_view(), name="user_ticker_create"),



]