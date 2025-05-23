from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class UserSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }

    def test_serialize_user(self):
        user = User.objects.create_user(**self.user_data)
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["email"], user.email)
        self.assertNotIn("password", serializer.data)

    def test_create_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data["email"])


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )

    def test_user_registration(self):
        data = {
            "email": "new@example.com",
            "password": "newpass123"
        }
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_get_current_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("users:me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_current_user(self):
        self.client.force_authenticate(user=self.user)
        data = {"email": "updated@example.com"}
        response = self.client.patch(reverse("users:me"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updated@example.com")