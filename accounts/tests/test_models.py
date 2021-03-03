from django.test import TestCase

from accounts.models import User


class UserModelTestCase(TestCase):
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

    def test_user_model_str(self):
        user = User.objects.get(username='user')
        self.assertEqual(str(user), user.username)

    # def test_get_absolute_url(self):
    #     user = User.objects.get(username='user')
    #     self.assertEqual(user.get_absolute_url(), '/profiles/user/') # TBC

    def test_user_full_name(self):
        user = User.objects.get(username='user')
        self.assertEqual(f'{user.first_name} {user.last_name}', 'firstly lastly')

    def test_user_short_name(self):
        user = User.objects.get(username='user')
        self.assertEqual(user.first_name, 'firstly')