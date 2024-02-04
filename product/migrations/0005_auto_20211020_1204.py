# Generated by Django 3.2.5 on 2021-10-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('0', 'Disabled'), ('1', 'Enabled')], max_length=2),
        ),
    ]