# Generated by Django 5.0.4 on 2024-05-04 20:21

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20240504_0123'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='owner',
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(default=uuid.UUID('2348e05d-6ad2-4033-a19a-c515c6dc262f'), on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='menu.restaurant'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='owner',
            field=models.ForeignKey(default=uuid.UUID('9013a774-39c5-4967-aa42-5424c170440f'), on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to=settings.AUTH_USER_MODEL),
        ),
    ]
