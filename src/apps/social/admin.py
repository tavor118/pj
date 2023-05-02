from django.contrib import admin

from src.apps.social.models import Bookmark, Comment, CommentReply, Like, Note


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    ordering = ["-id"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    ordering = ["-id"]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    ordering = ["-id"]


@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    ordering = ["-id"]


class CommentReplyInline(admin.TabularInline):
    model = CommentReply
    fields = ["question", "comment", "author", "content"]
    extra = 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ordering = ["-id"]

    inlines = [CommentReplyInline]
