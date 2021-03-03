from django.test import TestCase
from django.urls import reverse
from django.test import Client

from ..models import User


class AccountViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            first_name='firstly', last_name='lastly', username='user', email='user@email.com', password='upassword123'
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




# class LoginViewTests(TestCase):
#     def setUp(self):
#         User.objects.create_user(
#             first_name='firstly', last_name='lastly', username='user', email='user@email.com', password='upassword123'
#         )

#     def test_login_view(self):
#         response = self.client.get(reverse('accounts:login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Log In')
#         self.assertTemplateUsed(response, 'accounts/login.html')

#     def test_login(self):
#         c = Client()
#         valid_login = c.login(username='user', password='upassword123')
#         invalid_login = c.login(username='user', password='incorrect')
#         self.assertTrue(valid_login)
#         self.assertFalse(invalid_login)


# class LogoutViewTests(TestCase):
#     def setUp(self):
#         User.objects.create_user(
#             first_name='firstly', last_name='lastly', username='user', email='user@email.com', password='upassword123'
#         )

#     def test_logout_view(self):
#         response = self.client.get(reverse('accounts:logout'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Logged Out')
#         self.assertTemplateUsed(response, 'accounts/logout.html')
