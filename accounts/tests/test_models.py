from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='user@email.com', password='password123'
        )
        self.assertEqual(user.email, 'user@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='superuser@email.com', password='password123'
        )
        self.assertEqual(superuser.email, 'superuser@email.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
