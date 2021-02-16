from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserChangeForm, UserCreationForm
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.utils.translation import gettext_lazy as _


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ( 'username', 'email','password', 'id')}),
        (
            _('Personal info'),
            {'fields': ('full_name', 'email_confirmed', 'setup_complete')},
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2')}),
    )
    
    list_display = ['username', 'email', 'full_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
    search_fields = ['username', 'email', 'full_name']
    ordering = ('email',)
    readonly_fields = ['id', 'last_login', 'date_joined']
