from django import forms

from meals.models import Meal


class MealCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=True, widget=forms.Textarea(attrs={'class': 'form-control'})
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


class MealAddFoodForm(forms.ModelForm):
    pass