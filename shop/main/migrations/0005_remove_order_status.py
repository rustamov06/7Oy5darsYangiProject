# Generated by Django 5.1.7 on 2025-03-21 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_city_delivery_order_orderproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
