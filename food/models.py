from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import (
    Avg,
    Case,
    ExpressionWrapper,
    F,
    Func,
    Sum,
    Value,
    When,
    Window,
)
from utils.behaviours import Authorable, Nutritionable, Timestampable, Uuidable


class Brand(Authorable, Timestampable, Uuidable):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'pk': self.pk})


class Category(Authorable, Timestampable, Uuidable):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('food:category_detail', kwargs={'pk': self.pk})


class FoodQuerySet(models.QuerySet):
    def summary(self):
        return self.annotate(
            food_brand=F('brand__name'),
            data_value_measurement=Case(
                When(data_measurement='g', then=Value('100g')),
                When(data_measurement='ml', then=Value('100ml')),
                When(data_measurement='srv', then=Value('1 Serving')),
                output_field=models.CharField(),
            ),
        )

    def custom_summary(self, macro_1='protein', macro_2='carbohydrate', macro_3='fat'):
        return self.annotate(
            macro_1=F(f'{macro_1}'), macro_2=F(f'{macro_2}'), macro_3=F(f'{macro_3}')
        )


class Food(Uuidable, Nutritionable, Authorable, Timestampable):
    class Measurement(models.TextChoices):
        GRAMS = 'g', ('g')
        MILLILITRES = 'ml', ('ml')
        SERVINGS = 'srv', ('serving')

    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    data_value = models.IntegerField()
    data_measurement = models.CharField(max_length=50, choices=Measurement.choices)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(
        default=True,
        help_text='Designates whether this food is displayed in the database. Unselect this instead of deleting food.',
    )
    objects = FoodQuerySet.as_manager()

    class Meta:
        verbose_name = 'food'
        verbose_name_plural = 'food'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='unique_name_brand')
        ]

    def __str__(self):
        if self.data_measurement == 'g' or self.data_measurement == 'ml':
            return f'{self.name}, {self.brand.name}, {self.data_value}{self.data_measurement}'
        else:
            return f'{self.name}, {self.brand.name}, {self.data_value} {self.get_data_measurement_display().title()}'

    def get_absolute_url(self):
        return reverse('food:detail', kwargs={'pk': self.pk})

    @property
    def serving(self):
        """ Data value display for the food list page. """
        if self.data_measurement == 'g' or self.data_measurement == 'ml':
            return f'{self.data_value}{self.data_measurement}'
        else:
            return f'{self.data_value} Serv'# {self.get_data_measurement_display().title()}'



    @property
    def data_value_measurement_detail(self):
        """ Data value display for the food detail page. """
        if self.data_measurement == 'g' or self.data_measurement == 'ml':
            return f'{self.data_value}{self.data_measurement}'
        else:
            return f'{self.get_data_measurement_display().title()}'
