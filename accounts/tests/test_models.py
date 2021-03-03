from django.test import TestCase

from accounts.models import User


class UserManagerTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', email='user@email.com', password='password123')
        User.objects.create_superuser(username='superuser', email='superuser@email.com', password='password123')

    def test_create_user(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.email, 'user@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.get(username='superuser')
        self.assertEqual(superuser.username, 'superuser')
        self.assertEqual(superuser.email, 'superuser@email.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_model_str(self):
        user = User.objects.get(username='user')
        self.assertEqual(str(user), user.username)
