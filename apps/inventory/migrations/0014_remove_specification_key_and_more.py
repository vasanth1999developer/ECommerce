# Generated by Django 5.1.4 on 2025-01-01 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_subcategory_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specification',
            name='key',
        ),
        migrations.RemoveField(
            model_name='specification',
            name='sub_category',
        ),
    ]
