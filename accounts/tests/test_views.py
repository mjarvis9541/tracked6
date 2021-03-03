from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.tokens import default_token_generator
from ..forms import ResendActivationEmailForm
from ..models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib import auth


class BaseAuthTestCase(TestCase):
    def assertLoggedInAs(self, user):
        client_user = auth.get_user(self.client)
        self.assertEqual(client_user, user)
        assert client_user.is_authenticated()


class AccountViewTests(TestCase):
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

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Settings')
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_account_view_redirect_unauthorized_user(self):
        response = self.client.get(reverse('accounts:account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/index/')

    def test_change_name_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:change_name'))
        self.assertEqual(response.context['user'].username, 'user')

    def test_change_email_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:change_email'))
        self.assertEqual(response.context['user'].username, 'user')

    def test_change_username_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:change_username'))
        self.assertEqual(response.context['user'].username, 'user')

    def test_register_view(self):
        self.client.login(username='user', password='upassword123')
        response = self.client.get(reverse('accounts:register'), follow=True)

        self.assertEqual(response.status_code, 200)
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

    def test_activate_account_view(self):
        user = User.objects.get(username='user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse('accounts:activate_account', kwargs={'uidb64': uid, 'token': token}))
        self.assertRedirects(response, reverse('accounts:account_activation_complete'))
        # self.assertTemplateUsed(response, 'accounts/account_activation_invalid.html')

    def test_activate_account_complete_view(self):
        response = self.client.get(reverse('accounts:account_activation_complete'))
        self.assertTemplateUsed(response, 'accounts/account_activation_complete.html')

