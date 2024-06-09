from django.contrib import admin

from .models import Track, TrackS3


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass


@admin.register(TrackS3)
class TrackS3Admin(admin.ModelAdmin):
    pass
