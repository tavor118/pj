from rest_framework.viewsets import ReadOnlyModelViewSet

from src.apps.questions.models import Category, Question
from src.apps.questions.serializers import CategorySerializer, QuestionSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        # we only need the root nodes, children will be handled by serializer
        self.queryset = Category.objects.root_nodes().order_by("position")
        return super().list(request, *args, **kwargs)


class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = (
        Question.objects.select_related("category", "category__parent")
        .prefetch_related("links")
        .all()
    )
    serializer_class = QuestionSerializer
