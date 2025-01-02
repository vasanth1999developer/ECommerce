# Generated by Django 5.1.4 on 2024-12-30 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acess', '0005_alter_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='deleted_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
