from django.contrib import admin

from codertheory.shiritori import models


# Register your models here.


@admin.register(models.ShiritoriGame)
class ShiritoriGameAdmin(admin.ModelAdmin):
    # TODO limit current_player and winner to only valid Player instances
    pass


@admin.register(models.ShiritoriPlayer)
class ShiritoriPlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ShiritoriGameWord)
class ShiritoriGameWordAdmin(admin.ModelAdmin):
    pass
