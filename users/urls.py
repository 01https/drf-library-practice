from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import ManageUserView, CreateUserView


urlpatterns = [
    path("users/", CreateUserView.as_view(), name="register"),
    path("users/token/", TokenObtainPairView.as_view(), name="token"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("users/me/", ManageUserView.as_view(), name="me"),
]

app_name = "users"