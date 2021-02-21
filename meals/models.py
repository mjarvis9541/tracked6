from django.conf import settings
from django.db import models
from food.models import Food
from utils.behaviours import Timestampable, Uuidable


class Meal(Uuidable, Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    item_1 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_1')
    item_1_quantity = models.DecimalField(max_digits=4, decimal_places=2)
    item_2 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_2', null=True, blank=True)
    item_2_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_3 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_3', null=True, blank=True)
    item_3_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_4 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_4', null=True, blank=True)
    item_4_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_5 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_5', null=True, blank=True)
    item_5_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_6 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_6', null=True, blank=True)
    item_6_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_7 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_7', null=True, blank=True)
    item_7_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_8 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_8', null=True, blank=True)
    item_8_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_9 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_9', null=True, blank=True)
    item_9_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    item_10 = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='meal_items_10', null=True, blank=True)
    item_10_quantity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'meal'
        verbose_name_plural = 'saved meals'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='unique_meal_name'
            )
        ]
    
    def __str__(self):
        return self.name
    

    