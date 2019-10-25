import pytest


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(
        email="test@example.com",
        password="secret",
    )
    user.model = django_user_model
    return user


@pytest.fixture
def logged_client(client, user):
    client.login(email="test@example.com", password="secret")
    yield client
    client.logout()
