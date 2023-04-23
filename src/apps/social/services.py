from django.contrib.auth import get_user_model

from src.apps.social.models import Bookmark, Like, LikeType

User = get_user_model()


class LikeService:
    @staticmethod
    def toggle_like(user: User, question_id: int, like_type: LikeType) -> Like | None:
        """Toggle like or dislike to a question"""

        existing_like = Like.objects.filter(user=user, question_id=question_id).first()

        if not existing_like:
            like = Like.objects.create(
                user=user, question_id=question_id, like_type=like_type
            )
            return like

        if existing_like.like_type == like_type:
            existing_like.delete()
            return

        existing_like.like_type = like_type
        existing_like.save(update_fields=["like_type"])
        return existing_like


class BookmarkService:
    @staticmethod
    def toggle_bookmark(user: User, question_id: int) -> Bookmark | None:
        """Toggle bookmark for a question"""

        existing_bookmark = Bookmark.objects.filter(
            user=user, question_id=question_id
        ).first()

        if existing_bookmark:
            existing_bookmark.delete()
            return

        bookmark = Bookmark.objects.create(user=user, question_id=question_id)
        return bookmark
