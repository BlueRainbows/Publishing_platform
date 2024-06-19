from django.contrib import admin
from content.models import Content, LikeCount, Comment


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'publish')
    search_fields = ('created_at', 'publish')
    ordering = ('-created_at',)


@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('user', 'content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content',)
