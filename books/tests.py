from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import resolve

from books.models import Book
from books.serializers import BookSerializer

User = get_user_model()


class BookTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="adminpass",
            is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            password="userpass"
        )

        self.book = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            cover=Book.CoverType.HARD,
            inventory=3,
            daily_fee=1.99
        )

        self.books_url = reverse("books:books-list")
        self.book_detail_url = reverse("books:books-detail", args=[self.book.id])

    # ---------- MODEL ----------

    def test_book_str_representation(self):
        self.assertEqual(str(self.book), "Clean Code - Robert C. Martin")

    # ---------- SERIALIZER ----------

    def test_book_serializer_fields(self):
        serializer = BookSerializer(instance=self.book)
        self.assertEqual(serializer.data["title"], self.book.title)
        self.assertEqual(serializer.data["cover"], self.book.cover)
        self.assertEqual(serializer.data["daily_fee"], str(self.book.daily_fee))

    # ---------- VIEWSET ----------

    def test_list_books_anonymous(self):
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data[0])

    def test_create_book_forbidden_for_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.books_url, {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "cover": "SOFT",
            "inventory": 7,
            "daily_fee": "2.75"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_allowed_for_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.books_url, {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "cover": "SOFT",
            "inventory": 7,
            "daily_fee": "2.75"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Refactoring").exists())

    def test_update_book_admin_only(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.book_detail_url, {"title": "New Title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.book_detail_url, {"title": "Updated Title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book_admin_only(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    # ---------- URLS ----------

    def test_books_list_url_resolves(self):
        resolver = resolve(self.books_url)
        self.assertEqual(resolver.view_name, "books:books-list")

    def test_books_detail_url_resolves(self):
        resolver = resolve(self.book_detail_url)
        self.assertEqual(resolver.view_name, "books:books-detail")

    def test_books_list_url_returns_200(self):
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, 200)

    def test_books_detail_url_returns_200(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, 200)