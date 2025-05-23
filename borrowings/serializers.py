from rest_framework import serializers
from django.utils import timezone

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
        read_only_fields = ("id", "borrow_date", "user_id")

    def validate(self, attrs):
        borrow_date = timezone.now().date()
        expected_return_date = attrs["expected_return_date"]
        actual_return_date = attrs.get("actual_return_date")
        book_id = attrs.get("book_id")

        if expected_return_date < borrow_date:
            raise serializers.ValidationError("Expected return date cannot be earlier than borrow date")
        if actual_return_date:
            if expected_return_date and actual_return_date < borrow_date:
                raise serializers.ValidationError("Actual return date cannot be earlier than borrow date.")
        if book_id.inventory == 0:
            raise serializers.ValidationError("This book is out of stock")

        return attrs


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book_id = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
        read_only_fields = ("id", "borrow_date", "user_id")
