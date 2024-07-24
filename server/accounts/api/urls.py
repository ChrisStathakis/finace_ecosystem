from django.urls import path

from .views import CurrentUser, ProfileApiView

app_name = "profile"


urlpatterns = [
    path('current-user/', CurrentUser.as_view(), name='current_user'),
    path("profile/", ProfileApiView.as_view(), name="profile_view")

]