from django.urls import path

from .views import (PortfolioListApiView, PortfolioUpdateRetrieveApiView, UserTickerListApiView,
                    UserTickerRetrieveApiView, UserTickerUpdateDeleteApiView,  UserTickerCreateApiView,
                    efficient_frontier_view
                    )

app_name = 'api_portfolio'

urlpatterns = [
    path("/efficient-frontier/", efficient_frontier_view, name="efficient_frontier"),
    
    path("portfolios/list/", PortfolioListApiView.as_view(), name="portfolio_list"),
    path("portfolio/detail/<int:pk>/", PortfolioUpdateRetrieveApiView.as_view(), name="portfolio_update"),

    path("user-tickers/list/", UserTickerListApiView.as_view(), name="user_ticker_list"),
    path("user-tickers/detail/<int:pk>/", UserTickerRetrieveApiView.as_view(), name="user_ticker_detail"),
    path("user-tickers/update/<int:pk>/", UserTickerUpdateDeleteApiView.as_view(), name="user_ticker_update"),
    path("user-tickers/create/", UserTickerCreateApiView.as_view(), name="user_ticker_create"),



]