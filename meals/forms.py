from django import forms
from django.forms import BaseFormSet, formset_factory

from meals.models import Meal


class MealCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if 'name' in self.changed_data:
            if Meal.objects.filter(user=self.request.user, name=name).exists():
                self.add_error(
                    'name', 'You have already created a meal with this name.'
                )
        return cleaned_data



class BaseMealFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
            
        quantity = []
        for form in self.forms:
            attrs = form.cleaned_data
            if attrs.get('quantity'):
                quantity.append(attrs['quantity'])

        if not quantity:
            print('No quantities')
            raise forms.ValidationError('You have not selected any food to add')

        if len(quantity) > 10:
            print('quanities !> 10')
            raise forms.ValidationError(f'You can only add a maximum of 10 food items per meal. Currently {len(quantity)}.')


class AddFoodToMealForm(forms.Form):
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


AddFoodToMealFormSet = formset_factory(AddFoodToMealForm, formset=BaseMealFormset, extra=0)