from django.urls import path

from .views import (portfolio_view, create_portfolio_item_view, delete_ticker_view, sell_ticker_view
                    

                    )


app_name = "port"

urlpatterns = [
    path("", portfolio_view, name="home"),
    path("add-item/<int:pk>/<int:dk>/", create_portfolio_item_view, name="add_item"),
    path("sell/<int:pk>/", sell_ticker_view, name="sell"),
    path("delete/<int:pk>/", delete_ticker_view, name="delete")

    
]