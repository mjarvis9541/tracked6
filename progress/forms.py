from django import forms
from .models import Progress


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['date', 'weight', 'image', 'notes']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')

        if Progress.objects.exclude(id=self.instance.id).filter(user=self.user, date=date).exists():
            raise forms.ValidationError(
                'You have already entered a weight for this date.'
            )
        return cleaned_data