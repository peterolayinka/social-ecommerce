# Generated by Django 2.0 on 2017-12-28 04:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20171228_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 12, 28, 4, 11, 43, 662848, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
