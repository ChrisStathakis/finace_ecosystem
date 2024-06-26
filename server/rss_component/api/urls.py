from django.urls import path

from .views import (RssFeedListApiView, RssFeedDetailApiView)

app_name = 'api_rss_feed'

urlpatterns = [
    path('', RssFeedListApiView.as_view(), name="list"),
    path("detail/<int:pk>/", RssFeedDetailApiView.as_view(), name="detail"),
    

]