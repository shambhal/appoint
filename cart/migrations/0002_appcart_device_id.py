# Generated by Django 4.2 on 2023-12-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appcart',
            name='device_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
