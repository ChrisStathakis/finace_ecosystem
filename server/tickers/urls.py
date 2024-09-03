from django.urls import path

from .views import CreateTickerView, TickerListView, ticker_detail_view

app_name = "tickers"

urlpatterns = [
    path("", TickerListView.as_view(), name="list"),
    path("detail/<int:pk>/", ticker_detail_view, name="detail"),
    path("create/", CreateTickerView.as_view(), name="create"),

]