# Generated by Django 4.2 on 2023-12-18 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_ordertotals'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='device_id',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
