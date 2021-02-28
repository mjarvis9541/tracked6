from django.contrib.auth import get_user_model
from django.test import TestCase

from food.models import Brand, Category, Food

User = get_user_model()


class FoodDataTests(TestCase):
    def setUp(self):

        user = User.objects.create(username='user', password='password123')
        brand = Brand.objects.create(name='Tesco', description='None')
        category = Category.objects.create(name='Generic', description='None')

        Food.objects.create(
            name='Chicken Breast',
            brand=brand,
            category=category,
            data_value=100,
            data_measurement='g',
            energy=105,
            fat=1,
            saturates=1,
            carbohydrate=0,
            sugars=0,
            fibre=0,
            protein=22,
            salt=1,
            user_created=user,
            user_updated=user,
        )

    def test_brand_create(self):
        brand = Brand.objects.first()
        self.assertEqual(brand.name, 'Tesco')
        self.assertEqual(brand.description, 'None')

    def test_category_create(self):
        category = Category.objects.first()
        self.assertEqual(category.name, 'Generic')
        self.assertEqual(category.description, 'None')

    def test_food_create(self):
        brand = Brand.objects.get(name='Tesco')
        category = Category.objects.get(name='Generic')
        food = Food.objects.get(name='Chicken Breast')

        self.assertEqual(food.name, 'Chicken Breast')
        self.assertEqual(food.brand, brand)
        self.assertEqual(food.category, category)
        self.assertEqual(food.data_value, 100)
        self.assertEqual(food.data_measurement, 'g')
        self.assertEqual(food.energy, 105)
        self.assertEqual(food.fat, 1)
        self.assertEqual(food.saturates, 1)
        self.assertEqual(food.carbohydrate, 0)
        self.assertEqual(food.sugars, 0)
        self.assertEqual(food.fibre, 0)
        self.assertEqual(food.protein, 22)
        self.assertEqual(food.salt, 1)