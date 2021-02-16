from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields if field.name != 'id']
    list_filter = ['sex', 'height', 'weight']
    search_fields = ['user__username', 'user__full_name', 'date_of_birth']

    # fieldsets = [
    #     [None, {'fields': [
    #         'user',
    #         '',
    #     ]}]
    # ]