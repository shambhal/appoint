# Generated by Django 4.2 on 2023-12-24 09:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0016_book_unique_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='order_item_id',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.CreateModel(
            name='BookHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dated', models.DateField(default=django.utils.timezone.now, max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('order_id', models.IntegerField(blank=True, default=0)),
                ('order_item_id', models.IntegerField(blank=True, default=0)),
                ('book', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.book')),
            ],
        ),
    ]
