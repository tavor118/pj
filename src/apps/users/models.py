from django.contrib.auth.models import AbstractUser
from django.db.models import DateTimeField, EmailField
from django.utils import timezone

from src.apps.core.models import AutoDateTimeField


class User(AbstractUser):
    email = EmailField(max_length=255, unique=True)

    created_at = DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"<User [{self.id}]: {self.username}>"

    class Meta:
        ordering = ["-id"]
