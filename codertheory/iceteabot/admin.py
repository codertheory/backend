from django.contrib import admin

from codertheory.iceteabot import models


# Register your models here.


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscordChannel)
class DiscordChannelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CommandCall)
class CommandCallAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscordGuild)
class DiscordGuildAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscordResponse)
class DiscordResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscordMember)
class DiscordMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscordNickName)
class NickNameAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CommandPrefix)
class CommandPrefixAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ReactionRole)
class ReactionRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Reminder)
class ReminderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TagLookUp)
class TagLookUpAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TagCall)
class TagCallAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    pass
