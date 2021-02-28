from django import forms
from django.forms import formset_factory, widgets

from .models import Meal, MealItem


# add initial data here
class MealCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Meal
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if Meal.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError('You have already created a meal with this name.')
        return cleaned_data


class AddToMealForm(forms.ModelForm):
    class Meta:
        model = MealItem
        fields = ['quantity']

        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MealItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].disabled = True
        self.fields['id'].hidden = True

    id = forms.UUIDField()
    quantity = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'tabindex': "1", 'class': 'form-control', 'placeholder': 0}),
    )


AddToMealFormSet = formset_factory(MealItemForm, extra=0)
