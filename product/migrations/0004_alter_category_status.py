# Generated by Django 3.2.5 on 2021-10-20 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20211020_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.IntegerField(choices=[('0', 'Disabled'), ('1', 'Enabled')], default='1'),
        ),
    ]