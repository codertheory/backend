from django.contrib import admin

from codertheory.shiritori import models


# Register your models here.


@admin.register(models.ShiritoriGame)
class ShiritoriGameAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ShiritoriPlayer)
class ShiritoriPlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ShiritoriGameWord)
class ShiritoriGameWord(admin.ModelAdmin):
    pass
