from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer

User = get_user_model()

class BorrowingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.99
        )
        self.borrowing = Borrowing.objects.create(
            user_id=self.user,
            book_id=self.book,
            expected_return_date=date.today() + timedelta(days=7)
        )

    def test_borrowing_creation(self):
        self.assertEqual(self.borrowing.user_id, self.user)
        self.assertEqual(self.borrowing.book_id, self.book)
        self.assertEqual(self.borrowing.borrow_date, date.today())
        self.assertIsNone(self.borrowing.actual_return_date)

    def test_unique_constraint(self):
        with self.assertRaises(Exception):
            Borrowing.objects.create(
                user_id=self.user,
                book_id=self.book,
                expected_return_date=date.today() + timedelta(days=7)
            )

class BorrowingSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.99
        )
        self.valid_data = {
            "book_id": self.book.id,
            "expected_return_date": (date.today() + timedelta(days=7)).isoformat()
        }
        self.invalid_data = {
            "book_id": self.book.id,
            "expected_return_date": (date.today() - timedelta(days=1)).isoformat()
        }

    def test_valid_serializer(self):
        serializer = BorrowingSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        serializer = BorrowingSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())

class BorrowingViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="user@example.com", password="testpass")
        self.admin = User.objects.create_superuser(email="admin@example.com", password="adminpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.99
        )
        self.borrowing = Borrowing.objects.create(
            user_id=self.user,
            book_id=self.book,
            expected_return_date=date.today() + timedelta(days=7)
        )
        self.url = "/api/borrowings/"

    def test_list_borrowings_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_borrowings_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_user_id(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_is_active(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url, {"is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
