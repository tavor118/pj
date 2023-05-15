# Generated by Django 4.2 on 2023-04-25 19:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="question",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]