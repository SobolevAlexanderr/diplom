# Generated by Django 4.1.7 on 2023-04-03 13:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_blog_options_alter_blog_posted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 4, 3, 16, 30, 36, 473636), verbose_name='Опубликована'),
        ),
    ]