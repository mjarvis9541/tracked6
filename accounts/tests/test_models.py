from django.test import TestCase

from ..managers import UserManager
from ..models import User


class UserManagerTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            first_name='firstly', last_name='lastly', username='user', email='user@email.com', password='upassword123'
        )
        User.objects.create_superuser(username='superuser', email='superuser@email.com', password='spassword123')

    def test_create_user(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.email, 'user@email.com')
        self.assertTrue(user.check_password('upassword123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.get(username='superuser')
        self.assertEqual(superuser.username, 'superuser')
        self.assertEqual(superuser.email, 'superuser@email.com')
        self.assertTrue(superuser.check_password('spassword123'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserModelTestCase(TestCase):
    def setUp(self):
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

    # def test_get_absolute_url(self):
    #     user = User.objects.get(username='user')
    #     self.assertEqual(user.get_absolute_url(), '/profiles/user/') # TBC

    def test_user_full_name(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.get_full_name(), 'firstly lastly')

    def test_user_short_name(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.get_short_name(), 'firstly')
