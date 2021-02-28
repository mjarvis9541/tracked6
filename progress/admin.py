from django.contrib import admin

from .models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'weight', 'notes', 'image']
