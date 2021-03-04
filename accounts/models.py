from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from utils.models import LowerCaseCharField

from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    """
    Custom user model.
    Implemented as wanted the ability to switch out email/password for
    authentication over username/password.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            """
            Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
            """
        ),
    )
    is_banned = models.BooleanField(
        _('banned'),
        default=False,
        help_text=_(
            """
            Designates whether this user should be treated as banned.
            This prevents inactive users from re-activating their account by requesting a 'resend activation' email.
            """
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_change_pending = models.EmailField(
        _('email change pending'),
        null=True,
        help_text=_(
            """
            If the user has requested to change their registered email address, it will show here until it has been \
            confirmed via email. Once the user has confirmed their new email address, this field will be blank.
            """
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def get_absolute_url(self):
    #     return reverse('profiles:profile', kwargs={'pk':self.pk})

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this user. """
        send_mail(subject, message, from_email, [self.email], **kwargs)

