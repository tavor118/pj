from django.contrib.auth import get_user_model
from pytest import fixture, mark
from rest_framework.test import APIClient

from src.apps.questions.models import Question
from src.apps.social.models import Comment, CommentReply
from src.apps.social.serializers import WITH_REPLIES_QUERY_PARAM

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestCommentViewSet:
    list_url = "/api/questions/comments/"
    detail_url = "/api/questions/comments/{}/"

    @fixture
    def comment2(self, user: User, question: Question) -> Comment:
        content = "My second comment"
        comment = Comment.objects.create(
            author=user, question=question, content=content
        )
        return comment

    @fixture
    def comment_reply2(
        self, user: User, question: Question, comment: Comment
    ) -> CommentReply:
        content = "My second comment reply"
        comment_reply = CommentReply.objects.create(
            author=user, question=question, comment=comment, content=content
        )
        return comment_reply


class TestListCommentView(TestCommentViewSet):
    @mark.parametrize("is_authorized", [True, False])
    def test_list_comments(
        self,
        is_authorized: bool,
        client: APIClient,
        user: User,
        question: Question,
        comment: Comment,
        comment_reply: CommentReply,
        comment2: Comment,
        comment_reply2: CommentReply,
        django_assert_num_queries,
    ):
        url = f"{self.list_url}?{WITH_REPLIES_QUERY_PARAM}=true"

        if is_authorized:
            client.force_authenticate(user)

        # 3 queries - count, select, prefetch replies
        with django_assert_num_queries(3):
            response = client.get(url)

        assert response.status_code == 200, response.data

        assert response.data["count"] == 2
        result = response.data["results"][0]
        assert result["id"] == comment2.id
        assert result["content"] == comment2.content
        assert result["author"] == user.username
        assert result["question_title"] == question.title

        reply = response.data["results"][1]["replies"][0]
        assert reply["id"] == comment_reply.id
        assert reply["content"] == comment_reply.content


class TestDetailCommentView(TestCommentViewSet):
    @mark.parametrize("is_authorized", [True, False])
    def test_details_comment(
        self,
        is_authorized: bool,
        client: APIClient,
        user: User,
        comment: Comment,
        comment_reply: CommentReply,
    ):
        url = self.detail_url.format(comment.pk)

        if is_authorized:
            client.force_authenticate(user)

        response = client.get(url)

        assert response.status_code == 200, response.data

        result = response.data
        assert result["id"] == comment.id
        assert result["content"] == comment.content
        assert result["replies"] == []


class TestCreateCommentView(TestCommentViewSet):
    def test_create_comment(self, client: APIClient, user: User, question: Question):
        content = "test comment"
        data = {"content": content, "question": question.id}

        response = client.post(self.list_url, data=data)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.post(self.list_url, data=data)

        assert response.status_code == 201, response.data

        [comment] = Comment.objects.all()

        result = response.data
        assert result["id"] == comment.id
        assert result["content"] == content


class TestUpdateCommentView(TestCommentViewSet):
    def test_update_comment(
        self, client: APIClient, user: User, question: Question, comment: Comment
    ):
        url = self.detail_url.format(comment.pk)

        content = "test comment"
        data = {"content": content}

        response = client.put(url, data=data)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.put(url, data=data)

        assert response.status_code == 200, response.data

        result = response.data
        assert result["id"] == comment.id
        assert result["content"] == content


class TestDeleteCommentView(TestCommentViewSet):
    def test_delete_comment(self, client: APIClient, user: User, comment: Comment):
        url = self.detail_url.format(comment.pk)
        response = client.delete(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)

        response = client.delete(url)

        assert response.status_code == 204, response.data

        comment_count = Comment.objects.count()
        assert comment_count == 0
