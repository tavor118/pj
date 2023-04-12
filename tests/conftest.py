from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from pytest import fixture
from rest_framework.test import APIClient

User = get_user_model()


# Model fixtures
@fixture
def user_email() -> str:
    return "example@gmail.com"


@fixture
def username() -> str:
    return "user"


@fixture
def user_password() -> str:
    return "@123password"


@fixture
def admin_user(user_email: str, username: str, user_password: str) -> User:
    admin_user = User.objects.create_superuser(
        email="admin@gmail.com", username="admin", password=user_password
    )
    return admin_user


@fixture
def user(user_email: str, username: str, user_password: str) -> User:
    user = User.objects.create_user(
        email=user_email,
        username=username,
        password=user_password,
    )
    EmailAddress.objects.create(user=user, email=user_email, primary=True, verified=True)
    return user


# Client fixtures
@fixture
def client() -> APIClient:
    return APIClient()


@fixture
def admin_client(client: APIClient) -> APIClient:
    client = client.force_authenticate(user=admin_user)
    return client
