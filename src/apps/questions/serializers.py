from rest_framework.fields import ReadOnlyField, SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

from src.apps.questions.models import Category, Question, ResourceLink

# CATEGORY


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug", "position"]

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

    class Meta:
        model = Question
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "position",
            "links",
            "category",
            "url",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return reverse("api:question-detail", kwargs={"pk": obj.pk}, request=request)
