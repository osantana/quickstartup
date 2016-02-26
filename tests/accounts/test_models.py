# coding: utf-8


from django.test import TestCase
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserTestCase(TestCase):
    def test_basic_user(self):
        user = UserModel.objects.create_user(
            name="John Doe",
            email="test@example.com",
            password="secret",
        )

        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.get_full_name(), "John Doe")
        self.assertEqual(user.get_username(), "test@example.com")
        self.assertEqual(user.get_short_name(), "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_staff_user(self):
        user = UserModel.objects.create_user(
            name="John Doe",
            email="test@example.com",
            password="secret",
            is_staff=True,
        )

        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.get_full_name(), "John Doe")
        self.assertEqual(user.get_username(), "test@example.com")
        self.assertEqual(user.get_short_name(), "test@example.com")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser(self):
        user = UserModel.objects.create_superuser(
            name="Super John Doe",
            email="admin@example.com",
            password="ubbersekret",
        )

        self.assertEqual(user.name, "Super John Doe")
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.get_full_name(), "Super John Doe")
        self.assertEqual(user.get_username(), "admin@example.com")
        self.assertEqual(user.get_short_name(), "admin@example.com")
        self.assertTrue(user.is_staff, "Superuser is staff")
        self.assertTrue(user.is_superuser, "Superuser must be enable")

    def test_change_email(self):
        user = UserModel.objects.create_user(
            name="John Doe",
            email="test@example.com",
            password="secret",
        )

        user.set_new_email("new@example.com")
        self.assertEqual(user.email, "test@example.com")

        user.confirm_new_email()
        self.assertEqual(user.email, "new@example.com")

    def test_confirm_email_with_no_change(self):
        user = UserModel.objects.create_user(
            name="John Doe",
            email="test@example.com",
            password="secret",
        )

        user.confirm_new_email()
        self.assertEqual(user.email, "test@example.com")
