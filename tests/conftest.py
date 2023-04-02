from pytest import fixture
from rest_framework.test import APIClient


@fixture
def client() -> APIClient:
    return APIClient()


@fixture
def admin_client(client) -> APIClient:
    # TODO rewrite after user is created
    return client
