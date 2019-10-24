import pytest

pytestmark = pytest.mark.django_db


def test_basic_user(django_user_model):
    user = django_user_model.objects.create_user(
        name="John Doe",
        email="test@example.com",
        password="secret",
    )

    assert user.name == "John Doe"
    assert user.email == "test@example.com"
    assert user.get_full_name() == "John Doe"
    assert user.get_username() == "test@example.com"
    assert user.get_short_name() == "test@example.com"
    assert not user.is_staff
    assert not user.is_superuser


def test_staff_user(django_user_model):
    user = django_user_model.objects.create_user(
        name="John Doe",
        email="test@example.com",
        password="secret",
        is_staff=True,
    )

    assert user.name == "John Doe"
    assert user.email == "test@example.com"
    assert user.get_full_name() == "John Doe"
    assert user.get_username() == "test@example.com"
    assert user.get_short_name() == "test@example.com"
    assert user.is_staff
    assert not user.is_superuser


def test_superuser(django_user_model):
    user = django_user_model.objects.create_superuser(
        name="Super John Doe",
        email="admin@example.com",
        password="ubbersekret",
    )

    assert user.name == "Super John Doe"
    assert user.email == "admin@example.com"
    assert user.get_full_name() == "Super John Doe"
    assert user.get_username() == "admin@example.com"
    assert user.get_short_name() == "admin@example.com"
    assert user.is_staff, "Superuser is staff"
    assert user.is_superuser, "Superuser must be enable"


def test_change_email(django_user_model):
    user = django_user_model.objects.create_user(
        name="John Doe",
        email="test@example.com",
        password="secret",
    )

    user.new_email = "new@example.com"
    user.save()
    assert user.email == "test@example.com"

    user.confirm_new_email()
    assert user.email == "new@example.com"


def test_confirm_email_with_no_change(django_user_model):
    user = django_user_model.objects.create_user(
        name="John Doe",
        email="test@example.com",
        password="secret",
    )

    user.confirm_new_email()
    assert user.email == "test@example.com"
