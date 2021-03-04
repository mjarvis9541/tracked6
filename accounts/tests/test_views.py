from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.tokens import default_token_generator
from ..forms import ResendActivationEmailForm
from ..models import User
from .. import views
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import resolve
from django.contrib import auth
import unittest
from unittest.mock import patch, ANY

class BaseAuthTestCase(TestCase):
    def assertLoggedInAs(self, user):
        client_user = auth.get_user(self.client)
        self.assertEqual(client_user, user)
        assert client_user.is_authenticated()


class AccountViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_account_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/index/')
        self.assertEquals(response.status_code, 200)

    def test_account_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account'))
        self.assertEquals(response.status_code, 200)

    def test_account_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:account'))
        self.assertEquals(response.status_code, 302)

    def test_account_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:account'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/index/')

    def test_account_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account'))
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_account_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account'))
        self.assertContains(response, 'Account Settings')

    def test_account_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_account_url_resolves_to_account_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:account')
        self.assertEqual(resolve(url).func.view_class, views.AccountView)

    def test_account_view_context(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account'))
        self.assertEqual(response.context['user'].username, 'user')
        self.assertEqual(response.context['user'].email, 'email@email.com')


class ChangeNameViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_change_name_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/change-username/')
        self.assertEquals(response.status_code, 200)

    def test_change_name_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_name'))
        self.assertEquals(response.status_code, 200)

    def test_change_name_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:change_name'))
        self.assertEquals(response.status_code, 302)

    def test_change_name_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:change_name'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/change-name/')

    def test_change_name_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_name'))
        self.assertTemplateUsed(response, 'accounts/change_name.html')

    def test_change_name_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_name'))
        self.assertContains(response, 'Change Name')

    def test_change_name_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_name'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_change_name_url_resolves_to_change_name_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:change_name')
        self.assertEqual(resolve(url).func.view_class, views.ChangeNameView)


class ChangeUsernameViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_change_username_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/change-username/')
        self.assertEquals(response.status_code, 200)

    def test_change_username_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_username'))
        self.assertEquals(response.status_code, 200)

    def test_change_username_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:change_username'))
        self.assertEquals(response.status_code, 302)

    def test_change_username_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:change_username'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/change-username/')

    def test_change_username_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_username'))
        self.assertTemplateUsed(response, 'accounts/change_username.html')

    def test_change_username_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_username'))
        self.assertContains(response, 'Change Username')

    def test_change_username_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_username'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_change_username_url_resolves_to_change_username_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:change_username')
        self.assertEqual(resolve(url).func.view_class, views.ChangeUsernameView)


class ChangeEmailViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_change_email_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/change-username/')
        self.assertEquals(response.status_code, 200)

    def test_change_email_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_email'))
        self.assertEquals(response.status_code, 200)

    def test_change_email_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:change_email'))
        self.assertEquals(response.status_code, 302)

    def test_change_email_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:change_email'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/change-email/')

    def test_change_email_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_email'))
        self.assertTemplateUsed(response, 'accounts/change_email.html')

    def test_change_email_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_email'))
        self.assertContains(response, 'Change Email')

    def test_change_email_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:change_email'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_change_email_url_resolves_to_change_email_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:change_email')
        self.assertEqual(resolve(url).func.view_class, views.ChangeEmailView)


class AccountViewGeneralTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            first_name='firstly', last_name='lastly', username='user', email='user@email.com', password='upassword123'
        )
        User.objects.create_user(
            username='inactiveuser', email='inactive.user@email.com', password='password123', is_active=False
        )

    def test_account_view(self):
        self.client.login(username='user', password='upassword123')
        # response = self.client.get('accounts/index/')
        response = self.client.get(reverse('accounts:account'))

    def test_change_name_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:change_name'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'user')

    def test_change_email_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:change_email'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'user')

    def test_change_username_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:change_username'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'user')

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'first_name': 'Michael',
                'last_name': 'Jarvis',
                'username': 'mjarvis',
                'email': 'mjarvis@email.com',
                'password1': 'password123',
                'password2': 'password123',
            },
        )
        self.assertRedirects(response, reverse('accounts:account_activation_sent'))

    def test_register_view_redirect_logged_in_user(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:register'), follow=True)
        self.assertRedirects(response, '/accounts/index/')

        message = list(response.context.get('messages'))[0]

        self.assertEqual(message.tags, 'error')
        self.assertTrue(
            'You are already registered. If you wish to create a new account, please log out and try again.'
            in message.message
        )



    def test_account_activation_resend_view(self):
        response = self.client.get(reverse('accounts:account_activation_resend'))
        self.assertTemplateUsed(response, 'accounts/account_activation_resend.html')

        # Test post data
        self.client.login(username='inactiveuser', password='password123')
        response = self.client.post(
            reverse('accounts:account_activation_resend'), {'email': 'inactive.user@email.com'}
        )
        self.assertRedirects(response, reverse('accounts:account_activation_sent'))

    def test_account_activation_sent_view(self):
        response = self.client.get(reverse('accounts:account_activation_sent'))
        self.assertTemplateUsed(response, 'accounts/account_activation_sent.html')

    def test_account_activate_view_post(self):
        user = User.objects.get(username='user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.post(reverse('accounts:activate_account', kwargs={'uidb64': uid, 'token': token}))
        self.assertRedirects(response, reverse('accounts:account_activation_complete'))

        # Check token has expired
        response = self.client.post(reverse('accounts:activate_account', kwargs={'uidb64': uid, 'token': token}))
        self.assertTemplateUsed(response, 'accounts/account_activation_invalid.html')

    def test_activate_account_complete_view(self):
        response = self.client.get(reverse('accounts:account_activation_complete'))
        self.assertTemplateUsed(response, 'accounts/account_activation_complete.html')

    def test_account_activate_view_exception(self):
        response = self.client.post(reverse('accounts:activate_account', kwargs={'uidb64': 'bad-uid', 'token': 'bad-token'}))
        
        self.assertRaises(TypeError, msg=None)