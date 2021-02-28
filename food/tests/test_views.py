from unittest import skip

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from food.models import Brand, Category, Food


@skip('demonstrating skipping')
class TestSkip(TestCase):
    def test_skip_example(self):
        pass


class FoodTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@email.com', password='test1pass2word3'
        )
        self.brand = Brand.objects.create(name='Tesco', description='Supermarket')
        self.category = Category.objects.create(
            name='Generic', description='Generic category'
        )
        self.food = Food.objects.create(
            name='Chicken Breast',
            brand=self.brand,
            category=self.category,
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
            user_created=self.user,
            user_updated=self.user,
        )

    def test_food_list_view(self):
        self.client.login(email='testuser@email.com', password='test1pass2word3')
        response = self.client.get(reverse('food_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Breast')
        self.assertTemplateUsed(response, 'food/food_create.html')

    def test_food_list_view(self):
        self.client.login(email='testuser@email.com', password='test1pass2word3')
        response = self.client.get(reverse('food_create'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, '')
        self.assertTemplateUsed(response, 'bs5_food/food_create.html')