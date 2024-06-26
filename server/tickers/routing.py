from django.urls import path

from .consumers import TickerConsumer


websocket_urlpatterns = [
    path("ws/tickers/refresh/<int:port_id>/", TickerConsumer.as_asgi())
]