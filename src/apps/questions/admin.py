from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from src.apps.questions.models import Category, Question, ResourceLink


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["position"]


class ResourceLinkInline(admin.TabularInline):
    model = ResourceLink
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["position"]

    inlines = [ResourceLinkInline]
