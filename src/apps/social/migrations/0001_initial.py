# Generated by Django 4.2 on 2023-04-20 18:59

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("questions", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "like_type",
                    models.CharField(
                        choices=[("like", "Like"), ("dislike", "Dislike")],
                        default="like",
                        max_length=7,
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="questions.question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "question")},
            },
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to="questions.question",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "question")},
            },
        ),
    ]