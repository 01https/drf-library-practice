from django.db.models import F
from django.template.context_processors import request
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from borrowings.serializers import BorrowingSerializer, BorrowingRetrieveSerializer
from borrowings.models import Borrowing
from books.models import Book


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book_id", "user_id")
        if not self.request.user.is_staff:
            queryset = queryset.filter(user_id=self.request.user)

        elif self.request.user.is_staff and "user_id" in self.request.query_params:
            queryset = queryset.filter(user_id=self.request.query_params["user_id"])

        if "is_active" in self.request.query_params:
            is_active = self.request.query_params['is_active'].lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        return queryset

    def perform_create(self, serializer):
        borrowing = serializer.save(user_id=self.request.user)
        Book.objects.filter(
            id=borrowing.book_id.id
        ).update(inventory=F("inventory") - 1)