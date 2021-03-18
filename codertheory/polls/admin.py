from django.contrib import admin

from codertheory.polls import models


# Register your models here.


@admin.register(models.Poll)
class PollAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    pass
