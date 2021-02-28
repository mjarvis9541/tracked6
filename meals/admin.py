from django.contrib import admin

from .models import Meal, MealItem


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    pass


@admin.register(MealItem)
class MealItemAdmin(admin.ModelAdmin):
    pass
