from django.contrib import admin

from .forms import PageForm
from .models import Page


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    fieldsets = (
        (None, {'fields': ("slug", "template_name", "login_required")}),
    )
    list_display = ("path", "template_name")
    list_display_links = ("path", "template_name")
    list_filter = ("login_required",)
    search_fields = ("slug",)


admin.site.register(Page, PageAdmin)
