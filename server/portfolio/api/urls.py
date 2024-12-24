from django.urls import path

from .views import (UserTickerDeleteApiView, PortfolioListApiView, PortfolioUpdateRetrieveApiView, UserTickerListApiView,
                    UserTickerCreateApiView, UserTickerUpdateDeleteApiView, efficient_frontier_view,
                    UserTickerRetrieveApiView, ticker_homepage_api_view

                    )

app_name = "api_port"

urlpatterns = [
    path("", ticker_homepage_api_view, name="homepage"),
    path("portfolios/list/", PortfolioListApiView.as_view(), name="list"),
    path("portfolio/detail/<int:pk>/", PortfolioUpdateRetrieveApiView.as_view(), name="portfolio_update"),

    path("user-tickers/list/", UserTickerListApiView.as_view(), name="user_ticker_list"),
    path("user-tickers/detail/<int:pk>/", UserTickerRetrieveApiView.as_view(), name="user_ticker_detail"),
    path("user-tickers/update/<int:pk>/", UserTickerUpdateDeleteApiView.as_view(), name="user_ticker_update"),
    path("user-tickers/create/", UserTickerCreateApiView.as_view(), name="user_ticker_create"),
    path("delete/<int:pk>/", UserTickerDeleteApiView.as_view(), name="delete"),
    path("/efficient-frontier/", efficient_frontier_view, name="efficient_frontier"),
]