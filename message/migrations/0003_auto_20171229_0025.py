# Generated by Django 2.0 on 2017-12-29 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_auto_20171228_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='user_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='messagelist',
            name='user_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_list_from', to=settings.AUTH_USER_MODEL),
        ),
    ]
