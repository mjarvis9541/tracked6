from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.http import response
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .. import views
from ..models import User


# class BaseAuthTestCase(TestCase):
#     def assertLoggedInAs(self, user):
#         client_user = auth.get_user(self.client)
#         self.assertEqual(client_user, user)
#         assert client_user.is_authenticated()


class AccountViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_account_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/')
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
        self.assertRedirects(response, '/accounts/login/?next=/accounts/')

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
        self.assertNotContains(response, 'This should not be on the page')

    def test_account_url_resolves_to_account_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:account')
        self.assertEqual(resolve(url).func.view_class, views.AccountView)

    def test_account_view_context_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account'))
        self.assertEqual(response.context['user'].username, 'user')


class NameChangeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_name_change_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/name-change/')
        self.assertEquals(response.status_code, 200)

    def test_name_change_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:name_change'))
        self.assertEquals(response.status_code, 200)

    def test_name_change_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:name_change'))
        self.assertEquals(response.status_code, 302)

    def test_name_change_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:name_change'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/name-change/')

    def test_name_change_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:name_change'))
        self.assertTemplateUsed(response, 'accounts/name_change_form.html')

    def test_name_change_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:name_change'))
        self.assertContains(response, 'Change Name')

    def test_name_change_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:name_change'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_name_change_url_resolves_to_name_change_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:name_change')
        self.assertEqual(resolve(url).func.view_class, views.NameChangeView)

    def test_name_change_view_post_updates_name(self):
        self.client.login(username='user', password='password')
        self.client.post(reverse('accounts:name_change'), data={'first_name': 'Ringo', 'last_name': 'Starr'})
        user = User.objects.get(username='user')
        self.assertEqual(user.first_name, 'Ringo')
        self.assertEqual(user.last_name, 'Starr')


class UsernameChangeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_username_change_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/username-change/')
        self.assertEquals(response.status_code, 200)

    def test_username_change_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:username_change'))
        self.assertEquals(response.status_code, 200)

    def test_username_change_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:username_change'))
        self.assertEquals(response.status_code, 302)

    def test_username_change_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:username_change'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/username-change/')

    def test_username_change_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:username_change'))
        self.assertTemplateUsed(response, 'accounts/username_change_form.html')

    def test_username_change_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:username_change'))
        self.assertContains(response, 'Change Username')

    def test_username_change_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:username_change'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_username_change_url_resolves_to_username_change_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:username_change')
        self.assertEqual(resolve(url).func.view_class, views.UsernameChangeView)

    def test_username_change_view_invalid_post_data(self):
        self.client.login(username='user', password='password')
        user = User.objects.get(username='user')
        self.client.post(reverse('accounts:username_change'), data={'username': '!invalid_username'})
        self.assertEqual(user.username, 'user')

    def test_username_change_view_valid_post_data(self):
        self.client.login(username='user', password='password')
        self.client.post(reverse('accounts:username_change'), data={'username': 'new_username'})
        user = User.objects.get(username='new_username')
        self.assertEqual(user.username, 'new_username')


class EmailChangeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_email_change_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/email-change/')
        self.assertEquals(response.status_code, 200)

    def test_email_change_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change'))
        self.assertEquals(response.status_code, 200)

    def test_email_change_view_unauthorized_user_redirect_status_code(self):
        response = self.client.get(reverse('accounts:email_change'))
        self.assertEquals(response.status_code, 302)

    def test_email_change_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:email_change'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/email-change/')

    def test_email_change_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change'))
        self.assertTemplateUsed(response, 'accounts/email_change_form.html')

    def test_email_change_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change'))
        self.assertContains(response, 'Change Email')

    def test_email_change_view_incorrect_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change'))
        self.assertNotContains(response, 'This should not be on the html page')

    def test_email_change_url_resolves_to_email_change_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:email_change')
        self.assertEqual(resolve(url).func.view_class, views.EmailChangeView)

    def test_email_change_view_invalid_post_data(self):
        self.client.login(username='user', password='password')
        self.client.post(reverse('accounts:email_change'), data={'email': 'invalid_email_address'})
        user = User.objects.get(username='user')
        self.assertEqual(user.email_change_pending, None)

    def test_email_change_view_valid_post_data(self):
        self.client.login(username='user', password='password')
        self.client.post(reverse('accounts:email_change'), data={'email': 'new_email@email.com'})
        user = User.objects.get(username='user')
        self.assertEqual(user.email_change_pending, 'new_email@email.com')

    def test_email_change_view_success_redirect(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('accounts:email_change'), data={'email': 'new_email@email.com'})
        self.assertRedirects(response, reverse('accounts:email_change_done'))


class EmailChangeDoneViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_email_change_done_view_url(self):
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/email-change-done/')
        self.assertEquals(response.status_code, 200)

    def test_email_change_done_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change_done'))
        self.assertEquals(response.status_code, 200)

    def test_email_change_done_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change_done'))
        self.assertTemplateUsed(response, 'accounts/email_change_done.html')

    def test_email_change_url_resolves_to_email_change_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:email_change_done')
        self.assertEqual(resolve(url).func, views.email_change_done_view)


class EmailChangeConfirmViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_email_change_confirm_view_unsuccessful_post_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('accounts:email_change_confirm', kwargs={'uidb64': 'x', 'token': 'x'}))
        self.assertEquals(response.status_code, 200)

    def test_email_change_confirm_view_unsuccessful_post_exception(self):
        self.client.login(username='user', password='password')
        self.client.post(reverse('accounts:email_change_confirm', kwargs={'uidb64': 'x', 'token': 'x'}))
        self.assertRaises(TypeError, msg=None)

    def test_email_change_confirm_view_unsuccessful_post_template(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('accounts:email_change_confirm', kwargs={'uidb64': 'x', 'token': 'x'}))
        self.assertTemplateUsed(response, 'accounts/email_change_invalid.html')

    def test_email_change_confirm_view_successful_post_status_code(self):
        self.client.login(username='user', password='password')
        user = User.objects.get(username='user')
        user.email = 'old_email@email.com'
        user.email_change_pending = 'new_email@email.com'
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.post(reverse('accounts:email_change_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEquals(response.status_code, 302)

    def test_email_change_confirm_confirm_view_status_code(self):
        self.client.login(username='user', password='password')
        user = User.objects.get(username='user')
        user.email = 'old_email@email.com'
        user.email_change_pending = 'new_email@email.com'
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse('accounts:email_change_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertRedirects(response, reverse('accounts:email_change_complete'))


class EmailChangeCompleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_email_change_complete_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change_complete'))
        self.assertEquals(response.status_code, 200)

    def test_email_change_complete_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change_complete'))
        self.assertTemplateUsed(response, 'accounts/email_change_complete.html')

    def test_email_change_complete_view_correct_html_content(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:email_change_complete'))
        self.assertContains(response, 'Change Email Complete')


class RegisterViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_register_view_redirect_logged_in_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:register'), follow=True)
        self.assertRedirects(response, '/accounts/')
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, 'error')
        self.assertTrue(
            'You are already registered. If you wish to create a new account, please log out and try again.'
            in message.message
        )

    def test_register_view_status_code(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEquals(response.status_code, 200)

    def test_register_view_template(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_valid_post_data(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'first_name': 'Michae',
                'last_name': 'Jarvis',
                'username': 'mjarvis',
                'email': 'michael.jarvis@email.com',
                'password1': 'password',
                'password2': 'password',
            },
        )
        self.assertRedirects(response, reverse('accounts:account_activation_done'))

    def test_register_view_url_resolves_to_register_view(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func, views.register_view)


class AccountActivationViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')
        User.objects.create_user(
            username='inactive-user', email='inactive.user@email.com', password='password', is_active=False
        )

    def test_account_activation_view_status_code(self):
        response = self.client.get(reverse('accounts:account_activation'))
        self.assertEquals(response.status_code, 200)

    def test_account_activation_view_template(self):
        response = self.client.get(reverse('accounts:account_activation'))
        self.assertTemplateUsed(response, 'accounts/account_activation_form.html')

    def test_account_activation_view_valid_post_data_redirect(self):
        response = self.client.post(reverse('accounts:account_activation'), data={'email': 'inactive.user@email.com'})
        self.assertRedirects(response, reverse('accounts:account_activation_done'))


class AccountActivationDoneViewTests(SimpleTestCase):
    def test_account_activation_done_view_status_code(self):
        response = self.client.get(reverse('accounts:account_activation_done'))
        self.assertEquals(response.status_code, 200)

    def test_account_activation_done_view_template(self):
        response = self.client.get(reverse('accounts:account_activation_done'))
        self.assertTemplateUsed(response, 'accounts/account_activation_done.html')

    def test_account_activation_done_url_resolves_to_account_activation_done_view(self):
        url = reverse('accounts:account_activation_done')
        self.assertEqual(resolve(url).func, views.account_activation_done_view)


class AccountActivationConfirmViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_account_activation_view_status_code(self):
        response = self.client.get(
            reverse('accounts:account_activation_confirm', kwargs={'uidb64': 'none', 'token': 'none'})
        )
        self.assertEqual(response.status_code, 200)

    def test_account_activation_confirm_view_template(self):
        response = self.client.get(
            reverse('accounts:account_activation_confirm', kwargs={'uidb64': 'none', 'token': 'none'})
        )
        self.assertTemplateUsed(response, 'accounts/account_activation_invalid.html')

    def test_account_activation_confirm_view_redirect(self):
        user = User.objects.get(username='user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(
            reverse('accounts:account_activation_confirm', kwargs={'uidb64': uid, 'token': token})
        )
        self.assertRedirects(response, reverse('accounts:account_activation_complete'))

    def test_account_activation_confirm_url_resolves_to_account_activation_confirm_view(self):
        url = reverse('accounts:account_activation_confirm', kwargs={'uidb64': 'none', 'token': 'none'})
        self.assertEqual(resolve(url).func, views.account_activation_confirm_view)


class AccountActivationCompleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user', email='email@email.com', password='password')

    def test_account_activation_complete_view_status_code(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account_activation_complete'))
        self.assertEquals(response.status_code, 200)

    def test_account_activation_complete_view_template(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('accounts:account_activation_complete'))
        self.assertTemplateUsed(response, 'accounts/account_activation_complete.html')

    def test_account_view_unauthorized_user_redirect_url(self):
        response = self.client.get(reverse('accounts:account_activation_complete'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/register/account-activation-complete/')

    def test_account_activation_complete_url_resolves_to_account_activation_complete_view(self):
        self.client.login(username='user', password='password')
        url = reverse('accounts:account_activation_complete')
        self.assertEqual(resolve(url).func, views.account_activation_complete_view)