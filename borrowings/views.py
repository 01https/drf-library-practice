from rest_framework import viewsets
from borrowings.serializers import BorrowingSerializer, BorrowingRetrieveSerializer
from borrowings.models import Borrowing


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book_id", "user_id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer