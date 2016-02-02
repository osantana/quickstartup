# coding: utf-8


# noinspection PyUnusedLocal
def bootstrap_website_pages(apps, schema_editor=None):
    page_model = apps.get_model("qs_website", "Page")
    pages = [
        {"slug": "", "template_name": "website/landing.html"},
        {"slug": "privacy", "template_name": "website/privacy.html"},
        {"slug": "terms", "template_name": "website/terms.html"},
    ]

    for page in pages:
        page_model.objects.get_or_create(**page)
