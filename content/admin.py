from django.contrib import admin
from content.models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'publish')
    search_fields = ('created_at', 'publish')
    ordering = ('-created_at',)
