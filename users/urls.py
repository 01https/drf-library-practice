from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import ManageUserView, CreateUserView


urlpatterns = [
    path("user/", CreateUserView.as_view(), name="register"),
    path("user/token/", TokenObtainPairView.as_view(), name="token"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("user/me/", ManageUserView.as_view(), name="me"),
]

app_name = "users"