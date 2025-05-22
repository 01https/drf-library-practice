from django.urls import path
from rest_framework import routers
from django.urls import include

from borrowings.views import BorrowingsViewSet


router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet, basename="borrowing")

urlpatterns = [path("", include(router.urls))]

app_name = "borrowings"