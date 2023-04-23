from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.questions.models import Question
from src.apps.questions.serializers import QuestionSerializer
from src.apps.users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def get_liked_questions(self, request):
        questions = Question.objects.get_liked_questions_for_user(request.user)
        serializer = QuestionSerializer(questions, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False)
    def get_bookmarked_questions(self, request):
        questions = Question.objects.get_bookmarked_questions_for_user(request.user)
        serializer = QuestionSerializer(questions, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
