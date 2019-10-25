from django.test import override_settings
from django.urls import NoReverseMatch

from quickstartup.qs_pages.models import Page
from quickstartup.qs_pages.urlresolver import page_reverse
from ..base import BaseTestCase, TEMPLATES


class PageTest(BaseTestCase):
    @override_settings(TEMPLATES=TEMPLATES)
    def test_success_reverse(self):
        Page.objects.create(slug="about", template_name="about.html")
        url = page_reverse("about")
        self.assertEquals("/about/", url)

    def test_fail_reverse_missing_page(self):
        with self.assertRaises(NoReverseMatch):
            page_reverse("unknown")

    def test_fail_reverse_invalid_url(self):
        with self.assertRaises(NoReverseMatch):
            page_reverse("/")

    def test_bootstrap_pages(self):
        self.assertEquals(Page.objects.get(slug="").get_absolute_url(), "/")
        self.assertEquals(Page.objects.get(slug="terms").get_absolute_url(), "/terms/")
        self.assertEquals(Page.objects.get(slug="privacy").get_absolute_url(), "/privacy/")

    def test_path(self):
        page = Page.objects.get(slug="terms")
        self.assert_(page.path, "/terms/")
        self.assert_(str(page), "/terms/")

    def test_filter_invalid_pages(self):
        pages = Page.objects.all()
        self.assertNotIn("inv@lid", pages)

    def test_success_terms_page_access(self):
        response = self.client.get("/terms/")
        self.assertStatusCode(response, 200)
        self.assertContains(response, "<title>Terms of Service —")

    def test_success_terms_page_access_missing_trailing_slash(self):
        response = self.client.get("/terms")
        self.assertContains(response, "<title>Terms of Service — ")

    def test_success_privacy_page_access(self):
        response = self.client.get("/privacy/")
        self.assertStatusCode(response, 200)
        self.assertContains(response, "<title>Privacy Policy —")

    def test_fail_page_404(self):
        response = self.client.get("/unknown/")
        self.assertStatusCode(response, 404)

    def test_fail_invalid_url(self):
        response = self.client.get("/err/or/")
        self.assertStatusCode(response, 404)

    @override_settings(TEMPLATES=TEMPLATES, DEBUG=False)
    def test_call_template_with_error_and_debug_disabled(self):
        Page.objects.create(slug="buggy-template", template_name="buggy-template.html")
        response = self.client.get(page_reverse("buggy-template"))
        self.assertStatusCode(response, 404)  # original error is 404 because we dont map pages urls

    def test_index_page_anonymous_user(self):
        response = self.client.get("/")
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed(response, "website/landing.html")
        self.assertInHTML("<title>Django Quickstartup</title>", response.content.decode("utf-8"))
