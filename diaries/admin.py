from django.contrib import admin

from .models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('food', 'quantity', 'user', 'date', 'meal', )
    list_filter = ('user', 'date', 'meal')
