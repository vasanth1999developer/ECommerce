# Generated by Django 5.1.4 on 2025-01-08 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_remove_orderitem_product_remove_orderitem_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
