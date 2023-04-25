from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from pytest import fixture
from rest_framework.test import APIClient

from src.apps.questions.models import Category, Question
from src.apps.social.models import Bookmark, Like, LikeType

User = get_user_model()


# MODEL FIXTURES


# Users app
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
    EmailAddress.objects.create(
        user=user, email=user_email, primary=True, verified=True
    )
    return user


@fixture
def user2(user_password: str) -> User:
    user_email = "example2@gmail.com"
    username = "user2"
    user = User.objects.create_user(
        email=user_email,
        username=username,
        password=user_password,
    )
    EmailAddress.objects.create(
        user=user, email=user_email, primary=True, verified=True
    )
    return user


# Questions app
@fixture
def parent_category() -> Category:
    parent_category = Category.objects.create(title="Python", position=1)
    return parent_category


@fixture
def child_category(parent_category: Category) -> Category:
    child_category = Category.objects.create(
        parent=parent_category, title="Core", position=1
    )
    return child_category


@fixture
def question(child_category: Category) -> Question:
    question = Question.objects.create(
        category=child_category,
        title="What is Python?",
        content="Python is a programming language.",
        position=10,
    )
    return question


@fixture
def question2(child_category: Category) -> Question:
    question = Question.objects.create(
        category=child_category,
        title="Python Data Types",
        content="Python have mutable and immutable collection data types.",
        position=20,
    )
    return question


# Social app
@fixture
def like(user: User, question: Question) -> Like:
    like = Like.objects.create(user=user, question=question, like_type=LikeType.LIKE)
    return like


@fixture
def bookmark(user: User, question: Question) -> Like:
    bookmark = Bookmark.objects.create(user=user, question=question)
    return bookmark


# CLIENT FIXTURES
@fixture
def client() -> APIClient:
    return APIClient()


@fixture
def admin_client(client: APIClient) -> APIClient:
    client = client.force_authenticate(user=admin_user)
    return client
