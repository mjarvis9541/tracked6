import uuid
from django.conf import settings
from django.db import models

""" Reference: https://blog.kevinastone.com/django-model-behaviors """


class Uuidable(models.Model):
    """ Model behaviour that replaces the standard primary key id field with a uuid field """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Nutritionable(models.Model):
    """ Model behaviour that adds energy and macronutrient fields """

    energy = models.IntegerField(verbose_name='calories (kcal)')
    fat = models.DecimalField(verbose_name='fat (g)', max_digits=4, decimal_places=1)
    saturates = models.DecimalField(verbose_name='saturates (g)', max_digits=4, decimal_places=1)
    carbohydrate = models.DecimalField(verbose_name='carbohydrate (g)', max_digits=4, decimal_places=1)
    sugars = models.DecimalField(verbose_name='sugars (g)', max_digits=4, decimal_places=1)
    fibre = models.DecimalField(verbose_name='fibre (g)', max_digits=4, decimal_places=1)
    protein = models.DecimalField(verbose_name='protein (g)', max_digits=4, decimal_places=1)
    salt = models.DecimalField(verbose_name='salt (g)', max_digits=5, decimal_places=2)

    @property
    def sodium(self):
        if self.salt is not None:
            return round(self.salt * 400)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    datetime_created = models.DateTimeField('date created', auto_now_add=True)
    datetime_updated = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        abstract = True


class Authorable(models.Model):
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        verbose_name='created by',
        default='c64c16ee-fc7f-45c3-a84b-a81a6a29d5d6',
        related_name='%(app_label)s_%(class)s_user_created_related',
        related_query_name='%(app_label)s_%(class)s_user_created_rquery',
        )
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        verbose_name='updated by',
        default='c64c16ee-fc7f-45c3-a84b-a81a6a29d5d6',
        related_name='%(app_label)s_%(class)s_user_updated_related',
        related_query_name='%(app_label)s_%(class)s_user_updated_rquery',
        )

    class Meta:
        abstract = True
