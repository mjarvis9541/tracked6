from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import User


class UserManagerTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            first_name='firstly', last_name='lastly', username='user1', email='user1@email.com', password='password'
        )
        self.assertEqual(user.first_name, 'firstly')
        self.assertEqual(user.last_name, 'lastly')
        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.email, 'user1@email.com')
        self.assertTrue(user.check_password('password'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_username_value_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username=None)

    def test_create_user_no_email_value_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='user2', email=None)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            first_name='firstly',
            last_name='lastly',
            username='superuser',
            email='superuser@email.com',
            password='password',
        )
        self.assertEqual(superuser.first_name, 'firstly')
        self.assertEqual(superuser.last_name, 'lastly')
        self.assertEqual(superuser.username, 'superuser')
        self.assertEqual(superuser.email, 'superuser@email.com')
        self.assertTrue(superuser.check_password('password'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_not_staff_value_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username='superuser2', is_staff=False)

    def test_create_superuser_not_supuser_value_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username='superuser3', is_superuser=False)


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            first_name='firstly', last_name='lastly', username='user', email='user@email.com', password='upassword123'
        )
        User.objects.create_superuser(username='superuser', email='superuser@email.com', password='spassword123')

    def test_username_max_length(self):
        user = User.objects.get(username='user')
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(max_length, 150)

    def test_first_name_max_length(self):
        user = User.objects.get(username='user')
        max_length = user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_last_name_max_length(self):
        user = User.objects.get(username='user')
        max_length = user._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)

    def test_user_model_str(self):
        user = User.objects.get(username='user')
        self.assertEqual(str(user), user.username)

    def test_user_full_name(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.get_full_name(), 'firstly lastly')

    def test_user_short_name(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.get_short_name(), 'firstly')

    def test_model_clean_banned_user_raises_valdiation_error(self):
        with self.assertRaises(ValidationError):
            user = User(username='user', email='user@email.com', is_active=True, is_banned=True)
            user.clean()

    def test_model_clean_duplicate_username_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            user1 = User(username='user2', email='user2@email.com')
            user1.save()
            user2 = User(username='user2', email='another_email@email.com')
            user2.clean()

    def test_model_save_banned_user_raises_value_error(self):
        with self.assertRaises(ValueError):
            user = User(username='user2', email='user2@email.com', is_active=True, is_banned=True)
            user.save()

    def test_model_save_duplicate_username_raises_value_error(self):
        with self.assertRaises(ValueError):
            user1 = User(username='user2', email='user2@email.com')
            user1.save()
            user2 = User(username='user2', email='another_email@email.com')
            user2.save()

    def test_model_send_email(self):
        User.objects.create_user(username='user3', email='user3@email.com', password='password')
        user = User.objects.get(username='user3')
        User.email_user(user, subject='hello there', message='this is an email', from_email='admin@tracked6.com')
        self.assertEqual(mail.outbox[0].subject, 'hello there')
        self.assertEqual(mail.outbox[0].body, 'this is an email')
        self.assertEqual(mail.outbox[0].from_email, 'admin@tracked6.com')
        self.assertEqual(mail.outbox[0].to, ['user3@email.com'])
