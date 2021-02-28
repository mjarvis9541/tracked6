from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.behaviours import Uuidable

from .managers import UserManager


class User(Uuidable, PermissionsMixin, AbstractBaseUser):
    """
    Custom user model. Implemented as AbstractBaseUser for the following reasons:
    Wanted the ability to use email/password for authentication over username/password.
    Wanted to change first_name/last_name to full_name.
    """

    email = models.EmailField(_('email'), max_length=254, unique=True)
    email_confirmed = models.BooleanField(_('email confirmed'), default=False)
    full_name = models.CharField(_('full name'), max_length=70, null=True, blank=True)

    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether this user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    setup_complete = models.BooleanField(
        _('profile setup'),
        default=False,
        help_text='Confirms whether this user has gone through the initial setup and set their profile up. This is required to use the Food Diary.',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     return reverse('accounts:account')

    def get_full_name(self):
        if self.full_name:
            return self.full_name

    def get_short_name(self):
        if self.full_name:
            return self.full_name.split()[0]
