from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from pytest import fixture, mark
from rest_framework.test import APIClient

from src.apps.questions.models import Category, Question, ResourceLink
from src.apps.social.models import Bookmark, Comment, CommentReply, Like, LikeType, Note

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestQuestionViewSet:
    list_url = "/api/questions/"
    detail_url = "/api/questions/{}/"

    @fixture
    def link(self, question: Question) -> ResourceLink:
        link = ResourceLink.objects.create(
            question=question, title="Url Title", url="example.com/example"
        )
        return link

    @fixture
    def like2(self, user2: User, question: Question) -> Like:
        like = Like.objects.create(
            user=user2, question=question, like_type=LikeType.DISLIKE
        )
        return like

    @fixture
    def user3(self, user_password: str) -> User:
        user_email = "example3@gmail.com"
        username = "user3"
        user = User.objects.create_user(
            email=user_email,
            username=username,
            password=user_password,
        )
        EmailAddress.objects.create(
            user=user, email=user_email, primary=True, verified=True
        )
        return user

    @fixture
    def like3(self, user3: User, question: Question) -> Like:
        like = Like.objects.create(
            user=user3, question=question, like_type=LikeType.LIKE
        )
        return like

    @fixture
    def bookmark3(self, user3: User, question: Question) -> Like:
        bookmark = Bookmark.objects.create(user=user3, question=question)
        return bookmark

    @fixture
    def comment2(self, user: User, question: Question) -> Comment:
        content = "My second comment"
        comment = Comment.objects.create(
            author=user, question=question, content=content
        )
        return comment

    @fixture
    def note2(self, user2: User, question: Question) -> Note:
        content = "My second note"
        note = Note.objects.create(author=user2, question=question, content=content)
        return note


class TestListQuestionView(TestQuestionViewSet):
    def test_list(
        self,
        client: APIClient,
        user: User,
        child_category: Category,
        question: Question,
        question2: Question,
        link: ResourceLink,
        like: Like,
        like2: Like,
        like3: Like,
        bookmark: Bookmark,
        bookmark3: Bookmark,
        note: Note,
        note2: Note,
        comment: Comment,
        comment2: Comment,
        comment_reply: CommentReply,
        django_assert_num_queries,
    ):
        question3 = Question.objects.create(
            category=child_category,
            title="What is dictionary in Python?",
            content="In Python dictionaries are implemented as hash tables.",
            position=0,
        )

        with django_assert_num_queries(3):
            # 3 queries - count, select, prefetch links
            response = client.get(self.list_url)

        assert response.status_code == 200, response.data

        assert response.data["count"] == 3
        instance = response.data["results"][0]
        assert instance["id"] == question3.id
        assert instance["like_count"] == 0
        assert instance["dislike_count"] == 0
        assert instance["bookmark_count"] == 0
        instance = response.data["results"][1]
        assert instance["id"] == question.id
        assert instance["like_count"] == 2
        assert instance["dislike_count"] == 1
        assert instance["bookmark_count"] == 2
        assert instance["like_type"] is None
        assert instance["is_bookmarked"] is False
        assert instance["note_count"] is None
        assert instance["comment_count"] == 2

        client.force_authenticate(user)

        with django_assert_num_queries(3):
            # 3 queries - count, select, prefetch links
            response = client.get(self.list_url)

        assert response.data["count"] == 3
        instance = response.data["results"][1]
        assert instance["id"] == question.id
        assert instance["like_count"] == 2
        assert instance["dislike_count"] == 1
        assert instance["bookmark_count"] == 2
        assert instance["like_type"] == like.like_type
        assert instance["is_bookmarked"] is True
        assert instance["note_count"] == 1
        assert instance["comment_count"] == 2


class TestDetailQuestionView(TestQuestionViewSet):
    def test_details(
        self,
        client: APIClient,
        question: Question,
        link: ResourceLink,
        like: Like,
    ):
        response = client.get(self.detail_url.format(question.pk))

        assert response.status_code == 200, response.data

        assert response.data["id"] == question.id
        assert response.data["title"] == question.title
        assert response.data["content"] == question.content
        assert response.data["links"][0]["title"] == link.title
        assert response.data["like_count"] == 1
        assert response.data["dislike_count"] == 0


class TestToggleLike(TestQuestionViewSet):
    @mark.parametrize(
        ["like_type", "relative_path"],
        [[LikeType.LIKE, "toggle_like/"], [LikeType.DISLIKE, "toggle_dislike/"]],
    )
    def test_toggle_like(
        self,
        client: APIClient,
        question: Question,
        user: User,
        like_type: LikeType,
        relative_path: str,
    ):
        url = self.detail_url.format(question.pk) + relative_path
        likes = Like.objects.filter(user=user, question=question)

        response = client.post(url)

        assert response.status_code == 401, response.data
        assert likes.count() == 0

        client.force_authenticate(user)
        response = client.post(url)

        assert response.status_code == 201, response.data
        assert likes.count() == 1

        response = client.post(url)

        assert response.status_code == 204, response.data
        assert likes.count() == 0


class TestToggleBookmark(TestQuestionViewSet):
    relative_path = "toggle_bookmark/"

    def test_toggle_bookmark(
        self,
        client: APIClient,
        question: Question,
        user: User,
    ):
        url = self.detail_url.format(question.pk) + self.relative_path
        bookmarks = Bookmark.objects.filter(user=user, question=question)

        response = client.post(url)

        assert response.status_code == 401, response.data
        assert bookmarks.count() == 0

        client.force_authenticate(user)
        response = client.post(url)

        assert response.status_code == 201, response.data
        assert bookmarks.count() == 1

        response = client.post(url)

        assert response.status_code == 204, response.data
        assert bookmarks.count() == 0
