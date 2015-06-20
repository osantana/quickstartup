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

        self.assert_(user.name, "John Doe")
        self.assert_(user.email, "test@example.com")
        self.assert_(user.get_full_name(), "John Doe")
        self.assert_(user.get_username(), "test@example.com")
        self.assert_(user.get_short_name(), "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_staff_user(self):
        user = UserModel.objects.create_user(
            name="John Doe",
            email="test@example.com",
            password="secret",
            is_staff=True,
        )

        self.assert_(user.name, "John Doe")
        self.assert_(user.email, "test@example.com")
        self.assert_(user.get_full_name(), "John Doe")
        self.assert_(user.get_username(), "test@example.com")
        self.assert_(user.get_short_name(), "test@example.com")
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser(self):
        user = UserModel.objects.create_superuser(
            name="Super John Doe",
            email="admin@example.com",
            password="ubbersekret",
        )

        self.assert_(user.name, "Super John Doe")
        self.assert_(user.email, "admin@example.com")
        self.assert_(user.get_full_name(), "Super John Doe")
        self.assert_(user.get_username(), "admin@example.com")
        self.assert_(user.get_short_name(), "admin@example.com")
        self.assertTrue(user.is_staff, "Superuser is staff")
        self.assertTrue(user.is_superuser, "Superuser must be enable")
