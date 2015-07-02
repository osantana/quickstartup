# coding: utf-8


from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404

from .models import Page


def website_page(request, path):
    slug = path.strip("/")
    page = get_object_or_404(Page, slug=slug)
    context = RequestContext(request, {"page": page, "slug": slug, "path": path})
    return HttpResponse(page.template.render(context))


def index(request):
    return render(request, "website/landing.html")
