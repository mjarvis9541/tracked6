from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from utils.behaviours import Timestampable, Uuidable


class Progress(Uuidable, Timestampable):
    """
    Model for users to record daily progress indicators such as weight, pictures and notes.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, validators=[MaxValueValidator(limit_value=date.today)])
    slug = models.SlugField(max_length=255, unique=True)
    weight = models.DecimalField(
        verbose_name='weight (kg)',
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name='progress picture',
        upload_to='images/progress_pictures',
        null=True,
        blank=True,
        help_text='Upload an optional progress picture for this day.',
    )
    notes = models.TextField('notes', max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'progress log'
        verbose_name_plural = 'progress logs'
        constraints = [models.UniqueConstraint(fields=['user', 'date'], name='unique_user_date')]

    def __str__(self):
        return f'{self.user.username}, {self.date}'

    def get_absolute_url(self):
        return reverse('progress:list')

    def save(self, *args, **kwargs):
        slug_str = f'{self.date} {self.user.username}'
        self.slug = slugify(slug_str)
        super().save(*args, **kwargs)

    @property
    def weight_lb(self):
        if self.weight:
            return round(self.weight * Decimal(2.20462))

    @property
    def weight_st(self):
        if self.weight_lb:
            weight = {}
            weight["st"] = round(self.weight_lb // 14)
            weight["lb"] = round(self.weight_lb % 14)
            stone = weight["st"]
            pounds = weight["lb"]
            return f'{stone} st, {pounds} lb'
