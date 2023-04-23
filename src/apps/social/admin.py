from django.contrib import admin

from src.apps.social.models import Bookmark, Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    ordering = ["-id"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    ordering = ["-id"]
