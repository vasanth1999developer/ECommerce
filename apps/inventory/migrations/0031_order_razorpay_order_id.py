# Generated by Django 5.1.4 on 2025-01-07 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0030_alter_subcategory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(choices=[('placed', 'Placed'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default=None, max_length=512),
            preserve_default=False,
        ),
    ]
