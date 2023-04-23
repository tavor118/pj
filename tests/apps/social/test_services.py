from django.contrib.auth import get_user_model
from pytest import fixture

from src.apps.questions.models import Question
from src.apps.social.models import LikeType
from src.apps.social.services import LikeService

User = get_user_model()


@fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


class TestLikeService:
    @fixture
    def service(self) -> LikeService:
        return LikeService()

    def test_toggle_like(self, service: LikeService, question: Question, user: User):
        like = service.toggle_like(
            user, question_id=question.id, like_type=LikeType.LIKE
        )
        assert like.like_type == LikeType.LIKE
        assert like.user == user
        assert like.question == question

        like = service.toggle_like(
            user, question_id=question.id, like_type=LikeType.DISLIKE
        )
        assert like.like_type == LikeType.DISLIKE

        like = service.toggle_like(
            user, question_id=question.id, like_type=LikeType.DISLIKE
        )
        assert not like
