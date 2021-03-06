# Generated by Django 2.0 on 2017-12-27 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20171226_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='Lagos', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default='01', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=200, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='processing_time',
            field=models.CharField(default='Item will be shipped out within 2-3 working days', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
