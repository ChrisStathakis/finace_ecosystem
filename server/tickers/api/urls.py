from django.urls import path

from .views import (TickerListApiView, ticker_homepage_api_view,
                    TickerRetrieveApiView, TickerDataFrameListApiView,
                    TickerPredictionsApiView, TickerCreateApiView
                    )

app_name = 'api_tickers'

urlpatterns = [
    path('', ticker_homepage_api_view, name="home"),
    path('tickers/list/', TickerListApiView.as_view(), name="tickers_list"),
    path("ticker/create/", TickerCreateApiView.as_view(), name="ticker_create"),
    path("ticker/detail/<int:pk>/", TickerRetrieveApiView.as_view(), name="ticker_detail"),
    path("tickers/dataframe/", TickerDataFrameListApiView.as_view(), name="ticker_dataframe"),
    path("tickers/prediction/<int:pk>/", TickerPredictionsApiView.as_view(), name="ticker_prediction"),


]

# 43