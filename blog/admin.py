from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
        'content',
    ]
    list_display = [
        'title',
        'content',
        'user_created',
        'datetime_created',
    ]
    readonly_fields = [
        'id',
        'slug',
        'datetime_created',
        'datetime_updated',
    ]
