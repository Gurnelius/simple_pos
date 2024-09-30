# Generated by Django 5.1.1 on 2024-09-30 07:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleitem',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sale',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
