from django.contrib.auth import get_user_model
from django.db.models import (
    Case,
    CharField,
    Count,
    Exists,
    IntegerField,
    Manager,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Coalesce

from src.apps.core.models import LikeType
from src.apps.social.models import Bookmark, Like

User = get_user_model()


class QuestionManager(Manager):
    def get_extended_queryset(self):
        queryset = self.get_queryset()

        like_count = Count(
            Case(
                When(Q(likes__like_type=LikeType.LIKE), then="likes"),
                output_field=IntegerField(),
            ),
            distinct=True,
        )
        dislike_count = Count(
            Case(
                When(Q(likes__like_type=LikeType.DISLIKE), then="likes"),
                output_field=IntegerField(),
            ),
            distinct=True,
        )

        queryset = (
            queryset.select_related("category", "category__parent")
            .annotate(
                like_count=like_count,
                dislike_count=dislike_count,
                bookmark_count=Count("bookmarks", distinct=True),
            )
            .prefetch_related("links")
        )
        return queryset

    def get_question_list(self):
        queryset = self.get_extended_queryset()
        queryset = queryset.order_by("position").all()
        return queryset

    def get_question_list_for_user(self, user: User):
        queryset = self.get_extended_queryset()

        is_bookmarked = Exists(Bookmark.objects.filter(user=user))

        like_type = Like.objects.filter(user=user, question=OuterRef("pk")).values(
            "like_type"
        )[:1]
        # we need only the like_type field if like exists
        like_type = Coalesce(Subquery(like_type, output_field=CharField()), Value(None))

        queryset = (
            queryset.annotate(
                like_type=like_type,
                # annotate if question is bookmarked by the user
                is_bookmarked=is_bookmarked,
            )
            .order_by("position")
            .all()
        )
        return queryset

    def get_liked_questions_for_user(self, user: User):
        queryset = self.get_extended_queryset()
        queryset = (
            queryset.filter(likes__user=user, likes__like_type=LikeType.LIKE)
            .order_by("-likes__created_at")
            .all()
        )
        return queryset

    def get_bookmarked_questions_for_user(self, user: User):
        queryset = self.get_extended_queryset()
        queryset = (
            queryset.filter(bookmarks__user=user)
            .order_by("-bookmarks__created_at")
            .all()
        )
        return queryset
