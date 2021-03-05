from django.test.testcases import TestCase

from ..forms import AccountActivationForm, EmailChangeForm, UserCreationForm
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

    def test_user_creation_form_save(self):
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
        self.assertTrue(form.save())


class EmailChangeFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@email.com', password='password')
        self.anoter_user = User.objects.create_user(username='another', email='another@email.com', password='password')

    def test_email_already_registered_to_user(self):
        form = EmailChangeForm(user=self.user, data={'email': 'user@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email address is already registered to your account'])

    def test_email_already_registered_to_another_user(self):
        form = EmailChangeForm(user=self.user, data={'email': 'another@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email address is already registered'])

    def test_user_change_form_is_valid(self):
        form = EmailChangeForm(user=self.user, data={'email': 'new_email@email.com'})
        self.assertTrue(form.is_valid())


class ResendActivationEmailFormTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='active', email='active@email.com', password='password')
        User.objects.create_user(username='inactive', email='inactive@email.com', password='password', is_active=False)
        User.objects.create_user(
            username='banned', email='banned@email.com', password='password', is_active=False, is_banned=True
        )

    def test_user_account_exists(self):
        form = AccountActivationForm(data={'email': 'idonotexist@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email address has not been registered'])

    def test_user_account_is_not_active(self):
        form = AccountActivationForm(data={'email': 'active@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This account has already been activated'])

    def test_user_account_is_not_banned(self):
        form = AccountActivationForm(data={'email': 'banned@email.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This account is currently banned and cannot be reactivated'])

    def test_resend_activation_form_valid(self):
        form = AccountActivationForm(data={'email': 'inactive@email.com'})
        self.assertTrue(form.is_valid())
