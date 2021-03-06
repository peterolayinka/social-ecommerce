# Generated by Django 2.0 on 2017-12-26 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20171226_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='store',
            name='image',
            field=models.ImageField(blank=True, upload_to='stores/<django.db.models.fields.related.OneToOneField>'),
        ),
    ]
