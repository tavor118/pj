from pytest import fixture
from rest_framework.test import APIClient

from src.apps.questions.models import Category, Question, ResourceLink


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


class TestListQuestionView(TestQuestionViewSet):
    def test_list(
        self,
        client: APIClient,
        child_category: Category,
        question: Question,
        question2: Question,
        link: ResourceLink,
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
        assert response.data["results"][0]["id"] == question3.id


class TestDetailQuestionView(TestQuestionViewSet):
    def test_details(
        self,
        client: APIClient,
        question: Question,
        link: ResourceLink,
    ):
        response = client.get(self.detail_url.format(question.pk))

        assert response.status_code == 200, response.data

        assert response.data["id"] == question.id
        assert response.data["title"] == question.title
        assert response.data["content"] == question.content
        assert response.data["links"][0]["title"] == link.title
