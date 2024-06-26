# Generated by Django 5.0 on 2024-04-29 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_order_address_order_email_order_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='area',
            field=models.DecimalField(decimal_places=2, default='', max_digits=10, verbose_name='Площадь'),
        ),
        migrations.AddField(
            model_name='product',
            name='floors',
            field=models.IntegerField(default='', verbose_name='Этажи'),
        ),
        migrations.AddField(
            model_name='product',
            name='materials',
            field=models.CharField(default='', max_length=255, verbose_name='Материалы'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 4, 29, 19, 24, 2, 527137), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2024, 4, 29, 19, 24, 2, 527137), verbose_name='Дата комментария'),
        ),
    ]
