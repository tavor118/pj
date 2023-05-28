from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from src.apps.core.permissions import AuthorOrReadOnly
from src.apps.social.filters import CommentFilter
from src.apps.social.models import Comment, CommentReply, Note
from src.apps.social.serializers import (
    WITH_REPLIES_QUERY_PARAM,
    CommentReplySerializer,
    CommentSerializer,
    NoteSerializer,
)


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    permission_classes = [IsAuthenticated]

    filterset_fields = ["question"]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


WITH_REPLIES_PARAMETER = OpenApiParameter(
    name=WITH_REPLIES_QUERY_PARAM,
    location=OpenApiParameter.QUERY,
    description="Include replies in the response",
    required=False,
    type=OpenApiTypes.STR,
)


@extend_schema(tags=["comments"])
@extend_schema_view(
    list=extend_schema(parameters=[WITH_REPLIES_PARAMETER]),
    retrieve=extend_schema(parameters=[WITH_REPLIES_PARAMETER]),
)
class CommentViewSet(ModelViewSet):
    queryset = (
        Comment.objects.select_related("author", "question")
        .only(
            "id",
            "question__id",
            "question__title",
            "author__username",
            "content",
            "created_at",
            "updated_at",
        )
        .all()
    )

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CommentFilter
    ordering_fields = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()

        with_replies = self.request.query_params.get(WITH_REPLIES_QUERY_PARAM)
        if with_replies:
            replies = CommentReply.objects.select_related("author")
            queryset = queryset.prefetch_related(Prefetch("replies", queryset=replies))

        return queryset

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        kwargs["partial"] = True
        return serializer_class(*args, **kwargs)


@extend_schema(tags=["replies"])
class CommentReplyViewSet(ModelViewSet):
    queryset = CommentReply.objects.select_related("author").all()
    serializer_class = CommentReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        kwargs["partial"] = True
        return serializer_class(*args, **kwargs)
