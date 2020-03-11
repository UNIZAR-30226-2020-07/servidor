"""
Define some tests
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    """
    Tests for creating users
    """

    def test_create_user(self):
        """
        Test for create a normal user
        """
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # last_name is None for the AbstractUser option
            # last_name does not exist for the AbstractBaseUser option
            self.assertIsNone(user.last_name)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        """
        Test for create a superuser
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser('super_name', 'super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'super_name')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # last_name is None for the AbstractUser option
            # last_name does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.last_name)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', username = 'super_name',is_superuser=False)