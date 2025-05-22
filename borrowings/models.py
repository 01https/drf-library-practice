from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.conf import settings

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user_id", "book_id", "borrow_date"],
                name="unique_together_per_day"
            )
        ]

    def __str__(self):
        return self.borrow_date