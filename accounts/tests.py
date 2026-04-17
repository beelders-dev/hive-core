from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


class CustomUserTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username="mike", email="mike@email.com", password="mike123"
        )

        self.assertEqual(user.username, "mike")
        self.assertEqual(user.email, "mike@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class CustomUserAdminTests(TestCase):
    def test_create_admin_user(self):
        user_admin = get_user_model().objects.create_superuser(
            username="mike", email="mike@email.com", password="mike123"
        )

        self.assertEqual(user_admin.username, "mike")
        self.assertEqual(user_admin.email, "mike@email.com")
        self.assertTrue(user_admin.is_active)
        self.assertTrue(user_admin.is_staff)
        self.assertTrue(user_admin.is_superuser)
