from django.contrib.auth import get_user_model
from pytest import fixture, mark
from rest_framework.test import APIClient

from src.apps.questions.models import Question
from src.apps.social.models import Comment, CommentReply

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestCommentReplyViewSet:
    list_url = "/api/questions/comments/replies/"
    detail_url = "/api/questions/comments/replies/{}/"

    @fixture
    def comment_reply2(
        self, user: User, question: Question, comment: CommentReply
    ) -> CommentReply:
        content = "My second comment reply"
        comment_reply = CommentReply.objects.create(
            author=user, question=question, comment=comment, content=content
        )
        return comment_reply


class TestListCommentReplyView(TestCommentReplyViewSet):
    @mark.parametrize("is_authorized", [True, False])
    def test_list_comments(
        self,
        is_authorized: bool,
        client: APIClient,
        user: User,
        comment_reply: CommentReply,
        comment_reply2: CommentReply,
        django_assert_num_queries,
    ):
        if is_authorized:
            client.force_authenticate(user)

        # 2 queries - count, select
        with django_assert_num_queries(2):
            response = client.get(self.list_url)

        assert response.status_code == 200, response.data

        assert response.data["count"] == 2
        result = response.data["results"][0]
        assert result["id"] == comment_reply.id
        assert result["content"] == comment_reply.content
        assert result["author"] == user.username

        result = response.data["results"][1]
        assert result["id"] == comment_reply2.id
        assert result["content"] == comment_reply2.content
        assert result["author"] == user.username


class TestDetailCommentReplyView(TestCommentReplyViewSet):
    @mark.parametrize("is_authorized", [True, False])
    def test_details_comment(
        self,
        is_authorized: bool,
        client: APIClient,
        user: User,
        comment_reply: CommentReply,
    ):
        url = self.detail_url.format(comment_reply.pk)

        if is_authorized:
            client.force_authenticate(user)

        response = client.get(url)

        assert response.status_code == 200, response.data

        result = response.data
        assert result["id"] == comment_reply.id
        assert result["content"] == comment_reply.content


class TestCreateCommentReplyView(TestCommentReplyViewSet):
    def test_create_comment_reply(
        self, client: APIClient, user: User, question: Question, comment: Comment
    ):
        content = "test comment reply"
        data = {"content": content, "comment": comment.id}

        response = client.post(self.list_url, data=data)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.post(self.list_url, data=data)

        assert response.status_code == 201, response.data

        [comment_reply] = CommentReply.objects.all()

        result = response.data
        assert result["id"] == comment_reply.id
        assert result["content"] == content

        assert comment_reply.question_id == question.id


class TestUpdateCommentReplyView(TestCommentReplyViewSet):
    def test_update_comment_reply(
        self,
        client: APIClient,
        user: User,
        question: Question,
        comment: Comment,
        comment_reply: CommentReply,
    ):
        url = self.detail_url.format(comment_reply.pk)

        content = "test comment reply"
        data = {"content": content}

        response = client.put(url, data=data)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.put(url, data=data)

        assert response.status_code == 200, response.data

        result = response.data
        assert result["id"] == comment_reply.id
        assert result["content"] == content


class TestDeleteCommentReplyView(TestCommentReplyViewSet):
    def test_delete_comment(
        self, client: APIClient, user: User, comment_reply: CommentReply
    ):
        url = self.detail_url.format(comment_reply.pk)
        response = client.delete(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.delete(url)

        assert response.status_code == 204, response.data

        comment_count = CommentReply.objects.count()
        assert comment_count == 0
