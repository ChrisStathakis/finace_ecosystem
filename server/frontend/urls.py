from django.urls import path

from frontend.views import homepage_view
from .ajax_views import search_tickers_json_view


urlpatterns = [
    path('', homepage_view, name='homepage'),
    # ajax
    path('ajax-search-tickers/<int:pk>/', search_tickers_json_view, name='search_tickers_json_view'),


]