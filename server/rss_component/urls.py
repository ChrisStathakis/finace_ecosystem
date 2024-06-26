from django.urls import path

from .views import (RssFeedListView, analysis_rss_view, refresh_tickers_view, rss_detail_view)

app_name = 'rss'

urlpatterns = [
    path('list/', RssFeedListView.as_view(), name='list'),
    path('refresh/rss/', refresh_tickers_view, name='refresh_rss'),
    path('analysis/rss/', analysis_rss_view, name="analysis_rss"),
    path('detail/<int:pk>/', rss_detail_view, name="detail_view")


]