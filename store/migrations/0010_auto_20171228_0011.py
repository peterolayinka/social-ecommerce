# Generated by Django 2.0 on 2017-12-28 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20171227_2225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-updated',)},
        ),
    ]
