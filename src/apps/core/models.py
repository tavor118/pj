from django.db.models import TextChoices


class QuestionLevel(TextChoices):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class LikeType(TextChoices):
    LIKE = "like"
    DISLIKE = "dislike"
