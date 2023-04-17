from pytest import fixture
from rest_framework.test import APIClient

from src.apps.questions.models import Category


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestCategoryViewSet:
    list_url = "/api/categories/"
    detail_url = "/api/categories/{}/"

    @fixture
    def grandchild_category(self, child_category: Category) -> Category:
        grandchild_category = Category.objects.create(
            parent=child_category, title="Data Types", position=1
        )
        return grandchild_category


class TestListCategoryView(TestCategoryViewSet):
    def test_list(
        self,
        client: APIClient,
        parent_category: Category,
        child_category: Category,
        grandchild_category: Category,
    ):
        response = client.get(self.list_url)

        assert response.status_code == 200, response.data

        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": parent_category.id,
                    "position": parent_category.position,
                    "slug": parent_category.slug,
                    "title": parent_category.title,
                    "children": [
                        {
                            "id": child_category.id,
                            "position": child_category.position,
                            "slug": child_category.slug,
                            "title": child_category.title,
                            "children": [
                                {
                                    "children": [],
                                    "id": grandchild_category.id,
                                    "position": grandchild_category.position,
                                    "slug": grandchild_category.slug,
                                    "title": grandchild_category.title,
                                }
                            ],
                        }
                    ],
                }
            ],
        }

        assert response.data == expected_data, response.data


class TestDetailCategoryView(TestCategoryViewSet):
    def test_details(
        self,
        client: APIClient,
        parent_category: Category,
        child_category: Category,
        grandchild_category: Category,
    ):
        response = client.get(self.detail_url.format(child_category.pk))

        assert response.status_code == 200, response.data

        expected_data = {
            "id": child_category.id,
            "position": child_category.position,
            "slug": child_category.slug,
            "title": child_category.title,
            "children": [
                {
                    "children": [],
                    "id": grandchild_category.id,
                    "position": grandchild_category.position,
                    "slug": grandchild_category.slug,
                    "title": grandchild_category.title,
                }
            ],
        }

        assert response.data == expected_data, response.data
