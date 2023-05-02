from rest_framework.fields import (
    BooleanField,
    CharField,
    IntegerField,
    ReadOnlyField,
    SerializerMethodField,
)
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

from src.apps.questions.models import Category, Question, ResourceLink

# CATEGORY


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug", "position"]
        read_only_fields = [f for f in fields]

    def get_fields(self):
        fields = super().get_fields()
        fields["children"] = CategorySerializer(many=True, required=False)
        return fields


# QUESTION


class QuestionCategorySerializer(ModelSerializer):
    url = SerializerMethodField()
    parent_title = ReadOnlyField(source="parent.title")

    class Meta:
        model = Category
        fields = ["id", "title", "parent_title", "url"]
        read_only_fields = [f for f in fields]

    def get_url(self, obj):
        request = self.context.get("request")
        return reverse("api:category-detail", kwargs={"pk": obj.pk}, request=request)


class ResourceLinkSerializer(ModelSerializer):
    class Meta:
        model = ResourceLink
        fields = ["title", "url"]


class QuestionSerializer(ModelSerializer):
    url = SerializerMethodField()

    category = QuestionCategorySerializer(read_only=True)
    links = ResourceLinkSerializer(many=True, read_only=True)

    like_count = IntegerField()
    dislike_count = IntegerField()

    bookmark_count = IntegerField()

    like_type = CharField(allow_null=True, default=None)
    is_bookmarked = BooleanField(default=False)

    note_count = IntegerField(default=None)
    comment_count = IntegerField(default=None)

    class Meta:
        model = Question
        fields = [
            "id",
            "url",
            "title",
            "slug",
            "content",
            "position",
            "category",
            "links",
            "like_count",
            "dislike_count",
            "bookmark_count",
            "like_type",
            "is_bookmarked",
            "note_count",
            "comment_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [f for f in fields]

    def get_url(self, obj):
        request = self.context.get("request")
        return reverse("api:question-detail", kwargs={"pk": obj.pk}, request=request)
