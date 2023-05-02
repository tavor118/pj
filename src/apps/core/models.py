from django.db.models import DateTimeField, TextChoices
from django.utils import timezone


class AutoDateTimeField(DateTimeField):
    """Field that automatically sets the current time on save.
    Editable in the admin interface.
    """

    def pre_save(self, model_instance, add):
        return timezone.now()


class QuestionLevel(TextChoices):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class LikeType(TextChoices):
    LIKE = "like"
    DISLIKE = "dislike"
