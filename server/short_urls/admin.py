from django.contrib import admin

from server.admin import register
from server.short_urls.models import ShortURL


@register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("id", "original")
