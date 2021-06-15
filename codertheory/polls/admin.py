from django.contrib import admin

from codertheory.polls import models


# Register your models here.


@admin.register(models.Poll)
class PollAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ["option", "poll"]
    list_filter = ("poll",)
    search_fields = ['poll__id', 'option']


@admin.register(models.PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ["option", "poll"]
    search_fields = ['poll__id', 'option__name']
