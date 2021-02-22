from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from food.models import Food
from utils.behaviours import Timestampable, Uuidable


class Meal(Uuidable, Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True, help_text='Optional.')
    slug = models.SlugField(max_length=255, unique=True)
    
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
        return reverse('meals:detail', kwargs={'pk': self.id})


class MealItem(Uuidable, Timestampable):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = 'meal item'
        verbose_name_plural = 'meal items'

    def __str__(self):
        return f'{self.food.name} of {self.meal.name}'

    def get_absolute_url(self):
        return reverse('meals:detail', kwargs={'pk': self.meal.id})