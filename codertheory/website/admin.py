from django.contrib import admin

from codertheory.website import models


# Register your models here.


@admin.register(models.BannerButton)
class BannerButtonAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DisplayBanner)
class DisplayBannerAdmin(admin.ModelAdmin):
    pass
