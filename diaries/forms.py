from django import forms

from django.forms import BaseFormSet, formset_factory
from utils.forms import DateInput
from .models import Diary


class DiaryUpdateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['date', 'meal', 'quantity']
        widgets = {'date': DateInput()}


class BaseDiaryFormset(BaseFormSet):
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


class AddToDiaryForm(forms.Form):
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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     checkbox = cleaned_data.get('checkbox')
    #     quantity = cleaned_data.get('quantity')
    #     if checkbox and not quantity:
    #         msg = 'Quantity required.'
    #         self.add_error('quantity', msg)
    #     return cleaned_data


AddToDiaryFormSet = formset_factory(AddToDiaryForm, formset=BaseDiaryFormset, extra=0)










class BaseRecentDiaryFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
            
        checkboxes = []
        for form in self.forms:
            attrs = form.cleaned_data
            if attrs.get('checkbox'):
                checkboxes.append(attrs['checkbox'])

        if not checkboxes:
            print('no checkboxs')
            raise forms.ValidationError('You have not selected any food to add')


class AddRecentToDiaryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].disabled = True
        # self.fields['id'].hidden = True

    id = forms.UUIDField()
    checkbox = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input '}))
    quantity = forms.FloatField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 0}),
    )

    def clean(self):
        cleaned_data = super().clean()
        checkbox = cleaned_data.get('checkbox')
        quantity = cleaned_data.get('quantity')
        if checkbox and not quantity:
            msg = 'Quantity required.'
            self.add_error('quantity', msg)
        return cleaned_data


AddRecentToDiaryFormSet = formset_factory(AddRecentToDiaryForm, formset=BaseRecentDiaryFormset, extra=0)





class DiaryUpdateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['date', 'meal', 'quantity']
        widgets = {
            'date': DateInput(attrs={'class':'form-control'}),
            'meal': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
