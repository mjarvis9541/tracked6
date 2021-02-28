from django.contrib import admin

from .models import Brand, Category, Food


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'user_created',
        'datetime_created',
        'datetime_updated',
    ]
    list_filter = ['datetime_created']
    search_fields = ['name', 'description']
    readonly_fields = [
        'id',
        'datetime_created',
        'datetime_updated',
        'user_created',
        'user_updated',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'user_created',
        'datetime_created',
        'datetime_updated',
    ]
    list_filter = ['datetime_created']
    search_fields = ['name', 'description']
    readonly_fields = [
        'id',
        'datetime_created',
        'datetime_updated',
        'user_created',
        'user_updated',
    ]


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'brand',
        'serving',
        'energy',
        'fat',
        'saturates',
        'carbohydrate',
        'sugars',
        'fibre',
        'protein',
        'salt',
        'sodium',
        'category',
    ]
    list_filter = ['brand', 'category', 'datetime_created']
    search_fields = ['name', 'brand__name']
    readonly_fields = [
        'id',
        'datetime_created',
        'datetime_updated',
        'user_created',
        'user_updated',
        'sodium',
    ]
    fieldsets = [
        [
            None,
            {
                'fields': [
                    'name',
                    'brand',
                    'category',
                    'data_value',
                    'data_measurement',
                    'energy',
                    'fat',
                    'saturates',
                    'carbohydrate',
                    'sugars',
                    'fibre',
                    'protein',
                    'salt',
                    'sodium',
                    'description',
                    'active',
                    'user_updated',
                    'datetime_updated',
                    'user_created',
                    'datetime_created',
                    'slug',
                    'id',
                ]
            },
        ]
    ]
