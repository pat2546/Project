# Generated by Django 5.1.1 on 2024-10-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_quantity_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
