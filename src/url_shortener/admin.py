from django.contrib import admin

from .models import ShortURL


class ShortURLModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["original_url", "hash"]}),
        ("Date information", {"fields": ["created", "modified"], "classes": ["collapse"]}),
    ]

    list_display = ["original_url", "hash", "created", "modified"]
    list_filter = ["created"]
    search_fields = ["original_url", "hash"]


admin.site.register(ShortURL, ShortURLModelAdmin)
