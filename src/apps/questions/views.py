from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from src.apps.questions.models import Category, Question
from src.apps.questions.serializers import CategorySerializer, QuestionSerializer
from src.apps.social.models import LikeType
from src.apps.social.services import BookmarkService, LikeService


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.action == "list":
            # in list endpoint we only need the root nodes,
            # children will be handled by serializer
            return Category.objects.root_nodes().order_by("position")
        else:
            return self.queryset


class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = Question.objects.get_question_list()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Question.objects.get_question_list_for_user(self.request.user)
        else:
            return self.queryset

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_like(self, request: Request, pk: int):
        service = LikeService()
        like = service.toggle_like(
            request.user, question_id=pk, like_type=LikeType.LIKE
        )

        if like:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_dislike(self, request: Request, pk: int):
        service = LikeService()
        like = service.toggle_like(
            request.user, question_id=pk, like_type=LikeType.DISLIKE
        )

        if like:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_bookmark(self, request: Request, pk: int):
        service = BookmarkService()
        bookmark = service.toggle_bookmark(request.user, question_id=pk)

        if bookmark:
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_204_NO_CONTENT)
