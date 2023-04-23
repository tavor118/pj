from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    SlugField,
    TextField,
    URLField,
)
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from src.apps.core.models import QuestionLevel
from src.apps.questions.managers import QuestionManager

User = get_user_model()


class Category(MPTTModel):
    """For nested logic used django-mptt.
    Docs can be found here:
    https://django-mptt.readthedocs.io/en/latest/
    """

    title = CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
    )
    slug = SlugField(100)

    position = PositiveIntegerField(default=1)  # used for ordering

    objects = TreeManager()

    class MPTTMeta:
        order_insertion_by = ["title"]

    class Meta:
        unique_together = [["parent", "title"]]
        ordering = ["position"]
        verbose_name_plural = "Categories"

    def __str__(self) -> str:  # pragma: no cover
        return f"<Category [{self.id}]: {self.title} #{self.position}>"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Question(Model):
    title = CharField(max_length=255)
    slug = SlugField(max_length=255)
    category = ForeignKey(Category, on_delete=CASCADE, related_name="posts")
    content = TextField()

    position = PositiveIntegerField(default=1)  # used for ordering

    question_level = CharField(
        max_length=10,
        choices=QuestionLevel.choices,
        default=QuestionLevel.JUNIOR,
    )

    objects = QuestionManager()

    def __str__(self) -> str:  # pragma: no cover
        return f"<Question [{self.id}]: {self.title} #{self.position}>"

    class Meta:
        ordering = ["position"]
        verbose_name_plural = "Questions"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ResourceLink(Model):
    """Link to additional resources to a question"""

    question = ForeignKey(Question, on_delete=CASCADE, related_name="links")
    title = CharField(max_length=255)
    url = URLField(max_length=255)

    def __str__(self) -> str:  # pragma: no cover
        return f"<ResourceLink [{self.id}]: {self.url}>"
