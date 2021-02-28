from rest_framework import serializers

from ..models import Food


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'id',
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
            'user_created',
            'user_updated',
            'datetime_created',
            'datetime_updated',
        ]
