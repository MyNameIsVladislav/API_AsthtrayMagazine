# Generated by Django 3.2.6 on 2021-10-15 12:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 17, 12, 13, 0, 106715, tzinfo=utc)),
        ),
    ]
