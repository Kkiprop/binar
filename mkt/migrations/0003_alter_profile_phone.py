# Generated by Django 4.0 on 2023-02-05 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkt', '0002_product_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]