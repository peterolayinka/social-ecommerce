# Generated by Django 2.0 on 2017-12-30 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_auto_20171229_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='from_store',
            field=models.BooleanField(default=False),
        ),
    ]
