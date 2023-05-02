from django_filters import FilterSet, IsoDateTimeFilter

from src.apps.social.models import Comment


class CommentFilter(FilterSet):
    created_at_gt = IsoDateTimeFilter(field_name="created_at", lookup_expr="gt")
    created_at_lt = IsoDateTimeFilter(field_name="created_at", lookup_expr="lt")

    updated_at_gt = IsoDateTimeFilter(field_name="updated_at", lookup_expr="gt")
    updated_at_lt = IsoDateTimeFilter(field_name="updated_at", lookup_expr="lt")

    class Meta:
        model = Comment
        fields = [
            "author",
            "question",
            "created_at_gt",
            "created_at_lt",
            "updated_at_gt",
            "updated_at_lt",
        ]
