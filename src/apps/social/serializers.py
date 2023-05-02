from rest_framework.fields import (
    CharField,
    CurrentUserDefault,
    HiddenField,
    SerializerMethodField,
)
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from src.apps.questions.models import Question
from src.apps.social.models import Comment, CommentReply, Note


class NoteSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Note
        fields = [
            "id",
            "question",
            "author",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class CommentReplySerializer(ModelSerializer):
    author = CharField(source="author.username", read_only=True)
    comment = PrimaryKeyRelatedField(write_only=True, queryset=Comment.objects.all())

    class Meta:
        model = CommentReply
        fields = [
            "id",
            "comment",
            "author",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        validated_data["question"] = validated_data["comment"].question
        return super().create(validated_data)


# used to optionally prefetch comment replies
WITH_REPLIES_QUERY_PARAM = "with_replies"


class CommentSerializer(ModelSerializer):
    author = CharField(source="author.username", read_only=True)
    replies = SerializerMethodField()
    question = PrimaryKeyRelatedField(write_only=True, queryset=Question.objects.all())

    question_title = CharField(source="question.title", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "question",
            "question_title",
            "author",
            "content",
            "replies",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def get_replies(self, obj: Comment) -> list[dict]:
        with_replies = self.context["request"].query_params.get(
            WITH_REPLIES_QUERY_PARAM
        )
        if with_replies:
            serializer = CommentReplySerializer(obj.replies, many=True)
            return serializer.data
        return []

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
