from decimal import Decimal
from django.conf import settings
from django.db import models
from utils.behaviours import Uuidable, Timestampable
from django.utils import timezone
from django.urls import reverse


class Progress(Uuidable, Timestampable):
    """
    Model for users to record daily progress indicators such as weight, pictures and notes.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(
        verbose_name='weight (kg)',
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to='images', null=True, blank=True)
    notes = models.TextField('notes', max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Progress'
        verbose_name_plural = 'Progress'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date'], name='unique_user_date'
            )
        ]

    def __str__(self):
        return f'{self.date}: {self.user.username}'

    def get_absolute_url(self):
        return reverse('progress:detail', kwargs={'pk': self.pk})

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