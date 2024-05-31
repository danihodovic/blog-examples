from django.contrib import admin

from .models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
