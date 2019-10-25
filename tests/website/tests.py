import pytest
from django.test import override_settings
from django.urls import NoReverseMatch

from quickstartup.qs_pages.models import Page
from quickstartup.qs_pages.urlresolver import page_reverse
from ..base import TEMPLATES, check_contains, check_in_html, check_template_used

pytestmark = pytest.mark.django_db


@override_settings(TEMPLATES=TEMPLATES)
def test_success_reverse():
    Page.objects.create(slug="about", template_name="about.html")
    url = page_reverse("about")
    assert "/about/" == url


def test_fail_reverse_missing_page():
    with pytest.raises(NoReverseMatch):
        page_reverse("unknown")


def test_fail_reverse_invalid_url():
    with pytest.raises(NoReverseMatch):
        page_reverse("/")


def test_bootstrap_pages():
    assert Page.objects.get(slug="").get_absolute_url() == "/"
    assert Page.objects.get(slug="terms").get_absolute_url() == "/terms/"
    assert Page.objects.get(slug="privacy").get_absolute_url() == "/privacy/"


def test_path():
    page = Page.objects.get(slug="terms")
    assert page.path == "/terms/"
    assert str(page) == "/terms/"


def test_filter_invalid_pages():
    pages = Page.objects.all()
    assert "inv@lid" not in pages


def test_success_terms_page_access(client):
    response = client.get("/terms/")
    assert response.status_code == 200
    assert check_contains(response, "<title>Terms of Service —")


def test_success_terms_page_access_missing_trailing_slash(client):
    response = client.get("/terms")
    assert check_contains(response, "<title>Terms of Service — ")


def test_success_privacy_page_access(client):
    response = client.get("/privacy/")
    assert response.status_code == 200
    assert check_contains(response, "<title>Privacy Policy —")


def test_fail_page_404(client):
    response = client.get("/unknown/")
    assert response.status_code == 404


def test_fail_invalid_url(client):
    response = client.get("/err/or/")
    assert response.status_code == 404


@override_settings(TEMPLATES=TEMPLATES, DEBUG=False)
def test_call_template_with_error_and_debug_disabled(client):
    Page.objects.create(slug="buggy-template", template_name="buggy-template.html")
    response = client.get(page_reverse("buggy-template"))
    assert response.status_code == 404  # original error is 404 because we dont map pages urls


def test_index_page_anonymous_user(client):
    response = client.get("/")
    assert response.status_code == 200
    assert check_template_used(response, "website/landing.html")
    assert check_in_html("<title>Django Quickstartup</title>", response.content.decode("utf-8"))
