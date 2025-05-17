from django.db import models


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    cover = models.CharField(max_length=5, choices=CoverType)
    inventory = models.PositiveIntegerField(null=False, blank=False)
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Daily fee (USD)"
    )
