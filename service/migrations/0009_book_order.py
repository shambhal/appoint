# Generated by Django 4.2 on 2023-12-18 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_currency_code'),
        ('service', '0008_remove_book_user_book_email_book_name_book_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='order',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.order'),
            preserve_default=False,
        ),
    ]
