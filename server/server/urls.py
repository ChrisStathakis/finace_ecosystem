"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views
from frontend.api.views import homepage_api_view
from accounts.views import login_view, profile_view
from tickers.views import initial_data_view, ticker_play_area_view

urlpatterns = [

    path('admin/', admin.site.urls),
    path("profile/", profile_view, name="profile_view"),
    path('', include('frontend.urls')),
    path('rss/', include('rss_component.urls')),

    path('login/', login_view),

    path('api-auth/', include('rest_framework.urls')),


    path('api/', homepage_api_view, name="api_home"),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path("api/", include("accounts.api.urls")),
    path('api/tickers/', include('tickers.api.urls')),
    path("api/rss-feed/", include("rss_component.api.urls")),


    path("initial-data/", initial_data_view),
    path("play-area/<int:pk>/", ticker_play_area_view),

    # channels
    path('chat/', include("chat.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("tickers/", include("tickers.urls")),

    




]
