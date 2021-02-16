from django.conf import settings
from django.db import models
from food.models import Food
from utils.behaviours import Uuidable


class Meal(Uuidable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    item_1 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_1')
    item_1_quantity = models.DecimalField(max_digits=3, decimal_places=1)
    item_2 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_2', null=True, blank=True)
    item_2_quantity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    item_3 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_3', null=True, blank=True)
    item_3_quantity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    item_4 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_4', null=True, blank=True)
    item_4_quantity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    item_5 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_5', null=True, blank=True)
    item_5_quantity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        verbose_name = 'meal'
        verbose_name_plural = 'saved meals'
    
    def __str__(self):
        return self.name
    