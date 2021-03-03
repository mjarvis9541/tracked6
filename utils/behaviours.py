import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

""" Reference: https://blog.kevinastone.com/django-model-behaviors """




class Permalinkable(models.Model):
    """
    Requires a url parameter attribute in the model
    Adds a slug field to the model, sets absolute url to the url_name
    Automatically generates a slug
    # TODO: Handle case sensitivity.
    """

    slug = models.SlugField(max_length=255, editable=False)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        url_name = self.url_name
        return reverse(url_name, kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        slug_str = self.slug_str
        self.slug = slugify(slug_str)
        super().save(*args, **kwargs)


class Uuidable(models.Model):
    """
    Adds an id field as a UUIDField to the model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Nutritionable(models.Model):
    """
    Adds common calorie and macronutrient fields to the model.
    - Calories as an PostiveInteferField.
    - Macronutrients as a DecimalField, content formatted 000.0.
    - Salt as a DecimalField, content formatted as 000.00.
    """

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
    """
    Adds a 'datetime_created' and 'datetime_updated' field to the model. Both auto-popluated.
    """

    datetime_created = models.DateTimeField(verbose_name='created on', auto_now_add=True)
    datetime_updated = models.DateTimeField(verbose_name='updated on', auto_now=True)

    class Meta:
        abstract = True


class Authorable(models.Model):
    """
    Adds a 'user_created' and 'user_updated' field to the model, defaults to admin user.
    """

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='created by',
        related_name='%(app_label)s_%(class)s_user_created_related',
        related_query_name='%(app_label)s_%(class)s_user_created_rquery',
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='updated by',
        related_name='%(app_label)s_%(class)s_user_updated_related',
        related_query_name='%(app_label)s_%(class)s_user_updated_rquery',
    )

    class Meta:
        abstract = True
