from django.db.models import F
from rest_framework import viewsets

from borrowings.serializers import BorrowingSerializer, BorrowingRetrieveSerializer
from borrowings.models import Borrowing
from books.models import Book


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book_id", "user_id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        borrowing = serializer.save(user_id=self.request.user)
        Book.objects.filter(id=borrowing.book_id.id).update(inventory=F("inventory") - 1)