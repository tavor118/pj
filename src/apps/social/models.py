from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, CharField, DateTimeField, ForeignKey, Model
from django.utils import timezone

from src.apps.core.models import LikeType

User = get_user_model()


class Like(Model):
    like_type = CharField(max_length=7, choices=LikeType.choices, default=LikeType.LIKE)

    user = ForeignKey(User, on_delete=CASCADE)
    question = ForeignKey("questions.Question", on_delete=CASCADE, related_name="likes")

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"<Like [{self.id}]: {self.like_type.upper()}. "
            f"Question#{self.question_id} User#{self.user_id}>"
        )

    class Meta:
        unique_together = ("user", "question")


class Bookmark(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    question = ForeignKey(
        "questions.Question", on_delete=CASCADE, related_name="bookmarks"
    )

    created_at = DateTimeField(default=timezone.now)

    def __str__(self) -> str:  # pragma: no cover
        return (
            f"<Bookmark [{self.id}]: Question#{self.question_id} User#{self.user_id}>"
        )

    class Meta:
        unique_together = ("user", "question")
