from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

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
            raise ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']


class UserChangeEmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.get(email=self.user.email)
        if email == user.email:
            raise forms.ValidationError('This email address is already registered to your account')
        elif User.objects.exclude(email=user.email).filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered to another account')
        return email


class ResendActivationEmailForm(forms.Form):
    """ Resends activation email if user exists and is not actived """

    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('This email address has not been registered')
        if user.is_active:
            raise forms.ValidationError('This account has already been activated')
        if user.is_banned:
            raise forms.ValidationError('This account is currently banned and cannot be activated')
        else:
            return email
