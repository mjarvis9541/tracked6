import string

from django import forms
from django.utils.safestring import SafeData, SafeText, mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Brand, Category, Food
from diaries.models import Diary
from utils.forms import DateInput


SERVING_CHOICES = [
    ('', '---------'),
    ('100g', '100g'),
    ('100ml', '100ml'),
    ('1 Serving', '1 Serving'),
]

FOOD_SORT_CHOICES = [
    ('', 'Sort'),
    ('name', 'Name (a-z)'),
    ('-name', 'Name (z-a)'),
    ('energy', 'Calories (low-high)'),
    ('-energy', 'Calories (high-low)'),
    ('protein', 'Protein (low-high)'),
    ('-protein', 'Protein (high-low)'),
    ('carbohydrate', 'Carbs (low-high)'),
    ('-carbohydrate', 'Carbs (high-low)'),
    ('fat', 'Fat (low-high)'),
    ('-fat', 'Fat (high-low)'),
    ('-datetime_created', 'Recently Created'),
    ('-datetime_updated', 'Recently Updated'),
]

BRAND_SORT_CHOICES = [
    ('', 'Sort'),
    ('name', 'Name (a-z)'),
    ('-name', 'Name (z-a)'),
    ('-datetime_created', 'Recently Created'),
    ('-datetime_updated', 'Recently Updated'),
]


class FoodFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search'}
        ),
    )
    brand = forms.ChoiceField(
        required=False, widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        required=False, widget=forms.Select(attrs={'class': 'form-control'})
    )
    sort = forms.ChoiceField(
        required=False,
        choices=FOOD_SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        # Setting the choice fields in a way that makes them dynamic:
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices = [
            ('', 'All Brands'),
        ]  # Adds a default choice and sets to blank
        for x in Brand.objects.all().values_list('id', 'name'):
            self.fields['brand'].choices.append(tuple(x))
        self.fields['category'].choices = [
            ('', 'All Categories'),
        ]  # Adds a default choice and sets to blank
        for x in Category.objects.all().values_list('id', 'name'):
            self.fields['category'].choices.append(tuple(x))
        self.fields['sort'].choices = FOOD_SORT_CHOICES


class BrandFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search'}
        ),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=BRAND_SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class FoodCreateServingForm(forms.ModelForm):
    serving = forms.ChoiceField(
        choices=SERVING_CHOICES, widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Food
        fields = [
            'name',
            'brand',
            'category',
            'serving',
            'energy',
            'fat',
            'saturates',
            'carbohydrate',
            'sugars',
            'fibre',
            'protein',
            'salt',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'energy': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control'}),
            'saturates': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbohydrate': forms.NumberInput(attrs={'class': 'form-control'}),
            'sugars': forms.NumberInput(attrs={'class': 'form-control'}),
            'fibre': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control'}),
            'salt': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # def clean(self, *args, **kwargs):
    #     cleaned_data = super().clean()
    #     brand = cleaned_data.get('brand')
    #     name = cleaned_data.get('name')

    #     if 'name' in self.changed_data or 'brand' in self.changed_data:
    #         if (
    #             Food.objects.exclude(pk=self.instance.pk)
    #             .filter(brand=brand, name=name)
    #             .exists()
    #         ):
    #             food = Food.objects.filter(brand=brand, name=name).first()
    #             self.add_error(
    #                 'name',
    #                 _(
    #                     mark_safe(
    #                         f'A food with this name and brand already exists. \
    #                         <a href="{food.get_absolute_url()}" target="_blank">Click here</a> \
    #                             to check this is not a duplicate.'
    #                     )
    #                 ),
    #             )
    #     energy = cleaned_data.get('energy')
    #     fat = cleaned_data.get('fat')
    #     saturates = cleaned_data.get('saturates')
    #     carbohydrate = cleaned_data.get('carbohydrate')
    #     sugars = cleaned_data.get('sugars')
    #     protein = cleaned_data.get('protein')
    #     if saturates > fat:
    #         self.add_error('saturates', _('Saturates must not exceed total fat.'))
    #     if sugars > carbohydrate:
    #         self.add_error('sugars', _('Sugars must not exceed total carbohydrate.'))

    #     energy_from_fat = fat * 9
    #     energy_from_carbohydrate = carbohydrate * 4
    #     energy_from_protein = protein * 4
    #     total_energy = round(
    #         energy_from_fat + energy_from_carbohydrate + energy_from_protein
    #     )
    #     if total_energy > energy:
    #         msg = _(
    #             f'energy should be at least {total_energy} kcal for the total grams of protein, \
    #             carbohydrate and fat you have provided. Please double check these values; \
    #                 if correct, set energy to {total_energy} kcal.'
    #         )
    #         self.add_error('energy', msg)
    #     return cleaned_data


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class FoodDetailToDiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now()
        self.fields['quantity'].initial = 1

    class Meta:
        model = Diary
        fields = [
            'date',
            'meal',
            'quantity',
        ]
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'meal': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DiaryMealUpdateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = [
            'quantity'
        ]
