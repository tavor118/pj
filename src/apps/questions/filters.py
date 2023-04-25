from django_filters import CharFilter, FilterSet, IsoDateTimeFilter, NumberFilter

from src.apps.questions.models import Category, Question


class CategoryFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")  # only parents are available

    class Meta:
        model = Category
        fields = ["title"]


class QuestionFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    category = NumberFilter(lookup_expr="exact")

    created_at_gt = IsoDateTimeFilter(field_name="created_at", lookup_expr="gt")
    created_at_lt = IsoDateTimeFilter(field_name="created_at", lookup_expr="lt")

    updated_at_gt = IsoDateTimeFilter(field_name="updated_at", lookup_expr="gt")
    updated_at_lt = IsoDateTimeFilter(field_name="updated_at", lookup_expr="lt")

    class Meta:
        model = Question
        fields = [
            "title",
            "category",
            "created_at_gt",
            "created_at_lt",
            "updated_at_gt",
            "updated_at_lt",
        ]
