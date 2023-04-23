from django.contrib.auth import get_user_model
from pytest import fixture, mark
from rest_framework.test import APIClient

from src.apps.questions.models import Question, ResourceLink
from src.apps.social.models import Bookmark, Like

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestUserViewSet:
    list_url = "/api/users/"
    detail_url = "/api/users/{}/"

    @fixture
    def link(self, question: Question) -> ResourceLink:
        link = ResourceLink.objects.create(
            question=question, title="Url Title", url="example.com/example"
        )
        return link


class TestDetailView(TestUserViewSet):
    relative_path = "me/"

    @mark.parametrize("is_detail_view", [True, False])
    def test_get_detail(self, client: APIClient, user: User, is_detail_view: bool):
        if is_detail_view:
            url = self.detail_url.format(user.id)
        else:
            url = self.list_url + self.relative_path

        response = client.get(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)
        response = client.get(url)

        assert response.status_code == 200, response.data

        instance = response.data
        assert instance["id"] == user.id
        assert instance["username"] == user.username
        assert instance["email"] == user.email

    def test_update_user(self, client: APIClient, user: User, user_email: str):
        url = self.detail_url.format(user.id)

        response = client.patch(url, {"username": "new_username"})
        assert response.status_code == 401, response.data

        client.force_authenticate(user)
        response = client.put(url, {"username": "new_username"})

        assert response.status_code == 200, response.data

        instance = response.data
        assert instance["id"] == user.id
        assert instance["username"] == "new_username"

        # email change should be ignored
        new_email = "example2@gmail.com"
        response = client.patch(url, {"email": new_email})

        assert response.status_code == 200, response.data

        instance = response.data
        assert instance["id"] == user.id
        assert instance["email"] == user_email


class TestGetLikedQuestions(TestUserViewSet):
    relative_path = "get_liked_questions/"

    def test_liked_questions(
        self,
        client: APIClient,
        user: User,
        question: Question,
        like: Like,
        django_assert_num_queries,
    ):
        url = self.list_url + self.relative_path

        response = client.get(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)
        with django_assert_num_queries(2):
            # 2 queries - select, prefetch links
            response = client.get(url)

        assert response.status_code == 200, response.data

        instance = response.data[0]
        assert instance["id"] == question.id
        assert instance["like_type"] is None


class TestGetBookmarkedQuestions(TestUserViewSet):
    relative_path = "get_bookmarked_questions/"

    def test_get_bookmarked_questions(
        self,
        client: APIClient,
        user: User,
        question: Question,
        bookmark: Bookmark,
        django_assert_num_queries,
    ):
        url = self.list_url + self.relative_path

        response = client.get(url)
        assert response.status_code == 401, response.data

        client.force_authenticate(user)
        with django_assert_num_queries(2):
            # 2 queries - select, prefetch links
            response = client.get(url)

        assert response.status_code == 200, response.data

        instance = response.data[0]
        assert instance["id"] == question.id
        assert instance["like_type"] is None
