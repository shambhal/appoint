# Generated by Django 4.2 on 2023-12-21 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0013_book_order_id'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('dated', 'service', 'slot', 'status'), name='unique_booking'),
        ),
    ]
