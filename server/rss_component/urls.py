from django.urls import path

from .views import (RssFeedListView, rss_detail_view)

app_name = 'rss'

urlpatterns = [
    path('list/', RssFeedListView.as_view(), name='list'),
    path('detail/<int:pk>/', rss_detail_view, name="detail_view")
]