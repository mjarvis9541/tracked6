from django import forms
from django.utils.translation import gettext as _

from .models import User


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class EmailChangeForm(forms.Form):
    email = forms.EmailField(label=_('New email address'), required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.get(email=self.user.email)
        if email == user.email:
            raise forms.ValidationError('This email address is already registered to your account')
        elif User.objects.exclude(email=user.email).filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered')
        return email

    def is_valid(self):
        # Adds CSS class to invalid fields
        result = super().is_valid()
        # loop on *all* fields if key '__all__' found else only on errors:
        for x in self.fields if '__all__' in self.errors else self.errors:
            attrs = self.fields[x].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' form-invalid'})
        return result


class AccountActivationForm(forms.Form):
    """ Resends activation email if user exists and is not actived """

    email = forms.EmailField(label=_('email'), required=True)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('This email address has not been registered')
        if user.is_active:
            raise forms.ValidationError('This account has already been activated')
        if user.is_banned:
            raise forms.ValidationError('This account is currently banned and cannot be reactivated')
        return email
