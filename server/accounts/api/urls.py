from django.urls import path

from .views import CurrentUser

app_name = "profile"


urlpatterns = [
    path('current-user/', CurrentUser.as_view(), name='current_user'),

]