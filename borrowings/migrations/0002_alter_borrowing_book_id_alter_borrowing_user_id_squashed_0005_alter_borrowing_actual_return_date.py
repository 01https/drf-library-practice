# Generated by Django 5.2.1 on 2025-05-22 16:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('borrowings', '0002_alter_borrowing_book_id_alter_borrowing_user_id'), ('borrowings', '0003_alter_borrowing_actual_return_date'), ('borrowings', '0004_alter_borrowing_actual_return_date'), ('borrowings', '0005_alter_borrowing_actual_return_date')]

    dependencies = [
        ('books', '0001_initial'),
        ('borrowings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowing',
            name='book_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='actual_return_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
