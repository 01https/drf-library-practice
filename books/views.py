from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer
from books.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
