from django.test import SimpleTestCase
from django.test.testcases import TestCase
from ..forms import UserChangeForm, UserCreationForm, ResendActivationEmailForm
from ..models import User


class UserCreationFormTests(TestCase):
    def test_user_creation_form_valid_data(self):
        form = UserCreationForm(
            data={
                'first_name': 'Michael',
                'last_name': 'Jarvis',
                'username': 'mjarvis',
                'email': 'mjarvis@email.com',
                'password1': 'password123',
                'password2': 'password123',
            }
        )
        self.assertTrue(form.is_valid())

    def test_clean_password2(self):
        form = UserCreationForm(
            data={
                'first_name': 'Michael',
                'last_name': 'Jarvis',
                'username': 'mjarvis',
                'email': 'mjarvis@email.com',
                'password1': 'password123',
                'password2': 'password124',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['Passwords don\'t match'])


class ResendActivationEmailFormTestCase(TestCase):
    def setUp(self):
        # Create an active user
        User.objects.create(username='user', email='user@email.com', password='password123')

    def test_user_account_exists(self):
        form = ResendActivationEmailForm(data={'email': 'idonotexist@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email address has not been registered'])

    def test_user_account_is_not_active(self):
        form = ResendActivationEmailForm(data={'email': 'user@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This account has already been activated'])