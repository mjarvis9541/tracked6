from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_banned',
        'is_staff',
        'is_superuser',
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password', 'id')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'email', 'email_change_request')},
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_banned',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2')}),)

    search_fields = ('username', 'email')

    readonly_fields = ('id', 'email_change_request', 'last_login', 'date_joined')
