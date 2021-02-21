from django.conf import settings
from django.db import models
from django.utils import timezone
from food.models import Food
from .managers import DiaryQuerySet
from utils.behaviours import Uuidable, Timestampable
from django.urls import reverse


class Diary(Uuidable, Timestampable):
    class Meal(models.IntegerChoices):
        MEAL1 = 1, ('Breakfast')
        MEAL2 = 2, ('Morning Snack')
        MEAL3 = 3, ('Lunch')
        MEAL4 = 4, ('Afternoon Snack')
        MEAL5 = 5, ('Dinner')
        MEAL6 = 6, ('Evening Snack')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    meal = models.IntegerField(choices=Meal.choices)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
    objects = DiaryQuerySet.as_manager()

    class Meta:
        verbose_name = 'diary entry'
        verbose_name_plural = 'diary entries'
      # ordering = ('-datetime_created',)

    def __str__(self):
        return f'{self.food.data_value}{self.food.data_measurement} {self.food.name}'
    
    def get_absolute_url(self):
        return reverse('diaries:update', kwargs={'pk': self.pk})

    @property
    def brand(self):
        return self.food.brand

    @property
    def serving(self):
        data_value = self.quantity * self.food.data_value
        data_measurement = self.food.get_data_measurement_display()
        if data_measurement == 'g' or data_measurement == 'ml':
            return f'{round(data_value)}{data_measurement}'
        else:
            if data_value > 1:
                return f'{round(data_value)} {data_measurement.title()}s'     
            else: 
                return f'{round(data_value)} {data_measurement.title()}'     