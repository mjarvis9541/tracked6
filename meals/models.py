from django.conf import settings
from django.db import models
from django.db.models import (Avg, Case, Count, ExpressionWrapper, F, Func,
                              Sum, Value, When, Window)
from django.db.models.functions import Coalesce, Concat, Round
from django.urls import reverse
from django.utils.text import slugify
from food.models import Food
from utils.behaviours import Timestampable, Uuidable


class MealQuerySet(models.QuerySet):
    def summary(self):
        return self.annotate(
            item_count=Count('mealitem')
        )


class Meal(Uuidable, Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True, help_text='Optional.')
    slug = models.SlugField(max_length=255, unique=True)
    
    objects = MealQuerySet.as_manager()

    class Meta:
        verbose_name = 'meal'
        verbose_name_plural = 'meals'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='unique_meal_name'
            )
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = f'{self.user.username} {self.name}'
            self.slug = slugify(slug_str)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('meals:item_list', kwargs={'pk': self.id})


class Round1(Func):
    """ Postgres specific database function to round floating point numbers to 1 decimal place """

    function = 'ROUND'
    template = '%(function)s(%(expressions)s::numeric, 1)'


class Round2(Func):
    """ Postgres specific database function to round floating point numbers to 2 decimal places """

    function = 'ROUND'
    template = '%(function)s(%(expressions)s::numeric, 2)'


class MealItemQuerySet(models.QuerySet):
    def summary(self):
        return self.select_related('food', 'meal').annotate(
            food_name=F('food__name'),
            brand_name=F('food__brand__name'),
            data_measurement=F('food__data_measurement'),
            # serving_value=ExpressionWrapper(F('quantity') * F('food__data_value'), output_field=models.DecimalField()),
            serving_value=Case(
                # Round food measured in grams or milliliters to whole number, round food measured in servings to 1 decimal place
                When(data_measurement='g', then=Round(ExpressionWrapper(F('quantity') * F('food__data_value'), output_field=models.DecimalField()))),
                When(data_measurement='ml', then=Round(ExpressionWrapper(F('quantity') * F('food__data_value'), output_field=models.DecimalField()))),
                When(data_measurement='srv', then=Round1(ExpressionWrapper(F('quantity') * F('food__data_value'), output_field=models.DecimalField()))),
            ),
            serving_measurement=Case( 
                # Pluralise serving if value > 1
                When(data_measurement='g', then=Value('g')),
                When(data_measurement='ml', then=Value('ml')),
                When(data_measurement='srv', serving_value__gt=1, then=Value(' Servings')),
                When(data_measurement='srv', serving_value__lte=1, then=Value(' Serving')),
                default=Value(''),
                output_field=models.CharField(),
            ),
            energy=ExpressionWrapper(F('quantity') * F('food__energy'), output_field=models.IntegerField()),
            fat=F('quantity') * F('food__fat'),
            saturates=F('quantity') * F('food__saturates'),
            carbohydrate=F('quantity') * F('food__carbohydrate'),
            sugars=F('quantity') * F('food__sugars'),
            fibre=F('quantity') * F('food__fibre'),
            protein=F('quantity') * F('food__protein'),
            salt=F('quantity') * F('food__salt'),
            sodium=F('salt') * 400,
        )

    def total(self):
        return self.summary().aggregate(
            total_energy=Coalesce(Sum('energy'), 0),
            total_fat=Coalesce(Sum('fat'), 0),
            total_saturates=Coalesce(Sum('saturates'), 0),
            total_carbohydrate=Coalesce(Sum('carbohydrate'), 0),
            total_sugars=Coalesce(Sum('sugars'), 0),
            total_fibre=Coalesce(Sum('fibre'), 0),
            total_protein=Coalesce(Sum('protein'), 0),
            total_salt=Coalesce(Sum('salt'), 0),
            total_sodium=Coalesce(Sum('sodium'), 0),
        )

class MealItem(Uuidable, Timestampable):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)

    objects = MealItemQuerySet.as_manager()

    class Meta:
        verbose_name = 'meal item'
        verbose_name_plural = 'meal items'

    def __str__(self):
        return f'{self.food.name} of {self.meal.name}'

    def get_absolute_url(self):
        return reverse('meals:item_list', kwargs={'pk': self.meal.id})